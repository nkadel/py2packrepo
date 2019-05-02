%global pypi_name metaextract

%if 0%{?fedora} || 0%{?rhel} > 7
%global with_python3 1
%else
%global with_python3 0
%endif

Name:           python-%{pypi_name}
Version:        1.0.4
Release:        0%{?dist}
Summary:        Tool to collect metadata about a python module

License:        BSD
Source:         http://pypi.python.org/packages/source/m/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

%description
metaextract is a tool to collect metadata about a python module. For example
you may have a sdist tarball from the `Python Package Index`_ and you want to
know it's dependencies. metaextract can collect theses dependencies.
The tool was first developed in `py2pack`_ but is now it's own module to be
useful for others, too.


%package -n python2-%{pypi_name}
Summary:        %{summary}
# Test requirements
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-pytest-runner
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
metaextract is a tool to collect metadata about a python module. 


%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        %{summary}
# Test requirements
BuildRequires:  python3-devel
BuildRequires:  python3-pytest-runner
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
metaextract is a tool to collect metadata about a python module. 
%endif

%prep
%autosetup -n %{pypi_name}-%{version}


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


%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/*
%{_bindir}/metaextract2


%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/*
%{_bindir}/metaextract3
%{_bindir}/metaextract
%endif

%changelog
* Sat Oct 6 2018 Nico Kadel-Garcia <nkadel@gmail.com> - 1.0.4-0
- Initial import
- Add BuildRequires for pytest-runner
