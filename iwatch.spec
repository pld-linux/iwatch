#TODO -init file, config file
#
Summary:	iWatch - tools to check filesystem integrity
Summary(pl.UTF-8):	iWatch - narzędzie do sprawdzania integralności plików
Name:		iwatch
Version:	0.2.1
Release:	0.1
License:	GPL
Group:		Applications
Source0:	http://dl.sourceforge.net/sourceforge/iwatch/%{name}-%{version}.tgz
# Source0-md5:	b92e7a9b5912684f5e21ef38e22910b6
URL:		http://iwatch.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires:	kernel >= 2.6.13
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
iWatch is written in Perl and based on inotify, a file change
notification system, a kernel feature that allows applications to
request the monitoring of a set of files against a list of events.

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
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.xml
%attr(755,root,root) %{_bindir}/%{name}
%{_datadir}/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
