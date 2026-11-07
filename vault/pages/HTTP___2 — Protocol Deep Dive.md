title:: HTTP/2 — Protocol Deep Dive
type:: docs
domain:: [[Networking]]
topic:: [[Protocols]]
engagement:: read
complexity:: intermediate
size:: medium
medium:: docs
prerequisites:: [[Networking Fundamentals]], [[TCP/IP Basics]]
concepts:: [[HTTP/2]], [[Multiplexing]], [[Binary Framing]], [[Header Compression]], [[Stream Prioritization]]
tags:: http2, web
source:: /private/tmp/http2.md
ingested:: [[2026-07-09]]
state:: picked
picked:: [[2026-11-07]]
planned:: 2026-11
my-priority:: now

## Summary
Understanding HTTP/2: multiplexing, server push, header compression (HPACK), binary framing, stream prioritization. How it solves head-of-line blocking, reduces latency, and changes best practices for web performance (no more domain sharding, spriting, or concatenation).

## Key Takeaways
- HTTP/2 multiplexes multiple requests over a single TCP connection — no more head-of-line blocking at HTTP level
- Binary framing replaces text-based HTTP/1.1 — more efficient parsing and smaller overhead
- Old optimization tricks (domain sharding, sprite sheets) are anti-patterns in HTTP/2

## Prerequisites
- [[Networking Fundamentals]]
- [[TCP/IP Basics]]

## Checklist
- [ ] Read up on binary framing, streams and multiplexing
- [ ] Understand HPACK header compression
- [ ] Compare HTTP/1.1 head-of-line blocking vs HTTP/2 using curl -v --http2
- [ ] Inspect HTTP/2 frames in Wireshark (or nghttp -v)

## Notes
