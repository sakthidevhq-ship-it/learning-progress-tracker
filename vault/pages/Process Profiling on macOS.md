title:: Process Profiling on macOS
type:: docs
domain:: [[Systems]]
topic:: [[Operating Systems]]
engagement:: implement
status:: unread
progress:: 0
complexity:: intermediate
size:: medium
medium:: docs
prerequisites:: [[C Basics]], [[Linux Basics]]
concepts:: [[Process Profiling]], [[Flame Graphs]], [[dtrace]], [[Instruments]], [[CPU Profiling]], [[Memory Profiling]], [[System Calls]]
tags:: profiling, macos, debugging
source:: /private/tmp/proc.md
ingested:: [[2026-07-09]]
priority:: 34

## Summary
How to find and diagnose resource-hogging processes on macOS. Covers top, ps, Activity Monitor internals, Instruments.app for CPU/memory profiling, dtrace/dtruss for syscall tracing, sample and spindump for hang diagnosis, and how to read flame graphs. Understanding what your system is actually doing when it feels slow.

## Key Takeaways
- Activity Monitor shows RSS but not shared/compressed pages — use vm_stat for the real picture
- Instruments.app gives time-profiling flame graphs that attribute CPU to exact call stacks
- sample <PID> captures a 5-second profile from the command line without Instruments

## Prerequisites
- [[C Basics]]
- [[Linux Basics]]

## My Notes
