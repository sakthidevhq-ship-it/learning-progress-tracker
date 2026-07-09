title:: Raft — In Search of an Understandable Consensus Algorithm
type:: paper
domain:: [[Systems]]
topic:: [[Distributed Consensus]]
engagement:: read
status:: unread
progress:: 0
complexity:: intermediate
size:: deep-dive
medium:: paper
prerequisites:: [[Networking Fundamentals]], [[Concurrency Basics]]
concepts:: [[Raft Consensus]], [[Leader Election]], [[Log Replication]], [[Replicated State Machine]], [[Membership Changes]], [[Log Compaction]]
tags:: raft, consensus
source:: /private/tmp/raft.md
ingested:: [[2026-07-09]]
priority:: 34

## Summary
The Raft consensus algorithm, designed for understandability. Covers leader election, log replication, safety guarantees, membership changes, and log compaction. The go-to alternative to Paxos for building replicated state machines. Used in etcd, CockroachDB, and TiKV.

## Key Takeaways
- Raft decomposes consensus into leader election + log replication + safety — each independently understandable
- Strong leader model simplifies reasoning — all writes go through the leader
- Log compaction via snapshotting prevents unbounded log growth

## Prerequisites
- [[Networking Fundamentals]]
- [[Concurrency Basics]]

## My Notes
