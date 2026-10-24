title:: Gemini Flash Pretraining (Vlad Feinberg)
type:: article
state:: collected
source:: https://vladfeinberg.com/2025/04/24/gemini-flash-pretraining.html
ingested:: [[2026-10-24]]
note:: Gemini flash pretraining
domain:: [[ML/Infrastructure]]
topic:: [[Scaling Laws]]
complexity:: intermediate
size:: medium
concepts:: [[Scaling Laws]], [[Inference-Aware Scaling]], [[LLM-Guided Evolutionary Search]], [[Model Quantization]]
prerequisites:: [[LLM Basics]], [[Transformer Architecture]]

## Summary
Write-up (24 April 2025) of Vlad Feinberg's guest lecture on Gemini pretraining for Kai Li's Princeton systems-and-ML course (COS 568), with slides. Part one traces the history of neural scaling laws (drawing on Sebastian Borgeaud and Jean-Baptiste Alayrac's slides); part two asks how scaling should change when inference cost matters, as for a deployment-focused model like Gemini Flash, building on Jacob Austin's work. It closes with research directions academia can pursue without huge training budgets: quantization and kernels, FunSearch-style program search, and better statistics for fitting scaling laws.

## Key Takeaways
- Scaling laws are a planning tool, but the fitting method and experimental design change the recommendation
- Serving cost shifts the optimal trade-off toward smaller models trained on more data
- Least-squares and maximum-likelihood fits differ; choose (N, D) points by expected information gain
- Quantization, kernels and FunSearch-style search are high-leverage areas outside big labs
