title:: Nearfield: Real-Time Caller Voice Isolation
type:: docs
state:: collected
source:: https://github.com/Ground-State-Foundry/nearfield
ingested:: [[2026-11-14]]
note:: Evaluated 2026-11-14 against Krisp and raw audio on 8 kHz IndiaMART calls: cuts false barge-ins but VAD misses about twice as many replies and Soniox accuracy drops.
domain:: [[ML/Voice]]
topic:: [[Voice Activity]]
complexity:: intermediate
size:: quick-read
concepts:: [[Speech Enhancement]], [[Voice Activity Detection]]
prerequisites:: [[Streaming Speech Models]]

## Summary
An open-source, CPU real-time model (2.5 MB ONNX, 16 kHz) that keeps the voice close to the microphone and removes noise and background talkers, shipped as a Pipecat audio filter. v2 separates the two voices instead of v1's per-band gain, with a fast (48 ms) and best (80 ms) model and a clean-up stage (AGC, blip removal, pause gate).

## Key Takeaways
- v1 gated 32 frequency bands every 10 ms, which fails when a background talker shares the caller's bands; v2 separates voices
- Phone audio at 8 kHz is resampled to 16 kHz and back
- Any pre-VAD filter trades false barge-ins for missed quiet replies; measure both

## Learnings
- 2026-11-14 · On 281 audited 8 kHz replies at prod VAD settings, noise suppression before VAD nearly removes VAD starts during bot speech (18 to 3 with Krisp, 0 with Nearfield fast) but almost doubles the replies VAD misses (25 to 46-48), and lowers Soniox accuracy (Krisp about -5.5 points, Nearfield -9 to -13). Nearfield sometimes deletes the caller outright: 9 replies got no transcript.
