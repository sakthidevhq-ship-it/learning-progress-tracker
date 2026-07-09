title:: Spanner and Calvin — Globally Distributed Transactions
type:: paper
domain:: [[Systems]]
topic:: [[Distributed Databases]]
engagement:: read
status:: unread
progress:: 0
complexity:: advanced
size:: deep-dive
medium:: paper
prerequisites:: [[Consistency Models]], [[Raft Consensus]], [[Transactions]], [[Networking Fundamentals]]
concepts:: [[External Consistency]], [[TrueTime]], [[Deterministic Transactions]], [[Two-Phase Commit]], [[Multi-Datacenter Consistency]], [[Global Ordering]]
tags:: spanner, google, transactions
source:: /private/tmp/spanner.md
ingested:: [[2026-07-09]]
priority:: 32

## Summary
Google Spanner's globally distributed database with external consistency via TrueTime (GPS + atomic clocks), and Calvin's deterministic transaction ordering as an alternative approach. Covers the spectrum from strong consistency (Spanner) to deterministic execution (Calvin) to multi-datacenter consistency (MDCC).

## Key Takeaways
- Spanner uses GPS + atomic clocks (TrueTime) to bound clock uncertainty and provide external consistency
- Calvin avoids coordination overhead by deterministically ordering transactions before execution
- The CAP theorem is a spectrum — Spanner trades latency for consistency, not availability

## Prerequisites
- [[Consistency Models]]
- [[Raft Consensus]]
- [[Transactions]]
- [[Networking Fundamentals]]

## My Notes
