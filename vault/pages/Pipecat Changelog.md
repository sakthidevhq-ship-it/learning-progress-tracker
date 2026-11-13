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
- 2026-11-02 · Pipecat 1.9 added speculative replies: the LLM can start answering before the turn is confirmed, so the turn-stop path now calls a new private _push_aggregation(run_llm=False) to write the user's words without re-running the LLM. The public push_aggregation() still exists, but a subclass that overrode it silently stopped being called on that path; overriding framework methods couples you to which internal path calls them.
- 2026-11-02 · Pipecat 1.12 swapped NLTK sentence splitting for sentencex to drop a heavy dependency (runtime punkt data downloads, scikit-learn/scipy imports, tokenizer warm-up), not to split better, so boundaries can differ. The way to find every difference is to replay a large sample of real bot text through both splitters offline and group the diffs by pattern, rather than fixing cases like a stray '? ?' one at a time.
- 2026-11-04 · Before 1.15, setting user_turn_strategies replaced the turn rules Deepgram Flux recommends, so filtering incomplete turns switched Flux turn detection off. 1.15 (PR #6346) adds stop_merge_mode=EXTEND to add rules on top, and stop_mode=ALL so a turn ends only when every stop rule agrees.
- 2026-11-06 · Pipecat parses the incomplete-turn markers (✓ ○ ◐) only in _push_llm_text(). Our LLM service overrides pushed LLMTextFrame straight to TTS and skipped the parser, so filter_incomplete silently did nothing until each push went through _push_llm_text (#7377).
- 2026-11-06 · Agreeing with NLTK doesn't prove sentencex splits correctly: only 78 of 8,067 real bot messages (~1%) split differently. Proving it needs hand-labelled boundaries on those disagreements plus a control set where both agree, scored for wrong splits (choppy speech) and missed splits (later audio).
- 2026-11-11 · A tool call arrives in the same LLM stream as text: deltas carry either content or tool_calls fragments (id and name first, then the arguments JSON in pieces), and the stream ends with finish_reason=tool_calls. Text goes to TTS as it streams; tool calls are buffered until the stream ends, run, the result replaces an IN_PROGRESS placeholder in the context, and a second LLM request turns it into speech.
- 2026-11-11 · On barge-in during a tool call, INLINE awaits the tool inside the LLM task, so the interruption cancels it: the context records CANCELLED and one LLM request follows the caller's turn. SURVIVE_BARGE_IN only stops the speech and lets the tool run on; if the tool finishes while the caller is still talking, its result waits in the context and goes out in the same single request as their words.
- 2026-11-12 · Pipecat 1.15's ClassifierUserTurnStopStrategy (Jev, OpenAI, generic LLM or Cloudflare classifier) does nothing in a FIRST-mode stop list: the first strategy to decide ends the turn, a 0.15 s parity timer almost always beats the classifier's network round trip, so its short and long holds never apply. In FIRST mode it can only end a turn sooner, never hold it open.
- 2026-11-13 · ClassifierUserTurnStopStrategy gives the same three verdicts as filter_incomplete's markers (complete, short-incomplete, long-incomplete), but a separate classifier decides them at each pause with new words, outside the main LLM: nothing is added to the reply prompt, so there are no glyphs to strip and none can leak into TTS.
