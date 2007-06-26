%define name parrot
%define release		%mkrel 1
%define version 0.4.13

%define libname %mklibname %{name} %version
%define libname_devel  %mklibname -d %{name} 

Summary:    Virtual machine designed to compile and execute bytecode
Name:		%name
Version:	%version
Release:	%release
Source0:	ftp://ftp.cpan.org/pub/CPAN/authors/id/L/LT/LTOETSCH/%{name}-%{version}.tar.bz2
Patch0:      parrot-0.4.2-use_readline.patch
License:	GPL
Group:	    Development/Perl
Url:		http://www.parrotcode.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libicu-devel python

%description
Parrot is a virtual machine designed to efficiently compile and execute 
bytecode for interpreted languages. Parrot will be the target for the final 
Perl 6 compiler, and is already usable as a backend for Pugs, as well as 
variety of other languages

%package -n %libname
Summary:    Run time library for %{name}
Group:	    Development/Perl

%description -n %libname
Run time library for %{name}.

%package -n %libname_devel
Summary:    Devel files for %{name}
Group:	    Development/Perl
Provides:   lib%{name}-devel
Requires:   %libname = %version
Obsoletes:  %{libname}-devel

%description -n %libname_devel
Devel files for %{name}.

%prep
%setup -q
%patch0 -p0

%build
perl Configure.pl --prefix=%_prefix 
perl -pi -e 's|(LIB_DIR\s*=.*)/usr/lib\s*|${1}/%{_libdir}\n|' Makefile

find examples -type f | xargs chmod -x
# not parralel proof
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
rm -Rf $RPM_BUILD_ROOT/usr/share/doc/

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
%_libdir/*.so.*

%files -n %libname_devel
%defattr(-,root,root) 
%_includedir/*
%_libdir/*.so
%_libdir/*.a
%_libdir/pkgconfig/%name.pc

