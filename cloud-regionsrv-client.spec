#
# spec file for package cloud-regionsrv-client
#
# Copyright (c) 2020 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%define base_version 9.1.5
Name:           cloud-regionsrv-client
Version:        %{base_version}
Release:        0
Summary:        Cloud Environment Guest Registration
License:        LGPL-3.0-only
Group:          Productivity/Networking/Web/Servers
URL:            http://www.github.com:SUSE-Enceladus/cloud-regionsrv-client
Source0:        %{name}-%{version}.tar.bz2
Requires:       SUSEConnect
Requires:       ca-certificates
Requires:       cloud-regionsrv-client-config
Requires:       pciutils
Requires:       procps
Requires:       python3
Requires:       python3-M2Crypto
Requires:       python3-lxml
Requires:       python3-requests
Requires:       python3-urllib3
Requires:       python3-zypp-plugin
Requires:       regionsrv-certs
Requires:       zypper
BuildRequires:  systemd
%{?systemd_requires}
BuildRequires:  python3-M2Crypto
BuildRequires:  python3-lxml
BuildRequires:  python3-requests
BuildRequires:  python3-setuptools
BuildRequires:  python3-zypp-plugin
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

BuildArch:      noarch

%description
Obtain cloud SMT server information from the region server configured in
/etc/regionserverclnt.cfg

%package generic-config
Version:        1.0.0
Release:        0
Summary:        Cloud Environment Guest Registration Configuration
Group:          Productivity/Networking/Web/Servers
Provides:       cloud-regionsrv-client-config
Provides:       regionsrv-certs
Conflicts:      otherproviders(cloud-regionsrv-client-config)

%description generic-config
Generic configuration for the registration client. The configuration needs
to be adapted for the specific cloud framework after installation.

%package plugin-gce
Version:        1.0.0
Release:        0
Summary:        Cloud Environment Guest Registration Plugin for GCE
Group:          Productivity/Networking/Web/Servers
Requires:       cloud-regionsrv-client >= 6.0.0

%description plugin-gce
Guest registration plugin for images intended for Google Compute Engine

%package plugin-ec2
Version:        1.0.1
Release:        0
Summary:        Cloud Environment Guest Registration Plugin for Amazon EC2
Group:          Productivity/Networking/Web/Servers
Requires:       cloud-regionsrv-client >= 6.0.0

%description plugin-ec2
Guest registration plugin for images intended for Amazon EC2

%package plugin-azure
Version:        1.0.1
Release:        0
Summary:        Cloud Environment Guest Registration Plugin for Microsoft Azure
Group:          Productivity/Networking/Web/Servers
Requires:       cloud-regionsrv-client >= 6.0.0
Requires:       python3-dnspython

%description plugin-azure
Guest registration plugin for images intended for Microsoft Azure

%prep
%setup -q

%build
python3 setup.py build

%install
cp -r etc %{buildroot}
cp -r usr %{buildroot}
python3 setup.py install --prefix=%{_prefix}  --root=%{buildroot}
mkdir -p %{buildroot}/var/lib/regionService/certs
mkdir -p %{buildroot}/var/lib/cloudregister
install -d -m 755 %{buildroot}/%{_mandir}/man1
install -m 644 man/man1/* %{buildroot}/%{_mandir}/man1
gzip %{buildroot}/%{_mandir}/man1/*

%pre
%service_add_pre guestregister.service containerbuild-regionsrv.service

%post
%{_sbindir}/switchcloudguestservices
%{_sbindir}/updatesmtcache
%service_add_post guestregister.service containerbuild-regionsrv.service

%preun
%service_del_preun guestregister.service containerbuild-regionsrv.service

%postun
%service_del_postun guestregister.service containerbuild-regionsrv.service

%files
%defattr(-,root,root,-)
%doc README
%license LICENSE
%dir %{_usr}/lib/zypp
%dir %{_usr}/lib/zypp/plugins
%dir %{_usr}/lib/zypp/plugins/urlresolver
%dir /var/lib/cloudregister
%{_mandir}/man*/*
%{_sbindir}/containerbuild-regionsrv
%{_sbindir}/cloudguest-repo-service
%{_sbindir}/switchcloudguestservices
%{_sbindir}/registercloudguest
%{_sbindir}/updatesmtcache
%{_usr}/lib/zypp/plugins/urlresolver/susecloud
%{python3_sitelib}/cloudregister/__*
%{python3_sitelib}/cloudregister/reg*
%{python3_sitelib}/cloudregister/smt*
%{python3_sitelib}/cloudregister/VERSION
%{_unitdir}/guestregister.service
%{_unitdir}/containerbuild-regionsrv.service
%dir %{python3_sitelib}/cloudregister-%{base_version}-py%{py3_ver}.egg-info
%dir %{python3_sitelib}/cloudregister/
%{python3_sitelib}/cloudregister-%{base_version}-py%{py3_ver}.egg-info/*

%files generic-config
%defattr(-,root,root,-)
%dir /var/lib/regionService
%dir /var/lib/regionService/certs
%config %{_sysconfdir}/regionserverclnt.cfg

%files plugin-gce
%defattr(-,root,root,-)
%{python3_sitelib}/cloudregister/google*

%files plugin-ec2
%defattr(-,root,root,-)
%{python3_sitelib}/cloudregister/amazon*

%files plugin-azure
%defattr(-,root,root,-)
%{python3_sitelib}/cloudregister/msft*

%changelog
