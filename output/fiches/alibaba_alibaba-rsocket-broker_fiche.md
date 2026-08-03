---
## alibaba/alibaba-rsocket-broker
**Type:** Framework
**Domain:** Embedded
**Relevance score:** 62/100
**Problem solved:** Provide a reactive peer-to-peer communication system based on RSocket for distributed architectures (RPC, Pub/Sub, Streaming) without explicit thread management and with backpressure support.
**How it works:** The broker implements the RSocket protocol to establish asynchronous bidirectional connections between clients and servers. It uses a Control Plane to orchestrate communications, support service discovery, and manage Prometheus metrics. The reactive architecture eliminates blocking thread models and adapts data flows to receiver capabilities via backpressure.
**Chinese specificity:** Alibaba project integrating Chinese cloud infrastructure requirements (multi-cloud and cross-cloud environments). The project has been archived since July 2024 in favor of the community fork reactive-rsocket-broker.
**Western equivalent:** Spring Cloud Stream, Vert.x, Akka, gRPC with bidirectional streaming
**Maturity:** Experimental (updated 2024-10)
**Language:** Bilingual CN-EN
**Gitee:** https://gitee.com/alibaba/alibaba-rsocket-broker
---
