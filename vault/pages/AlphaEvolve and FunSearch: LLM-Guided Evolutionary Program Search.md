title:: AlphaEvolve and FunSearch: LLM-Guided Evolutionary Program Search
type:: paper
state:: collected
ingested:: [[2026-10-24]]
note:: Bleeding edge of agent loops (Layer just above LLM as black box, harnesses)
domain:: [[ML/Agents]]
topic:: [[Agentic Systems]]
complexity:: intermediate
size:: deep-dive
concepts:: [[LLM-Guided Evolutionary Search]], [[Agent Architecture]], [[Verifier Design]], [[Program Synthesis]]
prerequisites:: [[LLM Basics]], [[Agent Architecture]]

## Summary
Two DeepMind systems that wrap LLMs in an evolutionary loop with automatic evaluators, which Vlad Feinberg uses as components of his research workflow. FunSearch (Romera-Paredes et al., Nature 2023; https://deepmind.google/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/) evolves short programs scored by an evaluator and found new cap-set constructions and bin-packing heuristics. AlphaEvolve (Novikov et al., 2025; https://arxiv.org/abs/2506.13131) generalises this to an evolutionary coding agent that edits whole codebases: it improved Google data-centre scheduling, simplified accelerator circuits, sped up Gemini training kernels, and found a 48-multiplication algorithm for 4x4 complex matrices, the first improvement over Strassen in that setting in 56 years.

## Key Takeaways
- The pattern: an LLM proposes code, an automatic evaluator scores it, an evolutionary database keeps the best and most diverse candidates
- The evaluator is the hard part; problems with cheap, reliable scoring are the ones that fall
- FunSearch got its best results with a mid-sized proposal model: balance proposal rate against evaluation cost
- AlphaEvolve scales from single functions to whole files and real infrastructure wins
