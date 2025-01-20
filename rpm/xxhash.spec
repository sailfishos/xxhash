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
Patch1:         test-tools-do-not-override-cflags.patch
Patch2:         inline.patch
BuildRequires:  gcc-c++
BuildRequires:  time

%description
xxHash is a hash algorithm. It completes the SMHasher test suite which
evaluates collision, dispersion and randomness qualities of hash functions.
Hashes are identical on all platforms.

%package -n libxxhash
Summary:        Non-cryptographic hash algorithm
License:        BSD-2-Clause
Group:          System/Libraries
Provides:       libxxhash0 = %version

%description -n libxxhash
xxHash is a hash algorithm. It completes the SMHasher test suite which
evaluates collision, dispersion and randomness qualities of hash functions.
Hashes are identical on all platforms.

%package devel
Summary:        Headers for xxHash, a non-cryptographic hash algorithm
License:        BSD-2-Clause
Group:          Development/Libraries/C and C++
Requires:       %name = %version
Requires:       libxxhash = %version

%description devel
Headers and other development files for xxHash.

%package doc
Summary:        Documentation for xxHash
License:        BSD-2-Clause
Requires:       %{name} = %{version}

%description doc
Documentation for xxHash, a non-cryptographic hash algorithm

%prep
%autosetup -p1 -n %{name}-%{version}/%{name}

%build
# ALLOW_AVX just means "we guarantee we policed our %%optflags".
export CFLAGS="%optflags -DXXH_X86DISPATCH_ALLOW_AVX=1"
export CXXFLAGS="$CFLAGS"
export LDFLAGS="%{?build_ldflags}"
# DISPATCH=1 if you want AVX2/AVX512. But it does not seem to perform any
# better than the lowest-denomimation code on at least the 1135G7 and 5950X
# CPUs, and for both LP64 as well as ILP32 — it seems to be all within margin
# of error.
%make_build prefix=%_prefix libdir=%_libdir

%install
export CFLAGS="%optflags -DXXH_X86DISPATCH_ALLOW_AVX=1"
export CXXFLAGS="%optflags"
export LDFLAGS="%{?build_ldflags}"
%make_install prefix=%_prefix libdir=%_libdir
rm -rf %buildroot%_libdir/libxxhash.a

%check
export CFLAGS="%optflags"
export CXXFLAGS="%optflags"
export LDFLAGS="%{?build_ldflags}"
# not safe for parallel execution as it removes xxhash.o and recreates it with different flags
# the list is taken from test-all with non-working/irrelevant ones (such as ones that change the toolchain) removed
%make_build -j1 test test-unicode listL120 trailingWhitespace test-xxh-nnn-sums

%post -n libxxhash -p /sbin/ldconfig    
%postun -n libxxhash -p /sbin/ldconfig

%files
%license LICENSE
%_bindir/xxh*

%files -n libxxhash
%_libdir/libxxhash.so.*

%files devel
%_includedir/*.h
%_libdir/pkgconfig/*.pc
%_libdir/libxxhash.so

%files doc
%doc README.md
%_mandir/man1/xxh*

%changelog

