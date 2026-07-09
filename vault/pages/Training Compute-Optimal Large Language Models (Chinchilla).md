title:: Training Compute-Optimal Large Language Models (Chinchilla)
type:: paper
domain:: [[ML/Infrastructure]]
topic:: [[Scaling Laws]]
engagement:: read
status:: completed
progress:: 100
complexity:: advanced
size:: medium
medium:: paper
prerequisites:: [[LLM Basics]], [[Neural Network Fundamentals]]
concepts:: [[Scaling Laws]], [[Compute-Optimal Training]], [[LLM Basics]]
tags:: chinchilla, scaling
source:: https://arxiv.org/abs/2203.15556
ingested:: [[2026-07-09]]
priority:: 35

## Summary
The Chinchilla paper establishes revised scaling laws showing that most large language models of the time were significantly undertrained relative to their parameter count, and derives the compute-optimal trade-off between model size (N) and training tokens (D).

## Key Takeaways
- For a fixed compute budget, model size and training tokens should scale roughly equally — prior models like GPT-3 were far too large for their training data
- The Chinchilla-optimal 70B model, trained on 1.4T tokens, outperformed the much larger 280B-parameter Gopher
- Scaling laws provide a principled way to allocate a fixed compute budget before committing to an expensive training run

## Prerequisites
- [[LLM Basics]]
- [[Neural Network Fundamentals]]

## My Notes
