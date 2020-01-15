# SPDX-License-Identifier: GPL-2.0-only
# Copyright (C) 2019 Mellanox Technologies. All Rights Reserved.
#

%{!?_name: %define _name rshim}
%{!?_version: %define _version 2.0}
%{!?_release: %define _release 0}

%define debug_package %{nil}
%global _release1 %{_release}

Name: %{_name}
Version: %{_version}
Release: %{_release1}%{?_dist}
Summary: User-space rshim driver for BlueField SoC

%global WITH_SYSTEMD %(if ( test -d "%{_unitdir}" > /dev/null); then echo -n '1'; else echo -n '0'; fi)

Group: Applications/Internet	
License: GPLv2
URL: https://github.com/mellanox/rshim-user-space
Source: %{name}-%{version}.tar.gz
BuildRoot: %{?build_root:%{build_root}}%{!?build_root:/var/tmp/OFED}
Vendor: Mellanox Technologies

Obsoletes: %{name} < 2.0

%if "%{_vendor}" == "suse"
BuildRequires: pciutils-devel, libusb-devel, fuse-devel
%else
BuildRequires: pciutils-devel, libusbx-devel, fuse-devel
%endif

%description
This is the user-space driver to access the BlueField SoC via the rshim
interface. It provides ways to push boot stream, debug the target or login
into the target via virtual console or network interface.

%prep
%setup -q -n %{name}-%{version}

%build
./bootstrap.sh
%configure
make

%install
rm -rf %{buildroot}
%makeinstall -C src INSTALL_DIR="%{buildroot}%{_bindir}"
%if "%{WITH_SYSTEMD}" == "1"
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 0644 bfrshim.service %{buildroot}%{_unitdir}
%endif
%{__install} -d %{buildroot}%{_mandir}/man1
%{__install} -m 0644 man/bfrshim.1 %{buildroot}%{_mandir}/man1
%__spec_install_post

%post
%if "%{WITH_SYSTEMD}" == "1"
  systemctl daemon-reload
  systemctl enable bfrshim.service
%endif

%clean
rm -rf %{buildroot}

%preun
%if "%{WITH_SYSTEMD}" == "1"
systemctl stop bfrshim
%else
killall -9 bfrshim
%endif

%files
%defattr(-,root,root,-)
%%doc README.md
%if "%{WITH_SYSTEMD}" == "1"
%{_unitdir}/bfrshim.service
%endif
%{_bindir}/bfrshim
%{_mandir}/man1/bfrshim.1.gz

%changelog
* Mon Dec 16 2019 Liming Sun <lsun@mellanox.com>
- Initial packaging
