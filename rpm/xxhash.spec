#
# spec file for package xxhash
#
# Copyright (c) 2024 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.


Name:           xxhash
Version:        0.8.3
Release:        0
Summary:        Non-cryptographic hash algorithm
License:        BSD-2-Clause AND GPL-2.0-only
URL:            https://github.com/sailfishos/xxHash
Source0:        %{name}-%{version}.tar.xz
Patch1:         0001-test-tools-do-not-override-cflags.patch
Patch2:         0002-inline.patch
Patch3:         0003-disable-memory-optimisation-in-collision-test.patch
BuildRequires:  gcc-c++
BuildRequires:  time

%description
xxHash is a hash algorithm. It completes the SMHasher test suite which
evaluates collision, dispersion and randomness qualities of hash functions.
Hashes are identical on all platforms.

%package -n libxxhash
Summary:        Non-cryptographic hash algorithm
License:        BSD-2-Clause
Provides:       libxxhash0 = %version

%description -n libxxhash
xxHash is a hash algorithm. It completes the SMHasher test suite which
evaluates collision, dispersion and randomness qualities of hash functions.
Hashes are identical on all platforms.

%package devel
Summary:        Headers for xxHash, a non-cryptographic hash algorithm
License:        BSD-2-Clause
Requires:       %name = %version
Requires:       libxxhash = %version

%description devel
Headers and other development files for xxHash.

%global _make_env \
export CFLAGS="%optflags" \
export CXXFLAGS="$CFLAGS" \
export LDFLAGS="%{?build_ldflags}" \
%{nil}

%prep
%autosetup -p1 -n %{name}-%{version}/%{name}

%build
%{_make_env}
%make_build PREFIX=%_prefix LIBDIR=%_libdir

%install
%{_make_env}
%make_install PREFIX=%_prefix LIBDIR=%_libdir
rm -rf %buildroot%_libdir/libxxhash.a

%check
%{_make_env}
# not safe for parallel execution as it removes xxhash.o and recreates it with different flags
# the list is taken from test-all with non-working/irrelevant ones (such as ones that change the toolchain) removed
%make_build -j1 test test-unicode listL120 trailingWhitespace test-xxh-nnn-sums

%post -n libxxhash -p /sbin/ldconfig    
%postun -n libxxhash -p /sbin/ldconfig

%files
%license cli/COPYING
%_bindir/xxh*
%_mandir/man1/xxh*

%files -n libxxhash
%license LICENSE
%_libdir/libxxhash.so.*

%files devel
%_includedir/*.h
%_libdir/pkgconfig/*.pc
%_libdir/libxxhash.so
