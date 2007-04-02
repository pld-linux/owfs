#
# Conditional build:
%bcond_without	libusb		# build without USB support
%bcond_without	owphp		# build without PHP support
%bcond_without	owfs		# build without owfs support
%bcond_without	tcl		# build without tcl support
%bcond_without	owftpd		# build without owftpd support
%bcond_without	ownfsd		# build without ownfs support
#
Summary:	One-wire file system using FUSE
Summary(pl.UTF-8):	System plików 1-Wire wykorzystujący FUSE
Name:		owfs
Version:	2.6p3
Release:	0.1
Epoch:		2
License:	GPL v2+
Group:		Applications
Source0:	http://dl.sourceforge.net/owfs/%{name}-%{version}.tar.gz
# Source0-md5:	4fb8c5ef77b3b6cfff8d3659b29ddd83
URL:		http://owfs.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
%{?with_libusb:BuildRequires:	libusb-devel >= 0.1.5}
%{?with_owphp:BuildRequires:	swig-php }
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
%if %{with owfs}
	--enable-owfs		\
%endif
%if %{without owphp}
	--disable-owphp		\
%endif
%if %{without tcl}
	--disable-tcl		\
%endif
%if %{without libusb}
	--disable-usb		\
%endif
%if %{without owftpd}
	--disable-owftpd 	\
%endif
%if %{without ownfsd}
	--disable-ownfsd 	\
%endif
	--enable-parport	

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/man
cp -fa $RPM_BUILD_ROOT/usr/man $RPM_BUILD_ROOT%{_datadir}
rm -fr $RPM_BUILD_ROOT/usr/man

%clean
rm -rf $RPM_BUILD_ROOT

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

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
