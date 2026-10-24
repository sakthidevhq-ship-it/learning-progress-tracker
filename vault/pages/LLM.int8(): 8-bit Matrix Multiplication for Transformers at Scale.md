title:: LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale
type:: paper
state:: collected
source:: https://arxiv.org/abs/2208.07339
ingested:: [[2026-10-24]]
note:: LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale
domain:: [[ML/Infrastructure]]
topic:: [[Inference Optimization]]
complexity:: intermediate
size:: deep-dive
concepts:: [[Model Quantization]], [[Outlier Features]], [[Vector-wise Quantization]], [[Mixed-Precision Decomposition]]
prerequisites:: [[Transformer Architecture]], [[Linear Algebra Basics]], [[Neural Network Fundamentals]]

## Summary
Dettmers, Lewis, Belkada and Zettlemoyer (2022) show how to run 175B-parameter transformers with Int8 matrix multiplication and no loss in quality (https://arxiv.org/abs/2208.07339). Vector-wise quantization gives each row/column its own scale, and a mixed-precision decomposition keeps the few emergent outlier feature dimensions (which appear systematically around 6.7B parameters) in fp16 while the other 99.9% of values go through int8. Vlad Feinberg recommends it as the classic entry point to quantization because it exposes a strong set of tricks; it became the basis of bitsandbytes.

## Key Takeaways
- Naive per-tensor int8 breaks large models because a handful of hidden dimensions carry huge-magnitude outlier activations
- Outlier features emerge abruptly with scale (~6.7B params) and appear in nearly every layer and token
- Vector-wise scaling plus routing outlier columns through fp16 preserves full accuracy while halving inference memory
- Quantization is about finding the structure in activations and weights, not just picking a bit width
