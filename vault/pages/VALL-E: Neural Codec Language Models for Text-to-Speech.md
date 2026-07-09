title:: VALL-E: Neural Codec Language Models for Text-to-Speech
type:: paper
domain:: [[ML/Voice]]
topic:: [[Speech Synthesis]]
engagement:: read
status:: unread
progress:: 0
complexity:: advanced
size:: medium
medium:: paper
prerequisites:: [[Transformer Architecture]], [[LLM Basics]]
concepts:: [[Neural Audio Codec]], [[Zero-Shot Voice Cloning]], [[LLM Basics]]
tags:: vall-e, tts
source:: https://arxiv.org/abs/2301.02111
ingested:: [[2026-07-09]]
priority:: 27

## Summary
VALL-E treats text-to-speech as a conditional language modeling problem over discrete neural codec tokens, enabling zero-shot voice cloning from a short audio prompt without speaker-specific fine-tuning.

## Key Takeaways
- Framing TTS as next-token prediction over codec tokens lets it inherit in-context learning behavior from language modeling, enabling zero-shot cloning
- A short 3-second audio prompt is sufficient to condition the model on a target speaker's voice and acoustic environment
- Discretizing audio via a neural codec is what makes standard autoregressive LM architectures directly applicable to speech generation

## Prerequisites
- [[Transformer Architecture]]
- [[LLM Basics]]

## My Notes
