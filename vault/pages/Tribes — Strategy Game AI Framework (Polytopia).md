title:: Tribes — Strategy Game AI Framework (Polytopia)
type:: docs
domain:: [[Game AI]]
topic:: [[Strategy Game AI]]
engagement:: implement
status:: unread
progress:: 0
complexity:: intermediate
size:: deep-dive
medium:: docs
prerequisites:: [[Monte Carlo Tree Search]], [[Game Theory Basics]], [[Java Basics]]
concepts:: [[Forward Model Simulation]], [[Rolling Horizon Evolution]], [[Statistical Forward Planning]], [[4X Game AI]], [[Branching Factor Management]], [[Tech Tree Decisions]]
tags:: tribes, polytopia, mcts, framework
source:: https://github.com/GAIGResearch/Tribes
ingested:: [[2026-08-04]]
priority:: 30

## Summary
Exploration of GAIG Research's open-source Java re-implementation of The Battle of Polytopia as an AI research framework. A full 4X-lite strategy environment — tech trees, city management, unit combat, fog of war — with a fast forward model built for statistical forward planning agents. Ships baseline agents (MCTS, Rolling Horizon Evolutionary Algorithms, OSLA, rule-based) and supports multi-player games, making it a testbed for long-horizon planning, sparse rewards, and large branching factors that board-game AI methods struggle with.

## Key Takeaways
- Strategy games have branching factors that dwarf Go — per-turn action spaces explode combinatorially with unit count
- A fast forward model is the enabling asset: MCTS/RHEA agents are only as good as simulations-per-second
- RHEA (evolving action sequences) competes with MCTS when the horizon is long and rollouts are expensive
- Tech-tree decisions are the in-game version of your learning tracker's prerequisite graph — long-term investment under uncertainty

## Prerequisites
- [[Monte Carlo Tree Search]]
- [[Game Theory Basics]]
- [[Java Basics]]

## My Notes
