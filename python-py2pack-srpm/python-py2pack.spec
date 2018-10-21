# Fedora and RHEL split python2 and python3
# Older RHEL does not include python3 by default
%if 0%{?fedora} || 0%{?rhel} > 7
%global with_python3 1
%else
%global with_python3 0
%endif

# Fedora > 28 no longer publishes python2 by default
%if 0%{?fedora} > 28
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
Release:        0.3%{?dist}
Summary:        Generate distribution packages from PyPI
Group:          Development/Languages/Python

License:        BSD
Source:         http://pypi.python.org/packages/source/m/py2pack-%{version}.tar.gz
Source1:        fedora.spec.python-mult

%if 0%{with_python2}
# Test requirements
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
# Version dependency confuses RHEL 7, due to python-pbr vs. python2-pbr
#BuildRequires:  python2-pbr >= 1.0
BuildRequires:  python2-pbr
%endif # with_python2
%if 0%{with_python3}
# Test requirements
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr >= 1.0
%endif # with_python3
BuildArch:      noarch

%description
This script allows to generate RPM spec or DEB dsc files from Python modules.
It allows to list Python modules or search for them on the Python Package Index
(PyPI). Conveniently, it can fetch tarballs and changelogs making it an
universal tool to package Python modules.

%if 0%{with_python2}
%package -n python2-py2pack
Summary:        %{summary}
Requires:  python2-metaextract
%{?python_provide:%python_provide python2-py2pack}

%description -n python2-py2pack
This script allows to generate RPM spec or DEB dsc files from Python modules.
It allows to list Python modules or search for them on the Python Package Index
(PyPI). Conveniently, it can fetch tarballs and changelogs making it an
universal tool to package Python modules.
%endif # with_python2

%if 0%{with_python3}
%package -n python3-py2pack
Summary:        %{summary}
Requires:  python3-metaextract
%{?python_provide:%python_provide python3-py2pack}

%description -n python3-py2pack
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

%build
%if 0%{with_python2}
%py2_build
%endif # with_python2
%if 0%{with_python3}
%py3_build
%endif # with_python3

%install
%if 0%{with_python2}
%py2_install
%{__mv} $RPM_BUILD_ROOT%{_bindir}/py2pack $RPM_BUILD_ROOT%{_bindir}/py2pack2
%if ! 0%{with_python3}
%{__ln_s} py2pack2 $RPM_BUILD_ROOT%{_bindir}/py2pack
%endif # ! with_python3
%endif # with_python2

%if 0%{with_python3}
%py3_install
%{__mv} $RPM_BUILD_ROOT%{_bindir}/py2pack $RPM_BUILD_ROOT%{_bindir}/py2pack3
%{__ln_s} py2pack3  $RPM_BUILD_ROOT%{_bindir}/py2pack
%endif # with_python3

# Upstream does not provide tests with 0.1.0, although
# the master branch does contain tests. With the next
# release, tests should be enabled.

%if 0%{with_python2}
%files -n python2-py2pack
%license LICENSE
%doc README.rst
%{python2_sitelib}/*
%{_bindir}/py2pack2
%if ! 0%{with_python3}
%{_bindir}/py2pack
%endif # ! with_python3
%endif # with_python2

%if 0%{with_python3}
%files -n python3-py2pack
%license LICENSE
%doc README.rst
%{python3_sitelib}/*
%{_bindir}/py2pack3
%{_bindir}/py2pack
%endif # with_python3

%changelog
* Wed Oct 17 2018  Nico Kadel-Garcia <nkadel@gmail.com> - 0.8.3-0.1
- Set default template to fedora.spec
- Update fedora.spec from https://github.com/nkadel/nkadel-py2pack

* Sat Oct 6 2018 Nico Kadel-Garcia <nkadel@gmail.com> - 0.8.3-0
- Initial import
- Add with-python for RHEL 7
- Add python-pbr >= 1.0 dependencies
