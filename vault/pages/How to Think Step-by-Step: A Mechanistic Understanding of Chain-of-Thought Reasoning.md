title:: How to Think Step-by-Step: A Mechanistic Understanding of Chain-of-Thought Reasoning
type:: paper
domain:: [[ML/Foundations]]
topic:: [[Interpretability]]
engagement:: read
status:: unread
progress:: 0
complexity:: advanced
size:: deep-dive
medium:: paper
prerequisites:: [[Transformer Architecture]], [[Attention Mechanisms]], [[Multi-Head Attention]], [[Chain of Thought]]
concepts:: [[Mechanistic Interpretability]], [[Chain of Thought]], [[Activation Probing]], [[Attention Head Analysis]], [[Circuit Analysis]], [[Reasoning Decomposition]]
tags:: cot, interpretability, mechanistic
source:: https://arxiv.org/abs/2402.18312
ingested:: [[2026-07-14]]
priority:: 26

## Summary
Mechanistic interpretability study of how LLMs actually perform chain-of-thought reasoning. Probes internal activations during multi-step fictional-ontology reasoning to locate where and how the model decomposes tasks, finding that CoT emerges from parallel processing pathways rather than strictly sequential computation — the model uses distinct functional components: an early copying/induction circuit, mid-layer decision heads, and later answer-writing heads operating in parallel across reasoning steps.

## Key Takeaways
- CoT reasoning is not sequential inside the model — parallel pathways handle different reasoning sub-tasks simultaneously
- Distinct attention-head families specialize: induction/copying heads early, decision heads mid-network, answer-writers late
- Probing fictional ontologies isolates reasoning circuits from memorized world knowledge

## Prerequisites
- [[Transformer Architecture]]
- [[Attention Mechanisms]]
- [[Multi-Head Attention]]
- [[Chain of Thought]]

## My Notes
