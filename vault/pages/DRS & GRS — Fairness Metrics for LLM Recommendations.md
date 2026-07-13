title:: DRS & GRS — Fairness Metrics for LLM Recommendations
type:: docs
domain:: [[ML/Evaluation]]
topic:: [[Fairness Metrics]]
engagement:: implement
status:: completed
progress:: 100
complexity:: advanced
size:: medium
medium:: docs
prerequisites:: [[LLM Basics]], [[Prompt Engineering Fundamentals]]
concepts:: [[Fairness Evaluation]], [[Demographic Representation Score]], [[Geographic Representation Score]], [[Bias Measurement]], [[LLM Evaluation]], [[Recommendation Systems]]
tags:: fairness, metrics, personal-work
source:: /private/tmp/drs-grs.md
ingested:: [[2026-07-14]]
priority:: 26

## Summary
Personal research work: developed two novel metrics for evaluating fairness in LLM-generated recommendations. Demographic Representation Score (DRS) measures how equitably recommendations represent demographic groups; Geographic Representation Score (GRS) measures geographic distribution bias. Together they quantify whether an LLM's recommendation outputs systematically over- or under-represent populations, enabling measurable fairness evaluation instead of anecdotal spot-checks.

## Key Takeaways
- Representation fairness in LLM outputs can be scored quantitatively per demographic and geographic axis
- A metric pair (DRS + GRS) separates who is represented from where they are — the two biases behave differently
- Novel metrics make fairness regressions detectable in evaluation pipelines rather than post-hoc audits

## Prerequisites
- [[LLM Basics]]
- [[Prompt Engineering Fundamentals]]

## My Notes
