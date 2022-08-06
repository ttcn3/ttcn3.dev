---
title: Is there a standard library for TTCN-3?
---

No. However there are bits and pieces which come close:


## Core Language Specification

The [TTCN-3 core language specification] defines various functions for type conversion, string manipulation and more in Annex C. In Annex E you'll find some useful type definitions, such as `byte` or `unsignedshort`.

## LibCommon

ETSI further provides a [library](http://www.ttcn-3.org/index.php/development/devlibraries/devlib-libcommon) with common defintions and datastructures.

## Adapters and Codecs

Unfortunately there are no re-usable adapters or codecs available, yet.
