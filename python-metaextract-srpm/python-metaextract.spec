%global srcname metaextract

# Single python3 version in Fedora, python3_pkgversion macro not available
%{!?python3_pkgversion:%global python3_pkgversion 3}

%global with_python3 1

Name:           python-%{srcname}
Version:        1.0.4
Release:        0.1%{?dist}
Summary:        Tool to collect metadata about a python module

License:        BSD
Source:         http://pypi.python.org/packages/source/m/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

%description
metaextract is a tool to collect metadata about a python module. For example
you may have a sdist tarball from the `Python Package Index`_ and you want to
know it's dependencies. metaextract can collect theses dependencies.
The tool was first developed in `py2pack`_ but is now it's own module to be
useful for others, too.

%package -n python2-%{srcname}
Summary:        %{summary}
# Test requirements
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-pytest-runner
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
metaextract is a tool to collect metadata about a python module. 


%if 0%{?with_python3}
%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{summary}
# Test requirements
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-pytest-runner
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

%description -n python%{python3_pkgversion}-%{srcname}
metaextract is a tool to collect metadata about a python module. 
%endif

%prep
%autosetup -n %{srcname}-%{version}


%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif


%install
%py2_install
%{__mv} $RPM_BUILD_ROOT%{_bindir}/metaextract $RPM_BUILD_ROOT%{_bindir}/metaextract2

%if 0%{?with_python3}
%py3_install
%{__mv} $RPM_BUILD_ROOT%{_bindir}/metaextract $RPM_BUILD_ROOT%{_bindir}/metaextract3
%{__ln_s} metaextract3  $RPM_BUILD_ROOT%{_bindir}/metaextract
%endif


# Upstream does not provide tests with 0.1.0, although
# the master branch does contain tests. With the next
# release, tests should be enabled.


%files -n python2-%{srcname}
%license LICENSE
%doc README.rst
%{python2_sitelib}/*
%{_bindir}/metaextract2


%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/*
%{_bindir}/metaextract3
%{_bindir}/metaextract
%endif

%changelog
* Thu Apr 25 2019 Nico Kadel-Garcia <nkadel@gmail.com> - 1.0.4-0.1
- Activate with_python3

* Sat Oct 6 2018 Nico Kadel-Garcia <nkadel@gmail.com> - 1.0.4-0
- Initial import
- Add BuildRequires for pytest-runner
