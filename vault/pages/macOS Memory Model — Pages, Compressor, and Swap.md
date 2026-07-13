title:: macOS Memory Model — Pages, Compressor, and Swap
type:: docs
domain:: [[Systems]]
topic:: [[Operating Systems]]
engagement:: read
status:: unread
progress:: 0
complexity:: intermediate
size:: medium
medium:: docs
prerequisites:: [[Memory Management Concepts]], [[Linux Basics]]
concepts:: [[Virtual Memory]], [[Memory Pages]], [[Memory Compressor]], [[Swap Management]], [[Unified Memory]], [[Memory Pressure]], [[Mach VM]]
tags:: macos, memory, vm
source:: /private/tmp/macos-mem.md
ingested:: [[2026-07-09]]
priority:: 33

## Summary
How macOS manages memory differently from Linux. Covers Mach VM pages (free, active, inactive, speculative, wired, compressor), why 'free memory' being low is normal, how the in-RAM compressor works before swap kicks in, when swap thrashing happens and how to detect it, unified memory on Apple Silicon, and memory pressure as the real health signal.

## Key Takeaways
- macOS doesn't free RAM eagerly — low 'free' memory is normal; watch compressor size and swap rate instead
- The in-RAM compressor is unique to macOS — it compresses inactive pages in RAM before resorting to disk swap
- Apple Silicon unified memory means GPU and CPU share the same pool — large GPU tasks directly compete with apps

## Prerequisites
- [[Memory Management Concepts]]
- [[Linux Basics]]

## My Notes
