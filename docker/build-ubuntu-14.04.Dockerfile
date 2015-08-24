# This Dockerfile will create an image suitable for creating the Trusty DEB
# See do_docker.py for how to use this.
FROM ubuntu:14.04
MAINTAINER Jason Gunthorpe <jgunthorpe@obsidianresearch.com>

RUN /bin/echo -e "deb http://archive.ubuntu.com/ubuntu/ trusty-updates main universe\ndeb http://archive.ubuntu.com/ubuntu trusty main universe\ndeb http://security.ubuntu.com/ubuntu trusty-security main universe" > /etc/apt/sources.list

RUN apt-get update && apt-get install -y \
    build-essential \
    cython \
    debhelper \
    dh-python \
    libc6-dev \
    libibverbs-dev \
    python-sphinx \
    python2.7 \
    python2.7-dev \
    && \
    rm -f /var/cache/apt/archives/*.deb
