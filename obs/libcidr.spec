Name:		libcidr
Version:	1.2.3
Release:	1%{?dist}
Summary:	CIDR manipulating library

Group:		Development/Libraries
License:	BSD
URL:		https://www.over-yonder.net/~fullermd/projects/libcidr/
Source0:	libcidr-%{version}.tar.gz
#Patch0:		libcidr-extern.patch
#Patch1:		libcidr-pkgconfig.patch
BuildRequires:	gcc, cpp, make

%description
libcidr is a library to make it easier to handle IP addresses and blocks,
and manipulate them in various ways.

The core of the library is a pair of functions that take a human readable
string and turn it into our internal representation of a CIDR address block
(cidr_from_str() ), and one to take that internal representation and turn it
into a human-readable string (cidr_to_str() ). There are a large number of
options for how to format that string, as well.

Additionally, there are functions to compare different CIDR blocks, to determine
if they're equal, or if one is contained within the other. This functionality
can be useful for writing access-control code, or client-dependant configuration,
or similar things. There are functions to manipulate address blocks and determine
attributes of them, like network/broadcast addresses, the range of host addresses,
the number of available host addresses, etc. There are functions to split a CIDR
block into the two smaller blocks it contains, or to derive the parent block that
it is itself contained within. And there are functions to translate to and from
in_addr-type structures, which the operating system commonly uses to represent
addresses for handle socket connections and so forth.

%package -n libcidr0
Summary:    Shared library for %{name}
#hack to enable devel package beeing installable on CentOS_7
%ifarch x86_64
Provides:   libcidr.so.0()(64bit)
%endif

%description -n libcidr0
Shared library for %{name}.

%package devel
Summary: development files for CIDR manipulating library
Requires: libcidr0 = %{version}

%description devel
libcidr is a library to make it easier to handle IP addresses and blocks,
and manipulate them in various ways.

%prep
%setup -q
#%patch0 -p1
#%patch1 -p1

%build
make %{?_smp_mflags} \
  DESTDIR=%{buildroot} \
  PREFIX=%{_prefix} \
  CIDR_LIBDIR=%{_libdir} \
  CIDR_DOCDIR=%{_defaultdocdir}/%{name}-%{version} \
  CIDR_EXDIR=%{_defaultdocdir}/%{name}-%{version}/examples \
  CIDR_MANDIR=%{_mandir}


%install
make install \
  DESTDIR=%{buildroot} \
  PREFIX=%{_prefix} \
  CIDR_LIBDIR=%{_libdir} \
  CIDR_DOCDIR=%{_defaultdocdir}/%{name}-%{version} \
  CIDR_EXDIR=%{_defaultdocdir}/%{name}-%{version}/examples \
  CIDR_MANDIR=%{_mandir}

install -m 755 -d  %{buildroot}%{_libdir}/pkgconfig
sed -e "s#@libdir@#%{_libdir}#" -e "s#@version@#%{version}#" -e "s#@prefix@#%{_prefix}#" tools/libcidr.pc >%{buildroot}%{_libdir}/pkgconfig/libcidr.pc

%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files -n libcidr0
%attr(-,root,root)
%attr(755,root,root) %{_libdir}/libcidr.so.*

%files devel
%attr(-,root,root)
%{_bindir}/cidrcalc
%{_includedir}/libcidr.h
%{_libdir}/libcidr.so
%{_libdir}/pkgconfig/libcidr.pc
%doc /usr/share/doc
%doc /usr/share/man

%changelog

