%define libname libdwarves
%define libver 1

Name: dwarves
Version: 1.22
Release: 1%{?_tis_dist}.%{tis_patch_ver}
License: GPLv2
Summary: Debugging Information Manipulation Tools (pahole & friends)
URL: http://acmel.wordpress.com
Source: %{name}-%{version}.tar.bz2
Requires: %{libname}%{libver} = %{version}-%{release}
BuildRequires: gcc
BuildRequires: cmake >= 2.8.12
BuildRequires: zlib-devel
BuildRequires: elfutils-devel >= 0.130

%description
dwarves is a set of tools that use the debugging information inserted in
ELF binaries by compilers such as GCC, used by well known debuggers such as
GDB, and more recent ones such as systemtap.

Utilities in the dwarves suite include pahole, that can be used to find
alignment holes in structs and classes in languages such as C, C++, but not
limited to these.

It also extracts other information such as CPU cacheline alignment, helping
pack those structures to achieve more cache hits.

These tools can also be used to encode and read the BTF type information format
used with the Linux kernel bpf syscall, using 'pahole -J' and 'pahole -F btf'.

A diff like tool, codiff can be used to compare the effects changes in source
code generate on the resulting binaries.

Another tool is pfunct, that can be used to find all sorts of information about
functions, inlines, decisions made by the compiler about inlining, etc.

One example of pfunct usage is in the fullcircle tool, a shell that drivers
pfunct to generate compileable code out of a .o file and then build it using
gcc, with the same compiler flags, and then use codiff to make sure the
original .o file and the new one generated from debug info produces the same
debug info.

Pahole also can be used to use all this type information to pretty print raw data
according to command line directions.

Headers can have its data format described from debugging info and offsets from
it can be used to further format a number of records.

The btfdiff utility compares the output of pahole from BTF and DWARF to make
sure they produce the same results.

%package -n %{libname}%{libver}
Summary: Debugging information  processing library

%description -n %{libname}%{libver}
Debugging information processing library.

%package -n %{libname}%{libver}-devel
Summary: Debugging information library development files
Requires: %{libname}%{libver} = %{version}-%{release}

%description -n %{libname}%{libver}-devel
Debugging information processing library development files.

%prep
%setup -q

%build
%cmake -DCMAKE_BUILD_TYPE=Release .
make %{_smp_mflags}

%install
rm -Rf %{buildroot}
make install DESTDIR=%{buildroot}

%ldconfig_scriptlets -n %{libname}%{libver}

%files
%doc README.ctracer
%doc README.btf
%doc changes-v1.22
%doc NEWS
%{_bindir}/btfdiff
%{_bindir}/codiff
%{_bindir}/ctracer
%{_bindir}/dtagnames
%{_bindir}/fullcircle
%{_bindir}/pahole
%{_bindir}/pdwtags
%{_bindir}/pfunct
%{_bindir}/pglobal
%{_bindir}/prefcnt
%{_bindir}/scncopy
%{_bindir}/syscse
%{_bindir}/ostra-cg
%dir %{_datadir}/dwarves/
%dir %{_datadir}/dwarves/runtime/
%dir %{_datadir}/dwarves/runtime/python/
%defattr(0644,root,root,0755)
%{_mandir}/man1/pahole.1*
%{_datadir}/dwarves/runtime/Makefile
%{_datadir}/dwarves/runtime/linux.blacklist.cu
%{_datadir}/dwarves/runtime/ctracer_relay.c
%{_datadir}/dwarves/runtime/ctracer_relay.h
%attr(0755,root,root) %{_datadir}/dwarves/runtime/python/ostra.py*

%files -n %{libname}%{libver}
%{_libdir}/%{libname}.so.*
%{_libdir}/%{libname}_emit.so.*
%{_libdir}/%{libname}_reorganize.so.*

%files -n %{libname}%{libver}-devel
%doc MANIFEST README
%{_includedir}/dwarves/btf_encoder.h
%{_includedir}/dwarves/config.h
%{_includedir}/dwarves/ctf.h
%{_includedir}/dwarves/dutil.h
%{_includedir}/dwarves/dwarves.h
%{_includedir}/dwarves/dwarves_emit.h
%{_includedir}/dwarves/dwarves_reorganize.h
%{_includedir}/dwarves/elfcreator.h
%{_includedir}/dwarves/elf_symtab.h
%{_includedir}/dwarves/gobuffer.h
%{_includedir}/dwarves/hash.h
%{_includedir}/dwarves/libctf.h
%{_includedir}/dwarves/list.h
%{_includedir}/dwarves/rbtree.h
%{_libdir}/%{libname}.so
%{_libdir}/%{libname}_emit.so
%{_libdir}/%{libname}_reorganize.so

%changelog
* Wed Oct 13 2021 M. Vefa Bicakci <vefa.bicakci@windriver.com> - 1.22-1.tis
- Adapt the spec file included in the following dwarves release archive for
  StarlingX: https://fedorapeople.org/~acme/dwarves/dwarves-1.22.tar.bz2
- Modify the Release field for StarlingX.
- Avoid using cmake build macros that CentOS 7's rpmbuild does not have.
- Trim the changelog to include entries from the year 2021 only.

* Mon Aug 23 2021 Aug 17 2021 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.22-1
- New release: v1.22
- Introduce -j/--jobs option to specify the number of threads to use.
- Multithreaded DWARF loading, requires elfutils >= 0.178.
- Preparatory work for multithreaded BTF encoding, the focus for 1.23.
- Allow encoding BTF to a separate file.
- Show all different types with the same name, not just the first one found.
- Stop assuming that reading from stdin means pretty, add --prettify.
- Improve type resolution for the --header command line option.
- Do not consider the ftrace filter when encoding BTF for kernel functions.
- Lock calls to non-thread safe elfutils' dwarf_decl_file() and dwarf_decl_line().
- Change hash table size to one that performs better with current typical vmlinux files.
- Allow tweaking the hash table size from the command line.
- Add --kabi_prefix to avoid deduplication woes when using _RH_KABI_REPLACE().
- Add --with_flexible_array to show just types with flexible arrays.
- Support btfdiff with a detached BTF file.
- Introduce sorted type output (--sort).
- Disable incomplete CTF encoder.

* Fri Apr 9 2021 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.21-1
- New release: v1.21
- DWARF loader:
- Handle DWARF5 DW_OP_addrx properly
- Handle subprogram ret type with abstract_origin properly
- Check .notes section for LTO build info
- Check .debug_abbrev for cross-CU references
- Permit merging all DWARF CU's for clang LTO built binary
- Factor out common code to initialize a cu
- Permit a flexible HASHTAGS__BITS
- Use a better hashing function, from libbpf
- btf_encoder:
- Add --btf_gen_all flag
- Match ftrace addresses within ELF functions
- Funnel ELF error reporting through a macro
- Sanitize non-regular int base type
- Add support for the floating-point types
- Pretty printer:
- Honour conf_fprintf.hex when printing enumerations

* Tue Feb 2 2021 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.20-1
- New release: v1.20
- btf_encoder:
- Improve ELF error reporting using elf_errmsg(elf_errno())
- Improve objcopy error handling.
- Fix handling of 'restrict' qualifier, that was being treated as a 'const'.
- Support SHN_XINDEX in st_shndx symbol indexes
- Cope with functions without a name
- Fix BTF variable generation for kernel modules
- Fix address size to match what is in the ELF file being processed.
- Use kernel module ftrace addresses when finding which functions to encode.
- libbpf:
- Allow use of packaged version.
- dwarf_loader:
- Support DW_AT_data_bit_offset
- DW_FORM_implicit_const in attr_numeric() and attr_offset()
- Support DW_TAG_GNU_call_site, standardized rename of DW_TAG_GNU_call_site.
- build:
- Fix compilation on 32-bit architectures.
