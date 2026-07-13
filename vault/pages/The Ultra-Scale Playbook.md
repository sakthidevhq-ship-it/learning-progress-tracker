title:: The Ultra-Scale Playbook
type:: docs
domain:: [[ML/Infrastructure]]
topic:: [[Distributed Training]]
engagement:: read
status:: unread
progress:: 0
complexity:: advanced
size:: deep-dive
medium:: docs
prerequisites:: [[Tensor Parallelism]], [[Neural Network Fundamentals]]
concepts:: [[Tensor Parallelism]], [[Pipeline Parallelism]], [[Data Parallelism]], [[ZeRO]], [[Activation Recomputation]]
tags:: parallelism, training
source:: https://huggingface.co/spaces/nanotron/ultrascale-playbook
ingested:: [[2026-07-09]]
priority:: 36

## Summary
A Hugging Face guide to training large language models across thousands of GPUs, covering data/tensor/pipeline parallelism, ZeRO optimizer sharding, and activation recomputation strategies for maximizing throughput at scale.

## Key Takeaways
- Different parallelism strategies (data, tensor, pipeline) address different bottlenecks — memory, communication, or compute utilization — and are typically combined
- ZeRO shards optimizer states, gradients, and parameters across GPUs to eliminate memory redundancy without changing the math of training
- Activation recomputation trades extra forward-pass compute for dramatically reduced activation memory, enabling larger batch sizes or models

## Prerequisites
- [[Tensor Parallelism]]
- [[Neural Network Fundamentals]]

## My Notes
