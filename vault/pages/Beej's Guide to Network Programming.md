title:: Beej's Guide to Network Programming
type:: docs
domain:: [[Networking]]
topic:: [[Socket Programming]]
engagement:: implement
status:: unread
progress:: 0
complexity:: intermediate
size:: medium
medium:: docs
prerequisites:: [[C Basics]], [[Networking Fundamentals]], [[TCP/IP Basics]]
concepts:: [[Socket API]], [[TCP/UDP]], [[select/poll/epoll]], [[Non-Blocking IO]], [[Client-Server Architecture]]
tags:: sockets, beej
source:: https://beej.us/guide/bgnet/
ingested:: [[2026-07-09]]
priority:: 28

## Summary
The classic guide to Unix network programming with sockets. Covers socket API, TCP/UDP, client-server architecture, select/poll/epoll, non-blocking I/O, and building a simple HTTP server. Practical C code throughout.

## Key Takeaways
- Sockets abstract network communication to file descriptor read/write
- select() is portable but slow at scale — epoll/kqueue are the modern choice
- Non-blocking I/O with event loops is the foundation of all high-perf servers

## Prerequisites
- [[C Basics]]
- [[Networking Fundamentals]]
- [[TCP/IP Basics]]

## My Notes
