title:: Moshi: A Speech-Text Foundation Model for Real-Time Dialogue
type:: paper
domain:: [[ML/Voice]]
topic:: [[Speech Models]]
engagement:: read
status:: completed
progress:: 100
complexity:: advanced
size:: deep-dive
medium:: paper
prerequisites:: [[Transformer Architecture]], [[LLM Basics]]
concepts:: [[Streaming Speech Models]], [[Neural Audio Codec]], [[Inner Monologue]], [[Transformer Architecture]]
tags:: moshi, voice
source:: https://arxiv.org/abs/2410.00037
ingested:: [[2026-07-09]]
priority:: 27

## Summary
The Moshi paper introduces a full-duplex spoken dialogue model that jointly models an inner text monologue alongside audio tokens from a neural codec, enabling low-latency, natural-sounding real-time conversation without a separate ASR/TTS pipeline.

## Key Takeaways
- Modeling a hidden text 'inner monologue' alongside audio tokens gives the model reasoning capacity without sacrificing speech-to-speech latency
- A full-duplex architecture lets the model listen and speak simultaneously, enabling natural interruption and backchannel behavior
- A codec backbone with hierarchical audio tokens (à la RVQ) is key to keeping sequence lengths tractable for real-time generation

## Prerequisites
- [[Transformer Architecture]]
- [[LLM Basics]]

## My Notes
