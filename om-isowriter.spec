%define _empty_manifest_terminate_build 0
%global srcname om-isowriter
# lto causes crash
%define _disable_lto 1

Summary:	Tool to write hybrid ISO files onto USB disks
Name:		om-isowriter
Version:	2.6.2.2
Release:	1
License:	GPLv3+
Group:		File tools
#Url:		https://abf.io/soft/rosa-imagewriter
Source0:	%{name}-%{version}.tar.gz
BuildRequires:	qmake5
BuildRequires:	qt5-linguist-tools
BuildRequires:	qt5-devel
BuildRequires:	pkgconfig(udev)
Suggests:	%mklibname udev 1
# (tpg) needed for kdesu
Suggests:	kde-cli-tools >= 5.5.5

%description
om-isowriter is a tool to write a .iso file to a USB disk.

%files
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_docdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/kde4/services/ServiceMenus/*.desktop
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg

#----------------------------------------------------------------------------

%prep
%setup -q -n %{srcname}-%{version}
%autopatch -p1

%build
%qmake_qt5
make
%{_qt5_bindir}/lrelease RosaImageWriter.pro

# for lrelease
export PATH=%{_qt5_bindir}:$PATH
lang/build-translations

%install
mkdir -p                                               \
	%{buildroot}%{_bindir}                             \
	%{buildroot}%{_libdir}/%{name}/lang                \
	%{buildroot}%{_docdir}/%{name}                     \
	%{buildroot}%{_iconsdir}/hicolor/scalable/apps     \
	%{buildroot}%{_datadir}/applications               \
	%{buildroot}%{_datadir}/kde4/services/ServiceMenus
install -m 0755 om-isowriter %{buildroot}%{_libdir}/%{name}/%{name}
install -m 0644 lang/*.qm %{buildroot}%{_libdir}/%{name}/lang/
install -m 0644 doc/* %{buildroot}%{_docdir}/%{name}/
install -m 0644 res/icon-rosa.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
ln -sf %{_libdir}/%{name}/%{name} %{buildroot}%{_bindir}/%{name}

cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Version=1.0
Name=om-isowriter
Comment=Ttool to write a .iso file to a USB drive
Exec=%{_libdir}/%{name}/%{name} %%U
Icon=%{name}
Terminal=false
Type=Application
Categories=System;
MimeType=application/x-iso;application/x-cd-image
EOF

cat > %{buildroot}%{_datadir}/kde4/services/ServiceMenus/riw_write_iso_image.desktop <<EOF
[Desktop Entry]
Type=Service
Actions=WriteIsoImageToUsb;
ServiceTypes=KonqPopupMenu/Plugin
MimeType=application/x-iso;application/x-cd-image;inode/ISO-image

[Desktop Action WriteIsoImageToUsb]
Exec=%{_libdir}/%{name}/%{name} %%U
Name=Write to USB using om-isowriter
Icon=%{name}
EOF

desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/%{name}.desktop
