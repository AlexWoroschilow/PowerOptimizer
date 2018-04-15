Summary: Background power optimizer
Name: power-optimizer
Version: 0.2
Release: %(date +"%Y%m%d")
Source0: %{name}-%{version}.tar.gz
License: GPL
Group: Application/Web
BuildArch: noarch

%define binary /usr/bin/%{name}
%define logfile /var/log/%{name}.log
%define loglevel 20

%description
Step count challenge from the fitbase team

%prep
%setup -q

%install
install -d usr/bin $RPM_BUILD_ROOT/usr/bin
install -d usr/lib/power-optimizer $RPM_BUILD_ROOT/usr/lib/power-optimizer

install -d usr/lib/power-optimizer $RPM_BUILD_ROOT/usr/lib/power-optimizer/lib
cp -R usr/lib/power-optimizer/lib/* $RPM_BUILD_ROOT/usr/lib/power-optimizer/lib

install -d usr/lib/power-optimizer $RPM_BUILD_ROOT/usr/lib/power-optimizer/src
cp -R usr/lib/power-optimizer/src/* $RPM_BUILD_ROOT/usr/lib/power-optimizer/src

install -d usr/lib/power-optimizer $RPM_BUILD_ROOT/usr/lib/power-optimizer/res
cp -R usr/lib/power-optimizer/res/* $RPM_BUILD_ROOT/usr/lib/power-optimizer/res

install -d usr/lib/power-optimizer/ $RPM_BUILD_ROOT/usr/lib/power-optimizer/udev/rules.d
cp -R usr/lib/power-optimizer/udev/rules.d/* $RPM_BUILD_ROOT/usr/lib/power-optimizer/udev/rules.d

cp usr/lib/power-optimizer/power-optimizer.py $RPM_BUILD_ROOT/usr/lib/power-optimizer


touch $RPM_BUILD_ROOT%{binary}
chmod 755 $RPM_BUILD_ROOT%{binary}
echo "#!/bin/bash" > $RPM_BUILD_ROOT%{binary}
echo "PYTHON=\"/usr/bin/python3\"">> $RPM_BUILD_ROOT%{binary}
echo "BINARY=\"/usr/lib/power-optimizer/power-optimizer.py\"">> $RPM_BUILD_ROOT%{binary}
echo "exec \${PYTHON} \${BINARY} --log-level=%{loglevel} --log-file=%{logfile} \$@">> $RPM_BUILD_ROOT%{binary}

%post
cp /usr/lib/power-optimizer/udev/rules.d/70-power.rules /etc/udev/rules.d
udevadm control --reload-rules

%postun
rm -f /etc/udev/rules.d/70-power.rules
rm -f  /var/log/%{name}.log
rm -rf  /usr/lib/%{name}
udevadm control --reload-rules

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%dir /usr/lib/power-optimizer
%dir /usr/lib/power-optimizer/lib
%dir /usr/lib/power-optimizer/src
%dir /usr/lib/power-optimizer/res
%dir /usr/lib/power-optimizer/udev
%defattr(644,root,root,775)
%attr(755,root,root) /usr/lib/power-optimizer/power-optimizer.py
%attr(755,root,root) %{binary}
/usr/lib/power-optimizer/lib/*
/usr/lib/power-optimizer/src/*
/usr/lib/power-optimizer/res/*
/usr/lib/power-optimizer/udev/*
