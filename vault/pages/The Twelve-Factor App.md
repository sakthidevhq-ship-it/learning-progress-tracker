title:: The Twelve-Factor App
type:: docs
domain:: [[Systems]]
topic:: [[Architecture]]
engagement:: read
status:: unread
progress:: 0
complexity:: beginner
size:: quick-read
medium:: docs
concepts:: [[Twelve-Factor App]], [[Config Management]], [[Stateless Processes]], [[Disposability]], [[Dev-Prod Parity]]
tags:: 12factor, saas, heroku
source:: /private/tmp/12factor.md
ingested:: [[2026-07-09]]
priority:: 36

## Summary
Heroku's methodology for building SaaS applications. Twelve principles: codebase, dependencies, config, backing services, build/release/run, processes, port binding, concurrency, disposability, dev/prod parity, logs, admin processes. The foundation of modern cloud-native application design.

## Key Takeaways
- Store config in environment variables, never in code — one codebase, many deploys
- Processes should be stateless and share-nothing — any state goes to a backing service
- Treat logs as event streams — never write to local files in production

## My Notes
