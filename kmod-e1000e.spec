%define kmod_name e1000e
Name:    kmod-%{kmod_name}
Summary: Intel(R) Gigabit Ethernet Connection
Version: 3.3.5.3
Release: 2%{?kpkgversion:%(echo .%{kpkgversion} | tr - _)}
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

%build
make -C src KERNEL_SRC=%{_usrsrc}/kernels/%{kversion}

%install
%{__install} -d %{buildroot}/lib/modules/%{kversion}/drivers/net/ethernet/intel/%{kmod_name}/
%{__install} src/%{kmod_name}.ko %{buildroot}/lib/modules/%{kversion}/drivers/net/ethernet/intel/%{kmod_name}/

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

%changelog
* Fri Feb 24 2017 Michal Gawlik <michal.gawlik@thalesgroup.com> 3.3.5.3-2
- spec: remove old method of module autoloading (michal.gawlik@thalesgroup.com)
- spec: add used kernel version (michal.gawlik@thalesgroup.com)

* Fri Jan 13 2017 Michal Gawlik <michal.gawlik@thalesgroup.com> 3.3.5.3-1
- Update driver to 3.3.5.3 (tomasz.rostanski@thalesgroup.com.pl)

* Wed Aug 03 2016 Tomasz Rostanski <tomasz.rostanski@thalesgroup.com> 3.3.5-2
- kmod-e1000e.spec: do not modprobe the driver automatically
  (tomasz.rostanski@thalesgroup.com.pl)

* Wed Aug 03 2016 Tomasz Rostanski <tomasz.rostanski@thalesgroup.com> 3.3.5-1
- Driver update to version 3.3.5 (tomasz.rostanski@thalesgroup.com.pl)

* Mon Aug 01 2016 Tomasz Rostanski <tomasz.rostanski@thalesgroup.com> 3.3.4-2
- tito: use release tagger (tomasz.rostanski@thalesgroup.com.pl)
- kmod-igb.spec: overwrite mainline kernel driver if present
  (tomasz.rostanski@thalesgroup.com.pl)

* Wed Jul 13 2016 Tomasz Rostanski <tomasz.rostanski@thalesgroup.com> 3.3.4-1
- new package built with tito

