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
