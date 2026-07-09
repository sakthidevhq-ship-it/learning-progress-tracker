title:: Build a Reasoning Model (From Scratch)
type:: docs
domain:: [[ML/Infrastructure]]
topic:: [[Model Architecture]]
engagement:: implement
status:: unread
progress:: 0
complexity:: advanced
size:: deep-dive
medium:: docs
prerequisites:: [[LLM Basics]], [[Reinforcement Learning Basics]], [[Transformer Architecture]]
concepts:: [[Chain-of-Thought]], [[Reinforcement Learning Basics]], [[LLM Basics]], [[Transformer Architecture]]
tags:: raschka, reasoning
source:: https://www.manning.com/books/build-a-reasoning-model-from-scratch
ingested:: [[2026-07-09]]
priority:: 40

## Summary
Sebastian Raschka's follow-up book focused on implementing reasoning-capable language models from scratch, covering techniques like chain-of-thought training, reinforcement learning for reasoning, and inference-time compute scaling.

## Key Takeaways
- Reasoning capability can be induced post-hoc through targeted fine-tuning and RL rather than requiring architectural changes
- Inference-time compute scaling (longer chains of thought, sampling multiple paths) trades latency for improved answer quality
- Building a reasoning pipeline from scratch clarifies how reward signals for correctness propagate back into changes in model behavior

## Prerequisites
- [[LLM Basics]]
- [[Reinforcement Learning Basics]]
- [[Transformer Architecture]]

## My Notes
