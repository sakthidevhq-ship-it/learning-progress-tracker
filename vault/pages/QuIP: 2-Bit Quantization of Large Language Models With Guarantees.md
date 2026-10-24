title:: QuIP: 2-Bit Quantization of Large Language Models With Guarantees
type:: paper
state:: collected
ingested:: [[2026-10-24]]
note:: More quantization
domain:: [[ML/Infrastructure]]
topic:: [[Inference Optimization]]
complexity:: advanced
size:: deep-dive
concepts:: [[Model Quantization]], [[Incoherence Processing]], [[Adaptive Rounding]], [[Post-Training Quantization]]
prerequisites:: [[Linear Algebra Basics]], [[Transformer Architecture]], [[LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale]]

## Summary
First paper in Chris De Sa's group's quantization series (Chee, Cai, Kuleshov, De Sa, NeurIPS 2023; https://arxiv.org/abs/2307.13304). QuIP observes that quantization works best when weights and Hessians are 'incoherent' (no large, axis-aligned entries), so it multiplies them by random orthogonal matrices before quantizing, then applies LDLQ, an adaptive rounding procedure that minimises a quadratic proxy loss, is optimal within its class and is equivalent to GPTQ/OPTQ. It was the first post-training method to make 2-bit LLM weights viable, with theoretical guarantees.

## Key Takeaways
- Incoherence processing: rotate weights and Hessian with random orthogonal matrices so no single entry dominates
- LDLQ adaptive rounding minimises the Hessian-weighted rounding error and subsumes GPTQ/OPTQ
- Theory explains why incoherence makes low-bit rounding error small
- Makes 2-bit post-training quantization of large LLMs workable for the first time
