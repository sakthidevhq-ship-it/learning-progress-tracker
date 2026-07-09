title:: DSPy - Programming Language Models
type:: paper
domain:: [[ML/Frameworks]]
topic:: [[Prompt Engineering]]
engagement:: implement
status:: unread
progress:: 0
complexity:: intermediate
size:: deep-dive
medium:: paper
prerequisites:: [[LLM Basics]], [[Prompt Engineering Fundamentals]], [[Python]]
concepts:: [[Prompt Optimization]], [[Teleprompters]], [[LM Modules]], [[Chain of Thought]], [[ReAct Pattern]], [[Automated Prompt Tuning]]
tags:: dspy, stanford
source:: https://arxiv.org/abs/2310.03714
ingested:: [[2026-07-08]]
priority:: 39

## Summary
Stanford NLP's framework for algorithmically optimizing LM prompts and weights. Replaces hand-written prompts with declarative modules (ChainOfThought, ReAct, etc.) that are automatically compiled into optimized prompt chains or fine-tuning recipes. Introduces teleprompters for automated prompt optimization.

## Key Takeaways
- Declarative signatures replace fragile hand-written prompts
- Teleprompters automatically find optimal few-shot examples and instructions
- Modular composition of LM calls enables systematic optimization

## Prerequisites
- [[LLM Basics]]
- [[Prompt Engineering Fundamentals]]
- [[Python]]

## My Notes
