%global pypi_name metaextract

%global with_python3 1

%if 0%{?fedora} < 30
%global with_python2 1
%else
%global with_python2 0
%endif

Name:           python-%{pypi_name}
Version:        1.0.6
Release:        0%{?dist}
Summary:        Tool to collect metadata about a python module

License:        BSD
Source:         http://pypi.python.org/packages/source/m/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch
%if 0%{?rhel}
BuildRequires:  epel-rpm-macros
%endif

%description
metaextract is a tool to collect metadata about a python module. For example
you may have a sdist tarball from the `Python Package Index`_ and you want to
know it's dependencies. metaextract can collect theses dependencies.
The tool was first developed in `py2pack`_ but is now it's own module to be
useful for others, too.

%if %{with_python2}
%package -n python2-%{pypi_name}
Summary:        %{summary}
# Test requirements
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-pytest-runner
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
metaextract is a tool to collect metadata about a python module. 
%endif # with_python2

%if %{with_python3}
%package -n python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
# Test requirements
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-pytest-runner
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description -n python%{python3_pkgversion}-%{pypi_name}
metaextract is a tool to collect metadata about a python module. 
%endif

%prep
%autosetup -n %{pypi_name}-%{version}

%if %{with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%if %{with_python2}
%py2_build
%endif # with_python2

%if %{with_python3}
pushd %{py3dir}
%py3_build
popd
%endif

%install
%if %{with_python3}
# py3_install has to happen first
pushd %{py3dir}
%py3_install
%{__mv} $RPM_BUILD_ROOT%{_bindir}/metaextract $RPM_BUILD_ROOT%{_bindir}/metaextract-%{python3_version}
popd
%endif

%if %{with_python2}
%py2_install
%{__mv} $RPM_BUILD_ROOT%{_bindir}/metaextract $RPM_BUILD_ROOT%{_bindir}/metaextract-%{python2_version}
%endif # with_python2

# Make symlinks only after all install steps are completed
%if %{with_python3}
%{__ln_s} -f --no-dereference metaextract-%{python3_version} $RPM_BUILD_ROOT%{_bindir}/metaextract
%endif
%if %{with_python2}
%{__ln_s} -f --no-dereference metaextract-%{python3_version} $RPM_BUILD_ROOT%{_bindir}/metaextract
%endif

# Upstream does not provide tests with 0.1.0, although
# the master branch does contain tests. With the next
# release, tests should be enabled.

%if %{with_python2}
%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/*
%{_bindir}/metaextract-%{python2_version}
# Include linked binary if only with_python2
%if ! %{with_python3}
%{_bindir}/metaextract
%endif # # ! with_python3
%endif # with_python2

%if %{with_python3}
%files -n python%{python3_pkgversion}-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/*
%{_bindir}/metaextract-%{python3_version}
%{_bindir}/metaextract
%endif # with_python3

%changelog
* Sat Oct 5 2019 Nico Kadel-Garcia <nkadel@gmail.com> - 1.0.6-0
- Update to 1.0.6

* Thu May 2 2019 Nico Kadel-Garcia <nkadel@gmail.com> - 1.0.4-0.1
- Add python3_pkgversion for RHEL
- Straighten out symlinking for binaries

* Sat Oct 6 2018 Nico Kadel-Garcia <nkadel@gmail.com> - 1.0.4-0
- Initial import
- Add BuildRequires for pytest-runner
