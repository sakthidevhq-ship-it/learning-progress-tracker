title:: Language Server Protocol — How It Works
type:: docs
domain:: [[Systems]]
topic:: [[Developer Tooling]]
engagement:: read
status:: unread
progress:: 0
complexity:: intermediate
size:: medium
medium:: docs
prerequisites:: [[Networking Fundamentals]], [[Data Structures]]
concepts:: [[Language Server Protocol]], [[JSON-RPC]], [[AST]], [[Editor Architecture]], [[Process Communication]], [[IPC]]
tags:: lsp, vscode, ide
source:: /private/tmp/lsp.md
ingested:: [[2026-07-09]]
priority:: 34

## Summary
Understanding LSP end-to-end: what a language server is, how editors launch and communicate with them (JSON-RPC over stdio/socket), what capabilities they provide (completion, diagnostics, go-to-definition, rename), how they parse and hold ASTs in memory, why they're the biggest memory consumers in any editor, and how to profile/debug them when they misbehave.

## Key Takeaways
- LSP decouples language intelligence from editors — one server works with VS Code, Neovim, Emacs
- Language servers hold parsed ASTs and type info in memory — they're often the biggest process in your editor
- Servers communicate via JSON-RPC over stdio or sockets — standard protocol, language-agnostic

## Prerequisites
- [[Networking Fundamentals]]
- [[Data Structures]]

## My Notes
