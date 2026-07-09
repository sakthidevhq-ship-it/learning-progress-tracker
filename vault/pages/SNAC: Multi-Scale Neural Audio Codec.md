title:: SNAC: Multi-Scale Neural Audio Codec
type:: paper
domain:: [[ML/Voice]]
topic:: [[Audio Codecs]]
engagement:: read
status:: unread
progress:: 0
complexity:: intermediate
size:: quick-read
medium:: paper
prerequisites:: [[Neural Network Fundamentals]]
concepts:: [[Neural Audio Codec]], [[Residual Vector Quantization]], [[Multi-Scale Encoding]]
tags:: snac, codec
source:: https://arxiv.org/abs/2410.02981
ingested:: [[2026-07-09]]
priority:: 28

## Summary
SNAC introduces a neural audio codec that encodes speech into hierarchical, multi-scale discrete tokens at different temporal resolutions, improving compression efficiency and downstream generative modeling compared to flat residual vector quantization codecs.

## Key Takeaways
- Encoding audio at multiple temporal scales lets coarse tokens capture long-range structure while fine tokens capture local detail
- SNAC achieves lower bitrates than flat RVQ codecs at comparable perceptual audio quality
- Multi-scale codec tokens are a natural fit for hierarchical generation schemes used in modern speech LMs like Moshi

## Prerequisites
- [[Neural Network Fundamentals]]

## My Notes
