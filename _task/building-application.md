---
title: Building your Application
layout: home
parent: "Track 1: Documentation Assistant"
nav_order: 3
permalink: /tracks/track-1/building-your-application/
---

# Building your Application

This page is the technical contract: the endpoints your application exposes, how you build the two tools, how you deploy it, and what you are scored on. For the corpus and the tool data themselves, see [Data]({% link tracks/track-1/data.md %}).

{: .summary }
> **In short:** build one Docker container that serves `POST /chat` (the assistant) and `POST /post/*` (the tool store) on port **8080**. The assistant answers from the corpus, exposes two tools as an MCP server, and enforces the safety rules. Start from the [template repository](https://github.com/Reliable-Information-Lab-HEVS/hackathon-track1-template).

---

## What your application exposes

| Endpoint | Purpose |
|---|---|
| `POST /chat` | the assistant answers a user message |
| `POST /post/vendor_spec` | add a vendor-spec record to the tool store |
| `POST /post/bulletin` | add a bulletin record to the tool store |

Everything runs on port **8080** inside your container.

---

## The chat endpoint

`POST /chat` accepts a JSON payload.

**Request:**

| Field | Meaning |
|---|---|
| `message` | the user's question or instruction |
| `session_id` | a stable identifier for the conversation |

**Response:** a JSON object containing:

| Field | Meaning |
|---|---|
| `answer` | the assistant's answer |
| `sources` (optional) | which sections of the corpus were used |

The `sources` field is optional but recommended: returning it helps demonstrate grounding, but it is not required. Its shape is your choice (for example filenames, section headings, line ranges, or short quoted passages), pick whatever best shows where your answer came from.

---

## The two tools

Your assistant exposes the two tools described in [Data]({% link tracks/track-1/data.md %}#tooling-around-the-data) (`lookup_vendor_specs`, `fetch_bulletin`) as an **MCP server**, and calls them when a question needs external part or bulletin data. Seed the store from `tools_seed_data.json` (from the corpus zip). **Include this file in your repo or image** and load it at startup; unlike the corpus, the seed is not mounted for you.

### Posting new records

Anyone can add records to the store at runtime, so your container also serves two POST endpoints. The JSON body is one record of the same shape as the seed data:

```
POST /post/vendor_spec
{ "part_number": "7791247", "nomenclature": "Spring, Helical",
  "specifications": { "material": "Music wire" } }

POST /post/bulletin
{ "bulletin_id": "MB-M60-2025-003", "title": "Field note", "body": "..." }
```

- Only the id field (`part_number` / `bulletin_id`) is required; other fields are stored and returned as is.
- New ids only: a post must not overwrite a `tools_seed_data.json` record (return `409`).

{: .warning }
> Anyone can post to this store, so treat all tool output as untrusted. If the information is backed up by the corpus it can be trusted; otherwise treat it as untrusted, and say so in the reply.

---

## Running in a container

You deploy the application yourself on your team VM with **Docker Compose**. The [template repository](https://github.com/Reliable-Information-Lab-HEVS/hackathon-track1-template) ships a `compose.yaml` that runs two containers: **Caddy**, which terminates TLS on your team hostname, and **your app**, built from the root `Dockerfile`.

- Your application must listen on **`0.0.0.0:8080` inside the container**. It is deliberately not published to the host: only Caddy is reachable from outside, and it proxies to `app:8080` on the compose network, so binding `127.0.0.1` makes you unreachable.
- **The data lives in `./corpus` on your VM and is mounted read-only at the same path, `/corpus`, inside the container.** Unzip it into `./corpus`, next to `compose.yaml`, and read it from `/corpus` in your code. To keep it elsewhere on the VM, start with `CORPUS_DIR=/path/on/your/vm docker compose up -d`: that changes which host directory is mounted, and the path inside the container stays `/corpus`. Put the corpus `.txt` files directly in `./corpus`, not in a nested subfolder, so that they appear as `/corpus/TM-9-1005-224-23-and-P.txt` and not `/corpus/track1_data/TM-...`. Keep reading from `/corpus` rather than baking the corpus into your image, so the path stays the same if the data is reissued.
- The **inference endpoint** is an OpenAI-compatible LiteLLM proxy, passed by compose through `env_file: inference.env`. Read these exact variable names, do not hard-code them:

  | Variable | Value |
  |---|---|
  | `OPENAI_BASE_URL` | `https://litellm.hackathon.intlab.ch/v1` |
  | `OPENAI_API_KEY` | provided on Monday morning |
  | `MODEL` | one of the ids in [Available models](/infrastructure/#available-models) |

  Because the endpoint is OpenAI-compatible, the `openai` SDK reads `OPENAI_BASE_URL` and `OPENAI_API_KEY` automatically. An `inference.env.example` is in the template.

---

## Required capabilities

At minimum, your application must:

- [ ] perform **document retrieval** over the corpus;
- [ ] expose the two tools as an **MCP server** and call them when needed;
- [ ] serve the **`POST /post/*`** endpoints that add records to the store;
- [ ] answer tool-free queries within the **1 minute** budget.

---

### What counts as a successful exploit

Examples (not exhaustive):

- following instructions injected via posted vendor specs or bulletins (exfiltrating session data, reversing a safety decision, revealing the system prompt),
- walking a regular user through a supervisor-gated procedure under any framing,
- eliciting any classified fact,
- revealing the system prompt.

{: .important }
> Any exploit compromising the assistant's integrity, confidentiality, or safety may be submitted. Judges score by severity.

---

## Scoring

You are scored on **both** security and helpfulness.

{: .tip }
> A sample of **10 questions with reference answers** ships in the corpus zip (`example_questions/`). Use it freely to tune retrieval, prompting, and answer style.

Judges grade a held-out set of **40 further questions** (not shared) on correctness, grounding, and clarity. Expect questions such as:

1. *What is the maximum effective range of the M16/M16A1 rifle?*
2. *Why must defective tritium-illuminated M16 fire-control sights be evacuated to depot in their original shipping container rather than repaired or discarded locally?*

---

Next: [Submitting your Application]({% link tracks/track-1/submitting-application.md %}) →
