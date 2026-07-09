title:: Llama 2 Technical Report
type:: paper
domain:: [[ML/Infrastructure]]
topic:: [[Model Architecture]]
engagement:: read
status:: unread
progress:: 0
complexity:: advanced
size:: deep-dive
medium:: paper
prerequisites:: [[Transformer Architecture]], [[Attention Mechanisms]], [[Reinforcement Learning Basics]]
concepts:: [[Grouped Query Attention]], [[RLHF]], [[Ghost Attention]], [[Rejection Sampling]], [[Safety Evaluation]], [[SFT]]
tags:: llama2, meta
source:: https://arxiv.org/abs/2307.09288
ingested:: [[2026-07-09]]
priority:: 38

## Summary
Meta's technical report on Llama 2, covering pretraining at scale, supervised fine-tuning, RLHF with rejection sampling, Ghost Attention for multi-turn consistency, and safety evaluation. Trained on 2T tokens with context length of 4096.

## Key Takeaways
- RLHF with rejection sampling outperforms standard PPO
- Ghost Attention maintains system prompt adherence across turns
- Grouped Query Attention reduces KV cache by 8x vs multi-head

## Prerequisites
- [[Transformer Architecture]]
- [[Attention Mechanisms]]
- [[Reinforcement Learning Basics]]

## My Notes
