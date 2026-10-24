title:: Tiny Transformer in JAX, Flax and Optax that Learns 3-Digit Addition
type:: project
state:: collected
ingested:: [[2026-10-24]]
note:: A good starting point
domain:: [[ML/Foundations]]
topic:: [[Model Architecture]]
complexity:: intermediate
size:: medium
concepts:: [[Transformer Architecture]], [[Self-Attention]], [[Tokenization]], [[JAX]]
prerequisites:: [[Neural Network Fundamentals]], [[Transformer Architecture]], [[Python]]

## Summary
Starter project from Vlad Feinberg's 'How to Land a Frontier Lab Job' lesson plan: write a ~10M-parameter transformer from scratch using only jax, flax and optax in a free Colab (TPU, or a T4 GPU). Use a hard-coded vocabulary of the digits 0-9, space, '+' and '=', generate a dataset of up-to-3-digit addition problems, pad examples to a fixed length, and train it to learn addition. It should train quickly and is a warm-up for the JAX scaling book and Pallas kernels.

## Key Takeaways
- A fixed 13-token vocabulary keeps tokenization trivial so the focus is the model and training loop
- Padding to a fixed length keeps shapes static so jit compiles once
- Small enough to train in minutes on a free T4 or TPU
- Builds hands-on JAX fluency before scaling up

## Checklist
- [ ] Generate a dataset of simple up-to-3-digit numbers, have it learn addition
- [ ] Hard code the vocabulary to digits 0-9, space, + and =
- [ ] Train quickly on a T4 GPU (pad examples to a fixed length)
