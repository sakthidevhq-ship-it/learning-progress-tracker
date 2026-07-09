title:: The Illustrated Transformer
type:: article
domain:: [[ML/Foundations]]
topic:: [[Model Architecture]]
engagement:: read
status:: unread
progress:: 0
complexity:: beginner
size:: quick-read
medium:: article
prerequisites:: [[Neural Network Fundamentals]], [[Linear Algebra Basics]]
concepts:: [[Self-Attention]], [[Multi-Head Attention]], [[Positional Encoding]], [[Transformer Architecture]]
tags:: transformers, visual
source:: https://jalammar.github.io/illustrated-transformer/
ingested:: [[2026-07-09]]
priority:: 36

## Summary
Jay Alammar's widely-used visual walkthrough of the Transformer architecture, breaking down self-attention, multi-head attention, positional encoding, and the encoder-decoder stack with intuitive diagrams.

## Key Takeaways
- Self-attention lets each token directly attend to every other token in a sequence, removing the sequential bottleneck of RNNs
- Multi-head attention runs several attention computations in parallel subspaces, letting the model capture different types of relationships
- Positional encodings are necessary because attention itself is permutation-invariant and has no inherent notion of token order

## Prerequisites
- [[Neural Network Fundamentals]]
- [[Linear Algebra Basics]]

## My Notes
