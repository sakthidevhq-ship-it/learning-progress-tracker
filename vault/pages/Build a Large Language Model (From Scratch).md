title:: Build a Large Language Model (From Scratch)
type:: docs
domain:: [[ML/Foundations]]
topic:: [[Neural Networks]]
engagement:: implement
status:: unread
progress:: 0
complexity:: intermediate
size:: deep-dive
medium:: docs
prerequisites:: [[Neural Network Fundamentals]], [[Transformer Architecture]]
concepts:: [[Tokenization]], [[Self-Attention]], [[Transformer Architecture]], [[Pretraining]], [[Fine-Tuning]]
tags:: raschka, book
source:: https://www.manning.com/books/build-a-large-language-model-from-scratch
ingested:: [[2026-07-09]]
priority:: 30

## Summary
Sebastian Raschka's book walking through the full implementation of a GPT-style LLM in PyTorch, covering tokenization, attention, transformer blocks, pretraining, and fine-tuning for classification and instruction-following.

## Key Takeaways
- Implementing every component of a GPT model by hand — attention, layer norm, positional embeddings — builds far deeper understanding than using a library
- Pretraining and fine-tuning are treated as a continuum: the same architecture is reused across text generation, classification, and instruction-following tasks
- Small-scale from-scratch implementations reveal engineering details (masking, weight tying, data loading) that are often hidden by high-level frameworks

## Prerequisites
- [[Neural Network Fundamentals]]
- [[Transformer Architecture]]

## My Notes
