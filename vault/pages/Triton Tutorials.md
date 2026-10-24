title:: Triton Tutorials
type:: docs
state:: picked
source:: https://triton-lang.org/main/getting-started/tutorials/index.html
ingested:: [[2026-10-03]]
note:: Learn Triton before CUDA (roadmap).
domain:: [[ML/Infrastructure]]
topic:: [[GPU Kernels]]
complexity:: intermediate
size:: deep-dive
concepts:: [[Triton]], [[GPU Computing Basics]]
prerequisites:: [[Python]], [[GPU Computing Basics]]
picked:: [[2026-10-03]]
planned:: 2026-10

## Summary
The official Triton tutorials: vector add, fused softmax, matmul, layer norm and fused attention, written in Python. Triton is what torch.compile lowers to and what vLLM's and SGLang's attention backends are written in.

## Checklist
- [ ] Set up a Kaggle/Colab GPU notebook with Triton and run 01 vector add
- [ ] 01 vector add: benchmark against torch and compute achieved bandwidth
- [ ] 02 fused softmax: explain the speedup with a roofline sketch
- [ ] 03 matmul: try block sizes and @triton.autotune; compare with cuBLAS
- [ ] 05 layer norm: forward and backward
- [ ] 06 fused attention: read and annotate (may need an Ampere+ GPU)
- [ ] Write your own RMSNorm kernel and benchmark it against torch
