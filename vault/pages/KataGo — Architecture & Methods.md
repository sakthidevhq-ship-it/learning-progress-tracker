title:: KataGo — Architecture & Methods
type:: docs
domain:: [[Game AI]]
topic:: [[Self-Play Systems]]
engagement:: read
status:: unread
progress:: 0
complexity:: advanced
size:: deep-dive
medium:: docs
prerequisites:: [[Reinforcement Learning Basics]], [[Neural Network Fundamentals]], [[Game Theory Basics]]
concepts:: [[Monte Carlo Tree Search]], [[Auxiliary Training Targets]], [[Ownership Prediction]], [[Playout Cap Randomization]], [[Self-Play Efficiency]]
tags:: katago, go
source:: https://github.com/lightvector/KataGo
ingested:: [[2026-07-09]]
priority:: 28

## Summary
Deep dive into KataGo, one of the strongest open-source Go engines. The KataGoMethods.md document explains innovations: auxiliary policy targets, ownership prediction, dynamic komi, playout cap randomization. Achieves superhuman play with 50x less compute than AlphaZero.

## Key Takeaways
- Auxiliary targets (ownership, score) dramatically improve training efficiency
- Playout cap randomization prevents the engine from over-relying on search depth
- 50x less compute than AlphaZero through better training techniques, not bigger models

## Prerequisites
- [[Reinforcement Learning Basics]]
- [[Neural Network Fundamentals]]
- [[Game Theory Basics]]

## My Notes
