title:: Retrieval-Augmented Generation Approaches
type:: docs
domain:: [[ML/Frameworks]]
topic:: [[RAG]]
engagement:: implement
status:: unread
progress:: 0
complexity:: intermediate
size:: medium
medium:: docs
prerequisites:: [[LLM Basics]], [[Prompt Engineering Fundamentals]]
concepts:: [[Retrieval Augmented Generation]], [[Vector Search]], [[Chunking Strategies]], [[Prompt Engineering Fundamentals]]
tags:: rag, retrieval
source:: https://github.com/ml-curriculum/rag-approaches
ingested:: [[2026-07-09]]
priority:: 35

## Summary
A survey of RAG architectural patterns for grounding LLM outputs in external knowledge, covering retriever design, chunking strategies, and approaches for combining retrieval with generation.

## Key Takeaways
- RAG separates parametric knowledge (in model weights) from non-parametric knowledge (in a retrievable index), enabling cheap knowledge updates
- Chunking and embedding quality often matter more to end-to-end RAG performance than the choice of generator model
- Naive top-k retrieval can be improved substantially with re-ranking, query rewriting, and hybrid sparse/dense search

## Prerequisites
- [[LLM Basics]]
- [[Prompt Engineering Fundamentals]]

## My Notes
