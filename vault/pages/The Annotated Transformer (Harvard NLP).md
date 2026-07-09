title:: The Annotated Transformer (Harvard NLP)
type:: article
domain:: [[ML/Foundations]]
topic:: [[Model Architecture]]
engagement:: implement
status:: unread
progress:: 0
complexity:: intermediate
size:: deep-dive
medium:: article
prerequisites:: [[Self-Attention]], [[Neural Network Fundamentals]], [[Linear Algebra Basics]], [[Python]]
concepts:: [[Transformer Architecture]], [[Multi-Head Attention]], [[Positional Encoding]], [[Masking]], [[Label Smoothing]], [[Encoder-Decoder]], [[Layer Normalization]]
tags:: transformers, annotated, pytorch
source:: https://nlp.seas.harvard.edu/2018/04/03/attention.html
ingested:: [[2026-07-09]]
priority:: 34

## Summary
A line-by-line PyTorch implementation of 'Attention Is All You Need', annotated with explanations. Covers the full architecture: multi-head attention, positional encoding, encoder/decoder stacks, masking, label smoothing, and training loop. The definitive code companion to the original paper.

## Key Takeaways
- The full Transformer can be implemented in ~400 lines of PyTorch
- Masking prevents the decoder from attending to future positions
- Label smoothing trades a small amount of perplexity for better BLEU scores

## Prerequisites
- [[Self-Attention]]
- [[Neural Network Fundamentals]]
- [[Linear Algebra Basics]]
- [[Python]]

## My Notes
