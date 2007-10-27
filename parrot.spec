%define name parrot
%define release		%mkrel 1
%define version 0.4.17

%define libname %mklibname %{name} %version
%define libname_devel  %mklibname -d %{name} 

Summary:    Virtual machine designed to compile and execute bytecode
Name:		%name
Version:	%version
Release:	%release
Source0:	ftp://ftp.cpan.org/pub/CPAN/authors/id/L/LT/LTOETSCH/%{name}-%{version}.tar.gz
License:	GPL
Group:	    Development/Perl
Url:		http://www.parrotcode.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libicu-devel python icu perl-devel perl-doc readline-devel
BuildRequires: gmp-devel libaio-devel

%description
Parrot is a virtual machine designed to efficiently compile and execute 
bytecode for interpreted languages. Parrot will be the target for the final 
Perl 6 compiler, and is already usable as a backend for Pugs, as well as 
variety of other languages

%package -n %libname
Summary:    Run time library for %{name}
Group:	    Development/Perl
Obsoletes:  %{old_libname}
Provides:   lib%{name} = %{version}-%{release}
Obsoletes:  %mklibname %name 0.4.13
Obsoletes:  %mklibname %name 0.4.6

%description -n %libname
Run time library for %{name}.

%package -n %libname_devel
Summary:    Devel files for %{name}
Group:	    Development/Perl
Provides:   %{name}-devel = %version-%release
Requires:   %libname = %version
Obsoletes:  %mklibname -d %name 0.4.13
Obsoletes:  %mklibname -d %name 0.4.6

%description -n %libname_devel
Devel files for %{name}.

%prep
%setup -q

%build
perl Configure.pl --prefix=%_prefix 
perl -pi -e 's|(LIB_DIR\s*=.*)/usr/lib\s*|${1}/%{_libdir}\n|' Makefile

find examples -type f | xargs chmod -x
# not parralel proof
make

%install
rm -rf $RPM_BUILD_ROOT
#%makeinstall_std
make reallyinstall DESTDIR=$RPM_BUILD_ROOT
rm -Rf $RPM_BUILD_ROOT/usr/share/doc/
rm -fr $RPM_BUILD_ROOT/usr/src
rm -fr $RPM_BUILD_ROOT/usr/config
rm -fr $RPM_BUILD_ROOT/usr/compilers

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %libname -p /sbin/ldconfig

%postun -n %libname -p /sbin/ldconfig

%files
%defattr(-,root,root) 
# TODO
%doc NEWS README ChangeLog examples docs RESPONSIBLE_PARTIES TODO
%_bindir/*
%_prefix/lib/%name/

%files -n %libname 
%defattr(-,root,root) 
%_libdir/*.so.%{version}*

%files -n %libname_devel
%defattr(-,root,root) 
%_includedir/*
%_libdir/*.so
%_libdir/*.a
%_libdir/pkgconfig/%name.pc
