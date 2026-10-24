title:: Barbarians at the Gate: How AI is Upending Systems Research
type:: paper
state:: collected
ingested:: [[2026-10-24]]
note:: More quantization
domain:: [[ML/Agents]]
topic:: [[Agentic Systems]]
complexity:: intermediate
size:: medium
concepts:: [[AI-Driven Research for Systems]], [[LLM-Guided Evolutionary Search]], [[Verifier Design]], [[Agent Architecture]]
prerequisites:: [[LLM Basics]], [[AlphaEvolve and FunSearch: LLM-Guided Evolutionary Program Search]]

## Summary
Cheng, Liu, Pan, ..., Zaharia and Stoica (UC Berkeley, 2025; https://arxiv.org/abs/2510.06189) argue that systems research is unusually suited to AI-driven discovery because performance problems come with reliable verifiers: run the candidate in a real system or simulator against a workload and measure it. They call the generate-evaluate-refine loop AI-Driven Research for Systems (ADRS) and, using OpenEvolve, show case studies (multi-region cloud scheduling, MoE inference load balancing, LLM-based SQL queries, transaction scheduling) where evolved algorithms beat state-of-the-art human designs by up to 5x runtime or 50% cost. They distil best practices for prompts and evaluators and predict researchers will shift toward problem formulation.

## Key Takeaways
- AI discovery loops need a reliable verifier; systems benchmarks and simulators provide one
- ADRS = generate diverse candidates, evaluate on workloads, refine (e.g. with OpenEvolve)
- Evolved algorithms beat human state of the art on several real systems problems
- Evaluator construction and problem framing become the researcher's main job
