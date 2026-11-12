title:: Soniox Endpoint Detection
type:: docs
state:: collected
source:: https://docs.soniox.com/stt/rt/endpoint-detection
ingested:: [[2026-11-05]]
note:: Came up tuning Soniox endpointing vs Silero VAD on 8 kHz calls (Nov 4-5): Soniox's suggested 1500/0.3/level 2, v6 agent text input
domain:: [[ML/Voice]]
topic:: [[Voice Activity]]
complexity:: intermediate
size:: quick-read
concepts:: [[Endpointing]], [[Voice Activity Detection]]
prerequisites:: [[Streaming Speech Models]]

## Summary
Soniox's real-time API does semantic endpointing: the speech model uses pauses, intonation and context to decide an utterance is over, finalizes the segment and emits an <end> token. Earlier endpoints cut latency but give the model less time to revise words and split long speech into more segments. Tuning knobs include endpoint latency level, sensitivity and a maximum endpoint delay; manual finalization (<fin>) and agent text input sit alongside it.

## Key Takeaways
- <end> means Soniox's own endpoint fired; <fin> answers a finalize request you sent
- Aggressive endpointing trades word accuracy and turn splits for latency
- Endpointing also lowers diarization accuracy
- Tune for the application instead of picking the lowest latency

## Learnings
- 2026-11-04 · A turn can open and close without VAD: a background 'बंद कर' never tripped Silero, but Soniox's endpoint final (<end>, speech_final) opened the turn through the short-utterance start strategy and a 150 ms timer closed it. With endpoint detection off, Arc emits no final and that phrase never becomes a turn.
- 2026-11-04 · On Soniox v6 the setting that moves accuracy is agent text input (sending the bot's spoken words): 66% to 71%, 72.5% with context, on 274 audited prod replies. Endpoint knobs barely change accuracy, and VAD-only loses about 8% of turns.
- 2026-11-05 · Soniox says use VAD or endpointing, not both, at latency level 2 and sensitivity 0.3. Prod data says keep both and raise max_endpoint_delay from 800 to 1500 ms: Soniox alone ends about 10% of turns that VAD never heard (including wrongful hang-ups on lone low-confidence words), and 26% of its endpoints are followed by more caller speech within 1 s.
- 2026-11-12 · Soniox agent text rides the same single stream as the caller's audio for the whole call: words go in as agent_text frames, each bot turn is closed with end_of_segment, and nothing is re-sent on later turns. The frames carry no timestamps; Soniox places each one at the point in the audio where it arrives, and its docs ask for each piece 500 ms to 1 s before playback, following playback rather than TTS output.
