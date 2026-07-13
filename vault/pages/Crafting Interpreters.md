title:: Crafting Interpreters
type:: docs
domain:: [[Programming/Compilers]]
topic:: [[Language Implementation]]
engagement:: implement
status:: unread
progress:: 0
complexity:: intermediate
size:: deep-dive
medium:: docs
prerequisites:: [[Java Basics]], [[C Basics]], [[Data Structures]]
concepts:: [[Lexing]], [[Parsing]], [[AST]], [[Bytecode]], [[Virtual Machine]], [[Garbage Collection]], [[Closures]]
tags:: interpreters, book
source:: https://craftinginterpreters.com
ingested:: [[2026-07-09]]
priority:: 27

## Summary
Bob Nystrom's guide to building two complete interpreters: a tree-walk interpreter in Java (jlox) and a bytecode VM in C (clox). Covers scanning, parsing, name resolution, control flow, functions, closures, classes, inheritance, and garbage collection.

## Key Takeaways
- Tree-walk interpreters are simple but slow — bytecode VMs are the practical choice
- Pratt parsing elegantly handles operator precedence
- Mark-sweep GC is simple to implement and sufficient for most languages

## Prerequisites
- [[Java Basics]]
- [[C Basics]]
- [[Data Structures]]

## My Notes
