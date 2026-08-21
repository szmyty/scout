---
schema: aether.architecture-document/v1
id: scout-purpose
title: Scout Purpose
kind: architecture-document
version: 0.1.0
status: draft
owners: [szmyty]
created: 2026-08-21
updated: 2026-08-21
depends_on: []
related: [career-architecture]
supersedes: []
---

# Scout Purpose

Scout turns a large, noisy job market into a calm, privacy-safe queue of opportunities worth investigating. It is the public scouting and status surface, not the private career database.

Scout answers: what opportunities exist, which leads are verified, what is stale, which public-safe opportunities deserve attention, and what should happen next.

## Boundary

Scout may publish reviewed opportunity metadata, aggregate status, public methodology, and public-safe scoring outputs. It must not publish private application packets, exact private reasoning, personal constraints, reference identities, credentials, contact details, or secrets.

## Success

A human or AI agent can understand the scouting method, inspect the queue, and continue research without reconstructing the system from chat history.
