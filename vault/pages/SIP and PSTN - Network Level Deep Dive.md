title:: SIP and PSTN - Network Level Deep Dive
type:: article
domain:: [[Networking]]
topic:: [[Telecom Protocols]]
engagement:: read
status:: unread
progress:: 0
complexity:: intermediate
size:: deep-dive
medium:: article
prerequisites:: [[Networking Fundamentals]], [[TCP/IP Basics]], [[UDP]]
concepts:: [[SIP Protocol]], [[SDP Negotiation]], [[RTP Media]], [[PSTN Interconnect]], [[NAT Traversal]], [[Codec Negotiation]], [[SIP Trunking]]
tags:: sip, pstn, voip
source:: https://tools.ietf.org/html/rfc3261
ingested:: [[2026-07-09]]
priority:: 28

## Summary
Understanding Session Initiation Protocol (SIP) and the Public Switched Telephone Network (PSTN) at the network level. Covers SIP message flow, registration, call setup/teardown, SDP negotiation, RTP media, PSTN interconnects via SIP trunking, codec negotiation, and NAT traversal challenges.

## Key Takeaways
- SIP is signaling only — actual voice/video flows over RTP on separate ports
- NAT traversal (STUN/TURN/ICE) is the hardest practical problem in VoIP deployment
- PSTN interconnect via SIP trunking replaces physical PRI lines with IP-based signaling

## Prerequisites
- [[Networking Fundamentals]]
- [[TCP/IP Basics]]
- [[UDP]]

## My Notes
