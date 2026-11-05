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
- 2026-10-28 · A turn ends whichever way fires first: VAD stop after 0.5 s of quiet (a final arriving within the next 0.15 s still joins the turn), the STT final when VAD missed the speech (the bot answers ~0.17 s later, but two finals 0.4 s apart split one sentence into two turns), or a 2 s backstop when no final arrives, which can race the STT client's own 2 s finalize retry.
- 2026-11-04 · Prod runs Silero v6.0 (bundled in pipecat 1.6 and 1.12) and our flag loads v6.2; the jump I remembered as v4 to v6 was really v5.1.2 to v6.0. 6.2 published no metrics: its claimed gains are on low-quality phone calls and unusual voices, which our eval corpus barely covers.
- 2026-11-04 · Pipecat 1.12's rolling 400 ms volume doesn't favour v6.2 on the user and initial gates (same gap as on 1.6). Only on the barge-in gate, where volume used to decide alone, does 6.2 now fire where v6.0 misses.
