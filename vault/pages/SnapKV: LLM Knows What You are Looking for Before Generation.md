title:: SnapKV: LLM Knows What You are Looking for Before Generation
type:: paper
state:: collected
ingested:: [[2026-10-24]]
note:: More quantization
domain:: [[ML/Infrastructure]]
topic:: [[Inference Optimization]]
complexity:: intermediate
size:: medium
concepts:: [[KV Cache]], [[KV Cache Compression]], [[Attention Mechanisms]], [[SRAM vs HBM]]
prerequisites:: [[KV Cache]], [[Attention Mechanisms]], [[Transformer Architecture]]

## Summary
Li et al. (2024; https://arxiv.org/abs/2404.14469) attack the decoding-side bottleneck of long contexts: reading a huge KV cache from HBM for every generated token. They observe that each attention head consistently attends to a stable set of prompt positions, and that this pattern can be read from an 'observation window' at the end of the prompt. SnapKV keeps only the clustered, important KV positions per head, without fine-tuning, giving 3.6x faster generation and 8.2x better memory efficiency at 16K tokens with comparable accuracy, and up to 380K tokens on one A100-80GB.

## Key Takeaways
- Decode is bound by KV cache HBM bandwidth, so shrinking the cache speeds up every token
- Heads attend to consistent prompt features; the last prompt tokens predict which positions matter
- Per-head selection with pooling keeps neighbouring context and preserves accuracy
- Fine-tuning-free and drop-in: compression happens once after prefill
