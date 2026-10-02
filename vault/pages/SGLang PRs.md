title:: SGLang PRs
type:: project
state:: collected
source:: https://github.com/sgl-project/sglang
ingested:: [[2026-10-03]]
note:: SGLang PRs: after vLLM (see the GPU kernels & inference roadmap).
domain:: [[ML/Infrastructure]]
topic:: [[LLM Serving]]
complexity:: advanced
size:: deep-dive
concepts:: [[RadixAttention]], [[Prefix Caching]], [[KV Cache]], [[Continuous Batching]]
prerequisites:: [[LLM Basics]], [[Python]]

## Summary
Contribute to SGLang, the other big open-source LLM serving engine. It uses Triton for RadixAttention and is getting active AMD upstreaming, which leaves room for newcomers.

## Checklist
- [ ] Set up SGLang locally and run a small model
- [ ] Run its benchmarks and look for a regression or unhandled shape
- [ ] Land a first PR
