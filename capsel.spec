#
# _without_dist_kernel - without distribution kernel
#
%define		_rel		1
%define		_pre		pre5
%define		_orig_name	capsel

Summary:	Capsel - supports Linux-Privs security model
Summary(pl):	Capsel - wsparcie dla Linux-Privs
Name:		%{_orig_name}
Version:	1.9.99
Release:	%{_pre}.%{_rel}
Group:		Base/Kernel
License:	GPL v2
Source0:	http://cliph.linux.pl/capsel/capsel-1.9.99pre5.tar.gz
URL:		http://cliph.linux.pl/capsel/
%{!?_without_dist_kernel:BuildRequires: kernel-headers}
BuildRequires:	%{kgcc_package}
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:Requires:	kernel(capsel)}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Capsel module is a small but very powerful loadable Linux kernel module.
Its advanced security features allows to improve overall system security.

%description -l pl
Capsel jest ma³ym, ale bardzo potê¿nym ³adowalnym modu³em dla Linuksa.
Jego cechy pozwalaj± zwiêkszyæ bezpieczeñstwo systemu.

%package -n kernel-misc-capsel
Summary:	Capsel - supports Linux-Privs security model
Summary(pl):	Capsel - wsparcie dla Linux-Privs
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Provides:	kernel(capsel)

%description -n kernel-misc-capsel
Capsel - kernel module.

%description -n kernel-misc-capsel -l pl
Capsel - modu³ j±dra.

%package -n kernel-smp-misc-capsel
Summary:	Capsel - supports Linux-Privs security model
Summary(pl):	Capsel - wsparcie dla Linux-Privs
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Provides:	kernel(capsel)

%description -n kernel-smp-misc-capsel
Capsel - SMP kernel module.

%description -n kernel-smp-misc-capsel -l pl
Capsel - wieloprocesorowy modu³ j±dra.

%prep
%setup -q -n %{name}-%{version}%{_pre}

%build
mkdir bin/

%{__make} CC="%{kgcc} -DCONFIG_X86_LOCAL_APIC"
mv -f src/capsel.o bin/capsel.o

%{__make} clean

%{__make} CC="%{kgcc} -D__KERNEL_SMP=1 -DCONFIG_X86_LOCAL_APIC"
mv -f src/capsel.o bin/capselsmp.o

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{%{_sysconfdir}/%{_orig_name},/sbin/}
install capsel.conf	$RPM_BUILD_ROOT/%{_sysconfdir}/capsel/default
install src/user/capsel	$RPM_BUILD_ROOT/sbin/

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}
install bin/capsel.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/capsel.o

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp
install bin/capselsmp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/capsel.o

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-misc-capsel
/sbin/depmod -a

%postun	-n kernel-misc-capsel
/sbin/depmod -a

%post	-n kernel-smp-misc-capsel
/sbin/depmod -a

%postun	-n kernel-smp-misc-capsel
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%doc README CAPABILITIES ChangeLog TODO misc/* scripts/*
%attr(755,root,root) /sbin/*
%dir %attr(750,root,root) %{_sysconfdir}/capsel
%attr(750,root,root) %config(noreplace) %{_sysconfdir}/capsel/*

%files -n kernel-misc-capsel
%defattr(644,root,root,755)
%attr(644,root,root) /lib/modules/%{_kernel_ver}/*

%files -n kernel-smp-misc-capsel
%defattr(644,root,root,755)
%attr(644,root,root) /lib/modules/%{_kernel_ver}smp/*
