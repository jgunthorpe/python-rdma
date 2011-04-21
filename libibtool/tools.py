# Copyright 2011 Obsidian Research Corp. GPLv2, see COPYING.
from __future__ import with_statement;
import os;
import sys;
import optparse;
import inspect;

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
