title:: Language Models Can Control Their Own Attention (Declarative Attention)
type:: tweet
state:: collected
source:: https://x.com/omarsar0/status/2095612805496164801
ingested:: [[2026-10-03]]
domain:: [[ML/Infrastructure]]
topic:: [[Inference Optimization]]
complexity:: advanced
size:: quick-read
concepts:: [[KV Cache]], [[Attention Mechanisms]]
prerequisites:: [[Attention Mechanisms]]

## Summary
Google DeepMind paper (arXiv 2609.02737), via a tweet by omarsar0. The model declares in its own chain of thought where it needs to look (global, focus or local), and the inference engine parses those declarations like tool calls and skips most of the KV cache read. Zero-shot on off-the-shelf weights, attended tokens during decoding drop 52% on Gemma-4-31B and 31% on Qwen-3.6-27B.

## Key Takeaways
- Global attention re-reads the whole KV cache on every token
- Proxy-score sparsity still costs O(N) per step
- Let the model declare where to look; the engine enforces it
