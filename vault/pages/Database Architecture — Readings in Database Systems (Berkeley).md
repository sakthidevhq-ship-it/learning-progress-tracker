title:: Database Architecture — Readings in Database Systems (Berkeley)
type:: paper
domain:: [[Systems]]
topic:: [[Databases]]
engagement:: read
status:: unread
progress:: 0
complexity:: advanced
size:: deep-dive
medium:: paper
prerequisites:: [[Database Basics]], [[Transactions]], [[Consistency Models]]
concepts:: [[Storage Engines]], [[Query Optimization]], [[Column Stores]], [[MVCC]], [[Weak Isolation]], [[Dataflow Engines]], [[NewSQL]]
tags:: database, architecture, berkeley
source:: /private/tmp/db-architecture.md
ingested:: [[2026-07-09]]
priority:: 31

## Summary
Peter Bailis and Joe Hellerstein's curated collection of foundational database papers. Covers traditional RDBMS, new architectures (column stores, NewSQL), large-scale dataflow, weak isolation, query optimization, interactive analytics, and data integration. The canonical graduate-level database reading list.

## Key Takeaways
- Most databases implement weaker isolation than they claim — understanding the actual guarantees matters
- Column stores fundamentally changed analytics by trading write speed for read performance
- Query optimization is still mostly heuristic — cost-based optimizers make educated guesses, not optimal plans

## Prerequisites
- [[Database Basics]]
- [[Transactions]]
- [[Consistency Models]]

## My Notes
