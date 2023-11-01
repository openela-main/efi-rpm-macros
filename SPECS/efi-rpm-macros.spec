Summary: Common RPM Macros for building EFI-related packages
Name: efi-rpm-macros
Version: 3
Release: 3%{?dist}
Group: Development/System
License: GPLv3+
URL: https://github.com/rhboot/%{name}/
BuildRequires: git sed
BuildArch: noarch

Source0: https://github.com/rhboot/%{name}/releases/download/%{version}/%{name}-%{version}.tar.bz2
Patch0001: 0001-macros.efi-srpm-make-all-of-our-macros-always-expand.patch

%global debug_package %{nil}
%global _efi_vendor_ %(eval echo $(sed -n -e 's/rhel/redhat/' -e 's/^ID=//p' /etc/os-release))

%description
%{name} provides a set of RPM macros for use in EFI-related packages.

%package -n efi-srpm-macros
Summary: Common SRPM Macros for building EFI-related packages
Group: Development/System
BuildArch: noarch
Requires: rpm

%description -n efi-srpm-macros
efi-srpm-macros provides a set of SRPM macros for use in EFI-related packages.

%package -n efi-filesystem
Summary: The basic directory layout for EFI machines
Group: System Environment/Base
BuildArch: noarch
Requires: filesystem

%description -n efi-filesystem
The efi-filesystem package contains the basic directory layout for EFI
machine bootloaders and tools.

%prep
%autosetup -S git

%build
%make_build EFI_VENDOR=%{_efi_vendor_} clean all

%install
%make_install EFI_VENDOR=%{_efi_vendor_}

#%%files
#%%{!?_licensedir:%%global license %%%%doc}
#%%license LICENSE
#%%doc README
#%%{_rpmmacrodir}/macros.efi

%files -n efi-srpm-macros
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README
%{_rpmmacrodir}/macros.efi-srpm

%files -n efi-filesystem
%defattr(0700,root,root,-)
%verify(not mode) %dir /boot/efi
%verify(not mode) %dir /boot/efi/EFI
%verify(not mode) %dir /boot/efi/EFI/BOOT
%verify(not mode) %dir /boot/efi/EFI/%{_efi_vendor_}

%changelog
* Thu Nov 05 2020 Javier Martinez Canillas <javierm@redhat.com> - 3-3
- Ignore the mode bits when doing RPM verification of files in /boot/efi
  Resolves: rhbz#1845052

* Fri May 04 2018 Peter Jones <pjones@redhat.com> - 3-2
- Always provide macros for efi_arch and efi_alt_arch (and their _upper
  variants), and make efi_has_arch and efi_has_alt_arch 0 when they will be
  wrong.  This ensures everything can always expand when we're on a non-efi
  architecture.

* Fri May 04 2018 Peter Jones <pjones@redhat.com> - 3-1
- Update to version 3 to try and un-break rawhide composes due to
  ExclusiveArch constraints.

* Thu May 03 2018 Peter Jones <pjones@redhat.com> - 2-6
- Rework the macros for better srpm use.

* Wed May 02 2018 Peter Jones <pjones@redhat.com> - 2-5
- Add efi-filesystem subpackage

* Wed May 02 2018 Peter Jones <pjones@redhat.com> - 2-4
- Add %%{efi_has_alt_arch}

* Tue May 01 2018 Peter Jones <pjones@redhat.com> - 2-3
- Make an efi-srpm-macros subpackage to pull in so %%{efi} works in
  ExclusiveArch in koji.

* Tue May 01 2018 Peter Jones <pjones@redhat.com> - 2-2
- Fix the non-efi and non-efi-alt-arch cases, hopefully.

* Tue May 01 2018 Peter Jones <pjones@redhat.com> - 2-1
- Lots of rpmlint fixups and the like.

* Mon Apr 30 2018 Peter Jones <pjones@redhat.com> - 1-1
- First shot at building it.
