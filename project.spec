Summary: Background power consumption optimizer
Name: pcoptimizer
Version: 0.2
Release: %(date +"%Y%m%d")
Source0: %{name}-%{version}.tar.gz
License: GPL
Group: Application/Web
BuildArch: noarch

%define binary /usr/bin/%{name}
%define logfile /var/log/%{name}.log
%define config /etc/pcoptimizer/%{name}.conf

%define loglevel 20

%description
Step count challenge from the fitbase team

%prep
%setup -q

%install
install -d usr/bin $RPM_BUILD_ROOT/usr/bin
install -d usr/lib/pcoptimizer $RPM_BUILD_ROOT/usr/lib/pcoptimizer
install -d etc/pcoptimizer $RPM_BUILD_ROOT/etc/pcoptimizer

install -d usr/lib/pcoptimizer $RPM_BUILD_ROOT/usr/lib/pcoptimizer/lib
cp -R usr/lib/pcoptimizer/lib/* $RPM_BUILD_ROOT/usr/lib/pcoptimizer/lib

install -d usr/lib/pcoptimizer $RPM_BUILD_ROOT/usr/lib/pcoptimizer/modules
cp -R usr/lib/pcoptimizer/modules/* $RPM_BUILD_ROOT/usr/lib/pcoptimizer/modules

install -d usr/lib/pcoptimizer $RPM_BUILD_ROOT/usr/lib/pcoptimizer/res
cp -R usr/lib/pcoptimizer/res/* $RPM_BUILD_ROOT/usr/lib/pcoptimizer/res

install -d usr/lib/pcoptimizer/ $RPM_BUILD_ROOT/usr/lib/pcoptimizer/udev/rules.d
cp -R usr/lib/pcoptimizer/udev/rules.d/* $RPM_BUILD_ROOT/usr/lib/pcoptimizer/udev/rules.d

cp usr/lib/pcoptimizer/main.py $RPM_BUILD_ROOT/usr/lib/pcoptimizer


touch $RPM_BUILD_ROOT%{binary}
chmod 755 $RPM_BUILD_ROOT%{binary}
echo "#!/bin/bash" > $RPM_BUILD_ROOT%{binary}
echo "PYTHON=\"/usr/bin/python3\"">> $RPM_BUILD_ROOT%{binary}
echo "BINARY=\"/usr/lib/pcoptimizer/main.py\"">> $RPM_BUILD_ROOT%{binary}
echo "exec \${PYTHON} \${BINARY} --configfile=%{config} --loglevel=%{loglevel} --logfile=%{logfile} \$@">> $RPM_BUILD_ROOT%{binary}

%post
cp /usr/lib/pcoptimizer/udev/rules.d/70-power.rules /etc/udev/rules.d
udevadm control --reload-rules

%postun
rm -f /etc/udev/rules.d/70-power.rules
rm -f /var/log/%{name}.log
rm -rf /usr/lib/%{name}
rm -rf /etc/%{name}

udevadm control --reload-rules

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%dir /usr/lib/pcoptimizer
%dir /usr/lib/pcoptimizer/lib
%dir /usr/lib/pcoptimizer/modules
%dir /usr/lib/pcoptimizer/res
%dir /usr/lib/pcoptimizer/udev
%dir /etc/%{name}
%defattr(644,root,root,775)
%attr(755,root,root) /usr/lib/pcoptimizer/main.py
%attr(755,root,root) %{binary}
/usr/lib/pcoptimizer/lib/*
/usr/lib/pcoptimizer/modules/*
/usr/lib/pcoptimizer/res/*
/usr/lib/pcoptimizer/udev/*
