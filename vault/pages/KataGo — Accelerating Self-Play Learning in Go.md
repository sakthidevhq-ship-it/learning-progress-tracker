title:: KataGo — Accelerating Self-Play Learning in Go
type:: paper
domain:: [[Game AI]]
topic:: [[Self-Play Systems]]
engagement:: read
status:: unread
progress:: 0
complexity:: advanced
size:: medium
medium:: paper
prerequisites:: [[Reinforcement Learning Basics]], [[Neural Network Fundamentals]], [[Monte Carlo Tree Search]]
concepts:: [[Self-Play Acceleration]], [[Auxiliary Training Targets]], [[Data Augmentation]], [[Training Efficiency]]
tags:: katago, paper
source:: https://arxiv.org/abs/1902.10565
ingested:: [[2026-07-09]]
priority:: 28

## Summary
The paper behind KataGo's training innovations. Shows how auxiliary training targets, game outcome prediction, and various data augmentation techniques can accelerate self-play training by 50x compared to AlphaZero-style approaches.

## Key Takeaways
- Predicting ownership maps as auxiliary targets teaches the network spatial reasoning faster
- Game sampling and position augmentation multiply effective training data
- Efficiency gains compound — each technique contributes independently

## Prerequisites
- [[Reinforcement Learning Basics]]
- [[Neural Network Fundamentals]]
- [[Monte Carlo Tree Search]]

## My Notes
