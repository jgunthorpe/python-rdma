#!/usr/bin/python
import collections,inspect,sys,bisect
import rdma,rdma.madtransactor;

class Context(object):
    def __init__(self,op,gengen):
        self._opstack = collections.deque();
        self._op = op;
        self._gengen = gengen;
        self._exc = None;

class MADSchedule(rdma.madtransactor.MADTransactor):
    """This class provides a MADTransactor interface suitable for use by
    python coroutines. The implementation gets MAD parallelism by running
    multiple coroutines at once. coroutines are implemented as generators.
    A simple use of the class to fetch node infos for a list of paths:

    def get_nodeinfo(sched,node):
        node.ninf = yield sched.SubGet(IBA.SMPNodeInfo,I.path);

    nodes = [..];
    sched = rdma.sched.MADSchedual();
    sched.run(mqueue=(get_nodeinfo(sched,I) for I in nodes));

    The scheduler will pull generators from the start argument to run and
    invoke them to return MADs, bounding the total outstanding MAD count and
    returning replies as the result of yield. Calling queue() during coroutine
    execution will create a new coroutine."""

    max_outstanding = 4;
    """Maximum number of outstanding MADs at any time."""

    def __init__(self,umad):
        rdma.madtransactor.MADTransactor.__init__(self);
        self._umad = umad;
        self._keys = {};
        self._timeouts = []
        self._mqueue = collections.deque();
        self.max_outstanding = 4;
        self._replyqueue = collections.deque();

    def _sendMAD(self,ctx,mad):
        buf = mad[0]._buf;

        rep = self._umad._execute(buf,mad[1],sendOnly=True);
        if rep:
            self._replyqueue.append(rep);

        itm = [mad[1].mad_timeout + rdma.tools.clock_monotonic(),
               ctx,mad,mad[1].retries];
        bisect.insort(self._timeouts,itm);

        rmatch = self._getReplyMatchKey(buf);
        assert(rmatch not in self._keys);
        self._keys[rmatch] = itm;

    def _step(self,ctx,result):
        """Advance a context to its next yield statement. If result is None
        then this ctx is brand new. If ctx is not exhausted then it is put
        onto _mqueue for later"""
        while result is None or len(self._keys) <= self.max_outstanding:
            try:
                exc = ctx._exc
                if exc != None:
                    ctx._exc = None;
                    work = ctx._op.throw(*exc);
                elif result is None:
                    work = ctx._op.next();
                else:
                    work = ctx._op.send(result);
            except StopIteration:
                if ctx._opstack:
                    ctx._op = ctx._opstack.pop();
                    result = True;
                    continue;
                else:
                    return;
            except:
                # Flow exceptions up the stack of generators
                if ctx._opstack:
                    ctx._op = ctx._opstack.pop();
                    ctx._exc = sys.exc_info();
                    result = True;
                    continue;
                else:
                    raise;

            if inspect.isgenerator(work):
                if ctx._gengen:
                    # Create a new context
                    self._mqueue.append(ctx);
                    ctx = Context(work,False);
                else:
                    ctx._opstack.append(ctx._op);
                    ctx._op = work;
                result = None;
                continue;
            self._sendMAD(ctx,work);
            return;

        self._mqueue.append(ctx);

    def mqueue(self,works):
        """works is a generator returning coroutines. All coroutines
        can run in parallel."""
        assert(inspect.isgenerator(works));
        self._step(Context(works,True),None);

    def queue(self,work):
        """work is a single coroutine."""
        assert(inspect.isgenerator(work));
        self._step(Context(work,False),None);

    def run(self,queue=None,mqueue=None):
        """Schedule MADs. Exits once all the work has been completed.
        queue and mqueue arguments as passed straight to the
        queue and mqueue functions."""
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

            # Dispatch the MAD
            rmatch = self._getMatchKey(ret[0]);
            res = self._keys.get(rmatch);
            if res:
                del self._keys[rmatch];
                self._timeouts.remove(res);
                try:
                    payload = self._completeMAD(ret,*res[2]);
                except:
                    res[1]._exc = sys.exc_info();
                    payload = True;
                self._step(res[1],payload);

    def _do_timeout(self,res):
        """The timeout list entry res has timed out - either error it
        or issue a retry"""
        if res[3] == 0:
            # Pass the timeout back into MADTransactor and capture the
            # result
            try:
                self._completeMAD(None,*res[2]);
            except:
                res[1]._exc = sys.exc_info();
                self._step(res[1],True);
            else:
                assert(False);
        res[3] = res[3] - 1;

        # Resend
        mad = res[2];
        rep = self._umad._execute(mad[0]._buf,mad[1],sendOnly=True);
        if rep:
            self._replyqueue.append(rep);
        res[0] = mad[1].mad_timeout + rdma.tools.clock_monotonic();
        bisect.insort(self._timeouts,res);

    # Implement the MADTransactor interface. This is the asynchronous use model,
    # where the RPC functions return the work to do, not the result.
    def _doMAD(self,fmt,payload,path,attributeModifier,method,completer=None):
        self._prepareMAD(fmt,payload,attributeModifier,method);
        newer = payload if isinstance(payload,type) else payload.__class__;
        return (fmt,path,newer,completer);

    def _getNewTID(self):
        return self._umad._getNewTID();
