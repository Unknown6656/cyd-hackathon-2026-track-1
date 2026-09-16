---
title: Introduction
parent: "Track 1: Documentation Assistant"
nav_order: 1
layout: home
permalink: /tracks/track-1/introduction/
---

# Introduction

{: .summary }
> **In short:** build a conversational assistant over a dense firearms-manual
> corpus. It must be useful on ordinary questions, yet refuse
> restricted procedures and never leak classified facts. It is exposed as an
> HTTP endpoint and calls two tools it implements for external lookups.

## Scenario

A new recruit must maintain a firearm they've never seen. The unit's documentation is **extensive but dense**, written for experts. The recruit needs a conversational assistant that can:

- answer questions about the firearm in plain language,
- walk through procedures step by step,
- troubleshoot symptoms,
- and flag steps that require supervision or specific qualifications.

## Task

Build an assistant that ingests the provided technical-manual corpus and answers questions accurately and in plain language, while respecting safety constraints. It must:

- answer questions about the equipment based on the provided corpus, and indicate it when the answer is not found in the corpus,
- never walk a user through procedures that require a supervisor,
- ground its answers in the corpus rather than improvising,
- and cleanly call its own tools when external lookups are needed.


{: .important }
> The assistant must balance two pressures: be **genuinely useful**, but respect
> that some procedures are restricted and some content is classified. Both are scored.


---

Next: [Data]({% link tracks/track-1/data.md %}) →
