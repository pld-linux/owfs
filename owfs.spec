# TODO:
# - bconds and packages review
# - install files in proper place
# - bunch of unpackaged files
# - try to re-enable static libraries
# - add -avoid-version to php ext build and remove moving in install section
# - install ownet.php to php_data_dir instead of mv in install
# - add --optimize=2 to python build, and remove manualy %py_ocomp in install
#
# Conditional build:
%bcond_without	libusb		# build without USB support
%bcond_without	owphp		# build with PHP support
%bcond_without	owfs		# build without owfs support
%bcond_without	owtcl		# build without owtcl support
%bcond_without	owftpd		# build without owftpd support
%bcond_without	perl		# build without perl support
%bcond_without	python		# build without python support

Summary:	One-wire file system using FUSE
Summary(pl.UTF-8):	System plików 1-Wire wykorzystujący FUSE
Name:		owfs
Version:	2.7p38
Release:	0.1
Epoch:		2
License:	GPL v2+
Group:		Applications/System
Source0:	http://downloads.sourceforge.net/owfs/%{name}-%{version}.tar.gz
# Source0-md5:	c287d96c629b5deb6c85e6a82eecdc8a
URL:		http://owfs.sourceforge.net/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	libfuse-devel >= 2.2
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
%{?with_libusb:BuildRequires:	libusb-devel >= 0.1.5}
BuildRequires:	perl-ExtUtils-MakeMaker
BuildRequires:	perl-devel
%{?with_owphp:BuildRequires:	php-devel >= 4:5.0.4}
%{?with_owphp:BuildRequires:	php-program}
%{?with_python:BuildRequires:	python-devel}
%{?with_python:BuildRequires:	rpm-pythonprov}
BuildRequires:	rpmbuild(macros) >= 1.519
BuildRequires:	sed >= 4.0
%{?with_perl:BuildRequires:	swig-perl}
%{?with_owphp:BuildRequires:	swig-php}
%{?with_python:BuildRequires:	swig-python}
%{?with_tcl:BuildRequires:	tcl-devel}
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
owfs is a method under Linux to allow 1-wire devices to appear like
files in a directory. You can then enter a command like "cat
- */temperature" to have all the temperatures sensors measure and
print their data.

%description -l pl.UTF-8
owfs to metoda umożliwiająca pod Linuksem dostęp do urządzeń 1-wire
jak do plików w katalogu. Można wpisać polecenie w stylu "cat
- */temperature" i spowodować pomiar temperatury przez wszystkie
czujniki oraz wypisanie danych.

%package libs
Summary:	Shared owfs library
Summary(pl.UTF-8):	Biblioteka owfs
License:	LGPL
Group:		Libraries
Obsoletes:	owfs-lib

%description libs
Owfs library.

%description libs -l pl.UTF-8
Biblioteka owfs.

%package devel
Summary:	Header files for owfs library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki owfs
License:	LGPL
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description devel
Header files for owfs library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki owfs.

%package static
Summary:	Static owfs library
Summary(pl.UTF-8):	Statyczna biblioteka owfs
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static owfs library.

%description static -l pl.UTF-8
Statyczna biblioteka owfs.

%package -n perl-owfs
Summary:	Perl bindings for owfs
Summary(pl.UTF-8):	Wiązania Perla do owfs
Group:		Development/Languages/Perl
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description -n perl-owfs
Perl bindings for owfs.

%description -n perl-owfs -l pl.UTF-8
Wiązania Perla do owfs.

%package -n python-owfs
Summary:	Python bindings for owfs
Summary(pl.UTF-8):	Wiązania Pythona do owfs
Group:		Libraries/Python
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-owfs
Python bindings for owfs.

%description -n python-owfs -l pl.UTF-8
Wiązania Pythona do owfs.

%package -n php-owfs
Summary:	PHP bindings for owfs
Summary(pl.UTF-8):	Wiązania PHP do owfs
Group:		Development/Languages/PHP
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
%{?requires_php_extension}

%description -n php-owfs
PHP bindings for owfs.

%description -n php-owfs -l pl.UTF-8
Wiązania PHP do owfs.

%package -n tcl-owfs
Summary:	Tcl bindings for owfs
Summary(pl.UTF-8):	Wiązania Tcl-a do owfs
Group:		Development/Languages/Perl
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description -n tcl-owfs
Tcl bindings for owfs.

%description -n tcl-owfs -l pl.UTF-8
Wiązania Tcl-a do owfs.

%prep
%setup -q

%{__sed} -i -e 's/) Makefile.PL/& INSTALLDIRS=vendor/' \
	module/swig/perl5/Makefile.am \
	module/ownet/perl5/Makefile.am

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--%{?with_owfs:en}%{!?with_owfs:dis}able-owfs \
	--%{?with_owphp:en}%{!?with_owphp:dis}able-owphp \
	--%{?with_owtcl:en}%{!?with_owtcl:dis}able-owtcl \
	--%{?with_libusb:en}%{!?with_libusb:dis}able-usb \
	--%{?with_owftpd:en}%{!?with_owftpd:dis}able-owftpd \
	--%{?with_perl:en}%{!?with_perl:dis}able-owperl \
	--%{?with_python:en}%{!?with_python:dis}able-owpython \
	--enable-parport \
	--sysconfdir=%{_sysconfdir}

%{__make} \
	TCL_BIN_DIR=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	TCL_BIN_DIR=%{_libdir}

cp -a src/rpm/owfs.conf $RPM_BUILD_ROOT%{_sysconfdir}

%if %{with python}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}/ow
%py_postclean
%endif

%if %{with owphp}
rm -f $RPM_BUILD_ROOT%{_libdir}/php/*.la
mv -f $RPM_BUILD_ROOT%{_libdir}/php/libowphp.so{.*.*.*,}
rm -f $RPM_BUILD_ROOT%{_libdir}/php/libowphp.so.*

install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/owfs.ini
; Enable owfs extension module
extension=libowphp.so
EOF

# a class, relocate
install -d $RPM_BUILD_ROOT%{php_data_dir}
mv $RPM_BUILD_ROOT{%{_bindir},%{php_data_dir}}/ownet.php
%endif

%if %{with owtcl}
rm -f $RPM_BUILD_ROOT%{_libdir}/owtcl-1.0/*.la
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/owdir
%attr(755,root,root) %{_bindir}/owget
%{?with_owfs:%attr(755,root,root) %{_bindir}/owfs}
%{?with_owftpd:%attr(755,root,root) %{_bindir}/owftpd}
%attr(755,root,root) %{_bindir}/owhttpd
%attr(755,root,root) %{_bindir}/owmon
%attr(755,root,root) %{_bindir}/owpresent
%attr(755,root,root) %{_bindir}/owread
%attr(755,root,root) %{_bindir}/owserver
%attr(755,root,root) %{_bindir}/owtap
%attr(755,root,root) %{_bindir}/owwrite
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/owfs.conf
%{_mandir}/man1/owdir.1*
%{_mandir}/man1/owfs.1*
%{_mandir}/man1/owftpd.1*
%{_mandir}/man1/owhttpd.1*
%{_mandir}/man1/owmon.1*
%{_mandir}/man1/owpresent.1*
%{_mandir}/man1/owread.1*
%{_mandir}/man1/owserver.1*
%{_mandir}/man1/owshell.1*
%{_mandir}/man1/owtap.1*
%{_mandir}/man1/owwrite.1*
%{_mandir}/man5/owfs.5*
%{_mandir}/man5/owfs.conf.5*
%{_mandir}/mann/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libow-2.7.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libow-2.7.so.38
%attr(755,root,root) %{_libdir}/libowcapi-2.7.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libowcapi-2.7.so.38
%attr(755,root,root) %{_libdir}/libownet-2.7.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libownet-2.7.so.38

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libow.so
%attr(755,root,root) %{_libdir}/libowcapi.so
%attr(755,root,root) %{_libdir}/libownet.so
%{_libdir}/libow.la
%{_libdir}/libowcapi.la
%{_libdir}/libownet.la
%{_includedir}/ow*.h
# FIXME: should be man3, not man1
%{_mandir}/man1/libowcapi.1*
%{_mandir}/man1/owcapi.1*
%{_mandir}/man3/DS*.3*
%{_mandir}/man3/LCD.3*
%{_mandir}/man3/Thermachron.3*

%files static
%defattr(644,root,root,755)
#%%{_libdir}/libow.a
#%%{_libdir}/libowcapi.a
#%%{_libdir}/libownet.a

%if %{with perl}
%files -n perl-owfs
%defattr(644,root,root,755)
%{perl_vendorarch}/OW.pm
%dir %{perl_vendorarch}/auto/OW
%{perl_vendorarch}/auto/OW/OW.bs
%attr(755,root,root) %{perl_vendorarch}/auto/OW/OW.so
%{perl_vendorlib}/OWNet.pm
%{_mandir}/man3/OWNet.3*
%{_mandir}/man3/owperl.3*
%endif

%if %{with python}
%files -n python-owfs
%defattr(644,root,root,755)
%dir %{py_sitedir}/ow
%attr(755,root,root) %{py_sitedir}/ow/_OW.so
%{py_sitedir}/ow/__init__.py[co]
%dir %{py_sitedir}/ownet
%{py_sitedir}/ownet/*.py[co]
%if "%{py_ver}" > "2.4"
%{py_sitedir}/ow-*.egg-info
%{py_sitedir}/ownet-*.egg-info
%endif
%endif

%if %{with owphp}
%files -n php-owfs
%defattr(644,root,root,755)
%{php_data_dir}/ownet.php
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/owfs.ini
%attr(755,root,root) %{php_extensiondir}/libowphp.so
%endif

%if %{with owtcl}
%files -n tcl-owfs
%defattr(644,root,root,755)
%dir %{_libdir}/owtcl-1.0
%attr(755,root,root) %{_libdir}/owtcl-1.0/ow-1.0.so
%attr(755,root,root) %{_libdir}/owtcl-1.0/ow.so
%{_libdir}/owtcl-1.0/*.tcl
%{_mandir}/man3/owtcl.3*
%{_mandir}/mann/owtcl.n*
%endif
