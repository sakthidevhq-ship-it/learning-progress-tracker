title:: Pipecat Evals: Replay and LLM Judge (Pipecat 1.13)
type:: docs
state:: collected
ingested:: [[2026-10-26]]
note:: Used as the reference design for the squadstack-bot pipeline-evals harness (PR #7222), 2026-10-26
domain:: [[ML/Evaluation]]
topic:: [[Voice Agent Evaluation]]
complexity:: intermediate
size:: medium
concepts:: [[LLM-as-a-Judge]], [[Conversation Replay]], [[Voice Agent Evaluation]]
prerequisites:: [[Voice Activity Detection]], [[LLM Basics]]

## Summary
Pipecat 1.13's evaluation framework for voice agents (https://github.com/pipecat-ai/pipecat). Scenarios carry plain-English `eval:` criteria; an LLM judge checks them live after each bot reply and again offline by replaying the recorded conversation with `pipecat eval judge`. Failures are reported as structured assertion failures with a reason.

## Key Takeaways
- The judge is two calls: a small fast classifier returns yes/no/continue, then a second LLM call writes the reason
- Offline re-judging a recorded conversation lets you change criteria without re-running the call
- Rule-based checks (counts, timings, text matches) and an LLM judge cover different things: behaviour contracts vs response quality

## Learnings
- 2026-10-26 · Pipecat's eval judge is an LLM that checks plain-English eval criteria after each bot reply (a fast yes/no/continue classifier, then a second call for the reason) and can re-judge a recorded conversation offline; our harness kept only rule-based checks on timings and counts, since response correctness is out of scope.
