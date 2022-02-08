# Adapted https://src.fedoraproject.org/rpms/python-packaging/blob/rawhide/f/python-packaging.spec for SailfishOS
# TODO build wheel (missing dependency python-wheel)
%global dist_name packaging
# suffix of python executable
%global python_pkgversion 3

%define source_date_epoch_from_changelog 1
%define clamp_mtime_to_source_date_epoch 1
%define use_source_date_epoch_as_buildtime 1

# note: macros in name break OBS build
Name:           python3-packaging
Summary:        Core utilities for Python packages
Version:        21.3
Release:        1%{?dist}
License:        BSD or ASL 2.0
URL:            https://github.com/pypa/packaging
Source:         %{name}-%{version}.tar.bz2
BuildArch:      noarch
BuildRequires:  python%{python_pkgversion}-devel
BuildRequires:  python%{python_pkgversion}-setuptools

# disable tests by default due to missing dependencies
%bcond_without docs
%bcond_with tests
%if %{with tests}
BuildRequires:  python%{python_pkgversion}-pytest
BuildRequires:  python%{python_pkgversion}-pretend
%endif
%if %{with docs}
BuildRequires:  python%{python_pkgversion}-sphinx
%endif

%description
This module provides core utilities for Python packages like utilities for
dealing with versions, specifiers, markers etc.

%if %{with docs}
%package -n python-%{dist_name}-doc
Summary:        python-packaging documentation

%description -n python-%{dist_name}-doc
Documentation for python-packaging
%endif

%prep
%autosetup -n %{name}-%{version}/packaging

%build
%py3_build

%if %{with docs}
# Theme not available
sed -i '/html_theme = "furo"/d' docs/conf.py
sphinx-build docs html
# cleanup
rm -rf html/.{doctrees,buildinfo}
%endif

%install
%py3_install
echo '%{python3_sitelib}/packaging*' > %{pyproject_files}
# cleanup
rm %{buildroot}/%{python3_sitelib}/%{dist_name}-*.egg-info/SOURCES.txt

%check
%if %{with tests}
%pytest
%endif

%files -f %{pyproject_files}
%license LICENSE LICENSE.APACHE LICENSE.BSD
%doc README.rst CHANGELOG.rst CONTRIBUTING.rst

%if %{with docs}
%files -n python-%{dist_name}-doc
%license LICENSE LICENSE.APACHE LICENSE.BSD
%doc html
%endif

%changelog
* Fri Feb 04 2022 takimata <takimata@gmx.de> - 21.3-1
- Initial packaging for Chum
