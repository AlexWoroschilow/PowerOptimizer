Summary: Laptop performance optimizer
Name: performance
Version: 0.1
Release: %(date +"%Y%m%d")
Group: System Environment/Kernel
License: Apache
BuildArch: noarch
Requires(pre): python3


%description
Laptop performance optimizer

%prep
%setup -q

%install
install -d $RPM_BUILD_ROOT/etc/udev/rules.d
install -d $RPM_BUILD_ROOT/etc/performance

cp -R 70-performance.rules $RPM_BUILD_ROOT/etc/udev/rules.d
cp -R performance_* $RPM_BUILD_ROOT/etc/performance
cp -R powersave_* $RPM_BUILD_ROOT/etc/performance

%post
udevadm control --reload

%files 
%defattr(644,root,root,755)
%dir /etc/udev/rules.d
%dir /etc/performance

%attr(755,root,root) /etc/performance/*
/etc/udev/rules.d/*
