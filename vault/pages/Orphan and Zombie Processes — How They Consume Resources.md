title:: Orphan and Zombie Processes — How They Consume Resources
type:: docs
domain:: [[Systems]]
topic:: [[Operating Systems]]
engagement:: read
status:: unread
progress:: 0
complexity:: intermediate
size:: medium
medium:: docs
prerequisites:: [[C Basics]], [[Linux Basics]]
concepts:: [[Process Lifecycle]], [[Orphan Processes]], [[Zombie Processes]], [[Process Table]], [[Signal Handling]], [[Process Groups]]
tags:: processes, orphan, zombie
source:: /private/tmp/orphan.md
ingested:: [[2026-07-09]]
priority:: 34

## Summary
What happens when a parent process dies but its children keep running. Covers Unix process lifecycle (fork, exec, wait, exit), how orphans get reparented to init/launchd, how zombies retain PIDs and entries in the process table, why orphaned language servers and build tools silently accumulate and eat memory, and how to find and clean them up.

## Key Takeaways
- Orphan processes get reparented to PID 1 (init/launchd) and keep running with full resource usage
- Zombie processes are dead but their parent hasn't called wait() — they hold a process table entry until reaped
- Language servers spawned by editors often become orphans on editor crash — silently eating GBs of RAM

## Prerequisites
- [[C Basics]]
- [[Linux Basics]]

## My Notes
