Name:    coyim
Version: 0.3.6
Release: 1.2%{?dist}
Summary: A safe and secure chat client
URL: https://coy.im/
ExclusiveArch:  %{go_arches}
BuildRequires:  golang >= 1.6
BuildRequires:  gtk3-devel >= 3.20
BuildRequires:  git
BuildRequires:  desktop-file-utils
License:        GPLv3+
Source0: https://github.com/twstrike/%{name}/archive/v%{version}.tar.gz
Source1: coyim.1
Source2: coyim.desktop

%description
A safe and secure chat client for Jabber/XMPP.

%prep
%autosetup
cp -p %SOURCE1 ./build/

%build
mkdir -p src/github.com/twstrike
ln -s ../../../ src/github.com/twstrike/%{name}
export GOPATH=$(pwd):%{gopath}
make build-gui

%install
install -d %{buildroot}%{_bindir}
install -p -m 755 bin/%{name} %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}/man1
install -p -m 644 build/%{name}.1 %{buildroot}%{_mandir}/man1
desktop-file-install --dir=${RPM_BUILD_ROOT}%{_datadir}/applications %{SOURCE2}

%files
%defattr(-,root,root,-)
%doc CONTRIBUTING.md DOWNLOADING.md LICENSE LICENSE.xmpp-client README.md
%{_bindir}/%{name}
%{_mandir}/*
%{_datadir}/*

%changelog
* Wed Oct 12 2016 Hubert Figuiere <hub@figuiere.net> - 0.3.6-1
- Initial release
