#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
#
Summary:	Kinetic C client library
Summary(pl.UTF-8):	Biblioteka kliencka C Kinetic
Name:		kinetic-c
Version:	0.6.0
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	https://github.com/Seagate/kinetic-c/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	5f88679259cf90b7ccdddbb1cd3b64cc
Patch0:		%{name}-make.patch
URL:		https://github.com/Seagate/kinetic-c/
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	openssl-devel
BuildRequires:	protobuf-c-devel >= 1.0
BuildRequires:	socket99-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains a library for producing Kinetic C clients for
interacting with Kinetic object-based storage. The library uses the
cross-platform Seagate Kinetic protocol for standardizing interaces
between the Java simulator and Kinetic Device storage clusters.

%description -l pl.UTF-8
Ten pakiet zawiera bibliotekę do tworzenia w języku C klientów Kinetic
mających współpracować z opartym na obiektach systemem przechowywania
danych Kinetic. Biblioteka wykorzystuje wieloplatformowy protokół
Seagate Kinetic do standaryzacji interfejsów między symulatorem w
Javie a klastrami przechowującymi dane na urządzeniach Kinetic.

%package devel
Summary:	Header files for Kinetic C library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki C Kinetic
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Kinetic C library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki C Kinetic.

%package static
Summary:	Static Kinetic C library
Summary(pl.UTF-8):	Statyczna biblioteka C Kinetic
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Kinetic C library.

%description static -l pl.UTF-8
Statyczna biblioteka C Kinetic.

%package apidocs
Summary:	Kinetic C API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki C Kinetic
Group:		Documentation

%description apidocs
API documentation for Kinetic C library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki C Kinetic.

%prep
%setup -q
%patch0 -p1

%build
LDFLAGS="%{rpmldflags}" \
%{__make} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags} %{rpmcppflags}"

%if %{with apidocs}
doxygen config/Doxyfile
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	PREFIX=$RPM_BUILD_ROOT%{_prefix} \
	LIB=%{_lib}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md RELEASE.md
%attr(755,root,root) %{_libdir}/libkinetic-c-client.%{version}.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libkinetic-c-client.so
%{_includedir}/kinetic_client.h
%{_includedir}/kinetic_proto.h
%{_includedir}/kinetic_types.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libkinetic-c-client.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc docs/*.{css,html,js,png}
%endif
