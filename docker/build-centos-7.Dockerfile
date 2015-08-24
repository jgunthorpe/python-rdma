# This Dockerfile will create an image suitable for creating the el7 RPM
# See do_docker.py for how to use this.
FROM centos:7
MAINTAINER Jason Gunthorpe <jgunthorpe@obsidianresearch.com>

RUN yum install -y \
	Cython \
	gcc \
	libibverbs-devel \
	python-devel \
	python-sphinx \
	rpm-build \
	tar \
	&& yum clean all
