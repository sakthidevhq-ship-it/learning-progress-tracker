title:: Looped Transformers
type:: paper
state:: collected
ingested:: [[2026-10-03]]
domain:: [[ML/Foundations]]
topic:: [[Model Architecture]]
complexity:: advanced
size:: medium
concepts:: [[Transformer Architecture]]
prerequisites:: [[Transformer Architecture]]
source:: https://x.com/qinzytech/status/2095542341956428129
note:: Paper: arXiv 2506.18233 (Scaling Law for Looped Transformers). Rumoured behind OpenAI Astra; OpenAI pushed back.

## Summary
Transformers that reuse the same layers in a loop instead of stacking distinct ones. The Scaling Law for Looped Transformers paper (arXiv 2506.18233) finds that looping does not increase knowledge capacity but does increase reasoning capability, so the benchmark gains come from how knowledge is used. That could be a separate scaling axis for pre-training.

## Key Takeaways
- Looping does not add knowledge capacity
- Looping improves reasoning capability
- In looped models knowledge and reasoning come apart; in normal transformers they grow together
