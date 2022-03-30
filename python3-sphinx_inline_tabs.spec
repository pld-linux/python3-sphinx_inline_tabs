#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_with	tests	# unit tests (not included in sdist)

Summary:	Add inline tabbed content to your Sphinx documentation
Summary(pl.UTF-8):	Wstawianie treści z tabulacjami do dokumentacji Sphinksa
Name:		python3-sphinx_inline_tabs
Version:	2021.8.17b10
Release:	3
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/sphinx-inline-tabs/
Source0:	https://files.pythonhosted.org/packages/source/s/sphinx-inline-tabs/sphinx_inline_tabs-%{version}.tar.gz
# Source0-md5:	4f2f5fded69590e6442101f3757de770
URL:		https://pypi.org/project/sphinx-inline-tabs/
BuildRequires:	python3-modules >= 1:3.8
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-Sphinx >= 3
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-xdist
%endif
%if %{with doc}
BuildRequires:	python3-Sphinx >= 3
BuildRequires:	python3-furo
BuildRequires:	python3-myst_parser
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
Requires:	python3-modules >= 1:3.8
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Add inline tabbed content to your Sphinx documentation.

%description -l pl.UTF-8
Wstawianie treści z tabulacjami do dokumentacji Sphinksa.

%package apidocs
Summary:	API documentation for Python sphinx_inline_tabs module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona sphinx_inline_tabs
Group:		Documentation

%description apidocs
API documentation for Python sphinx_inline_tabs module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona sphinx_inline_tabs.

%prep
%setup -q -n sphinx_inline_tabs-%{version}

# force setuptools for pythonegg dependencies
%{__sed} -i -e 's/distutils.core/setuptools/' setup.py

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests
%endif

%if %{with doc}
cd docs
PYTHONPATH=$(pwd)/../src \
%{__python3} -m sphinx . build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%{py3_sitescriptdir}/sphinx_inline_tabs
%{py3_sitescriptdir}/sphinx_inline_tabs-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/*
%endif
