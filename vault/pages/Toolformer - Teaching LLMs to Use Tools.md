title:: Toolformer - Teaching LLMs to Use Tools
type:: paper
domain:: [[ML/Agents]]
topic:: [[Agentic Systems]]
engagement:: read
status:: unread
progress:: 0
complexity:: intermediate
size:: medium
medium:: paper
prerequisites:: [[LLM Basics]], [[Prompt Engineering Fundamentals]], [[ReAct Pattern]]
concepts:: [[Self-Supervised Tool Learning]], [[API Call Insertion]], [[Tool Selection]], [[Few-Shot Tool Use]]
tags:: toolformer, tool-use
source:: https://arxiv.org/abs/2305.10601
ingested:: [[2026-07-09]]
priority:: 41

## Summary
Meta's paper on training LLMs to autonomously decide when and how to use external tools (calculator, search, calendar, translator). Self-supervised approach: the model learns to insert API calls where they improve prediction.

## Key Takeaways
- Models can learn tool use in a self-supervised way without human annotation
- Tool calls are inserted where they reduce perplexity on future tokens
- The model learns WHEN to use tools, not just how — knowing when NOT to call is key

## Prerequisites
- [[LLM Basics]]
- [[Prompt Engineering Fundamentals]]
- [[ReAct Pattern]]

## My Notes
