title:: OpenVINO Contributions
type:: project
state:: collected
source:: https://github.com/openvinotoolkit/openvino
ingested:: [[2026-11-09]]
note:: Aim from 2026-11-09: two merged PRs in ~6-8 weeks at 6-8 h/week on the Ryzen 4600U ThinkPad over ssh. PR 1: add a missing aten:: op to the PyTorch frontend (C++ translator + Python layer test). PR 2: speech work in openvino.genai (WhisperPipeline).
domain:: [[ML/Infrastructure]]
topic:: [[Inference Optimization]]
complexity:: intermediate
size:: deep-dive
concepts:: [[Model Conversion]], [[Graph Frontends]], [[CPU Inference]]
prerequisites:: [[Python]], [[Data Structures]]

## Summary
Intel's open-source toolkit for converting and running models, built mainly for CPU inference (its GPU and NPU plugins are Intel-only). The goal is two merged PRs: a missing aten:: op translator in the PyTorch frontend, then speech work in openvino.genai such as WhisperPipeline, all on a CPU-only Ryzen laptop.

## Key Takeaways
- PyTorch frontend op translators are 30-150 lines of C++ plus a Python layer test; copy an existing translator in src/frontends/pytorch/src/op/
- First builds take 30-60+ minutes; use ccache and build only the needed parts
- openvino.genai can build against a nightly OpenVINO package instead of compiling the core
- Review and CI take longer than writing the code
