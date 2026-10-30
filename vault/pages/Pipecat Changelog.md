title:: Pipecat Changelog
type:: docs
state:: collected
source:: https://github.com/pipecat-ai/pipecat/blob/main/CHANGELOG.md
ingested:: [[2026-10-27]]
note:: Used to summarise the Pipecat 1.6.0 → 1.12.0 upgrade for squadstack-bot (#7139), 2026-10-27
domain:: [[ML/Voice]]
topic:: [[Voice Agent Frameworks]]
complexity:: intermediate
size:: medium
concepts:: [[Pipeline Lifecycle]], [[Voice Agent Evaluation]]
prerequisites:: [[Voice Activity Detection]]

## Summary
The release notes for Pipecat, the open-source Python framework for real-time voice agents. Each release lists Added, Changed, Deprecated, Removed and Fixed entries; it's the source to read before an upgrade to see what changes how a pipeline starts, stops, fails and which defaults moved.

## Key Takeaways
- 1.8.0 is the big lifecycle release: services connect during setup in parallel, frames are held until the start signal reaches each processor, and teardown runs in parallel
- Later 1.x releases mostly change defaults and swap dependencies, which can shift behaviour without any code change on your side

## Learnings
- 2026-10-27 · In Pipecat 1.8.0 services connect while the pipeline is being set up, in parallel, so startup costs as much as the slowest service instead of the sum; a setup step over 20 s now silently ends the pipeline, and teardown also runs in parallel, so custom early-connect and cleanup overrides break.
- 2026-10-30 · Pipecat observers used to hear the same frame once per processor it passed through, so ten built-in observers each kept a set of seen frame IDs that grew for the whole session (~8-40 MB/hour). pipecat#5908 (1.9) makes WorkerObserver mark a frame's first push (FramePushed.first_push, or observe_every_push=False), so observers keep no IDs and pipelines ran 17-19% faster; any custom observer relying on the old repeats can break.
- 2026-10-30 · Since pipecat#5232 (1.8.0) VAD volume is the loudness of a rolling 400 ms window kept by the VAD class, not of each 32 ms frame on its own, and calculate_audio_volume now raises 'audio too short' on less than 400 ms of audio, which crashes code that called it per frame.
