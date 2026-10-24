title:: AQLM: Extreme Compression of Large Language Models via Additive Quantization
type:: paper
state:: collected
ingested:: [[2026-10-24]]
note:: More quantization
domain:: [[ML/Infrastructure]]
topic:: [[Inference Optimization]]
complexity:: advanced
size:: deep-dive
concepts:: [[Model Quantization]], [[Additive Quantization]], [[Multi-Codebook Quantization]], [[Vector Quantization]]
prerequisites:: [[Linear Algebra Basics]], [[Transformer Architecture]], [[LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale]]

## Summary
Egiazarian, Panferov, Kuznedelev, Frantar, Babenko and Alistarh (ICML 2024; https://arxiv.org/abs/2401.06118) bring classic multi-codebook Additive Quantization from information retrieval to 2-3 bit LLM compression. Each group of weights is the sum of codewords from several learned codebooks, learned in an input-adaptive way and jointly optimised across each transformer block. AQLM was the first scheme Pareto-optimal in accuracy vs size below 3 bits per parameter, with GPU and CPU kernels that match or beat fp16 speed. Vlad Feinberg lists it as a different branch of the same tech tree as the QuIP family.

## Key Takeaways
- Represents weight groups as sums of codewords from multiple codebooks (additive quantization)
- Codebooks are learned against layer inputs (calibration data), not just weight reconstruction
- Joint fine-tuning of codebooks per transformer block recovers accuracy at 2 bits
- Practical kernels show extreme compression need not cost decode speed
