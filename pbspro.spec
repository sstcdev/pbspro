
#
# Copyright (C) 1994-2019 Altair Engineering, Inc.
# For more information, contact Altair at www.altair.com.
#
# This file is part of the PBS Professional ("PBS Pro") software.
#
# Open Source License Information:
#
# PBS Pro is free software. You can redistribute it and/or modify it under the
# terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# PBS Pro is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Commercial License Information:
#
# For a copy of the commercial license terms and conditions,
# go to: (http://www.pbspro.com/UserArea/agreement.html)
# or contact the Altair Legal Department.
#
# Altair’s dual-license business model allows companies, individuals, and
# organizations to create proprietary derivative works of PBS Pro and
# distribute them - whether embedded or bundled with other software -
# under a commercial license agreement.
#
# Use of Altair’s trademarks, including but not limited to "PBS™",
# "PBS Professional®", and "PBS Pro™" and Altair’s logos is subject to Altair's
# trademark licensing policies.
#

%if !%{defined pbs_name}
%define pbs_name pbspro
%endif

%if !%{defined pbs_version}
%define pbs_version 19.1.2
%endif

%if !%{defined pbs_release}
%define pbs_release 0
%endif

%if !%{defined pbs_prefix}
%define pbs_prefix /opt/pbs
%endif

%if !%{defined pbs_home}
%define pbs_home /var/spool/pbs
%endif

%if !%{defined pbs_dbuser}
%define pbs_dbuser postgres
%endif

%define pbs_client client
%define pbs_execution execution
%define pbs_server server
%define pbs_devel devel
%define pbs_dist %{pbs_name}-%{pbs_version}.tar.gz

%if !%{defined _unitdir}
%define _unitdir /usr/lib/systemd/system
%endif
%if %{_vendor} == debian && %(test -f /etc/os-release && echo 1 || echo 0)
%define _vendor_ver %(cat /etc/os-release | awk -F[=\\".] '/^VERSION_ID=/ {print \$3}')
%define _vendor_id %(cat /etc/os-release | awk -F= '/^ID=/ {print \$2}')
%endif
%if 0%{?suse_version} >= 1210 || 0%{?rhel} >= 7 || (x%{?_vendor_id} == xdebian && 0%{?_vendor_ver} >= 8) || (x%{?_vendor_id} == xubuntu && 0%{?_vendor_ver} >= 16)
%define have_systemd 1
%endif

Name: %{pbs_name}
Version: %{pbs_version}
Release: %{pbs_release}
Source0: %{pbs_dist}
Summary: PBS Professional
License: AGPLv3 with exceptions
URL: http://www.pbspro.org
Vendor: Altair Engineering, Inc.
Prefix: %{?pbs_prefix}%{!?pbs_prefix:%{_prefix}}

%bcond_with alps
%bcond_with cpuset
%bcond_with ptl

BuildRoot: %{buildroot}
BuildRequires: gcc
BuildRequires: make
BuildRequires: rpm-build
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: hwloc-devel
BuildRequires: libX11-devel
BuildRequires: libXt-devel
BuildRequires: libedit-devel
BuildRequires: libical-devel
BuildRequires: ncurses-devel
BuildRequires: perl
BuildRequires: postgresql-devel >= 9.1
BuildRequires: postgresql-contrib >= 9.1
BuildRequires: python-devel >= 2.6
BuildRequires: python-devel < 3.0
BuildRequires: tcl-devel
BuildRequires: tk-devel
BuildRequires: swig
BuildRequires: zlib-devel
%if %{defined suse_version}
BuildRequires: libexpat-devel
BuildRequires: libopenssl-devel
BuildRequires: libXext-devel
BuildRequires: libXft-devel
BuildRequires: fontconfig
BuildRequires: timezone
BuildRequires: python-xml
%else
BuildRequires: expat-devel
BuildRequires: openssl-devel
BuildRequires: libXext
BuildRequires: libXft
%endif

# Pure python extensions use the 32 bit library path
%{!?py_site_pkg_32: %global py_site_pkg_32 %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(0)")}
%{!?py_site_pkg_64: %global py_site_pkg_64 %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%description
PBS Professional® is a fast, powerful workload manager and
job scheduler designed to improve productivity, optimize
utilization & efficiency, and simplify administration for
HPC clusters, clouds and supercomputers.

%package %{pbs_server}
Summary: PBS Professional for a server host
Group: System Environment/Base
Conflicts: pbspro-execution
Conflicts: pbspro-client
Conflicts: pbspro-client-ohpc
Conflicts: pbspro-execution-ohpc
Conflicts: pbspro-server-ohpc
Conflicts: pbs
Conflicts: pbs-mom
Conflicts: pbs-cmds
Requires: bash
Requires: expat
Requires: postgresql-server >= 9.1
Requires: postgresql-contrib >= 9.1
Requires: python >= 2.6
Requires: python < 3.0
Requires: tcl
Requires: tk
%if %{defined suse_version}
Requires: smtp_daemon
%else
Requires: smtpdaemon
%endif
Requires: hostname
Requires: libical
Autoreq: 1

%description %{pbs_server}
PBS Professional® is a fast, powerful workload manager and
job scheduler designed to improve productivity, optimize
utilization & efficiency, and simplify administration for
HPC clusters, clouds and supercomputers.

This package is intended for a server host. It includes all
PBS Professional components.

%package %{pbs_execution}
Summary: PBS Professional for an execution host
Group: System Environment/Base
Conflicts: pbspro-server
Conflicts: pbspro-client
Conflicts: pbspro-client-ohpc
Conflicts: pbspro-execution-ohpc
Conflicts: pbspro-server-ohpc
Conflicts: pbs
Conflicts: pbs-mom
Conflicts: pbs-cmds
Requires: bash
Requires: expat
Requires: python >= 2.6
Requires: python < 3.0
%if 0%{?suse_version} >= 1500
Requires: hostname
%endif
Autoreq: 1

%description %{pbs_execution}
PBS Professional® is a fast, powerful workload manager and
job scheduler designed to improve productivity, optimize
utilization & efficiency, and simplify administration for
HPC clusters, clouds and supercomputers.

This package is intended for an execution host. It does not
include the scheduler, server, or communication agent. It
does include the PBS Professional user commands.

%package %{pbs_client}
Summary: PBS Professional for a client host
Group: System Environment/Base
Conflicts: pbspro-server
Conflicts: pbspro-execution
Conflicts: pbspro-client-ohpc
Conflicts: pbspro-execution-ohpc
Conflicts: pbspro-server-ohpc
Conflicts: pbs
Conflicts: pbs-mom
Conflicts: pbs-cmds
Requires: bash
Requires: python >= 2.6
Requires: python < 3.0
Autoreq: 1

%description %{pbs_client}
PBS Professional® is a fast, powerful workload manager and
job scheduler designed to improve productivity, optimize
utilization & efficiency, and simplify administration for
HPC clusters, clouds and supercomputers.

This package is intended for a client host and provides
the PBS Professional user commands.


%package %{pbs_devel}
Summary: PBS Professional Development Package
Group: Development/System

%description %{pbs_devel}
PBS Professional® is a fast, powerful workload manager and
job scheduler designed to improve productivity, optimize
utilization & efficiency, and simplify administration for
HPC clusters, clouds and supercomputers.


%if %{with ptl}

%define pbs_ptl ptl

%if !%{defined ptl_prefix}
%define ptl_prefix %{pbs_prefix}/../ptl
%endif

%package %{pbs_ptl}
Summary: PBS Test Lab for testing PBS Professional
Group: System Environment/Base
Requires: python-nose
Requires: python-beautifulsoup
%if 0%{?rhel}
Requires: pexpect
%else
Requires: python-pexpect
%endif
Requires: python-defusedxml
Prefix: %{ptl_prefix}

%description %{pbs_ptl}
PBS Test Lab is a test harness and test suite intended to validate the
functionality of PBS Professional®.

%endif

%if 0%{?opensuse_bs}
# Do not specify debug_package for OBS builds.
%else
%if %{defined suse_version}
%debug_package
%endif
%endif

%prep
%setup

%build
[ -f configure ] || ./autogen.sh
[ -d build ] && rm -rf build
mkdir build
cd build
../configure \
	PBS_VERSION=%{pbs_version} \
	--prefix=%{pbs_prefix} \
%if %{with ptl}
	--enable-ptl \
%endif
%if %{defined suse_version}
	--libexecdir=%{pbs_prefix}/libexec \
%endif
%if %{with alps}
	--enable-alps \
%endif
%if %{with cpuset}
	--enable-cpuset \
%endif
	--with-pbs-server-home=%{pbs_home} \
	--with-database-user=%{pbs_dbuser}
%{__make} %{?_smp_mflags}

%install
cd build
%make_install
mandir=$(find %{buildroot} -type d -name man)
[ -d "$mandir" ] && find $mandir -type f -exec gzip -9 -n {} \;
install -D %{buildroot}/%{pbs_prefix}/libexec/pbs_init.d %{buildroot}/etc/init.d/pbs

%post %{pbs_server}
ldconfig %{_libdir}
# do not run pbs_postinstall when the CLE is greater than or equal to 6
imps=0
cle_release_version=0
cle_release_path=/etc/opt/cray/release/cle-release
if [ -f ${cle_release_path} ]; then
        cle_release_version=`grep RELEASE ${cle_release_path} | cut -f2 -d= | cut -f1 -d.`
fi
[ "${cle_release_version}" -ge 6 ] 2>/dev/null && imps=1
if [ $imps -eq 0 ]; then
${RPM_INSTALL_PREFIX:=%{pbs_prefix}}/libexec/pbs_postinstall server \
	%{version} ${RPM_INSTALL_PREFIX:=%{pbs_prefix}} %{pbs_home} %{pbs_dbuser}
fi

%post %{pbs_execution}
ldconfig %{_libdir}
# do not run pbs_postinstall when the CLE is greater than or equal to 6
imps=0
cle_release_version=0
cle_release_path=/etc/opt/cray/release/cle-release
if [ -f ${cle_release_path} ]; then
        cle_release_version=`grep RELEASE ${cle_release_path} | cut -f2 -d= | cut -f1 -d.`
fi
[ "${cle_release_version}" -ge 6 ] 2>/dev/null && imps=1
if [ $imps -eq 0 ]; then
${RPM_INSTALL_PREFIX:=%{pbs_prefix}}/libexec/pbs_postinstall execution \
	%{version} ${RPM_INSTALL_PREFIX:=%{pbs_prefix}} %{pbs_home}
fi

%post %{pbs_client}
ldconfig %{_libdir}
# do not run pbs_postinstall when the CLE is greater than or equal to 6
imps=0
cle_release_version=0
cle_release_path=/etc/opt/cray/release/cle-release
if [ -f ${cle_release_path} ]; then
        cle_release_version=`grep RELEASE ${cle_release_path} | cut -f2 -d= | cut -f1 -d.`
fi
[ "${cle_release_version}" -ge 6 ] 2>/dev/null && imps=1
if [ $imps -eq 0 ]; then
${RPM_INSTALL_PREFIX:=%{pbs_prefix}}/libexec/pbs_postinstall client \
	%{version} ${RPM_INSTALL_PREFIX:=%{pbs_prefix}}
fi

%post %{pbs_devel}
ldconfig %{_libdir}

%preun %{pbs_server}
if [ "$1" != "1" ]; then
	# This is an uninstall, not an upgrade.
	${RPM_INSTALL_PREFIX:=%{pbs_prefix}}/libexec/pbs_preuninstall server \
		%{version} ${RPM_INSTALL_PREFIX:=%{pbs_prefix}} %{defined have_systemd}
fi

%preun %{pbs_execution}
if [ "$1" != "1" ]; then
	# This is an uninstall, not an upgrade.
	${RPM_INSTALL_PREFIX:=%{pbs_prefix}}/libexec/pbs_preuninstall execution \
		%{version} ${RPM_INSTALL_PREFIX:=%{pbs_prefix}} %{defined have_systemd}
fi

%preun %{pbs_client}
if [ "$1" != "1" ]; then
	# This is an uninstall, not an upgrade.
	${RPM_INSTALL_PREFIX:=%{pbs_prefix}}/libexec/pbs_preuninstall client \
		%{version} ${RPM_INSTALL_PREFIX:=%{pbs_prefix}} %{defined have_systemd}
fi

%postun %{pbs_server}
if [ "$1" != "1" ]; then
	# This is an uninstall, not an upgrade.
	ldconfig %{_libdir}
	echo
	echo "NOTE: /etc/pbs.conf and the PBS_HOME directory must be deleted manually"
	echo
fi

%postun %{pbs_execution}
if [ "$1" != "1" ]; then
	# This is an uninstall, not an upgrade.
	ldconfig %{_libdir}
	echo
	echo "NOTE: /etc/pbs.conf and the PBS_HOME directory must be deleted manually"
	echo
fi

%postun %{pbs_client}
if [ "$1" != "1" ]; then
	# This is an uninstall, not an upgrade.
	ldconfig %{_libdir}
	echo
	echo "NOTE: /etc/pbs.conf must be deleted manually"
	echo
fi

%postun %{pbs_devel}
ldconfig %{_libdir}

%posttrans %{pbs_server}
${RPM_INSTALL_PREFIX:=%{pbs_prefix}}/libexec/pbs_posttrans \
	${RPM_INSTALL_PREFIX:=%{pbs_prefix}}

%posttrans %{pbs_execution}
${RPM_INSTALL_PREFIX:=%{pbs_prefix}}/libexec/pbs_posttrans \
	${RPM_INSTALL_PREFIX:=%{pbs_prefix}}

%files %{pbs_server}
%defattr(-,root,root, -)
%dir %{pbs_prefix}
%{pbs_prefix}/*
%attr(4755, root, root) %{pbs_prefix}/sbin/pbs_rcp
%attr(4755, root, root) %{pbs_prefix}/sbin/pbs_iff
%attr(644, root, root) %{pbs_prefix}/lib*/libpbs.la
%{_sysconfdir}/profile.d/pbs.csh
%{_sysconfdir}/profile.d/pbs.sh
%config(noreplace) %{_sysconfdir}/profile.d/*
%if %{defined have_systemd}
%attr(644, root, root) %{_unitdir}/pbs.service
%else
%exclude %{_unitdir}/pbs.service
%endif
%exclude %{pbs_prefix}/unsupported/*.pyc
%exclude %{pbs_prefix}/unsupported/*.pyo
%exclude %{pbs_prefix}/lib*/*.a
%exclude %{pbs_prefix}/include/*
%doc README.md
%license LICENSE

%files %{pbs_execution}
%defattr(-,root,root, -)
%dir %{pbs_prefix}
%{pbs_prefix}/*
%attr(4755, root, root) %{pbs_prefix}/sbin/pbs_rcp
%attr(4755, root, root) %{pbs_prefix}/sbin/pbs_iff
%attr(644, root, root) %{pbs_prefix}/lib*/libpbs.la
%{_sysconfdir}/profile.d/pbs.csh
%{_sysconfdir}/profile.d/pbs.sh
%config(noreplace) %{_sysconfdir}/profile.d/*
%if %{defined have_systemd}
%attr(644, root, root) %{_unitdir}/pbs.service
%else
%exclude %{_unitdir}/pbs.service
%endif
%exclude %{pbs_prefix}/bin/printjob_svr.bin
%exclude %{pbs_prefix}/etc/pbs_db_schema.sql
%exclude %{pbs_prefix}/libexec/pbs_schema_upgrade
%exclude %{pbs_prefix}/etc/pbs_dedicated
%exclude %{pbs_prefix}/etc/pbs_holidays*
%exclude %{pbs_prefix}/etc/pbs_resource_group
%exclude %{pbs_prefix}/etc/pbs_sched_config
%exclude %{pbs_prefix}/lib*/init.d/sgiICEplacement.sh
%exclude %{pbs_prefix}/lib*/python/altair/pbs_hooks/*
%exclude %{pbs_prefix}/libexec/install_db
%exclude %{pbs_prefix}/sbin/pbs_comm
%exclude %{pbs_prefix}/sbin/pbs_dataservice
%exclude %{pbs_prefix}/sbin/pbs_ds_monitor
%exclude %{pbs_prefix}/sbin/pbs_ds_password
%exclude %{pbs_prefix}/sbin/pbs_ds_password.bin
%exclude %{pbs_prefix}/sbin/pbs_sched
%exclude %{pbs_prefix}/sbin/pbs_server
%exclude %{pbs_prefix}/sbin/pbs_server.bin
%exclude %{pbs_prefix}/sbin/pbsfs
%exclude %{pbs_prefix}/unsupported/*.pyc
%exclude %{pbs_prefix}/unsupported/*.pyo
%exclude %{pbs_prefix}/lib*/*.a
%exclude %{pbs_prefix}/include/*
%doc README.md
%license LICENSE

%files %{pbs_client}
%defattr(-,root,root, -)
%dir %{pbs_prefix}
%{pbs_prefix}/*
%attr(4755, root, root) %{pbs_prefix}/sbin/pbs_iff
%attr(644, root, root) %{pbs_prefix}/lib*/libpbs.la
%{_sysconfdir}/profile.d/pbs.csh
%{_sysconfdir}/profile.d/pbs.sh
%config(noreplace) %{_sysconfdir}/profile.d/*
%exclude %{pbs_prefix}/bin/mpiexec
%exclude %{pbs_prefix}/bin/pbs_attach
%exclude %{pbs_prefix}/bin/pbs_tmrsh
%exclude %{pbs_prefix}/bin/printjob_svr.bin
%exclude %{pbs_prefix}/etc/pbs_db_schema.sql
%exclude %{pbs_prefix}/etc/pbs_dedicated
%exclude %{pbs_prefix}/etc/pbs_holidays*
%exclude %{pbs_prefix}/etc/pbs_resource_group
%exclude %{pbs_prefix}/etc/pbs_sched_config
%exclude %{pbs_prefix}/include
%exclude %{pbs_prefix}/lib*/MPI
%exclude %{pbs_prefix}/lib*/init.d
%exclude %{pbs_prefix}/lib*/python/altair/pbs_hooks
%exclude %{pbs_prefix}/lib*/python/pbs_bootcheck*
%exclude %{pbs_prefix}/libexec/install_db
%exclude %{pbs_prefix}/libexec/pbs_habitat
%exclude %{pbs_prefix}/libexec/pbs_schema_upgrade
%exclude %{pbs_prefix}/libexec/pbs_init.d
%exclude %{pbs_prefix}/sbin/pbs_comm
%exclude %{pbs_prefix}/sbin/pbs_demux
%exclude %{pbs_prefix}/sbin/pbs_dataservice
%exclude %{pbs_prefix}/sbin/pbs_ds_monitor
%exclude %{pbs_prefix}/sbin/pbs_ds_password
%exclude %{pbs_prefix}/sbin/pbs_ds_password.bin
%exclude %{pbs_prefix}/sbin/pbs_idled
%exclude %{pbs_prefix}/sbin/pbs_mom
%exclude %{pbs_prefix}/sbin/pbs_rcp
%exclude %{pbs_prefix}/sbin/pbs_sched
%exclude %{pbs_prefix}/sbin/pbs_server
%exclude %{pbs_prefix}/sbin/pbs_server.bin
%exclude %{pbs_prefix}/sbin/pbs_upgrade_job
%exclude %{pbs_prefix}/sbin/pbsfs
%exclude %{pbs_prefix}/unsupported/*.pyc
%exclude %{pbs_prefix}/unsupported/*.pyo
%exclude %{_unitdir}/pbs.service
%exclude %{pbs_prefix}/lib*/*.a
%exclude %{pbs_prefix}/include/*
%exclude /etc/init.d/pbs
%doc README.md
%license LICENSE

%files %{pbs_devel}
%defattr(-,root,root, -)
%{pbs_prefix}/lib*/*.a
%{pbs_prefix}/include/*
%doc README.md
%license LICENSE

%if %{with ptl}
%files %{pbs_ptl}
%defattr(-,root,root, -)
%dir %{ptl_prefix}
%{ptl_prefix}/*
%{_sysconfdir}/profile.d/ptl.csh
%{_sysconfdir}/profile.d/ptl.sh
%endif

%changelog
* Wed Mar 20 2019 Minghui Liu <mliu@altair.com> - 1.27
- Add pbspro-devel package
* Thu Dec 13 2018 Michael Karo <mike0042@gmail.com> - 1.26
- Remove pbspro-rpmlintrc from source list
- Updates to conditional build of pbspro-ptl package
* Mon Dec 10 2018 bayucan <bayucan@altair.com> - 1.25
- Add changelog
* Wed Nov 28 2018 bayucan <bayucan@altair.com> - 1.24
- Handle non-conffile-in-etc,explicit-lib-dependency
* Wed Nov 14 2018 bayucan <bayucan@altair.com> - 1.23
- Enable pbspro-rpmlintrc under opensuse
* Thu Oct 25 2018 riyazhakki <riyazhakki@gmail.com> - 1.22
- Add a M4 macro to enable online data compression in TPP
* Wed Sep 12 2018 Bhroam Mann <bmann@altair.com> - 1.21
- Remove reference to ibm-* platforms.
* Mon Aug 27 2018 Hiren Vadalia <hiren.vadalia@altair.com> - 1.20
- Add new OSes in CI and remove all old OSes and hacks from Travis
* Tue Aug 7 2018 Michael Karo <mike0042@gmail.com> - 1.19
- Build PBS Pro on OpenSUSE Tumbleweed
* Thu May 10 2018 sandisamp <sandisamp@gmail.com> - 1.18
- Fix declare not found error in ubuntu and added requires bash in spec file
* Mon Feb 5 2018 Michael Karo <mike0042@gmail.com> - 1.17
- Update OSS version from 17.1.0 to 18.1.0
* Thu Dec 14 2017 Dinesh <dineshjoshi1306@gmail.com> - 1.16
- Fix copyright headers
* Tue Sep 26 2017 lisa-altair <lisa@altair.com> - 1.15
- Remove calling pbs_postinstall on CLE6.0
* Tue Jun 13 2017 Hiren Vadalia <hiren.vadalia@altair.com> - 1.14
- Update PBS version to 17
* Thu Mar 23 2017 Kevin Liu <minghui.liu@trincoll.edu> - 1.13
- Update copyright year in source file headers
* Thu Mar 9 2017 Michael Karo <mike0042@gmail.com> - 1.12
- Update to support installations and upgrades on Cray XC CLE 5.2
* Thu Jan 5 2017 nithinj <nithin.johnson@altair.com> - 1.11
- Update as pbs_mom not coming up after switching on compute node on cpuset machines
* Fri Nov 18 2016 Jan Krcmar <honza801@gmail.com> 1.10
- Add debian package building support using rpmbuild and alien.
* Mon Aug 8 2016 Michael Karo <mike0042@gmail.com> - 1.9
- Update to allow sendmail or postfix to satisfy requirements
* Mon Aug 1 2016 nithinj <nithin.johnson@altair.com> - 1.8
- Update so that systemd pbs unit file refer path from pbs.conf file
* Wed Jun 29 2016 Michael Karo <mike0042@gmail.com> - 1.7
- Specify libexecdir on SUSE systems
* Wed Jun 22 2016 nithinj <nithin.johnson@altair.com> - 1.6
- Replace init script with unit file for systems that support systemd process management
* Thu Jun 16 2016 Michael Karo <mike0042@gmail.com> - 1.5
- Handle starting multinode jobs
* Wed Jun 15 2016 Michael Karo <mike0042@gmail.com> - 1.4
- Build PBS Pro under non-OHPC OBS instance
* Fri Jun 3 2016 Nithin Johnson <nithin.johnson@altair.com> - 1.3
- Add timezone and python-xml as dependencies
* Wed May 25 2016 Michael Karo <mike0042@users.noreply.github.com> - 1.2
- Update version to 14.0.1
* Mon May 23 2016 arungrover <arun.grover@altair.com> - 1.1
- Change to make sure that unsupported hook files are not compiled and packaged.
* Thu May 12 2016 Hiren Vadalia <hiren.vadalia@altair.com> - 1.0
- Initial commit of pbspro
