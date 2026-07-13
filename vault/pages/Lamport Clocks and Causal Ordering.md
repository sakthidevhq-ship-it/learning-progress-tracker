title:: Lamport Clocks and Causal Ordering
type:: paper
domain:: [[Systems]]
topic:: [[Distributed Systems]]
engagement:: read
status:: unread
progress:: 0
complexity:: intermediate
size:: medium
medium:: paper
prerequisites:: [[Concurrency Basics]]
concepts:: [[Lamport Clocks]], [[Happens-Before Relation]], [[Logical Clocks]], [[Causal Ordering]], [[Total Ordering]], [[Vector Clocks]]
tags:: lamport, clocks, ordering
source:: /private/tmp/lamport-clocks.md
ingested:: [[2026-07-09]]
priority:: 33

## Summary
Lamport's foundational 'Time, Clocks, and the Ordering of Events in a Distributed System'. Defines happens-before relation, logical clocks, and total ordering in distributed systems. The paper that established how to reason about time and causality when there's no global clock.

## Key Takeaways
- Physical time is unreliable in distributed systems — logical clocks capture causality instead
- The happens-before relation is a partial order — concurrent events have no defined ordering
- Vector clocks extend Lamport clocks to detect true concurrency (not just order)

## Prerequisites
- [[Concurrency Basics]]

## My Notes
