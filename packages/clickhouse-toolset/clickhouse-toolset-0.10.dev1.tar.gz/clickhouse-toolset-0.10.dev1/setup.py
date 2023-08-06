import os
import subprocess
import re
import sys
import shutil
from sys import platform
from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext
from setuptools.wheel import Wheel

NAME = 'clickhouse-toolset'
# https://www.python.org/dev/peps/pep-0440/#developmental-releases
VERSION = '0.10.dev1'

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CLICKHOUSE_PATH = os.path.join(ROOT_DIR, 'ClickHouse')
CLICKHOUSE_BUILD_PATH = os.path.join(ROOT_DIR, 'ch_build')
LIBC_PATH = os.path.join(ROOT_DIR, 'musl')
LIBC_BUILD_PATH = os.path.join(ROOT_DIR, 'musl_build')

class ClickHouseParsersBuildExt(build_ext):
    def run(self):
        if (os.path.isfile(os.path.join(CLICKHOUSE_BUILD_PATH, 'src/Parsers/libclickhouse_parsers.a')) and
            os.path.isfile(os.path.join(CLICKHOUSE_BUILD_PATH, 'src/libdbms.a'))):
            return

        cmake_cmd = os.environ.get('CMAKE_BIN', 'cmake')
        try:
            subprocess.check_output([cmake_cmd, '--version'])
        except OSError:
            raise RuntimeError(
                'CMake must be installed to build the following extensions: ' +
                ', '.join(e.name for e in self.extensions))

        if not os.path.exists(os.path.join(CLICKHOUSE_PATH, 'CMakeLists.txt')):
            raise RuntimeError('Git submodules are not initialized. Run: `git submodule update --init --recursive`.')

        if not os.path.exists(CLICKHOUSE_BUILD_PATH):
            os.makedirs(CLICKHOUSE_BUILD_PATH)

        cmake_args = [
            '-DCMAKE_C_COMPILER=clang',
            '-DCMAKE_CXX_COMPILER=clang++',
            '-DUSE_STATIC_LIBRARIES=TRUE',
            '-DMAKE_STATIC_LIBRARIES=TRUE',
            '-DENABLE_TESTS=FALSE',
            '-DCMAKE_C_FLAGS=-fPIC',
            '-DCMAKE_CXX_FLAGS=-fPIC',
            '-DCMAKE_BUILD_TYPE=Release',
            '-DWERROR=0',
            '-Wno-dev',
            '-DENABLE_AMQPCPP=FALSE',
            '-DENABLE_AVRO=FALSE',
            '-DENABLE_BASE64=FALSE',
            '-DENABLE_BROTLI=FALSE',
            '-DENABLE_CAPNP=FALSE',
            '-DENABLE_CASSANDRA=FALSE',
            '-DENABLE_CCACHE=FALSE',
            '-DENABLE_CPUID=FALSE',
            '-DENABLE_CURL=FALSE',
            '-DENABLE_CYRUS_SASL=FALSE',
            '-DENABLE_DATASKETCHES=FALSE',
            '-DENABLE_FASTOPS=FALSE',
            '-DENABLE_GRPC=FALSE',
            '-DENABLE_GSASL_LIBRARY=FALSE',
            '-DENABLE_H3=FALSE',
            '-DENABLE_HDFS=FALSE',
            '-DENABLE_HYPERSCAN=FALSE',
            '-DENABLE_KRB5=FALSE',
            '-DENABLE_LDAP=FALSE',
            '-DENABLE_LIBPQXX=FALSE',
            '-DENABLE_MSGPACK=FALSE',
            '-DENABLE_MYSQL=FALSE',
            '-DENABLE_NURAFT=FALSE',
            '-DENABLE_ODBC=FALSE',
            '-DENABLE_ORC=FALSE',
            '-DENABLE_PARQUET=FALSE',
            '-DENABLE_PROTOBUF=FALSE',
            '-DENABLE_RAPIDJSON=FALSE',
            '-DENABLE_RDKAFKA=FALSE',
            '-DENABLE_REPLXX=FALSE',
            '-DENABLE_ROCKSDB=FALSE',
            '-DENABLE_S3=FALSE',
            '-DENABLE_SSL=FALSE',
            '-DENABLE_STATS=FALSE',
            '-DUSE_INTERNAL_AVRO_LIBRARY=FALSE',
            '-DUSE_INTERNAL_AWS_S3_LIBRARY=FALSE',
            '-DUSE_INTERNAL_BROTLI_LIBRARY=FALSE',
            '-DUSE_INTERNAL_CAPNP_LIBRARY=FALSE',
            '-DUSE_INTERNAL_CURL=FALSE',
            '-DUSE_INTERNAL_GRPC_LIBRARY=FALSE',
            '-DUSE_INTERNAL_GTEST_LIBRARY=FALSE',
            '-DUSE_INTERNAL_H3_LIBRARY=FALSE',
            '-DUSE_INTERNAL_HDFS3_LIBRARY=FALSE',
            '-DUSE_INTERNAL_HYPERSCAN_LIBRARY=FALSE',
            '-DUSE_INTERNAL_LDAP_LIBRARY=FALSE',
            '-DUSE_INTERNAL_LIBGSASL_LIBRARY=FALSE',
            '-DUSE_INTERNAL_MSGPACK_LIBRARY=FALSE',
            '-DUSE_INTERNAL_MYSQL_LIBRARY=FALSE',
            '-DUSE_INTERNAL_ODBC_LIBRARY=FALSE',
            '-DUSE_INTERNAL_ORC_LIBRARY=FALSE',
            '-DUSE_INTERNAL_PARQUET_LIBRARY=FALSE',
            '-DUSE_INTERNAL_PROTOBUF_LIBRARY=FALSE',
            '-DUSE_INTERNAL_RAPIDJSON_LIBRARY=FALSE',
            '-DUSE_INTERNAL_RDKAFKA_LIBRARY=FALSE',
            '-DUSE_INTERNAL_REPLXX_LIBRARY=FALSE',
            '-DUSE_INTERNAL_SNAPPY_LIBRARY=FALSE',
            '-DUSE_INTERNAL_SSL_LIBRARY=FALSE',
            '-DUSE_INTERNAL_ROCKSDB_LIBRARY=FALSE',

            '-DENABLE_EMBEDDED_COMPILER=FALSE',
            '-DUSE_INTERNAL_LLVM_LIBRARY=FALSE',

            '-DENABLE_ICU=FALSE',
            '-DUSE_INTERNAL_ICU_LIBRARY=FALSE',

            '-DENABLE_JEMALLOC=FALSE',

            '-DUSE_SIMDJSON=FALSE',
            '-DUSE_SENTRY=FALSE',

            '-DENABLE_THINLTO=FALSE',  # Issues in CI, slower link times and doesn't make our use case faster
        ]

        if platform == 'darwin':
            cmake_args += [
                '-DUSE_INTERNAL_LIBCXX_LIBRARY=FALSE'
            ]

        subprocess.check_call([cmake_cmd, CLICKHOUSE_PATH] + cmake_args, cwd=CLICKHOUSE_BUILD_PATH)

        build_args = [
            '--config', 'Release',
            '--target', 'src/Parsers/libclickhouse_parsers.a',
        ]
        subprocess.check_call([cmake_cmd, '--build', CLICKHOUSE_BUILD_PATH] + build_args)
        build_args = [
            '--config', 'Release',
            '--target', 'src/libdbms.a'
        ]
        subprocess.check_call([cmake_cmd, '--build', CLICKHOUSE_BUILD_PATH] + build_args)

class LibcBuildExt(build_ext):
    def run(self):
        if os.path.isfile(LIBC_BUILD_PATH + '/lib/libc.a'):
            return

        if not os.path.exists(LIBC_PATH):
            raise RuntimeError('Git submodules are not initialized. Run: `git submodule update --init --recursive`.')

        if not os.path.exists(LIBC_BUILD_PATH):
            os.makedirs(LIBC_BUILD_PATH)

        subprocess.check_call([LIBC_PATH + '/configure', 'CC=clang', 'CFLAGS=-fPIC -O3'], cwd=LIBC_BUILD_PATH)
        subprocess.check_call(['make', '-j'], cwd=LIBC_BUILD_PATH)

class BuildExtFromWheel(build_ext):
    def run(self):
        wheel_base_url = os.environ.get('WHEEL_BASE_URL', 'https://storage.googleapis.com/tinybird-bdist_wheels')

        minor_version = sys.version_info.minor
        # https://www.python.org/dev/peps/pep-0491/#file-name-convention
        language_version = f'cp3{minor_version}'
        # https://docs.python.org/3/whatsnew/3.8.html#build-and-c-api-changes
        # https://bugs.python.org/issue36707
        # cpython + WITH_PYMALLOC
        abi_tag = f'cp3{minor_version}m' if minor_version < 8 else f'cp3{minor_version}'

        def escape_name_component(x):
            # https://www.python.org/dev/peps/pep-0491/#escaping-and-unicode
            return re.sub(r"[^\w\d.]+", "_", x, re.UNICODE)

        wheel_target_name = '-'.join([escape_name_component(x) for x in [
            NAME,
            VERSION,
            language_version,
            abi_tag,
            self.plat_name.replace('.', '_'),
        ]]) + '.whl'
        wheel_pathname = os.path.join('/tmp', wheel_target_name)
        in_url = f'{wheel_base_url}/{wheel_target_name}'
        build_dir = self.get_finalized_command('build_py').build_lib

        from urllib.request import urlopen
        with urlopen(in_url) as wheel_in, open(wheel_pathname, 'wb') as wheel_out:
            wheel_out.write(wheel_in.read())

            # We remove whatever copies were done before and replace everything with the contents of the wheel
            shutil.rmtree(build_dir)
            print("PIP DETECTED: WRITING DOWNLOADED whl to " + build_dir)
            w = Wheel(wheel_pathname)
            w.install_as_egg(build_dir)


# This was taken from a compilation command, some of them might be unnecessary
include_paths = [
    '../ch_build/includes/configs',
    'src',
    '../ch_build/src',
    '../ch_build/src/Core/include',
    'base/glibc-compatibility/memcpy',
    'base/common/..',
    '../ch_build/base/common/..',
    'contrib/cityhash102/include',
    'contrib/cctz/include',
    '../ch_build/contrib/zlib-ng',
    'contrib/zlib-ng',
    'base/pcg-random/.',
    'contrib/lz4/lib',
    'contrib/sparsehash-c11',
    'contrib/miniselect/include',
    'contrib/pdqsort'
]

if platform != "darwin":
    include_paths += [
        'contrib/libcxx/include',
        'contrib/libcxxabi/include',
    ]

include_paths += [
    'contrib/antlr4-runtime',
    'contrib/fast_float/include',
    'contrib/xz/src/liblzma/api',
    'contrib/zstd/lib',
    'contrib/re2',
    'contrib/boost',
    'contrib/poco/Net/include',
    'contrib/poco/Foundation/include',
    'contrib/poco/Util/include',
    'contrib/poco/JSON/include',
    'contrib/poco/XML/include',
    'contrib/fmtlib-cmake/../fmtlib/include',
    'contrib/double-conversion',
    'contrib/dragonbox/include',
    '../ch_build/contrib/re2_st',
    'contrib/croaring/cpp',
    'contrib/croaring/include',
    'contrib/libdivide/.',
    'contrib/poco/MongoDB/include',
]

if platform != "darwin":
    include_paths += [
        'contrib/libc-headers/x86_64-linux-gnu',
        'contrib/libc-headers',
    ]

include_dirs = [f'{CLICKHOUSE_PATH}/{rel_path}' for rel_path in include_paths]

LIBRARIES_WITH_PATHS = [
    ('dbms', './src'),
    ('dbms', './src'),  # Need to be added twice to find all symbols (for some reason)
    ('clickhouse_parsers', './src/Parsers'),
    ('clickhouse_parsers_new', './src/Parsers/New'),
    ('clickhouse_common_io', './src'),
    ('clickhouse_dictionaries_embedded', './src/Dictionaries/Embedded'),
    ('clickhouse_common_config', './src/Common/Config'),
    ('clickhouse_common_zookeeper', './src/Common/ZooKeeper'),
    ('string_utils', './src/Common/StringUtils'),
    ('common', './base/common'),
    ('widechar_width', './base/widechar_width'),
    ('zstd', './contrib/zstd-cmake'),
    ('cityhash', './contrib/cityhash102'),
    ('roaring', './contrib/croaring-cmake'),
    ('re2', './contrib/re2'),
    ('re2_st', './contrib/re2_st'),
    ('lz4', './contrib/lz4-cmake'),
    ('fmt', './contrib/fmtlib-cmake')
]
if platform != "darwin":
    LIBRARIES_WITH_PATHS += [
        ('tzdata', './contrib/cctz-cmake'),
    ]
LIBRARIES_WITH_PATHS += [
    ('cctz', './contrib/cctz-cmake'),
    ('lzma', './contrib/xz'),
    ('dragonbox_to_chars', './contrib/dragonbox-cmake'),
    ('double-conversion', './contrib/double-conversion-cmake'),
    ('antlr4-runtime', './contrib/antlr4-runtime-cmake'),
    ('_boost_system', './contrib/boost-cmake'),
    ('_boost_program_options', './contrib/boost-cmake'),
    ('_boost_filesystem', './contrib/boost-cmake'),
    ('_boost_context', './contrib/boost-cmake'),
    ('_poco_mongodb', './contrib/poco-cmake/MongoDB'),
    ('_poco_net', './contrib/poco-cmake/Net'),
    ('_poco_util', './contrib/poco-cmake/Util'),
    ('_poco_json', './contrib/poco-cmake/JSON'),
    ('_poco_json_pdjson', './contrib/poco-cmake/JSON'),
    ('_poco_xml', './contrib/poco-cmake/XML'),
    ('_poco_xml_expat', './contrib/poco-cmake/XML'),
    ('_poco_foundation', './contrib/poco-cmake/Foundation'),
    ('_poco_foundation_pcre', './contrib/poco-cmake/Foundation'),
    ('z', './contrib/zlib-ng'),
]
if platform != "darwin":
    LIBRARIES_WITH_PATHS += [
        ('cxx', './contrib/libcxx-cmake'),
        ('cxxabi', './contrib/libcxxabi-cmake'),
        #('memcpy', './base/glibc-compatibility/memcpy'),
        #('glibc-compatibility', './base/glibc-compatibility'),
        ('unwind', './contrib/libunwind-cmake'),
    ]


class CustomBuildWithClang(build_ext):
    @staticmethod
    def cflags():
        return '-std=gnu++2a -fPIC -O3 -DNDEBUG'

    @staticmethod
    def ldflags():
        return "-shared -Wl,-O3,--sort-common,-z,relro,-z,now -s -fuse-ld=lld -Wl,--whole-archive"

    @staticmethod
    def extra_libs():
        # Add CH static libs
        libs = ['-Wl,--no-whole-archive,--start-group']
        libs += [os.path.join(CLICKHOUSE_BUILD_PATH, p) + "/lib" + l + ".a" for (l, p) in LIBRARIES_WITH_PATHS]
        libs.append('-Wl,--end-group')

        # Get CH default libs from the build logs (hacky but it works, kinda)
        ninja_path = os.path.join(CLICKHOUSE_BUILD_PATH, "build.ninja")
        task = subprocess.Popen(
            ["grep nodefault " + ninja_path + " | head -n1 | sed -n -e 's/^.*\(-nodefaultlibs\)/\\1/p'"], shell=True,
            stdout=subprocess.PIPE)
        libs += list(filter(lambda flag: not flag.startswith('-l'), task.stdout.read().decode('utf-8').split()))

        libs += [
            '-Wl,--start-group',
            LIBC_BUILD_PATH + '/lib/libcrypt.a',
            LIBC_BUILD_PATH + '/lib/libm.a',
            LIBC_BUILD_PATH + '/lib/librt.a',
            LIBC_BUILD_PATH + '/lib/libpthread.a',
            LIBC_BUILD_PATH + '/lib/libdl.a',
            LIBC_BUILD_PATH + '/lib/libresolv.a',
            LIBC_BUILD_PATH + '/lib/libutil.a',
            LIBC_BUILD_PATH + '/lib/libxnet.a',
            LIBC_BUILD_PATH + '/lib/libc.a',
            '-Wl,--end-group',
            ]
        return libs

    def build_extensions(self):
        if platform != "darwin":
            self.compiler.set_executable("compiler_so", "clang++ " + self.cflags())
            self.compiler.set_executable("compiler", "clang " + self.cflags())
            self.compiler.set_executable("compiler_cxx", "clang++ " + self.cflags())
            self.compiler.set_executable("linker_so", "clang++ " + self.ldflags())
            self.run_command('libc_libs')
        self.run_command('clickhouse_parsers')
        build_ext.build_extensions(self)

    def build_extension(self, ext):
        if platform != "darwin":
            ext.extra_link_args = self.extra_libs()
        build_ext.build_extension(self, ext)


library_dirs = []
libraries = []
if platform == "darwin":
    library_dirs = [os.path.join(CLICKHOUSE_BUILD_PATH, p) for (_, p) in LIBRARIES_WITH_PATHS]
    libraries = [l for (l, _) in LIBRARIES_WITH_PATHS]
    libraries += ['c++', 'c++abi']

chquery = Extension(
    'chtoolset._query',
    sources=['src/query.cpp'],
    depends=['src/ClickHouseQuery.h'],
    include_dirs=include_dirs,
    # Only used for OSX
    extra_compile_args=['-std=gnu++2a'],
    library_dirs=library_dirs,
    libraries=libraries
)

build_ext_class = CustomBuildWithClang

setup(
    name=NAME,
    version=VERSION,
    url='https://gitlab.com/tinybird/clickhouse-toolset',
    author='Raul Ochoa',
    author_email='raul@tinybird.co',
    packages=['chtoolset'],
    package_dir={'': 'src'},
    python_requires='>=3.6, <3.11',
    install_requires=[],
    extras_require={
        'test': [
            'pytest',
        ],
        'build': [
            'twine',
            'wheel',
        ]
    },
    cmdclass={
        'clickhouse_parsers': ClickHouseParsersBuildExt,
        'libc_libs': LibcBuildExt,
        'build_ext': build_ext_class,
    },
    ext_modules=[chquery]
)
