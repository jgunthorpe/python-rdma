# This Dockerfile will create an image suitable for creating the Trusty DEB
# See do_docker.py for how to use this.
FROM ubuntu:16.04
MAINTAINER Jason Gunthorpe <jgunthorpe@obsidianresearch.com>

RUN apt-get update && apt-get install -y \
    build-essential \
    cython \
    debhelper \
    dh-python \
    libc6-dev \
    libibverbs-dev \
    python-sphinx \
    python2.7 \
    python2.7-dev
