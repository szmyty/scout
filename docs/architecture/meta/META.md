---
schema: aether.architecture-document/v1
id: scout-meta
title: Scout Meta Architecture
kind: architecture-document
version: 0.1.0
status: draft
owners: [szmyty]
created: 2026-08-21
updated: 2026-08-21
depends_on: [scout-epistemology, scout-ai-constitution]
related: []
supersedes: []
---
# Scout Meta Architecture

Scout uses the complete 18-concern Aether-compatible architecture corpus.

Reading order: Purpose/Vision/Principles; Epistemology/Ontology; Foundations/System/Architecture; Methodology/PursuitEV; Operator Model/Experience Design; AI Constitution; Decisions/Roadmap.

This corpus owns durable meaning and boundaries. `AGENTS.md` owns operational instructions. `docs/PURSUIT-EV.md` owns scoring formulas. Runtime code owns implementation detail.

When a chat/provider changes, the next agent should treat repository documents as durable context, reverify live job facts, and continue from canonical state rather than conversational memory.
