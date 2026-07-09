title:: Redpanda - Kafka-Compatible Streaming
type:: docs
domain:: [[Systems]]
topic:: [[Streaming]]
engagement:: read
status:: unread
progress:: 0
complexity:: intermediate
size:: medium
medium:: docs
prerequisites:: [[Networking Fundamentals]], [[Concurrency Basics]], [[Linux Basics]]
concepts:: [[Event Streaming]], [[Thread-Per-Core]], [[Raft Consensus]], [[Log-Structured Storage]], [[Zero-Copy Networking]]
tags:: kafka, streaming
source:: https://github.com/redpanda-data/redpanda
ingested:: [[2026-07-09]]
priority:: 34

## Summary
Exploration of Redpanda, a Kafka-compatible streaming platform written in C++ using Seastar. Covers its architecture: thread-per-core design, no JVM/ZooKeeper dependency, Raft for replication, and how it achieves lower latency than Kafka.

## Key Takeaways
- Thread-per-core eliminates lock contention — each core owns its data
- Raft replaces ZooKeeper for simpler, more predictable consensus
- Seastar's future/promise model enables zero-copy I/O at kernel bypass speeds

## Prerequisites
- [[Networking Fundamentals]]
- [[Concurrency Basics]]
- [[Linux Basics]]

## My Notes
