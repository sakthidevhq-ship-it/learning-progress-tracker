title:: QTIP: Quantization with Trellises and Incoherence Processing
type:: paper
state:: collected
ingested:: [[2026-10-24]]
note:: More quantization
domain:: [[ML/Infrastructure]]
topic:: [[Inference Optimization]]
complexity:: advanced
size:: deep-dive
concepts:: [[Model Quantization]], [[Trellis-Coded Quantization]], [[Vector Quantization]], [[Incoherence Processing]]
prerequisites:: [[QuIP#: Even Better LLM Quantization with Hadamard Incoherence and Lattice Codebooks]]

## Summary
Third paper in Chris De Sa's group's series (Tseng, Sun, Hou, De Sa, NeurIPS 2024; https://arxiv.org/abs/2406.11235). Vector quantization needs a codebook exponential in its dimension, which caps VQ methods like QuIP# at around 8 dimensions. QTIP instead uses trellis-coded quantization, a stateful decoder that decouples codebook size from bitrate and effective dimension, enabling ultra-high-dimensional quantization. It designs a hardware-efficient 'bitshift' trellis with codes ranging from lookup-only to computed (lookup-free), reaching state-of-the-art quality and inference speed.

## Key Takeaways
- VQ quality improves with dimension, but codebook size grows exponentially with it
- Trellis-coded quantization gets high effective dimension with a small stateful decoder
- Bitshift trellis and computed codes make decoding fast enough for memory-bound LLM inference
- Since inference is memory-bound, better low-bit weights translate directly into throughput
