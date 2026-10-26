title:: Silero VAD
type:: docs
domain:: [[ML/Voice]]
topic:: [[Voice Activity]]
engagement:: implement
complexity:: beginner
size:: quick-read
medium:: docs
prerequisites:: [[Neural Network Fundamentals]]
concepts:: [[Voice Activity Detection]], [[Endpointing]], [[Barge-in Detection]]
tags:: vad, endpointing
source:: https://github.com/snakers4/silero-vad
ingested:: [[2026-07-09]]
state:: collected

## Summary
Documentation and code for Silero VAD, a lightweight, pre-trained voice activity detection model used for endpointing and barge-in detection in real-time speech applications.

## Key Takeaways
- Silero VAD runs in real time on CPU, making it practical for on-device or low-latency streaming pipelines
- Accurate endpointing is critical for conversational latency — waiting too long to detect end-of-speech directly adds to perceived response time
- Barge-in detection (recognizing when a user interrupts) requires VAD to run continuously even while the system is speaking

## Prerequisites
- [[Neural Network Fundamentals]]

## Notes

## Learnings
- 2026-10-26 · Running Silero at 16 kHz on 8 kHz call audio doesn't just halve how often it runs: each 512-sample window spans 64 ms, so window-counted start/stop thresholds double (0.5 s stop becomes ~1 s), and the model hears speech at double speed an octave up, so confidence collapses (22 of 23 Hindi clips never fired). That was the silent 1.6.0 canary regression.
- 2026-10-26 · Evals should be a behaviour contract per component: keep a baseline of how VAD (or STT, LLM, TTS) behaves on fixed inputs and flag meaningful drift; black-box timing bounds (100-300 ms of slack) and clean -16 LUFS clips only catch outright failure, not a VAD that got a few frames worse.
