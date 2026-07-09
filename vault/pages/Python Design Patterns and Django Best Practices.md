title:: Python Design Patterns and Django Best Practices
type:: docs
domain:: [[Programming/Python]]
topic:: [[Design Patterns]]
engagement:: read
status:: unread
progress:: 0
complexity:: intermediate
size:: medium
medium:: docs
prerequisites:: [[Python]]
concepts:: [[Design Patterns]], [[State Machines]], [[WSGI]], [[Django Migrations]], [[Factory Pattern]], [[Observer Pattern]]
tags:: patterns, python, django
source:: /private/tmp/patterns.md
ingested:: [[2026-07-09]]
priority:: 28

## Summary
Design patterns applied to Python: factory, observer, strategy, state machines (FSM), decorator. Django-specific patterns: WSGI internals, zero-downtime migrations, cached_property, and deployment with Fabric. Understanding how Django serves requests from WSGI to response.

## Key Takeaways
- WSGI is the interface between Python web apps and servers — understanding it demystifies Django's request lifecycle
- Finite state machines formalize complex business logic that would otherwise be spaghetti if/else chains
- Zero-downtime migrations require splitting schema changes from data changes across multiple deploys

## Prerequisites
- [[Python]]

## My Notes
