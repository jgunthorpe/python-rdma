# This Dockerfile will create an image suitable for creating the el6 RPM
# See do_docker.py for how to use this.
FROM centos:6
MAINTAINER Jason Gunthorpe <jgunthorpe@obsidianresearch.com>

RUN yum install -y \
	gcc \
	libibverbs-devel \
	python-devel \
	python-sphinx \
	rpm-build \
	tar \
	&& yum clean all

ADD http://vault.centos.org/7.1.1503/os/Source/SPackages/Cython-0.19-3.el7.src.rpm /tmp/
RUN rpmbuild --rebuild /tmp/Cython-0.19-3.el7.src.rpm && \
    rpm -U /root/rpmbuild/RPMS/x86_64/Cython-0.19-3.el6.x86_64.rpm && \
    rm -rf /root/rpmbuild
