#
# _without_dist_kernel - without distribution kernel
#
%define		_orig_name	capsel
%define		_pre		rc1

Summary:	Capsel - supports Linux-Privs security model
Summary(pl):	Capsel - obs³uga modelu bezpieczeñstwa Linux-Privs
Name:		%{_orig_name}
Version:	2.0
%define	_rel	6
Release:	%{_pre}.%{_rel}
Group:		Base/Kernel
License:	GPL v2
Source0:	http://cliph.linux.pl/capsel/capsel-%{version}%{_pre}.tar.gz
Source1:	%{name}.init
Patch0:		%{name}-2.0rc2.diff
Patch1:		%{name}-no_kernel_smp.patch
Patch2:		%{name}-include-fix.patch
URL:		http://cliph.linux.pl/capsel/
%{!?_without_dist_kernel:BuildRequires: kernel-headers}
BuildRequires:	%{kgcc_package}
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:Requires:	kernel(capsel)}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Capsel module is a small but very powerful loadable Linux kernel
module. Its advanced security features allows to improve overall
system security.

%description -l pl
Capsel jest ma³ym, ale bardzo potê¿nym ³adowalnym modu³em dla Linuksa.
Jego cechy pozwalaj± zwiêkszyæ bezpieczeñstwo systemu.

%package -n kernel-misc-capsel
Summary:	Capsel - supports Linux-Privs security model
Summary(pl):	Capsel - obs³uga modelu bezpieczeñstwa Linux-Privs
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
Summary(pl):	Capsel - obs³uga modelu bezpieczeñstwa Linux-Privs
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Provides:	kernel(capsel)

%description -n kernel-smp-misc-capsel
Capsel - SMP kernel module.

%description -n kernel-smp-misc-capsel -l pl
Capsel - modu³ j±dra SMP.

%prep
%setup -q -n %{name}-%{version}%{_pre}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
mkdir bin/

%{__make} CC="%{kgcc} -DCONFIG_X86_LOCAL_APIC"
mv -f src/capsel.o bin/capsel.o

%{__make} clean

%{__make} CC="%{kgcc} -D__KERNEL_SMP=1 -D__SMP__ -DCONFIG_X86_LOCAL_APIC"
mv -f src/capsel.o bin/capselsmp.o

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{%{_sysconfdir}/{%{_orig_name},rc.d/init.d},/sbin/}
install capsel.conf	$RPM_BUILD_ROOT/%{_sysconfdir}/capsel/default
install src/user/capsel	$RPM_BUILD_ROOT/sbin/

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install bin/capsel.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/capsel.o

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc
install bin/capselsmp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/capsel.o

install %{SOURCE1}	$RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d/capsel

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add capsel
if [ -f /var/lock/subsys/capsel ]; then
        /etc/rc.d/init.d/capsel restart 1>&2
else
        echo "Run \"/etc/rc.d/init.d/caspel start\" to start capsel."
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/capsel ]; then
                /etc/rc.d/init.d/capsel stop 1>&2
        fi
        /sbin/chkconfig --del capsel
fi

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
%doc README CAPABILITIES ChangeLog TODO misc scripts conf
%attr(755,root,root) /sbin/*
%dir %attr(750,root,root) %{_sysconfdir}/capsel
%attr(755,root,root) %{_sysconfdir}/rc.d/init.d/capsel
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/capsel/*

%files -n kernel-misc-capsel
%defattr(644,root,root,755)
%attr(644,root,root) /lib/modules/%{_kernel_ver}/misc/*

%files -n kernel-smp-misc-capsel
%defattr(644,root,root,755)
%attr(644,root,root) /lib/modules/%{_kernel_ver}smp/misc/*
