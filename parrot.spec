%define name    parrot
%define version 2.3.0
%define release %mkrel 2

%define libname        %mklibname %{name}
%define libname_devel  %mklibname -d %{name} 

%define _requires_exceptions perl(Parrot::Pmc2c::.*)
%define _provides_exceptions perl(File::Which)

Name:          %name
Version:       %version
Release:       %release

Summary:       Parrot Virtual Machine
License:       Artistic 2.0
Group:         Development/Perl
Url:           http://www.parrot.org/
Source0:       ftp://ftp.parrot.org/pub/parrot/releases/devel/%{version}/%{name}-%{version}.tar.gz
Patch0:        parrot-2.3.0-remove_md2_upstream_r45824.patch

BuildRequires: gdbm-devel
BuildRequires: gmp-devel
BuildRequires: libicu-devel
BuildRequires: ncurses-devel
BuildRequires: perl-doc
BuildRequires: readline-devel

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}

%description
Parrot is a virtual machine designed to efficiently compile and execute 
bytecode for interpreted languages. Parrot will be the target for the final 
Perl 6 compiler, and is already usable as a backend for Pugs, as well as 
variety of other languages

#--

%package -n %libname
Summary:    Parrot Virtual Machine run time library
License:    Artistic 2.0
Group:      Development/Perl
Provides:   lib%{name} = %{version}-%{release}
Requires:   %{name} = %{version}-%{release}
Requires:   %{_libdir}/pkgconfig

%description -n %libname
Run time library for %{name}.

#--

%package -n %{name}-doc
Summary:    Parrot Virtual Machine documentation
License:    Artistic 2.0
Group:      Development/Perl

%description -n %{name}-doc
Documentation for %{name}.

#--

%package -n %libname_devel
Summary:    Parrot Virtual Machine development headers and libraries
License:    Artistic 2.0
Group:      Development/Perl
Provides:   %{name}-devel = %{version}-%{release}
Requires:   %libname = %{version}

%description -n %libname_devel
Development files for %{name}.

#--

%package -n %{name}-src
Summary:    Parrot Virtual Machine sources
License:    Artistic 2.0
Group:      Development/Perl
Provides:   %{name}-src = %{version}-%{release}

%description -n %{name}-src
Sources of %{name}.


%prep
%setup -q
%patch0 -p1 -b .md2
%{__perl} -pi -e 's,"lib/,"%{_lib}/, if (/CONST_STRING\(interp,/)' \
    src/library.c
%{__perl} -pi -e "s,'/usr/lib','%{_libdir}',;s,runtime/lib/,runtime/%{_lib}/," \
    tools/dev/install_files.pl \
    tools/dev/mk_manifest_and_skip.pl

%build
%{__perl} Configure.pl \
    --prefix=%{_usr} \
    --libdir=%{_libdir} \
    --sysconfdir=%{_sysconfdir} \
    --infodir=%{_datadir}/info \
    --mandir=%{_mandir} \
    --cc="%{__cc}" \
    --parrot_is_shared \
    --lex=/usr/bin/flex \
    --yacc=/usr/bin/yacc \
    --libs='-lcurses -lm -lrt'

    #--cxx=%{__cxx} \
# the following Configure.pl flag makes the compile goes boom
    #--optimize="$RPM_OPT_FLAGS -maccumulate-outgoing-args" \

%make
export LD_LIBRARY_PATH=$( pwd )/blib/lib
%make parrot_utils
%make installable
%make html


%install
rm -rf $RPM_BUILD_ROOT

export LD_LIBRARY_PATH=$( pwd )/blib/lib
make install DESTDIR=$RPM_BUILD_ROOT

# Drop the docs so rpm can pick them up itself.
rm -rf $RPM_BUILD_ROOT/%{_docdir}/parrot

# Force permissions on doc directories.
find docs examples -type d -exec chmod 755 {} \;
find docs examples -type f -exec chmod 644 {} \;

# Force permissions on shared libs so they get stripped.
find $RPM_BUILD_ROOT%{_libdir} -type f \( -name '*.so' -o -name '*.so.*' \) \
    -exec chmod 755 {} \;

%check
export LD_LIBRARY_PATH=$( pwd )/blib/lib
#make test

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root,-)
%doc ChangeLog CREDITS NEWS PBC_COMPAT PLATFORMS README
%doc RESPONSIBLE_PARTIES TODO
%exclude %{_bindir}/parrot_config
%exclude %{_bindir}/parrot_debugger
%exclude %{_bindir}/pbc_*
%{_bindir}/*

%files -n %{name}-doc
%defattr(-,root,root,-)
%doc docs examples

%files -n %libname
%defattr(-,root,root,-)
%{_libdir}/parrot
%{_libdir}/*.so.*

%files -n %libname_devel
%defattr(-,root,root,-)
%{_bindir}/parrot_config
%{_bindir}/parrot_debugger
%{_bindir}/pbc_disassemble
%{_bindir}/pbc_merge
%{_bindir}/pbc_to_exe
%{_bindir}/pbc_dump
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_libdir}/*.a

%files -n %{name}-src
%defattr(-,root,root,-)
/usr/src/parrot
