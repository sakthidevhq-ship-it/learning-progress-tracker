title:: Distil-Whisper: Robust Knowledge Distillation for Fast Speech Recognition
type:: paper
domain:: [[ML/Voice]]
topic:: [[ASR]]
engagement:: read
status:: unread
progress:: 0
complexity:: intermediate
size:: medium
medium:: paper
prerequisites:: [[Neural Network Fundamentals]], [[Transformer Architecture]]
concepts:: [[Knowledge Distillation]], [[Streaming ASR]], [[Chunked Inference]]
tags:: whisper, streaming
source:: https://arxiv.org/abs/2311.01899
ingested:: [[2026-07-09]]
priority:: 29

## Summary
Distil-Whisper distills OpenAI's Whisper into a smaller model that runs significantly faster with minimal accuracy loss, and explores chunked inference strategies for streaming ASR with favorable latency-accuracy tradeoffs.

## Key Takeaways
- Distillation transfers Whisper's transcription ability to a much smaller student model, achieving 6x faster inference with comparable word error rate
- Chunked inference splits long audio into overlapping segments, trading a small accuracy cost for the ability to stream partial transcripts
- Latency-accuracy tradeoffs in streaming ASR are tunable via chunk size, making the same model adaptable to different real-time constraints

## Prerequisites
- [[Neural Network Fundamentals]]
- [[Transformer Architecture]]

## My Notes
