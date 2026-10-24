title:: QuIP#: Even Better LLM Quantization with Hadamard Incoherence and Lattice Codebooks
type:: paper
state:: collected
ingested:: [[2026-10-24]]
note:: More quantization
domain:: [[ML/Infrastructure]]
topic:: [[Inference Optimization]]
complexity:: advanced
size:: deep-dive
concepts:: [[Model Quantization]], [[Incoherence Processing]], [[Vector Quantization]], [[Lattice Codebooks]], [[Post-Training Quantization]]
prerequisites:: [[QuIP: 2-Bit Quantization of Large Language Models With Guarantees]], [[Linear Algebra Basics]]

## Summary
Follow-up from Chris De Sa's group (Tseng, Chee, Sun, Kuleshov, De Sa, ICML 2024; https://arxiv.org/abs/2402.04396). QuIP# replaces QuIP's random orthogonal matrices with a fast randomized Hadamard transform, moves from scalar to vector quantization with a hardware-friendly codebook built on the E8 lattice (the optimal 8-dimensional unit-ball packing), and adds inter-layer fine-tuning. The result is state-of-the-art quality at 2-4 bits per weight with fast inference kernels.

## Key Takeaways
- Randomized Hadamard transform gives cheaper, better incoherence than dense random rotations
- Vector quantization with an E8-lattice codebook exploits the ball-shaped distribution of incoherent weights
- The E8P codebook is small and symmetric enough to decode quickly on GPU
- Fine-tuning after quantization closes much of the remaining gap at 2 bits
