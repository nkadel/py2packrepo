%global dummy pbr

Name:       python2-%dummy
Version:    3.1.1
Release:    0%{?dist}
Summary:    Dummy package depending on python-%dummy
License:    Public Domain
Requires:   python-%dummy >= %version
BuildArch:  noarch

%description
This package exists only to allow packagers to uniformly depend on
python2-%dummy instead of conditionalizing those dependencies based on the
version of EPEL or Fedora.  It contains no files.

%files

%changelog
* Thu Oct 18 2018 Nico Kadel-Garcia <nkadel@gmail.com> - 3.1.1-0
- Imported from python2-sphinx to use for python2-pbr
