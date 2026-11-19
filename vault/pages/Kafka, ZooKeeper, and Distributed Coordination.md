title:: Kafka, ZooKeeper, and Distributed Coordination
type:: paper
domain:: [[Systems]]
topic:: [[Streaming]]
engagement:: read
complexity:: intermediate
size:: deep-dive
medium:: paper
prerequisites:: [[Raft Consensus]], [[Networking Fundamentals]], [[Concurrency Basics]]
concepts:: [[Log-Structured Storage]], [[Atomic Broadcast]], [[Distributed Coordination]], [[Consumer Groups]], [[Partition Leadership]], [[Event Sourcing]]
tags:: kafka, zookeeper, atomic-broadcast
source:: /private/tmp/kafka-dist.md
ingested:: [[2026-07-09]]
state:: collected

## Summary
The distributed systems infrastructure stack: Kafka's log-based message broker with ZooKeeper's atomic broadcast protocol (Zab), Omega's flexible cluster scheduling, and Thialfi's client notification service. Covers how these systems achieve high-throughput, fault-tolerant coordination at internet scale.

## Key Takeaways
- Kafka treats messages as an append-only log — consumers track their own offset, enabling replay
- ZooKeeper's Zab protocol is a variant of Paxos optimized for primary-backup replication
- Moving from ZooKeeper to Raft (KRaft) simplifies Kafka's operational model

## Prerequisites
- [[Raft Consensus]]
- [[Networking Fundamentals]]
- [[Concurrency Basics]]

## Notes

## Learnings
- 2026-11-19 · Cheap coordination with Redis for an hourly summary across many workers: every event INCRs a counter, SET NX on a throttle key lets exactly one worker win the right to post, and that worker reads and clears the counts in one MULTI/EXEC, so an event landing in between goes into this summary or the next, never lost or doubled. On Redis Cluster those keys need a shared hash tag, or the transaction spans slots and fails.
