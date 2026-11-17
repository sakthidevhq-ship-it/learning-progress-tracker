title:: Zero-Downtime Postgres Schema Migrations
type:: docs
domain:: [[Systems]]
topic:: [[Databases]]
engagement:: implement
complexity:: intermediate
size:: medium
medium:: docs
prerequisites:: [[Database Basics]]
concepts:: [[Schema Migrations]], [[Lock Timeouts]], [[Zero-Downtime Deploys]], [[Advisory Locks]], [[Database Fundamentals]]
source:: unknown
ingested:: [[2026-07-09]]
state:: collected

## Summary
Practical guide to performing safe schema migrations on production Postgres databases. Covers lock timeout strategies, retry patterns, and advisory lock usage for achieving zero-downtime deployments.

## Key Takeaways
- Lock timeouts prevent long-running queries from blocking migrations
- Retry patterns handle transient lock contention gracefully
- Advisory locks enable coordination between deployment and application logic

## Prerequisites
- [[Database Basics]]

## Notes

## Learnings
- 2026-11-17 · The same expand-before-use rule applies to config stored in a shared DB: main added a stage STT 'router' field and agents were edited to use it, but the 1.15 branch's Pydantic model has extra='forbid', so every canary call for those agents failed at set-up. Old readers must tolerate new fields (or the field must ship to every running version) before any writer starts storing it.
