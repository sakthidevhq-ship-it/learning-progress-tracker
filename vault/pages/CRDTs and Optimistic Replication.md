title:: CRDTs and Optimistic Replication
type:: paper
domain:: [[Systems]]
topic:: [[Distributed Replication]]
engagement:: read
status:: unread
progress:: 0
complexity:: advanced
size:: deep-dive
medium:: paper
prerequisites:: [[Networking Fundamentals]], [[Concurrency Basics]], [[Consistency Models]]
concepts:: [[CRDTs]], [[Eventual Consistency]], [[Conflict Resolution]], [[Causal Consistency]], [[Optimistic Replication]], [[Vector Clocks]]
tags:: crdt, replication, eventual-consistency
source:: /private/tmp/crdt.md
ingested:: [[2026-07-09]]
priority:: 31

## Summary
Convergent and Commutative Replicated Data Types (CRDTs) — data structures that can be replicated across nodes and updated independently, with mathematical guarantees of eventual convergence without coordination. Covers G-Counters, PN-Counters, OR-Sets, LWW-Registers, and the theory of optimistic replication with causal consistency.

## Key Takeaways
- CRDTs guarantee convergence without coordination — mathematically impossible to have conflicts
- The trade-off: CRDTs can only express monotonically growing state — deletions require tombstones
- Optimistic replication accepts temporary divergence for availability — CRDTs make convergence automatic

## Prerequisites
- [[Networking Fundamentals]]
- [[Concurrency Basics]]
- [[Consistency Models]]

## My Notes
