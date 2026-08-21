---
schema: aether.architecture-document/v1
id: scout-architecture
title: Scout Architecture
kind: architecture-document
version: 0.1.0
status: draft
owners: [szmyty]
created: 2026-08-21
updated: 2026-08-21
depends_on: [scout-foundations, scout-system]
related: [career-architecture]
supersedes: []
---
# Scout Architecture

Scout is the public opportunity-intelligence projection of a larger career-search system.

- `szmyty/scout`: public methodology, sanitized queue, dashboard.
- `szmyty/career`: private canonical opportunity/application state.
- `szmyty/resume`: public reusable document-generation engine.
- AI/chat sessions: replaceable research/orchestration workers, never canonical storage.

Information flows from Career to Scout only through an explicit reviewed export. Scout never reads Career at runtime.

A new agent should be able to read this corpus, `AGENTS.md`, and `docs/PURSUIT-EV.md` and resume scouting without prior chat history.
