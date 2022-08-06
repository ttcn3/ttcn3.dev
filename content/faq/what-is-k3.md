---
title: What is k3?
---

[k3](https://gitlabe1.ext.net.nokia.com/k3/k3) is the closed-source predecessor
of ntt. k3 provides various TTCN-3 tools, plugins and libraries.

* Test suite management
* Next generation test executor (k3s)
* TTCN-3 runtime (k3r)
* TTCN-3 compiler (k3c, mtc)
* ASN.1 compiler (OSS Nokalva ASN.1 Tools 10.6)
* Tools: Linter, CTags, Codebrowser, T3XF, Terminator, protoc-gen-ttcn3
* Reports: Textviewer, Callgraph, Stability, Flamegraph, JUnit, MSC, Message Coverage
* Libraries: SutControl, Config, Conversion, ExtProc, Math, OS, Snow3G, Strings, TCI-TM, TestManager, UDPSLogger, Utility, ZUC, Stringify
* Codecs: ASN.1, Binary, JSON, LaMe, MuLTI, Protobuf, SACK, Simple, TTCN-3, Text
* Transports: CCSStub, CCS, IPC, SCTP, TCP, UDP, ZMQ

k3 has been a great success in Nokia since 2008: Before k3 it took about 20 minutes to generate a test executable from 100,000 lines of TTCN-3 source code. Mostly because C++ compilers can be very slow. With k3 we were able to compile 2,000,000 lines of TTCN-3 source code in less than a minute.

Over the years code quality has degraded and maintenance has become quite
expensive. Therefore many components of k3 have been replaced with their open-source
counterparts in ntt already.
