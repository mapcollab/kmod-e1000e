%define kmod_name e1000e
Name:    kmod-%{kmod_name}
Summary: Intel(R) Gigabit Ethernet Connection
Version: 3.3.4
Release: 1
Source: %{name}-%{version}.tar.gz
Vendor: Intel Corporation
License: GPL
ExclusiveOS: linux
Group: System Environment/Kernel
Provides: %{name}
URL: http://support.intel.com/support/go/linux/e1000e.htm
BuildRoot: %{_tmppath}/%{name}-%{version}-root

# do not generate debugging packages by default - newer versions of rpmbuild
# may instead need:
%define debug_package %{nil}
%debug_package %{nil}

Requires: kernel, fileutils, findutils, gawk, bash

%if %{?kpkgversion:1}%{?!kpkgversion:0}
Requires: kernel = %{kpkgversion}
BuildRequires: kernel-devel = %{kpkgversion}
%endif

%description
This package contains the Linux driver for the Intel(R) Gigabit Family of Server Adapters.

%prep
%setup
%if "%{?kversion:1}%{?!kversion:0}%{?kpkgversion:1}%{?!kpkgversion:0}" != "11"
echo 'kversion (path to kernel src) and kpkgversion (version of kernel pkg) must be defined externally!'
exit 1
%endif

%{__cat} <<EOF > kmod-%{kmod_name}.modules
#!/bin/bash
modprobe %{kmod_name} &>/dev/null
EOF

%build
make -C src KERNEL_SRC=%{_usrsrc}/kernels/%{kversion}

%install
%{__install} -d %{buildroot}/lib/modules/%{kversion}/drivers/net/ethernet/intel/%{kmod_name}/
%{__install} -d %{buildroot}%{_sysconfdir}/sysconfig/modules/
%{__install} src/%{kmod_name}.ko %{buildroot}/lib/modules/%{kversion}/drivers/net/ethernet/intel/%{kmod_name}/
%{__install} kmod-%{kmod_name}.modules %{buildroot}%{_sysconfdir}/sysconfig/modules/

# Sign the modules(s).
%if %{?_with_modsign:1}%{!?_with_modsign:0}
# If the module signing keys are not defined, define them here.
%{!?privkey: %define privkey %{_sysconfdir}/pki/SECURE-BOOT-KEY.priv}
%{!?pubkey: %define pubkey %{_sysconfdir}/pki/SECURE-BOOT-KEY.der}
for module in $(find %{buildroot} -type f -name \*.ko);
do %{__perl} /usr/src/kernels/%{kversion}/scripts/sign-file \
    sha256 %{privkey} %{pubkey} $module;
done
%endif


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0755,root,root) /lib/modules/%(echo %{kversion})/drivers/net/ethernet/intel/%{kmod_name}/%{kmod_name}.ko
%attr(0755,root,root) %{_sysconfdir}/sysconfig/modules/kmod-%{kmod_name}.modules

%changelog
* Wed Jul 13 2016 Tomasz Rostanski <tomasz.rostanski@thalesgroup.com> 3.3.4-1
- new package built with tito

