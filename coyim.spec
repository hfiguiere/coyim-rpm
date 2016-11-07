Name:    coyim
Version: 0.3.7
Release: 1%{?dist}
Summary: A safe and secure chat client
URL: https://coy.im/
ExclusiveArch:  %{go_arches}
BuildRequires:  golang >= 1.6
BuildRequires:  gtk3-devel >= 3.20
BuildRequires:  git
BuildRequires:  desktop-file-utils
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
License:        GPLv3+
Source0: https://github.com/twstrike/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1: coyim.1
Source2: coyim.desktop

%description
A safe and secure chat client for Jabber/XMPP.

%prep
%autosetup  -n %{name}-%{version}

%build
mkdir -p src/github.com/twstrike
ln -s ../../../ src/github.com/twstrike/%{name}
export GOPATH=$(pwd):%{gopath}
make build-gui

%install
install -d %{buildroot}%{_bindir}
install -p -m 755 bin/%{name} %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}/man1
install -p -m 644 %SOURCE1 %{buildroot}%{_mandir}/man1
for size in 16x16 32x32 128x128 256x256 512x512; do
    install -d %{buildroot}%{_datadir}/icons/hicolor/${size}/apps
    install -p build/mac-bundle/coy.iconset/icon_${size}.png %{buildroot}%{_datadir}/icons/hicolor/${size}/apps/%{name}.png
done
desktop-file-install --dir=${RPM_BUILD_ROOT}%{_datadir}/applications %{SOURCE2}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%defattr(-,root,root,-)
%doc CONTRIBUTING.md DOWNLOADING.md LICENSE LICENSE.xmpp-client README.md
%{_bindir}/%{name}
%{_mandir}/man1/*
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*

%changelog
* Sun Nov 06 2016 Hubert Figuiere <hub@figuiere.net> - 0.3.7-1
- Upstream 0.3.7 https://coy.im/coyim/update/2016/10/27/release-notes-0.3.7.html
* Wed Oct 12 2016 Hubert Figuiere <hub@figuiere.net> - 0.3.6-1.3
- Initial release
