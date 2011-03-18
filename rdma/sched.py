# Copyright 2011 Obsidian Research Corp. GLPv2, see COPYING.
import collections,inspect,sys,bisect
import rdma,rdma.madtransactor;

class Context(object):
    _parent = None;
    _exc = None;
    _done = False;
    _result = None;
    _work = None;
    _retries = 0;

    def __init__(self,op,gengen,parent=None):
        self._opstack = collections.deque();
        self._op = op;
        self._gengen = gengen;
        if gengen:
            self._children = set();
        if parent is not None:
            self._parent = parent;
            self._parent._children.add(self);

class MADSchedule(rdma.madtransactor.MADTransactor):
    """This class provides a MADTransactor interface suitable for use by
    python coroutines. The implementation gets MAD parallelism by running
    multiple coroutines at once. coroutines are implemented as generators."""

    #: Maximum number of outstanding MADs at any time.
    max_outstanding = 4;
    #: Set to return a result from a coroutine
    result = None;

    #: :class:`dict` of contexts to a list of coroutines waiting on them
    _ctx_waiters = None;

    Work = collections.namedtuple("Work","buf fmt path newer completer");

    @property
    def is_async(self):
        return True;

    def __init__(self,umad):
        """*umad* is a :class:`rdma.umad.UMAD` instance which will be used to
        issue the MADs."""
        rdma.madtransactor.MADTransactor.__init__(self);
        self.end_port = umad.end_port;
        self._umad = umad;
        self.trace_func = umad.trace_func
        self._keys = {};
        self._timeouts = []
        self._mqueue = collections.deque();
        self.max_outstanding = 4;
        self._replyqueue = collections.deque();
        self._ctx_waiters = collections.defaultdict(list);

    def _sendMAD(self,ctx,work):
        buf = work.buf;
        path = work.path;
        rep = self._umad._execute(buf,path,sendOnly=True);
        if rep:
            self._replyqueue.append(rep);

        itm = (path.mad_timeout + rdma.tools.clock_monotonic(),ctx);
        ctx._work = work;
        ctx._retries = path.retries;
        bisect.insort(self._timeouts,itm);

        rmatch = self._get_reply_match_key(buf);
        assert(rmatch not in self._keys);
        self._keys[rmatch] = itm;

    def _finish_ctx(self,ctx):
        """Called when ctx is done and won't be called any more. This triggers
        things yielding on the context."""
        ctx._done = True;
        if ctx._parent is not None:
            ctx._parent._children.remove(ctx);
            if not ctx._parent._children and ctx._parent._done:
                self._finish_ctx(ctx._parent);

        if ctx._gengen:
            for I in ctx._children:
                if not I._done:
                    return;

        waits = self._ctx_waiters.get(ctx);
        if waits is None:
            return;
        del self._ctx_waiters[ctx];
        for I in waits:
            self._mqueue.appendleft(I);

    def _step(self,ctx,result):
        """Advance a context to its next yield statement. If result is None
        then this ctx is brand new. If ctx is not exhausted then it is put
        onto _mqueue for later"""
        while result is None or len(self._keys) <= self.max_outstanding:
            if ctx._result is not None:
                result = ctx._result;
                ctx._result = None;
            try:
                exc = ctx._exc
                if exc is not None:
                    ctx._exc = None;
                    work = ctx._op.throw(*exc);
                elif result is None:
                    work = ctx._op.next();
                else:
                    work = ctx._op.send(result);
            except StopIteration:
                if ctx._opstack:
                    ctx._op = ctx._opstack.pop();
                    if self.result is not None:
                        ctx._result = self.result;
                        self.result = None;
                    result = True;
                    continue;
                else:
                    self._finish_ctx(ctx);
                    return;
            except:
                # Flow exceptions up the stack of generators
                if ctx._opstack:
                    ctx._op = ctx._opstack.pop();
                    ctx._exc = sys.exc_info();
                    result = True;
                    continue;
                else:
                    self._finish_ctx(ctx);
                    raise;

            if isinstance(work,Context):
                self._ctx_waiters[work].append(ctx);
                return;

            if inspect.isgenerator(work):
                if ctx._gengen:
                    # Create a new context
                    self._mqueue.append(ctx);
                    ctx = Context(work,False,ctx);
                else:
                    ctx._opstack.append(ctx._op);
                    ctx._op = work;
                result = None;
                continue;

            try:
                self._sendMAD(ctx,work);
            except:
                ctx._exc = sys.exc_info();
                result = True;
                continue;
            return;

        self._mqueue.append(ctx);

    def mqueue(self,works):
        """*works* is a generator returning coroutines. All coroutines
        can run in parallel.

        :returns: An opaque context reference."""
        assert(inspect.isgenerator(works));
        ctx = Context(works,True);
        self._step(ctx,None);
        return ctx;

    def queue(self,work):
        """*work* is a single coroutine, or *work* is a tuple of coroutines.

        :returns: An opaque context reference."""
        if isinstance(work,tuple):
            for I in work:
                self.queue(I);
            return;
        assert(inspect.isgenerator(work));
        ctx = Context(work,False);
        self._step(ctx,None);
        return ctx;

    def run(self,queue=None,mqueue=None):
        """Schedule MADs. Exits once all the work has been completed.
        *queue* and *mqueue* arguments as passed straight to the
        :meth:`queue` and :meth:`mqueue` methods."""
        self._ctx_waiters.clear();
        self._keys.clear();
        self._replyqueue.clear();
        self._mqueue.clear();
        if queue:
            self.queue(queue);
        if mqueue:
            self.mqueue(mqueue);

        while self._keys or self._mqueue:
            while len(self._keys) <= self.max_outstanding and self._mqueue:
                self._step(self._mqueue.pop(),True);

            # Wait for a MAD
            if self._replyqueue:
                ret = self._replyqueue.pop();
            else:
                if not (self._keys or self._mqueue):
                    break;
                ret = self._umad.recvfrom(self._timeouts[0][0]);
                if ret is None:
                    # Purge timed out values
                    now = rdma.tools.clock_monotonic();

                    # During timeout processing we might cause new MAD
                    # sends so we have to iterate here carefully.
                    while self._timeouts:
                        k = self._timeouts[0];
                        if k[0] <= now:
                            del self._timeouts[0];
                        self._do_timeout(k);
                    continue;

            # Dispatch the MAD
            rmatch = self._get_match_key(ret[0]);
            res = self._keys.get(rmatch);
            if res:
                del self._keys[rmatch];
                self._timeouts.remove(res);
                try:
                    work = res[1]._work
                    payload = self._completeMAD(ret,work.fmt,
                                                work.path,
                                                work.newer,
                                                work.completer);
                except:
                    res[1]._exc = sys.exc_info();
                    payload = True;
                self._step(res[1],payload);
            else:
                if self.trace_func is not None:
                    self.trace_func(self,rdma.madtransactor.TRACE_UNEXPECTED,
                                    ret=ret);

    def _do_timeout(self,res):
        """The timeout list entry res has timed out - either error it
        or issue a retry"""
        ctx = res[1]
        work = ctx._work;
        if ctx._retries == 0:
            # Pass the timeout back into MADTransactor and capture the
            # result
            rmatch = self._get_reply_match_key(work.buf);
            del self._keys[rmatch];
            try:
                self._completeMAD(None,work.fmt,work.path,
                                  work.newer,work.completer);
            except:
                ctx._exc = sys.exc_info();
                self._step(ctx,True);
            else:
                assert(False);
            return
        ctx._retries = ctx._retries - 1;

        # Resend
        rep = self._umad._execute(work.buf,work.path,sendOnly=True);
        if rep:
            self._replyqueue.append(rep);
        res = (mad[1].mad_timeout + rdma.tools.clock_monotonic(),ctx);
        bisect.insort(self._timeouts,res);

    # Implement the MADTransactor interface. This is the asynchronous use model,
    # where the RPC functions return the work to do, not the result.
    def _doMAD(self,fmt,payload,path,attributeModifier,method,completer=None):
        buf = self._prepareMAD(fmt,payload,attributeModifier,method,path);
        newer = payload if isinstance(payload,type) else payload.__class__;
        return self.Work(buf,fmt,path,newer,completer);

    def _get_new_TID(self):
        return self._umad._get_new_TID();
