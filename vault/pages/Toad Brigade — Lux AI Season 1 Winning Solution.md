title:: Toad Brigade — Lux AI Season 1 Winning Solution
type:: article
domain:: [[Game AI]]
topic:: [[Competition Strategy]]
engagement:: read
status:: unread
progress:: 0
complexity:: intermediate
size:: medium
medium:: article
prerequisites:: [[Reinforcement Learning Basics]], [[Neural Network Fundamentals]]
concepts:: [[Imitation Learning]], [[Leaderboard Mining]], [[Self-Play Fine-Tuning]], [[Behavioral Cloning]]
tags:: lux-ai, imitation-learning
source:: https://kaggle.com/lux-ai-toad-brigade
ingested:: [[2026-07-09]]
priority:: 30

## Summary
Writeup of the winning Lux AI strategy using imitation learning from leaderboard replays. Instead of training from scratch, they learned to imitate the best bots on the leaderboard, then fine-tuned with self-play.

## Key Takeaways
- Imitating top leaderboard bots bootstraps learning faster than random self-play
- Behavioral cloning from replays + self-play fine-tuning is a powerful combo
- The leaderboard itself is a dataset — mine it

## Prerequisites
- [[Reinforcement Learning Basics]]
- [[Neural Network Fundamentals]]

## My Notes
