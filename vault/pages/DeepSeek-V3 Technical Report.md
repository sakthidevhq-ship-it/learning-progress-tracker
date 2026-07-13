title:: DeepSeek-V3 Technical Report
type:: paper
domain:: [[ML/Infrastructure]]
topic:: [[Model Architecture]]
engagement:: read
status:: unread
progress:: 0
complexity:: advanced
size:: deep-dive
medium:: paper
prerequisites:: [[Mixture of Experts]], [[KV Cache]], [[Multi-Head Attention]], [[Transformer Architecture]]
concepts:: [[Mixture of Experts]], [[KV Cache]], [[Multi-Head Attention]], [[Transformer Architecture]]
tags:: deepseek, moe
source:: https://arxiv.org/abs/2412.19437
ingested:: [[2026-07-09]]
priority:: 38

## Summary
DeepSeek-V3 is a 671B-parameter (37B active) mixture-of-experts language model that introduces Multi-head Latent Attention for KV cache compression and multi-token prediction as an auxiliary training objective, achieving strong performance at relatively low training cost.

## Key Takeaways
- Multi-head Latent Attention compresses the KV cache via a low-rank projection, cutting inference memory substantially versus standard MHA/GQA
- Sparse MoE routing lets DeepSeek-V3 have 671B total parameters while only activating 37B per token, balancing capacity and inference cost
- Multi-token prediction as an auxiliary objective improves training signal density and enables speculative-decoding-like inference speedups

## Prerequisites
- [[Mixture of Experts]]
- [[KV Cache]]
- [[Multi-Head Attention]]
- [[Transformer Architecture]]

## My Notes
