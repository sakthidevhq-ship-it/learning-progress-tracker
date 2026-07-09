title:: SoundStorm: Efficient Parallel Audio Generation
type:: paper
domain:: [[ML/Voice]]
topic:: [[Speech Synthesis]]
engagement:: read
status:: unread
progress:: 0
complexity:: advanced
size:: medium
medium:: paper
prerequisites:: [[Transformer Architecture]], [[Neural Network Fundamentals]]
concepts:: [[Non-Autoregressive Generation]], [[Neural Audio Codec]], [[Parallel Decoding]]
tags:: soundstorm, tts
source:: https://arxiv.org/abs/2305.09636
ingested:: [[2026-07-09]]
priority:: 26

## Summary
SoundStorm introduces a non-autoregressive, parallel decoding scheme for generating audio tokens from a neural codec, using an iterative masked-token approach that produces long-form audio far faster than autoregressive TTS models.

## Key Takeaways
- Parallel, iterative mask-and-predict decoding (borrowed from MaskGIT) generates audio tokens far faster than autoregressive sampling
- Coarse-to-fine generation over hierarchical codec tokens preserves audio quality while enabling parallelism
- SoundStorm can generate 30 seconds of audio in under 2 seconds on a TPU, making it practical for real-time TTS pipelines

## Prerequisites
- [[Transformer Architecture]]
- [[Neural Network Fundamentals]]

## My Notes
