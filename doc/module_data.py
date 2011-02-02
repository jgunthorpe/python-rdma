
import sphinx;
import sphinx.util.compat;
import sphinx.pycode;
import sphinx.pycode.pgen2.token as token;
import docutils;
import docutils.nodes;
import sys;

class MyVisitor(sphinx.pycode.AttrDocVisitor):
    """Mildly hackish replacement for find_attr_docs that also retains
    the source order of the data definitions."""
    def __init__(self,scope,encoding):
        sphinx.pycode.AttrDocVisitor.__init__(self,sphinx.pycode.number2name,
                                              scope,encoding);
        self.data = [];

    def visit_expr_stmt(self, node):
        if sphinx.pycode._eq in node.children:
            for i in range(0, len(node) - 1, 2):
                target = node[i]
                if target.type != token.NAME:
                    # don't care about complex targets
                    continue
                namespace = '.'.join(self.namespace)
                if namespace.startswith(self.scope):
                    self.data.append((namespace, target.value));
        return sphinx.pycode.AttrDocVisitor.visit_expr_stmt(self,node);

class ModuleDataDirective(sphinx.util.compat.Directive):
    required_arguments = 1;
    bitmap = dict((1<<I,"(1 << %u)"%(I)) for I in range(0,64));

    # If I was smarter I'd figure out how to create the table directly
    def tableize(self,lst,idx):
        width = max(len(I[idx]) for I in lst);
        yield "="*width;
        for I in lst:
            yield I[idx].ljust(width);
        yield "="*width;

    def to_section(self,sub,res,title):
        if title:
            # res.insert(0,(title,".."));
            sub.append(title,"<module_data>");
            sub.append("^"*len(title),"<module_data>");
            sub.append("","<module_data>");

        for I in ("%s %s %s"%I for I in zip(self.tableize(res,0),self.tableize(res,1),
                                            self.tableize(res,2))):
            sub.append(I,"<module_data>");
        sub.append("","<module_data>");
        res[:] = ();

    def make_row(self,membername,value):
        membername = ":data:`rdma.IBA.%s`"%(membername)
        bit = self.bitmap.get(value);
        if bit:
            return (membername,"0x%x"%(value),"%r = %s"%(value,bit));
        return (membername,"0x%x"%(value),repr(value));

    def run(self):
        __import__(self.arguments[0]);
        self.object = sys.modules[self.arguments[0]];
        self.analyzer = sphinx.pycode.ModuleAnalyzer.for_module(self.arguments[0]);
        self.analyzer.parse();
        attr_visitor = MyVisitor('',self.analyzer.encoding);
        attr_visitor.visit(self.analyzer.parsetree)

        sub = docutils.statemachine.ViewList();
        res = [];
        title = None;
        for namespace,membername in attr_visitor.data:
            member = getattr(self.object,membername);
            if not (isinstance(member,int) or isinstance(member,long)):
                continue;
            doc = attr_visitor.collected.get((namespace,membername));
            if doc is not None:
                if res:
                    self.to_section(sub,res,title);
                title = doc[0];
            res.append(self.make_row(membername,member));
        if res:
            self.to_section(sub,res,title);

        node = docutils.nodes.paragraph();
        node.document = self.state.document;
        self.state.nested_parse(sub,0,node,match_titles=2);
        return node.children;

def setup(app):
    app.add_directive("module_data",ModuleDataDirective);
