title:: Physics of Language Models: Knowledge Storage and Extraction
type:: paper
domain:: [[ML/Infrastructure]]
topic:: [[Model Architecture]]
engagement:: read
status:: unread
progress:: 0
complexity:: advanced
size:: medium
medium:: paper
prerequisites:: [[Transformer Architecture]], [[LLM Basics]]
concepts:: [[Mechanistic Interpretability]], [[Knowledge Storage]], [[Transformer Architecture]]
tags:: knowledge, internals
source:: https://arxiv.org/abs/2309.14316
ingested:: [[2026-07-09]]
priority:: 38

## Summary
Part of the Physics of Language Models series, this work uses controlled synthetic experiments to study how transformer language models internally store and retrieve factual knowledge, revealing structure behind memorization and generalization.

## Key Takeaways
- Controlled synthetic pretraining setups allow precise measurement of how and when models memorize versus generalize facts
- The way knowledge is represented internally affects how reliably it can later be extracted via prompting or fine-tuning
- Data augmentation during pretraining (e.g., paraphrased facts) significantly improves a model's ability to flexibly retrieve stored knowledge

## Prerequisites
- [[Transformer Architecture]]
- [[LLM Basics]]

## My Notes
