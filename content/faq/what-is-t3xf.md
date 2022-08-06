---
title: What is T3XF/TASM?
---

t3xf (TTCN-3 Executable Format) is a binary representation of input TTCN-3 source text, suitable for execution by a native application, its main purpose expected to be the execution of test cases against a system under test.

t3xf can be thought of as one possible binary dump of the abstract syntax tree created by a TTCN-3 compiler after all semantic checking has been performed. t3xf is conceived as a file format. No provision is made for streaming or for editing. Transmission of whole files is not only possible but will be required in systems that support testing distributed across a number of host machines.

tasm (T3xf Assembly) is an extension to t3xf allowing objects to be loaded lazily and hence reducing the time for loading t3xf files. 
