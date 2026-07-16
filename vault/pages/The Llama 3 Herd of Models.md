title:: The Llama 3 Herd of Models
type:: paper
domain:: [[ML/Infrastructure]]
topic:: [[Training Optimization]]
engagement:: read
status:: unread
progress:: 0
complexity:: advanced
size:: deep-dive
medium:: paper
prerequisites:: [[LLM Basics]], [[RLHF]]
concepts:: [[Post-Training]], [[Direct Preference Optimization]], [[Supervised Fine-Tuning]], [[LLM Basics]]
tags:: llama3, post-training
source:: https://arxiv.org/abs/2407.21783
ingested:: [[2026-07-09]]
priority:: 34

## Summary
Meta's Llama 3.1 paper details the full training recipe for the Llama 3 herd, including pretraining data curation, architecture choices, and a multi-stage post-training pipeline combining supervised fine-tuning, rejection sampling, and DPO.

## Key Takeaways
- The Llama 3.1 post-training pipeline iterates SFT, rejection sampling, and DPO across multiple rounds rather than a single alignment pass
- Rejection sampling with a reward model generates high-quality SFT data by sampling many completions and keeping the best
- Data quality and iterative refinement of the training recipe mattered as much as scale for the final model's capabilities

## Prerequisites
- [[LLM Basics]]
- [[RLHF]]

## My Notes
