Name: python-rdma
Version: 1.0
Release: 1el6
Summary: RDMA functionality for python

License: GPLv2+
URL: https://github.com/jgunthorpe/python-rdma
Vendor: Obsidian Research Corporation
Source: python-rdma-%{version}.tgz

BuildRequires: gcc
BuildRequires: libibverbs-devel
BuildRequires: python-devel
BuildRequires: python-sphinx
BuildRequires: Cython

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
This package contains the Python module rdma which provides a Python API for
the Linux RDMA stack. It is an amalgamation of the functionality contained in
the Open Fabrics Alliance packages libibmad, libibumad, libibverbs,
libibnetdisc and infiniband-diags.

A new API was developed for this library that is designed to take advantage of
Python features and provides a very uniform, integrated design across all the
different aspects of IB and RDMA programming. It has a particular focus on
ease of use and correct operation of the IB and RDMA protocol stacks.

The module is written entirely in Python and only relies on external system
libraries to provide ibverbs functionality.

%prep
%setup

# Record the GIT version this RPM was built from
echo "__git_head__ = '"`zcat %{sources} | git get-tar-commit-id`"'" >> rdma/__init__.py

%build
env CFLAGS="$RPM_OPT_FLAGS" python setup.py build
python setup.py docs

%install
python setup.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
install -m 755 -d %{buildroot}/%{_defaultdocdir}/%{name}-%{version}
install -m 644 doc/license.rst %{buildroot}/%{_defaultdocdir}/%{name}-%{version}/COPYING
install -m 755 -d %{buildroot}/%{_defaultdocdir}/%{name}-%{version}/html
cp -r doc/html/* %{buildroot}/%{_defaultdocdir}/%{name}-%{version}/html/

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc %{_defaultdocdir}/%{name}-%{version}/*
