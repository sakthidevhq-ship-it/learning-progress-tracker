title:: Mixtral - Sparse Mixture of Experts
type:: paper
domain:: [[ML/Infrastructure]]
topic:: [[Inference Optimization]]
engagement:: read
status:: unread
progress:: 0
complexity:: advanced
size:: medium
medium:: paper
prerequisites:: [[Transformer Architecture]], [[Mixture of Experts]], [[Attention Mechanisms]]
concepts:: [[Sparse MoE]], [[Expert Routing]], [[Load Balancing]], [[Top-K Gating]], [[Expert Specialization]]
tags:: mixtral, moe
source:: https://arxiv.org/abs/2312.10997
ingested:: [[2026-07-09]]
priority:: 40

## Summary
Mistral AI's Mixtral 8x7B model using sparse Mixture of Experts. Each token is routed to 2 of 8 expert FFN layers, achieving quality matching Llama 2 70B at 6x lower inference cost. Covers routing, load balancing, and expert specialization.

## Key Takeaways
- Sparse routing means only 2 of 8 experts activate per token — 6x cheaper inference
- Experts naturally specialize by topic without explicit supervision
- Load balancing loss prevents expert collapse where all tokens route to one expert

## Prerequisites
- [[Transformer Architecture]]
- [[Mixture of Experts]]
- [[Attention Mechanisms]]

## My Notes
