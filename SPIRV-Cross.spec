Summary:	Tool for parsing and converting SPIR-V to other shader languages
Name:		SPIRV-Cross
Version:	1.4.363.0
Release:	1
License:	Apache v2.0
Group:		Development/Tools
Source0:	https://github.com/KhronosGroup/SPIRV-Cross/archive/vulkan-sdk-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	4049053c7b27ec33aee89aec7ebcf7b1
Patch0:		install-cmake.patch
URL:		https://github.com/KhronosGroup/SPIRV-Cross
BuildRequires:	cmake >= 3.13
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SPIRV-Cross is a practical tool and library for performing reflection
on SPIR-V and disassembling SPIR-V back to high level languages.

%package libs
Summary:	SPIRV-Cross shared librar
Summary(pl.UTF-8):	Biblioteka dzielona SPIRV-Cross
Group:		Libraries

%description libs
SPIRV-Cross shared library.

%description libs -l pl.UTF-8
Biblioteka dzielona SPIRV-Cross.

%package devel
Summary:	Header files for %{name}
Summary(pl.UTF-8):	Pliki nagłówkowe %{name}
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for %{name}.

%description devel -l pl.UTF-8
Pliki nagłówkowe %{name}.

%package static
Summary:	Static %{name} libraries
Summary(pl.UTF-8):	Statyczne biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} libraries.

%description static -l pl.UTF-8
Statyczne biblioteki %{name}.

%prep
%setup -q -n %{name}-vulkan-sdk-%{version}
%patch -P0 -p1

%build
%cmake -B build \
	-DSPIRV_CROSS_CLI=ON \
	-DSPIRV_CROSS_STATIC=ON \
	-DSPIRV_CROSS_SHARED=ON

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/spirv-cross

%files libs
%defattr(644,root,root,755)
%{_libdir}/libspirv-cross-c-shared.so.*.*.*
%ghost %{_libdir}/libspirv-cross-c-shared.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libspirv-cross-c-shared.so
%{_includedir}/spirv_cross
%{_datadir}/cmake/spirv_cross_c_shared
%{_pkgconfigdir}/spirv-cross-c-shared.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libspirv-cross-*.a
%{_datadir}/cmake/spirv_cross_c
%{_datadir}/cmake/spirv_cross_core
%{_datadir}/cmake/spirv_cross_cpp
%{_datadir}/cmake/spirv_cross_glsl
%{_datadir}/cmake/spirv_cross_hlsl
%{_datadir}/cmake/spirv_cross_msl
%{_datadir}/cmake/spirv_cross_reflect
%{_datadir}/cmake/spirv_cross_util
%{_pkgconfigdir}/spirv-cross-c.pc
