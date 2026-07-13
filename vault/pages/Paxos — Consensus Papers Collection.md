title:: Paxos — Consensus Papers Collection
type:: paper
domain:: [[Systems]]
topic:: [[Distributed Consensus]]
engagement:: read
status:: unread
progress:: 0
complexity:: advanced
size:: deep-dive
medium:: paper
prerequisites:: [[Networking Fundamentals]], [[Concurrency Basics]], [[Raft Consensus]]
concepts:: [[Paxos Consensus]], [[Multi-Paxos]], [[Quorum]], [[Proposer-Acceptor-Learner]], [[FLP Impossibility]], [[Partial Synchrony]]
tags:: paxos, consensus, lamport
source:: /private/tmp/paxos.md
ingested:: [[2026-07-09]]
priority:: 31

## Summary
The family of Paxos consensus papers: Lamport's 'The Part-Time Parliament' (original), 'Paxos Made Simple' (accessible rewrite), 'Paxos Made Live' (Google's engineering experience), and 'Paxos Made Practical'. Covers single-decree Paxos, Multi-Paxos, and the gap between theory and production implementation.

## Key Takeaways
- Paxos guarantees safety (never disagree) but not liveness (may stall) — FLP impossibility
- Multi-Paxos amortizes leader election across many decisions — practical systems use this, not basic Paxos
- The gap between Paxos-the-paper and Paxos-in-production is enormous — 'Made Live' documents this honestly

## Prerequisites
- [[Networking Fundamentals]]
- [[Concurrency Basics]]
- [[Raft Consensus]]

## My Notes
