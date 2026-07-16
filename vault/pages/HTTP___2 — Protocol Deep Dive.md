title:: HTTP/2 — Protocol Deep Dive
type:: docs
domain:: [[Networking]]
topic:: [[Protocols]]
engagement:: read
status:: unread
progress:: 0
complexity:: intermediate
size:: medium
medium:: docs
prerequisites:: [[Networking Fundamentals]], [[TCP/IP Basics]]
concepts:: [[HTTP/2]], [[Multiplexing]], [[Binary Framing]], [[Header Compression]], [[Stream Prioritization]]
tags:: http2, web
source:: /private/tmp/http2.md
ingested:: [[2026-07-09]]
priority:: 27

## Summary
Understanding HTTP/2: multiplexing, server push, header compression (HPACK), binary framing, stream prioritization. How it solves head-of-line blocking, reduces latency, and changes best practices for web performance (no more domain sharding, spriting, or concatenation).

## Key Takeaways
- HTTP/2 multiplexes multiple requests over a single TCP connection — no more head-of-line blocking at HTTP level
- Binary framing replaces text-based HTTP/1.1 — more efficient parsing and smaller overhead
- Old optimization tricks (domain sharding, sprite sheets) are anti-patterns in HTTP/2

## Prerequisites
- [[Networking Fundamentals]]
- [[TCP/IP Basics]]

## My Notes
