# Grab the tarball thus:
#  wget http://nodeload.github.com/dcramer/mangodb/tarball/master -O mangodb-0.0.1.tar.gz 
#
# You can build Python 2.7 RPMS thus:
#  http://blog.milford.io/2012/01/building-and-installing-python-2-7-rpms-on-centos-5-7/

%define name mangodb
%define version 0.0.1
%define release 1
%define mango_home /opt/%{name}-%{version}
%define mango_user mango
%define mango_group mango

# Github gets wonky with the automatically generated project tarballs
# you may need to adjust this.
%define sad_github_tarball_root dcramer-mangodb-b046796

Summary: MangoDB sharting server.
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.gz
Source1: mangodb.init
License: If you use this, you must donate $1 to someone more intelligent than you.
Group: System/Daemons
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Requires: python27, /usr/sbin/useradd, /usr/sbin/usermod, /sbin/chkconfig, /sbin/service
Vendor: David Cramer <dcramer@gmail.com>
Packager: Nathan Milford <nathan@milford.io>
Provides: MangoDB
Url: https://github.com/dcramer/mangodb

%description
MangoDB is one of the fastest databases in existence. It allows you to store 
ANY KIND OF DATA you want without any IO bottleneck. You're only limited by the
size of your pipe.

If you're familiar with MongoDB then you'll feel write at home with Mango. We'll
instantly map all of your existing data without ANY EFFORT with a new and
improved AUTO SHARTING ALGORITHM.

%prep
%setup -n %{sad_github_tarball_root}

%install
install -d -m 755 %{buildroot}/%{mango_home}/
install    -m 644 %{_builddir}/%{sad_github_tarball_root}/requirements.txt %{buildroot}/%{mango_home}/
install    -m 644 %{_builddir}/%{sad_github_tarball_root}/README.rst       %{buildroot}/%{mango_home}/

install -d -m 755 %{buildroot}/%{mango_home}/bin/
install    -m 755 %{_builddir}/%{sad_github_tarball_root}/server.py        %{buildroot}/%{mango_home}/bin

install -d -m 755 %{buildroot}/%{_initrddir}
install    -m 755 %_sourcedir/mangodb.init %{buildroot}/%{_initrddir}/%{name}

install -d -m 755 %{buildroot}/var/log/%{name}

cd %{buildroot}/opt/
ln -s %{name}-%{version} %{name}
cd -

%pre
getent group %{mango_group} >/dev/null || groupadd -r %{mango_group}
getent passwd %{mango_user} >/dev/null || /usr/sbin/useradd --comment "MangoDB Daemon User" --shell /bin/bash -M -r -g %{mango_group} --home %{mango_home} %{mango_user}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,%{mango_user},%{mango_group})
/opt/%{name}
%{mango_home}
%{_initrddir}/%{name}
/var/log/%{name}

%post
chkconfig --add %{name}
%preun 
service %{name} stop >/dev/null 2>&1
chkconfig --del %{name}

%changelog
* Wed Jun 20 2012 Nathan Milford <nathan@milford.io> - 0.0.1
- First release.
