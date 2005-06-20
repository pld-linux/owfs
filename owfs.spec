#
# Note that library has diffrent licence!
#
# Conditional build:
%bcond_without libusb		# build without USB support
#
#%define extra_ver	a

Summary:	One-wire file system using FUSE
Summary(pl):	system plików 1-Wire wykorzystuj±cy FUSE
Name:		owfs
Version:	2.1p0RC
Release:	0.1
License:	GPL v2+
Group:		Applications
Source0:	http://dl.sourceforge.net/owfs/%{name}-%{version}.tar.gz
# Source0-md5:	a4a42dc1ce2b2d248642251417159429
URL:		http://oww.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	swig-php
BuildRequires:	libtool
%{?with_libusb:BuildRequires:	libusb-devel >= 0.1.5}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Oww is a Linux interface to the Dallas Semiconductor / AAGElectronica
1-Wire weather station kits.

%description -l pl
Oww jest linuksowym interfejsem do stacji pogody Dallas Semiconductor
/ AAGElectronica pracuj±cych na szynie 1-Wire.

%package lib
Summary:	Shared gcc library
Summary(pl):	Biblioteka gcc
License:	LGPL
Group:		Libraries

%description lib
Shared library.

%description lib -l pl
Biblioteka

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure		\
		--enable-owphp		\
		--enable-owfs		\
		--enable-usb		\
		--enable-parport	\

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
