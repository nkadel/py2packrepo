%global srcname py2pack

%if 0%{?fedora} || 0%{?rhel} > 7
%global with_python3 1
%else
%global with_python3 0
%endif

Name:           python-%{srcname}
Version:        0.8.3
Release:        0%{?dist}
Summary:        Tool to collect metadata about a python module
Group:          Development/Languages/Python

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
BuildRequires:  python2-pbr >= 1.0
Requires:  python2-metaextract
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
metaextract is a tool to collect metadata about a python module. 


%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        %{summary}
# Test requirements
BuildRequires:  python3-devel
BuildRequires:  python3-pbr >= 1.0
Requires:  python3-metaextract
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
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
%{__mv} $RPM_BUILD_ROOT%{_bindir}/py2pack $RPM_BUILD_ROOT%{_bindir}/py2pack2

%if 0%{?with_python3}
%py3_install
%{__mv} $RPM_BUILD_ROOT%{_bindir}/py2pack $RPM_BUILD_ROOT%{_bindir}/py2pack3
%{__ln_s} py2pack3  $RPM_BUILD_ROOT%{_bindir}/py2pack
%endif

# Upstream does not provide tests with 0.1.0, although
# the master branch does contain tests. With the next
# release, tests should be enabled.


%files -n python2-%{srcname}
%license LICENSE
%doc README.rst
%{python2_sitelib}/*
%{_bindir}/py2pack2


%if 0%{?with_python3}
%files -n python3-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/*
%{_bindir}/py2pack3
%{_bindir}/py2pack
%endif

%changelog
* Sat Oct 6 2018 Nico Kadel-Garcia <nkadel@gmail.com> - 0.8.3-0
- Initial import
- Add with-python for RHEL 7
- Add python-pbr >= 1.0 dependencies
