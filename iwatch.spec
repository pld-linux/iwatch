#TODO -init file, config file
#
Summary:	iWatch - tools to check filesystem integrity
Summary(pl.UTF-8):	iWatch - narzędzie do sprawdzania integralności systemu plików
Name:		iwatch
Version:	0.2.1
Release:	0.1
License:	GPL
Group:		Applications/File
Source0:	http://dl.sourceforge.net/iwatch/%{name}-%{version}.tgz
# Source0-md5:	b92e7a9b5912684f5e21ef38e22910b6
URL:		http://iwatch.sourceforge.net/
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires:	uname(release) >= 2.6.13
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
iWatch is a tool to check filesystem integrity written in Perl and
based on inotify, a file change notification system, a kernel feature
that allows applications to request the monitoring of a set of files
against a list of events.

%description -l pl.UTF-8
iWatch to narzędzie do sprawdzania integralności systemu plików
napisane w Perlu, oparte o system powiadamiania o zmianach plików
inotify - mechanizm jądra pozwalający aplikacjom żądać monitorowania
zbioru plików pod kątem listy zdarzeń.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}/%{name},%{_datadir}/%{name}}

install iwatch $RPM_BUILD_ROOT%{_bindir}
install iwatch.dtd $RPM_BUILD_ROOT%{_datadir}/%{name}
install iwatch.xml $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog README iwatch.xml.example
%attr(755,root,root) %{_bindir}/%{name}
%{_datadir}/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.xml
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
