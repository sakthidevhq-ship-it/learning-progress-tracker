title:: PostgreSQL Internals — EXPLAIN, Indexes, and Bloom Filters
type:: docs
domain:: [[Systems]]
topic:: [[Databases]]
engagement:: read
status:: unread
progress:: 0
complexity:: intermediate
size:: deep-dive
medium:: docs
prerequisites:: [[Database Basics]]
concepts:: [[Query Planning]], [[EXPLAIN ANALYZE]], [[Index Design]], [[Bloom Filters]], [[Lateral Joins]], [[Query Optimization]]
tags:: postgres, explain, internals
source:: /private/tmp/pg.md
ingested:: [[2026-07-09]]
priority:: 33

## Summary
Deep dive into PostgreSQL internals: reading and visualizing EXPLAIN ANALYZE output, understanding query planner decisions, lateral joins, following a SELECT through Postgres internals, index maintenance strategies, monitoring unused indexes, and using Bloom filters for probabilistic membership testing.

## Key Takeaways
- EXPLAIN ANALYZE shows actual vs estimated rows — large mismatches indicate stale statistics or bad plans
- Bloom filters trade space for speed — test membership in constant time with a small false-positive rate
- Unused indexes slow writes without helping reads — monitor and drop them

## Prerequisites
- [[Database Basics]]

## My Notes
