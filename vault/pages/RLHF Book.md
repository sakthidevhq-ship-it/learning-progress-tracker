title:: RLHF Book
type:: docs
domain:: [[ML/Foundations]]
topic:: [[RLHF]]
engagement:: read
status:: unread
progress:: 0
complexity:: advanced
size:: deep-dive
medium:: docs
prerequisites:: [[Reinforcement Learning Basics]], [[RLHF]]
concepts:: [[RLHF]], [[Reward Models]], [[PPO]], [[Direct Preference Optimization]], [[Post-Training]]
tags:: rlhf, dpo, book
source:: https://rlhfbook.com
ingested:: [[2026-07-09]]
priority:: 27

## Summary
Nathan Lambert's comprehensive book on reinforcement learning from human feedback, covering the full post-training pipeline: reward modeling, PPO, and Direct Preference Optimization as a simpler alternative.

## Key Takeaways
- Modern post-training pipelines chain SFT, reward modeling, and preference optimization rather than relying on a single technique
- DPO reframes the RLHF objective as a classification loss over preference pairs, avoiding the instability of PPO-based RL loops
- Reward model quality and preference data curation are often the limiting factor in alignment quality, not the optimization algorithm

## Prerequisites
- [[Reinforcement Learning Basics]]
- [[RLHF]]

## My Notes
