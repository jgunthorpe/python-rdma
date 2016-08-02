#!/usr/bin/env python
# Copyright 2015 Obsidian Research Corp. See COPYING.
# PYTHON_ARGCOMPLETE_OK
import argparse
import grp
import imp
import inspect
import json
import multiprocessing
import os
import pwd
import re
import shutil
import subprocess
import sys
import tempfile
from contextlib import contextmanager;

project = "python-rdma";

def get_build_args():
    """Return extra docker arguments for building. This is the system APT proxy."""
    args = [];
    if os.path.exists("/etc/apt/apt.conf.d/01proxy"):
        # The line in this file must be 'Acquire::http { Proxy "http://dockerhub.edm.orcorp.ca:3142"; };'
        with open("/etc/apt/apt.conf.d/01proxy") as F:
            proxy = F.read().strip().split('"')[1];
            args.append("--build-arg");
            args.append('http_proxy="%s"'%(proxy))
    return args;

def get_version():
    return imp.load_source('__tmp__','rdma/__init__.py').__version__;

def spec_xform_release(old,new,lines):
    res = [];
    for I in lines:
        if I.startswith("Release:"):
            I = I.replace(old,new);
        res.append(I);
    return res;

class Environment(object):
    aliases = set();
    def image_name(self):
        return "build-%s/%s"%(project,self.name);

class centos6(Environment):
    dockerfile = "docker/build-centos-6.Dockerfile";
    name = "centos6";

    def rpm_spec_xform(self,x):
        return x;

class centos7(Environment):
    dockerfile = "docker/build-centos-7.Dockerfile";
    name = "centos7";

    def rpm_spec_xform(self,x):
        return spec_xform_release("el6","el7",x);

class trusty(Environment):
    dockerfile = "docker/build-ubuntu-14.04.Dockerfile";
    name = "ubuntu-14.04";
    aliases = {"trusty"};

    is_deb = True;

class jessie(Environment):
    dockerfile = "docker/build-debian-8.Dockerfile";
    name = "debian-8";
    aliases = {"jessie"};

    is_deb = True;

class xenial(Environment):
    dockerfile = "docker/build-ubuntu-16.04.Dockerfile";
    name = "ubuntu-16.04";
    aliases = {"xenial"};

    is_deb = True;

environments = [centos6(),
                centos7(),
                trusty(),
                jessie(),
                xenial(),
];

class ToEnvAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values == "all":
            setattr(namespace, self.dest, sorted(environments,key=lambda x:x.name))
            return;

        for I in environments:
            if I.name == values or values in I.aliases:
                setattr(namespace, self.dest, [I])
                return;

def env_choices():
    """All the names that can be used with ToEnvAction"""
    envs = set(("all",));
    for I in environments:
        envs.add(I.name);
        envs.update(I.aliases);
    return envs;

def sh_cmd(args,allowfail=False):
    """Invoke a command"""
    ret = subprocess.call(args=args);
    if not allowfail and ret:
        raise subprocess.CalledProcessError(ret,args[0]);

def sh_cmd_str(args,allowfail=False):
    p = subprocess.Popen(args=args,stdout=subprocess.PIPE);
    res = p.communicate()[0];
    if not allowfail and p.returncode:
        raise subprocess.CalledProcessError(p.returncode,args[0]);
    return res;

def docker_cmd(env,*cmd):
    """Invoke docker"""
    if env.sudo:
        args = ["sudo","docker"];
    else:
        args = ["docker"];
    for I in cmd:
        args.append(I);
    sh_cmd(args);

def docker_cmd_str(env,*cmd):
    """Invoke docker"""
    if env.sudo:
        args = ["sudo","docker"];
    else:
        args = ["docker"];
    for I in cmd:
        args.append(I);
    return sh_cmd_str(args);

@contextmanager
def private_tmp(args):
    """Simple version of Python 3's tempfile.TemporaryDirectory"""
    dfn = tempfile.mkdtemp();
    try:
        yield dfn;
    finally:
        try:
            shutil.rmtree(dfn);
        except:
            # The debian builds result in root owned files because we don't use fakeroot
            sh_cmd(['sudo','rm','-rf',dfn]);

@contextmanager
def inDirectory(dir):
    cdir = os.getcwd();
    try:
        os.chdir(dir);
        yield True;
    finally:
        os.chdir(cdir);

def get_image_id(args,image_name):
    img = json.loads(docker_cmd_str(args,"inspect",image_name));
    image_id = img[0]["Id"];
    # Newer dockers put a prefix
    if ":" in image_id:
        image_id = image_id.partition(':')[2];
    return image_id;

def set_ccache(args,opts,tmpdir,home):
    if not args.ccache:
        return;
    opts.extend(["-v","%s/.ccache/:/ccache"%(os.getenv("HOME")),
                 "-e","CCACHE_DIR=/ccache",
                 "-e","CCACHE_COMPRESS=1",
                 "-e","CCACHE_COMPILERCHECK=content",
             ]);

def run_rpm_build(args,spec_file,env):
    version = get_version();
    with open(spec_file,"r") as F:
        for ln in F:
            if ln.startswith("Version:"):
                ver = ln.strip().partition(' ')[2];
                assert(ver == get_version());

            if ln.startswith("Source:"):
                tarfn = ln.strip().partition(' ')[2];
    tarfn = tarfn.replace("%{version}",get_version());

    image_id = get_image_id(args,env.image_name());
    with private_tmp(args) as tmpdir:
        os.mkdir(os.path.join(tmpdir,"SOURCES"));
        os.mkdir(os.path.join(tmpdir,"tmp"));

        sh_cmd(["git","archive",
               "--prefix","%s/"%(os.path.splitext(tarfn)[0]),
               "--output",os.path.join(tmpdir,"SOURCES",tarfn),
               "HEAD"]);

        with open(spec_file,"r") as inF:
            spec = list(inF);
        with open(os.path.join(tmpdir,spec_file),"w") as outF:
            outF.write("".join(env.rpm_spec_xform(spec)));

        home = os.path.join(os.path.sep,"home",os.getenv("LOGNAME"));
        vdir = os.path.join(home,"rpmbuild");

        opts = [
            "run",
            "--rm=true",
            "-v","%s:%s"%(tmpdir,vdir),
            "-w",vdir,
            "-h","builder-%s"%(image_id[:12]),
            "-e","HOME=%s"%(home),
            "-e","TMPDIR=%s"%(os.path.join(vdir,"tmp")),
        ];
        set_ccache(args,opts,tmpdir,home);

        # rpmbuild complains if we do not have an entry in passwd and group
        # for the user we are going to use to do the build.
        with open(os.path.join(tmpdir,"go.py"),"w") as F:
            print >> F,"""
import os;
with open("/etc/passwd","a") as F:
   print >> F, {passwd!r};
with open("/etc/group","a") as F:
   print >> F, {group!r};
os.setgid({gid:d});
os.setuid({uid:d});
""".format(passwd=":".join(str(I) for I in pwd.getpwuid(os.getuid())),
           group=":".join(str(I) for I in grp.getgrgid(os.getgid())),
           uid=os.getuid(),
           gid=os.getgid());

            # Transfer ccache options into a macro, rpmbuild clears the environment
            ccopts = [I for I in opts if I.startswith("CCACHE_")];
            if ccopts:
                bopts = ["--define",
                          "_ccache_options %s"%(" ".join(ccopts))]
            else:
                bopts = [];
            bopts.extend(["-bb",spec_file]);

            print >> F,'os.execlp("rpmbuild","rpmbuild",%s)'%(
                ",".join(repr(I) for I in bopts));

        if args.run_shell:
            opts.append("-ti");
        opts.append(env.image_name());

        if args.run_shell:
            opts.append("/bin/bash");
        else:
            opts.extend(["python","go.py"]);

        docker_cmd(args,*opts)

        print
        for path,jnk,files in os.walk(os.path.join(tmpdir,"RPMS")):
            for I in files:
                print "Final RPM: ",os.path.join("..",I);
                shutil.move(os.path.join(path,I),
                            os.path.join("..",I));

def run_deb_build(args,env):
    image_id = get_image_id(args,env.image_name());
    with private_tmp(args) as tmpdir:
        os.mkdir(os.path.join(tmpdir,"src"));
        os.mkdir(os.path.join(tmpdir,"tmp"));

        opwd = os.getcwd();
        with inDirectory(os.path.join(tmpdir,"src")):
            sh_cmd(["git",
                    "--git-dir",os.path.join(opwd,".git"),
                    "reset","--hard","HEAD"]);

        home = os.path.join(os.path.sep,"home",os.getenv("LOGNAME"));

        opts = [
            "run",
            "--read-only",
            "--rm=true",
            "-v","%s:%s"%(tmpdir,home),
            "-w",os.path.join(home,"src"),
            "-h","builder-%s"%(image_id[:12]),
            "-e","HOME=%s"%(home),
            "-e","TMPDIR=%s"%(os.path.join(home,"tmp")),
            "-e","DEB_BUILD_OPTIONS=parallel=%u"%(multiprocessing.cpu_count()),
        ];
        set_ccache(args,opts,tmpdir,home);

        # Create a go.py that will let us run the compilation as the user and
        # then switch to root only for the packaging step. We need to run
        # the build as non-root so things like ccache and dart pub cache
        # create cache files with the right user.
        with open(os.path.join(tmpdir,"go.py"),"w") as F:
            print >> F,"""
import os,sys;
child = os.fork();
if child == 0:
   os.setgid({gid:d});
   os.setuid({uid:d});
   os.execlp("debian/rules","debian/rules","build");
pid,status = os.waitpid(child,0);
if status != 0:
   sys.exit(status);
os.execlp("debian/rules","debian/rules","binary");
""".format(uid=os.getuid(),
           gid=os.getgid());

        if args.run_shell:
            opts.append("-ti");
        opts.append(env.image_name());

        if args.run_shell:
            opts.append("/bin/bash");
        else:
            opts.extend(["python",os.path.join(home,"go.py")]);

        docker_cmd(args,*opts);

        print
        for I in os.listdir(tmpdir):
            if I.endswith(".deb"):
                print "Final DEB: ",os.path.join("..",I);
                shutil.move(os.path.join(tmpdir,I),
                            os.path.join("..",I));

def args_build_images(parser):
    parser.add_argument("--env",action=ToEnvAction,choices=env_choices(),default="all");
def cmd_build_images(args):
    """Run from the top level source directory to make the docker images that are
    needed for building. This only needs to be run once."""
    for I in args.env:
        opts = ["build"] + \
               get_build_args() + [
                   "-f",I.dockerfile,
                   "-t",I.image_name(),
                   "docker/"];
        docker_cmd(args,*opts);

def args_pkg(parser):
    parser.add_argument("ENV",action=ToEnvAction,choices=env_choices());
    parser.add_argument("--run-shell",default=False,action="store_true",
                        help="Instead of running the build, enter a shell");
    parser.add_argument("--ccache",default=False,action="store_true",
                        help="Turn on cc cache for building");
def cmd_pkg(args):
    """Build a package in the given environment."""
    for env in args.ENV:
        if hasattr(env,"is_deb"):
            run_deb_build(args,env);
        if hasattr(env,"rpm_spec_xform"):
            run_rpm_build(args,"%s.spec"%(project),env);

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Operate docker for building this package')
    subparsers = parser.add_subparsers(title="Sub Commands");

    funcs = globals();
    for k,v in funcs.items():
        if k.startswith("cmd_") and inspect.isfunction(v):
            sparser = subparsers.add_parser(k[4:].replace('_','-'),
                                            help=v.__doc__);
            funcs["args_" + k[4:]](sparser);
            sparser.set_defaults(func=v);

    try:
        import argcomplete;
        argcomplete.autocomplete(parser);
    except ImportError:
        pass;

    args = parser.parse_args();
    args.sudo = True;

    # This script must always run from the top of the git tree, and a git
    # checkout is mandatory.
    git_top = sh_cmd_str(["git","rev-parse","--git-dir"]).strip();
    if git_top != ".git":
        os.chdir(os.path.dirname(git_top));

    if not args.func(args):
        sys.exit(100);
    sys.exit(0);
