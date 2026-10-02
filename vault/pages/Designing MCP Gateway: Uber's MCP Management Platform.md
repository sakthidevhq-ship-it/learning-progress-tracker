title:: Designing MCP Gateway: Uber's MCP Management Platform
type:: tweet
state:: collected
source:: https://x.com/ubereng/status/2106071967619322330
ingested:: [[2026-10-03]]
domain:: [[ML/Agents]]
topic:: [[Agentic Systems]]
complexity:: intermediate
size:: medium
concepts:: [[Tool Use]], [[Agent Architecture]], [[Model Context Protocol]]
prerequisites:: [[Tool Use]]

## Summary
Uber Engineering on the gateway behind all MCP traffic at Uber: over 800 MCP servers and 5,000 tools. A registry (control plane) catalogues servers and tools; a proxy (data plane) translates MCP calls to HTTP, gRPC and TChannel and back. AutoCrawler, a Cadence workflow, scans the IDL registry, uses an LLM to write tool descriptions and registers tools disabled by default; native MCPFx servers are found via heartbeats.

## Key Takeaways
- Centralise MCP in a gateway instead of every team building its own integration
- Split a registry (discovery, ownership, enablement) from a proxy (protocol translation at runtime)
- Generate tools from existing IDLs automatically, with LLM-written descriptions, disabled by default
- One place for security and observability across agents
