#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
#
%define		_orig_name	capsel
%define		_pre		rc1

%define	_rel	11
Summary:	Capsel - supports Linux-Privs security model
Summary(pl.UTF-8):	Capsel - obsługa modelu bezpieczeństwa Linux-Privs
Name:		%{_orig_name}
Version:	2.0
Release:	%{_pre}.%{_rel}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://cliph.linux.pl/capsel/capsel-%{version}%{_pre}.tar.gz
# Source0-md5:	f886467eb458812f8ee426541c7e4e06
Source1:	%{name}.init
Patch0:		%{name}-2.0rc2.diff
Patch1:		%{name}-no_kernel_smp.patch
Patch2:		%{name}-include-fix.patch
URL:		http://cliph.linux.pl/capsel/
BuildRequires:	%{kgcc_package}
%{?with_dist_kernel:BuildRequires:	kernel-headers}
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
%{?with_dist_kernel:Requires:	kernel(capsel)}
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Capsel module is a small but very powerful loadable Linux kernel
module. Its advanced security features allows to improve overall
system security.

%description -l pl.UTF-8
Capsel jest małym, ale bardzo potężnym ładowalnym modułem dla Linuksa.
Jego cechy pozwalają zwiększyć bezpieczeństwo systemu.

%package -n kernel-misc-capsel
Summary:	Capsel - supports Linux-Privs security model
Summary(pl.UTF-8):	Capsel - obsługa modelu bezpieczeństwa Linux-Privs
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Provides:	kernel(capsel)

%description -n kernel-misc-capsel
Capsel - kernel module.

%description -n kernel-misc-capsel -l pl.UTF-8
Capsel - moduł jądra.

%package -n kernel-smp-misc-capsel
Summary:	Capsel - supports Linux-Privs security model
Summary(pl.UTF-8):	Capsel - obsługa modelu bezpieczeństwa Linux-Privs
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Provides:	kernel(capsel)

%description -n kernel-smp-misc-capsel
Capsel - SMP kernel module.

%description -n kernel-smp-misc-capsel -l pl.UTF-8
Capsel - moduł jądra SMP.

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
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/{%{_orig_name},rc.d/init.d},/sbin} \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{/misc,smp/misc}

install capsel.conf	$RPM_BUILD_ROOT%{_sysconfdir}/capsel/default
install src/user/capsel	$RPM_BUILD_ROOT/sbin/

install bin/capsel.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/capsel.o
install bin/capselsmp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/capsel.o

install %{SOURCE1}	$RPM_BUILD_ROOT/etc/rc.d/init.d/capsel

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add capsel
%service capsel restart

%preun
if [ "$1" = "0" ]; then
	%service capsel stop
	/sbin/chkconfig --del capsel
fi

%post	-n kernel-misc-capsel
%depmod %{_kernel_ver}

%postun	-n kernel-misc-capsel
%depmod %{_kernel_ver}

%post	-n kernel-smp-misc-capsel
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-misc-capsel
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc README CAPABILITIES ChangeLog TODO misc scripts conf
%attr(755,root,root) /sbin/*
%dir %attr(750,root,root) %{_sysconfdir}/capsel
%attr(754,root,root) /etc/rc.d/init.d/capsel
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/capsel/*

%files -n kernel-misc-capsel
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*

%files -n kernel-smp-misc-capsel
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/*
