title:: Zero-Downtime Postgres Schema Migrations
type:: docs
domain:: [[Systems]]
topic:: [[Databases]]
engagement:: implement
status:: unread
progress:: 0
complexity:: intermediate
size:: medium
medium:: docs
prerequisites:: [[Database Basics]]
concepts:: [[Schema Migrations]], [[Lock Timeouts]], [[Zero-Downtime Deploys]], [[Advisory Locks]], [[Database Fundamentals]]
source:: unknown
ingested:: [[2026-07-09]]
priority:: 33

## Summary
Practical guide to performing safe schema migrations on production Postgres databases. Covers lock timeout strategies, retry patterns, and advisory lock usage for achieving zero-downtime deployments.

## Key Takeaways
- Lock timeouts prevent long-running queries from blocking migrations
- Retry patterns handle transient lock contention gracefully
- Advisory locks enable coordination between deployment and application logic

## Prerequisites
- [[Database Basics]]

## My Notes
