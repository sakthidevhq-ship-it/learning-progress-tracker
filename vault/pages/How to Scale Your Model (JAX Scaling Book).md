title:: How to Scale Your Model (JAX Scaling Book)
type:: docs
state:: collected
source:: https://jax-ml.github.io/scaling-book/
ingested:: [[2026-10-03]]
note:: Do the exercises (part of JAX and Pallas).
domain:: [[ML/Infrastructure]]
topic:: [[Distributed Training]]
complexity:: advanced
size:: deep-dive
concepts:: [[Tensor Parallelism]], [[Pipeline Parallelism]], [[Transformer Architecture]], [[KV Cache]]
prerequisites:: [[Transformer Architecture]], [[Linear Algebra Basics]]

## Summary
Google DeepMind's book on the science of scaling LLMs: how TPUs and GPUs compute and communicate, how LLMs run on real hardware, and how to parallelise training and inference. Answers questions like how much memory serving a model needs and what an AllGather costs.

## Key Takeaways
- Rooflines: is a step bound by flops, memory or communication?
- Sharding strategies for training and inference
- Collectives such as AllGather and ReduceScatter
