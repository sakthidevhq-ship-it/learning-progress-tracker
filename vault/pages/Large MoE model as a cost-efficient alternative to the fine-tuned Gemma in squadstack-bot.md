title:: Large MoE model as a cost-efficient alternative to the fine-tuned Gemma in squadstack-bot
type:: project
state:: collected
ingested:: [[2026-11-23]]
note:: Explore whether a large mixture-of-experts model, run in a cost efficient way, could replace the current LLM (a fine-tuned Gemma) in squadstack-bot. Idea from 23 Nov 2026; source session: https://claude.ai/code/cshk_01Tmz1bGX69NBHGfxUZriWz5JtoX9zzcPaCCDxgyhgy2nM
domain:: [[ML/Infrastructure]]
topic:: [[Inference Optimization]]
complexity:: advanced
size:: deep-dive
concepts:: [[Mixture of Experts]], [[Expert Caching]], [[Inference Cost]]
prerequisites:: [[Mixture of Experts]]

## Summary
Idea only, nothing explored yet. Explore whether a large mixture-of-experts model, run in a cost efficient way, could replace the current LLM (a fine-tuned Gemma) in squadstack-bot. Builds on the MoE Expert Offloading Bench project.

## Key Takeaways
- A MoE model uses only a few experts per token and usage is skewed (gpt-oss-20b at a 4 GB cap: the most used quarter of experts covers 67% of picks), so the memory that must be fast can be much smaller than the model. Not yet checked against squadstack-bot's needs.
- The laptop measurements are 1 to 12 tokens/sec on a CPU; a production bot needs its own targets (time to first token, tokens/sec, concurrent calls, cost per call) before this can be judged.

## Checklist
- [ ] Find out what the fine-tuned Gemma costs and how fast it is today
- [ ] Set targets: time to first token, tokens/sec, concurrent calls, cost per call
- [ ] Check whether a general MoE model matches the fine-tuned Gemma's quality without fine-tuning
- [ ] Check whether hidden reasoning tokens (gpt-oss writes them before answering) are acceptable for latency

## Learnings
- 2026-11-23 · Our Gemma workload is prefill, not generation: ~34K-token prompts (89% cached, ~94% on the first request), ~35 output tokens, 6.4 LLM requests per call-minute, with the LLM busy only ~6% of call time. Compute per prompt token is about 2 × the parameters used per token, so a large MoE can do less work than dense Gemma 4 31B (DeepSeek V4.1 Flash uses ~8B per prompt token, ~4× less). The catch is that one copy needs 4–8 GPUs, so it only gets cheap with many concurrent calls per copy.
- 2026-11-23 · Measured baseline to beat: maya (Gemma 4 31B FP8, one GPU per copy) generates ~100 tok/s with 122 ms median TTFT on Pipeshift H200, and ~290 tok/s on Simplismart. Cheap API prices for big MoEs (e.g. OpenCode's 60% off GLM 5.3 and V4.1 Flash) are a funded promotion, not a serving-cost signal, and at list prices our call pattern costs about the same as running a GPU server.
