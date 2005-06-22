#
# Note that library has diffrent licence!
# XXX: where is this library???
#
# Conditional build:
%bcond_without libusb		# build without USB support
#
#%define extra_ver	a

Summary:	One-wire file system using FUSE
Summary(pl):	System plików 1-Wire wykorzystuj±cy FUSE
Name:		owfs
Version:	2.1p0RC
Release:	0.1
License:	GPL v2+
Group:		Applications
Source0:	http://dl.sourceforge.net/owfs/%{name}-%{version}.tar.gz
# Source0-md5:	a4a42dc1ce2b2d248642251417159429
URL:		http://owfs.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
%{?with_libusb:BuildRequires:	libusb-devel >= 0.1.5}
BuildRequires:	swig-php
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
owfs is a method under Linux to allow 1-wire devices to appear like
files in a directory. You can then enter a command like "cat
*/temperature" to have all the temperatures sensors measure and print
their data.

%description -l pl
owfs to metoda umo¿liwiaj±ca pod Linuksem dostêp do urz±dzeñ 1-wire
jak do plików w katalogu. Mo¿na wpisaæ polecenie w stylu "cat
*/temperature" i spowodowaæ pomiar temperatury przez wszystkie
czujniki oraz wypisanie danych.

%package lib
Summary:	Shared gcc library
Summary(pl):	Biblioteka gcc
License:	LGPL
Group:		Libraries

%description lib
Shared library.

%description lib -l pl
Biblioteka wspó³dzielona.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-owfs \
	--enable-owphp \
	--enable-parport \
	--enable-usb

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/*
%{_datadir}/oww
