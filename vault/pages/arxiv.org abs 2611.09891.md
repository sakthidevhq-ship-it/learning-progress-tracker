title:: https://arxiv.org/abs/2611.09891
type:: paper
state:: collected
source:: https://arxiv.org/abs/2611.09891
ingested:: [[2026-11-22]]
note:: NVIDIA: once an LLM has reasoned through a problem, run the solution as CPU code for rephrased/re-numbered versions, 16x-291x cheaper (via Rohan Paul on X: https://x.com/rohanpaul_ai/status/2124177125247013266). InferencePad link: on gpt-oss-20b the hidden reasoning is most of the reply (71/71 tokens for 'What is your name', 2,068 tokens ~24 min under the 4 GB cap), so skipping re-reasoning on repeat questions is a bigger lever than per-token speedups.
enrich:: pending

## Learnings
- 2026-11-22 · CPU-ARC (NVIDIA): solve a question once with a big model, have a second model turn that reasoning into a Python program with tests, and when a reworded or re-numbered version comes back, run the program on the CPU instead of calling an LLM (16x–291x cheaper). It separates finding a solution, which needs the model, from applying it, which is plain computation.
