title:: Direct Preference Optimization: Your Language Model is Secretly a Reward Model
type:: paper
domain:: [[ML/Foundations]]
topic:: [[RLHF]]
engagement:: read
status:: unread
progress:: 0
complexity:: advanced
size:: medium
medium:: paper
prerequisites:: [[RLHF]], [[Reinforcement Learning Basics]]
concepts:: [[Direct Preference Optimization]], [[RLHF]], [[Reward Models]]
tags:: dpo
source:: https://arxiv.org/abs/2305.18290
ingested:: [[2026-07-09]]
priority:: 27

## Summary
The DPO paper shows that the RLHF objective can be reformulated as a simple classification loss directly over a language model's policy, eliminating the need for a separate reward model and unstable RL training like PPO.

## Key Takeaways
- DPO derives a closed-form relationship between the optimal RLHF policy and a reward function, letting preference data train the policy directly
- Removing the separate reward model and PPO loop makes preference tuning far more stable and easier to implement
- DPO matches or exceeds PPO-based RLHF on tasks like summarization and sentiment control while being simpler to tune

## Prerequisites
- [[RLHF]]
- [[Reinforcement Learning Basics]]

## My Notes
