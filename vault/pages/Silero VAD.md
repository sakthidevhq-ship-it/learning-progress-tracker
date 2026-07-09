title:: Silero VAD
type:: docs
domain:: [[ML/Voice]]
topic:: [[Voice Activity]]
engagement:: implement
status:: unread
progress:: 0
complexity:: beginner
size:: quick-read
medium:: docs
prerequisites:: [[Neural Network Fundamentals]]
concepts:: [[Voice Activity Detection]], [[Endpointing]], [[Barge-in Detection]]
tags:: vad, endpointing
source:: https://github.com/snakers4/silero-vad
ingested:: [[2026-07-09]]
priority:: 31

## Summary
Documentation and code for Silero VAD, a lightweight, pre-trained voice activity detection model used for endpointing and barge-in detection in real-time speech applications.

## Key Takeaways
- Silero VAD runs in real time on CPU, making it practical for on-device or low-latency streaming pipelines
- Accurate endpointing is critical for conversational latency — waiting too long to detect end-of-speech directly adds to perceived response time
- Barge-in detection (recognizing when a user interrupts) requires VAD to run continuously even while the system is speaking

## Prerequisites
- [[Neural Network Fundamentals]]

## My Notes
