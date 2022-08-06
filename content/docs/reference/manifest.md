---
title: Manifest
---

To execute a test suite you usually need more than just a bunch of TTCN-3 source
files: You need generators, adapters, codecs, a lot of scripting, compile time
configuration, runtime configuration, post processing tools, caching of
build-artifacts and more. A manifest file provides a stable frame for
tools to work together nicely.

Every ntt test suite should provide a manifest file `package.yml` at
the root of the test suite directory structure. Supported fields:


| Name               | Type              | Details
| ------------------ | ----------------- | --------
| `name`             | string            | Name of the test suite.
| `sources`          | string[]          | TTCN-3 Source files containing tests.
| `imports`          | string[]          | Packages the suite depends on. This could be adapters, codecs, generators, ...
| `timeout`          | number            | Default timeout for tests in seconds.
| `test_hook`        | string            | Path to test hook script.
| `parameters_file`  | string            | Path to module parameters file.
| `variables`        | map[string]string | A key value list of custom variables.


**Environment Variables**

Manifest values can be overwritten by environment variables. Environment
variables will always take precedence over regular variables. Regular variables
have to be declared in a TOML formatted file `ntt.env` or in `variables` section in
the manifest:

    $ echo '{"variables": {"NTT_NAME": "OrignalName" }, "name": "$NTT_NAME" }' > package.yml

    $ ntt show -- name
    OriginalName

    $ NTT_NAME=NewName ntt show -- name
    NewName


You also can overwrite arrays like `sources` or `imports` with environment
variables (`NTT_SOURCES="foo.ttcn3 bar.ttcn3" ...`), but note that spaces might
become problematic.

