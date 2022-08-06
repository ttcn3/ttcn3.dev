---
title: CMake
---

ntt provides a CMake module with functions to help use the NTT/K3 Test
infrastructure.  It searches for program `ntt` and stores its location in
variable `NTT_EXECUTABLE` and creates imported target `ntt::ntt`.

It further provides function `add_ttcn3_suite` for generating a test suite
manifest and function `protobuf_generate_ttcn3` for calling a protoc generator
plugin.


**Conventience Commands**
The CMake module uses the TGT parameter from `add_ttcn3_suite` to create
additional commands to make your CMake live easier:
* `$TGT.lint`: run [linter](#ntt-lint) against test suite.
* `$TGT.tags`: generate [cTags](#ntt-tags) file
* `$TGT.tests`: generate [testcase list](#ntt-list).
* `$TGT.deps`: generate [module dependency graph](#ntt-list).


## add_ttnc3_suite

Add a TTCN-3 test suite manifest for use with NTT and CTest:

```cmake
  add_ttcn3_suite(TGT
        SOURCES src1...
        [DEPENDS ...]
        [NAME name]
        [TIMEOUT secs]
        [TEST_HOOK executable]
        [PARAMETER_FILE file]
        [WORKING_DIRECTORY dir]
        [TARGETS target1...]
  )
```

`add_ttcn3_suite` creates a target TGT and test suite manifest
`package.yml` as `BYPRODUCT`.

The options are:

`SOURCES src1...`  
The list of .ttcn3 source files or source directories. When passing directories ntt will automatically include new TTCN-3 files in the test suite (globbing)without need to rerun CMake configuration.

`DEPENDS target1...|directory...`  
Specifies additional TTCN-3 packages required by the test suite.
If the argument specifies a target it will be replaced by the location of
the target directory (`$<TARGET_FILE_DIR>`). Additionally a target-level
dependency will be added so that the depending target will be built before
this test suite.

`NAME`  
Specfies the name of the test suite. If this option is not provided, ntt
will assign one.

`TIMEOUT seconds`  
Specifies a timeout after which a test case will be aborted.

`TEST_HOOK executable`  
Specifies an executable to be used as test hook.
If TEST_HOOK specifies an executable target (created by ADD_EXECUTABLE) it
will automatically be replaced by the location of the executable created at
build time. Additionally a target-level dependency will be added so that
the executable target will be built before this hook is used.

`PARAMETER_FILE file`  
Specifies a file containing TOML formatted test configuration.

`WORKING_DIRECTORY dir`  
Specifies the directory in which to run the tests. If this option is not
provided, the current binary directory is used.

`TARGETS target1...`  
Add additional target-level dependencies. This is used to assure SUTs or thid-party code generators are built before a test is executed.



## protobuf_generate_ttcn3

Call protoc generator plugin for TTCN-3 output.

```cmake
  protobuf_generate_ttcn3(TGT protofile1...)
```

`protobuf_generate_ttcn3` creates a target TGT for generating TTCN-3 files from
proto-files.  You may use use global variable `Protobuf_IMPORT_DIRS` to add
custom include directories.  

## Example

```cmake
find_package(Protobuf REQUIRED)
find_package(NTT REQUIRED)
protobuf_generate_ttcn3(proto_itf
  foo.proto
  bar.proto
)

add_ttcn3_suite(suite1
    SOURCES   tests.ttcn3
    TEST_HOOK hook.py
    DEPENDS
        proto_itf # see https://github.com/nokia/ntt/issues/195
    TARGETS
        mySUT
)
```
