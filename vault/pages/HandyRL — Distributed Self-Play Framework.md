title:: HandyRL — Distributed Self-Play Framework
type:: docs
domain:: [[Game AI]]
topic:: [[Self-Play Systems]]
engagement:: read
status:: unread
progress:: 0
complexity:: intermediate
size:: medium
medium:: docs
prerequisites:: [[Reinforcement Learning Basics]], [[Python]], [[Concurrency Basics]]
concepts:: [[Distributed Self-Play]], [[Experience Replay]], [[Centralized Training]], [[Parallel Rollouts]], [[Actor-Critic]]
tags:: handyrl, self-play
source:: https://github.com/DeNA/HandyRL
ingested:: [[2026-07-09]]
priority:: 30

## Summary
DeNA's framework for distributed reinforcement learning with self-play. Clean architecture for training game-playing agents across multiple workers. Key patterns: centralized training with distributed rollout workers, experience replay, and parallel environment stepping.

## Key Takeaways
- Centralized learner + distributed actors is the standard self-play architecture
- Experience replay buffers decouple data collection from training
- Config-driven agent definitions make experimentation fast

## Prerequisites
- [[Reinforcement Learning Basics]]
- [[Python]]
- [[Concurrency Basics]]

## My Notes
