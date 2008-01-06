# TODO:
# - bconds and packages review
# - install files in proper place
# - files
# - with owphp doesn't build
#
# Conditional build:
%bcond_without	libusb		# build without USB support
%bcond_with	owphp		# build without PHP support
%bcond_without	owfs		# build without owfs support
%bcond_without	tcl		# build without tcl support
%bcond_without	owftpd		# build without owftpd support
#
Summary:	One-wire file system using FUSE
Summary(pl.UTF-8):	System plików 1-Wire wykorzystujący FUSE
Name:		owfs
Version:	2.7p2
Release:	0.2
Epoch:		2
License:	GPL v2+
Group:		Applications
Source0:	http://dl.sourceforge.net/owfs/%{name}-%{version}.tar.gz
# Source0-md5:	aafe3ca1ff30e88c332b5443d1b3b744
URL:		http://owfs.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	libfuse-devel
%{?with_libusb:BuildRequires:	libusb-devel >= 0.1.5}
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl-devel
%{?with_owphp:BuildRequires:	php-devel}
%{?with_owphp:BuildRequires:	php-program}
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	swig-perl
%{?with_owphp:BuildRequires:	swig-php}
BuildRequires:	swig-python
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

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--%{?with_owfs:en}%{!?with_owfs:dis}able-owfs \
	--%{?with_owphp:en}%{!?with_owphp:dis}able-owphp \
	--%{?with_tcl:en}%{!?with_tcl:dis}able-tcl \
	--%{?with_libusb:en}%{!?with_libusb:dis}able-usb \
	--%{?with_owftpd:en}%{!?with_owftpd:dis}able-owftpd \
	--enable-parport

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/mann/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/lib*.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
