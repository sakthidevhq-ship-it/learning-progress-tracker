title:: Recurrent Neural Networks: RNN, LSTM, GRU
type:: docs
domain:: [[ML/Foundations]]
topic:: [[Sequence Models]]
engagement:: read
status:: unread
progress:: 0
complexity:: intermediate
size:: medium
medium:: docs
prerequisites:: [[Neural Network Fundamentals]], [[Linear Algebra Basics]]
concepts:: [[Simple RNN]], [[LSTM]], [[GRU]], [[Backpropagation Through Time]], [[Vanishing Gradients]]
tags:: rnn, lstm, gru
source:: https://github.com/ml-curriculum/rnns
ingested:: [[2026-07-09]]
priority:: 28

## Summary
A curriculum module on sequence modeling with recurrent architectures, covering vanilla RNNs, LSTM and GRU gating mechanisms, backpropagation through time, and the vanishing/exploding gradient problem.

## Key Takeaways
- Vanilla RNNs struggle with long-range dependencies due to vanishing/exploding gradients through repeated multiplication
- LSTM and GRU gates let the network learn what to remember and forget, mitigating the vanishing gradient problem
- BPTT unrolls the recurrence into a feedforward computation graph, making standard backprop applicable at the cost of memory

## Prerequisites
- [[Neural Network Fundamentals]]
- [[Linear Algebra Basics]]

## My Notes
