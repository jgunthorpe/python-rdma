# Copyright 2011 Obsidian Research Corp. GPLv2, see COPYING.
from __future__ import with_statement;
import os;
import sys;
import optparse;
import inspect;

class CmdError(Exception):
    """Thrown for any command line or command operation failures."""
    pass;

class MyHelpFormatter(optparse.IndentedHelpFormatter):
    def format_usage(self, usage):
        return usage + "\n";

class MyOptParse(optparse.OptionParser):
    #: Global verbosity for exception reporting
    verbosity = 0;

    def __init__(self,cmd,option_list = [],description = None):
        optparse.OptionParser.__init__(self,option_list=option_list,
                                       description=description,
                                       formatter=MyHelpFormatter());

        self.current_command = cmd;
        self.prog = "%s %s"%(os.path.basename(sys.argv[0]),cmd.__name__[4:]);

    def parse_args(self,args,values = None,expected_values=-1):
        (args,values) = optparse.OptionParser.parse_args(self,args,values);
        if expected_values != -1 and \
           len(values) != expected_values:
            self.error("Got %u arguments but expected %u"%(
                len(values),expected_values));
        return (args,values);

    def get_usage(self):
        usage = inspect.getdoc(self.current_command);
        docer = None;
        try:
            docer = self.current_command.func_globals[self.current_command.func_name + "_help"];
        except KeyError:
            pass;
        if docer is not None:
            usage = docer(self,self.current_command,usage);

        return self.formatter.format_usage(self.expand_prog_name(usage));

    def format_help(self, formatter=None):
        """Defer computing the help text until it is actually asked for."""
        return optparse.OptionParser.format_help(self,formatter);

default_module = __name__.rpartition('.')[0];

def get_cmd_func(name):
    # Fetch the commands dict from the top level
    commands = sys.modules['__main__'].commands;

    loc = commands[name];
    module = "." + name;
    func = "cmd_%s"%(name);
    shown = True;
    if loc is not None:
        if len(loc) >= 3:
            shown = loc[2];
        if len(loc) >= 2:
            func = loc[1];
        if len(loc) >= 1:
            module = loc[0];

    if module[0] == '.':
        module = default_module + module;

    rmodule = sys.modules.get(module);
    if rmodule is None:
        __import__(module);
        rmodule = sys.modules[module];
    return getattr(rmodule,func),shown;

def cmd_help(argv,o):
    """Display the help text
       Usage: %prog"""
    # Fetch the commands dict from the top level
    commands = sys.modules['__main__'].commands;

    (args,values) = o.parse_args(argv);

    if len(argv) == 0:
        # Abuse the optparse help formatter to format the help text for
        # our commands
        class Formatter(MyHelpFormatter):
            def format_option(self, option):
                if option.action == "help":
                    self.option_strings[option] = "help";
                else:
                    self.option_strings[option] = self.option_strings[option][3:];
                return MyHelpFormatter.format_option(self,option);

        o = MyOptParse(cmd_help);
        for k in sorted(commands.iterkeys()):
            if k == "help":
                continue
            func,shown = get_cmd_func(k);
            if not shown:
                continue;
            doc = inspect.getdoc(func);
            doc = [i for i in doc.split("\n") if len(i) != 0];
            o.add_option("--x" + k,action="store_true",help=doc[0]);

        prog = os.path.basename(sys.argv[0]);
        print "%s - %s\n"%(prog,o.top_mod.banner)
        print "Usage: %s command [args]"%(prog)
        print
        print o.format_option_help(Formatter());
        print "%s help [command] shows detailed help for each command"%(prog)
        return True;

    if len(argv) == 1 and commands.has_key(argv[0]):
        func,shown = get_cmd_func(argv[0]);
        o = MyOptParse(func);
        func(["--help"],o);
    else:
        print "No help text for %s"%(argv);
    return True;
