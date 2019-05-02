# Single python3 version in Fedora, python3_pkgversion macro not available
%{!?python3_pkgversion:%global python3_pkgversion 3}

# Fedora and RHEL split python2 and python3
%global with_python3 1

# Fedora > 28 no longer publishes python2 by default
%if 0%{?fedora} > 29
%global with_python2 0
%else
%global with_python2 1
%endif

# Older RHEL does not use dnf, does not support "Suggests"
%if 0%{?fedora} || 0%{?rhel} > 7
%global with_dnf 1
%else
%global with_dnf 0
%endif

Name:           python-py2pack
Version:        0.8.3
Release:        0.6%{?dist}
Summary:        Generate distribution packages from PyPI
Group:          Development/Languages/Python

License:        BSD
Source:         http://pypi.python.org/packages/source/m/py2pack-%{version}.tar.gz
Source1:        fedora.spec.python-mult

%if %{with_python2}
# Test requirements
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-pbr
%endif # with_python2
%if %{with_python3}
# Test requirements
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-pbr >= 1.0
%endif # with_python3

BuildArch:      noarch

%description
This script allows to generate RPM spec or DEB dsc files from Python modules.
It allows to list Python modules or search for them on the Python Package Index
(PyPI). Conveniently, it can fetch tarballs and changelogs making it an
universal tool to package Python modules.

%if %{with_python2}
%package -n python2-py2pack
Summary:        %{summary}
Requires:  python2-metaextract
Requires:  python2-jinja2
%{?python_provide:%python_provide python2-py2pack}

%description -n python2-py2pack
This script allows to generate RPM spec or DEB dsc files from Python modules.
It allows to list Python modules or search for them on the Python Package Index
(PyPI). Conveniently, it can fetch tarballs and changelogs making it an
universal tool to package Python modules.
%endif # with_python2

%if %{with_python3}
%package -n python%{python3_pkgversion}-py2pack
Summary:        %{summary}
Requires:  python%{python3_pkgversion}-metaextract
Requires:  python%{python3_pkgversion}-jinja2
%{?python_provide:%python_provide python%{python3_pkgversion}-py2pack}
%if ! %{with_python2}
Obsoletes: python2-py2pack < %{version}-%{release}
%endif

%description -n python%{python3_pkgversion}-py2pack
This script allows to generate RPM spec or DEB dsc files from Python modules.
It allows to list Python modules or search for them on the Python Package Index
(PyPI). Conveniently, it can fetch tarballs and changelogs making it an
universal tool to package Python modules.
%endif

%prep
%autosetup -n py2pack-%{version}
%{__install} -m0644 %{SOURCE1} py2pack/templates/fedora.spec

# Reset default to fedora.spec
sed -i.fedora "s/'opensuse.spec'/'fedora.spec'/g" py2pack/__init__.py

%if %{with_python3}
echo "Enabling python3 compilation in:  %{py3dir}"
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
%endif # with_python3

%install
%if %{with_python3}
pushd %{py3dir}
%py3_install
%{__mv} $RPM_BUILD_ROOT%{_bindir}/py2pack $RPM_BUILD_ROOT%{_bindir}/py2pack-%{py3_version}
popd
%endif # with_python3

%if %{with_python2}
%py2_install
%{__mv} $RPM_BUILD_ROOT%{_bindir}/py2pack $RPM_BUILD_ROOT%{_bindir}/py2pack-%{py2_version}
%endif # with_python2

# Make symlinks only after all install steps are completed
%if %{with_python3}
%{__ln_s} -f py2pack-%{py3_version} $RPM_BUILD_ROOT%{_bindir}/py2pack
%endif
%if %{with_python2}
%{__ln_s} -f py2pack-%{py3_version} $RPM_BUILD_ROOT%{_bindir}/py2pack
%endif

# Upstream does not provide tests with 0.1.0, although
# the master branch does contain tests. With the next
# release, tests should be enabled.

%if %{with_python2}
%files -n python2-py2pack
%license LICENSE
%doc README.rst
%{python2_sitelib}/*
%{_bindir}/py2pack-%{py2_version}
%if ! %{with_python3}
%{_bindir}/py2pack
%endif # ! with_python3
%endif # with_python2

%if %{with_python3}
%files -n python%{python3_pkgversion}-py2pack
%license LICENSE
%doc README.rst
%{python3_sitelib}/*
%{_bindir}/py2pack-%{py3_version}
%{_bindir}/py2pack
%endif # with_python3

%changelog
* Sat Apr 27 2019 Nico Kadel-Garcia <nkadel@gmail.com> - 0.8.3-0.6
- Update fedora.spec.python-mult with latest py2pack values for Fedora > 30
- Disable python2 building

* Sat Nov 10 2018 Nico Kadel-Garcia <nkadel@gmail.com> - 0.8.3-0.6
- Use BuildRequires "python-" instead of "python2-" for RHEL, to avoid EPEL dependencies
- Add Requires python-jinja2

* Mon Oct 22 2018 Nico Kadel-Garcia <nkadel@gmail.com> - 0.8.3-0.5
- Add "dist" to Release field in fedora.epc

* Sun Oct 21 2018 Nico Kadel-Garcia <nkadel@gmail.com> - 0.8.3-0.4
- Update handling of python3 and provides in fedora.spec
- Add python-setuptools dependencies to fedora.spec

* Wed Oct 17 2018 Nico Kadel-Garcia <nkadel@gmail.com> - 0.8.3-0.1
- Set default template to fedora.spec
- Update fedora.spec from https://github.com/nkadel/nkadel-py2pack

* Sat Oct 6 2018 Nico Kadel-Garcia <nkadel@gmail.com> - 0.8.3-0
- Initial import
- Add with-python for RHEL 7
- Add python-pbr >= 1.0 dependencies
