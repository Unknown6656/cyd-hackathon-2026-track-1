---
title: Extensions
parent: "Track 1: Documentation Assistant"
nav_order: 6
layout: home
permalink: /tracks/track-1/extensions/
---

# Extensions

{: .summary }
> **Optional.** Once your core assistant works, these are directions to take it
> further. They are pointers, not requirements: pick any, all, or none, and feel
> free to go your own way.

Your baseline is the assistant from [Building your Application]({% link tracks/track-1/building-application.md %}). Everything here is on top of that.

---

## 1. Add a user interface

Your assistant is an HTTP endpoint, which is enough for grading but not much to look at. A chat UI makes it easy to demo and to test by hand.

{: .tip }
> [Open WebUI](https://openwebui.com) is an open-source chat interface you can point at your assistant. It speaks the OpenAI chat format, so you will likely add a thin adapter between it and your `/chat` endpoint, or expose an OpenAI-compatible route alongside it.

---

## 2. Add more manuals

The corpus is four manuals. Adding more is a good way to stress-test your retrieval and grounding at a larger scale, and to see whether your safety behaviour holds on documents you have not tuned against.

{: .tip }
> [liberatedmanuals.com](https://liberatedmanuals.com/) is the source of the provided corpus and has many more manuals to draw from.

The graded questions are about the provided corpus, so this is about robustness and generality rather than the score directly. Do not remove or alter the provided manuals.

---

## 3. Your own extension

Free choice. If you have an idea that makes the assistant more useful, safer, or more interesting, build it. A few directions to spark ideas:

- richer **citations**: highlight the exact passage behind each answer;
- **uncertainty signalling**: say how confident an answer is, or flag when it is guessing;
- **multilingual** evaluation of questions and answers;


{: .tip }
> Surprise us. The pointers above are starting points, not a menu.
