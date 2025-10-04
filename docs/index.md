---
title: Idea Layer · v0.1
description: Receipts for ideas. Get credit. Get paid.
layout: default
---

# Idea Layer · v0.1
**Receipts for ideas. Get credit. Get paid.**

Three tiny, signed artifacts:

- **IR — Idea Receipt**: snapshot of a claim (private hash, κ stress, Δhol drift).
- **VR — Validation Receipt**: one check with a score and method.
- **LR — Listing Receipt**: public roll-up (Frontier 🟦 / Gold 🟨) for directories or exchanges.

## Start here
- **Schemas (v0.1)**
  - [IR – Idea Receipt](../schemas/v0.1/ir.schema.json)
  - [VR – Validation Receipt](../schemas/v0.1/vr.schema.json)
  - [LR – Listing Receipt](../schemas/v0.1/lr.schema.json)
- **Policy / thresholds**
  - [Defaults (v0.1)](../policies/v0.1/)
- **Examples**
  - [Sample receipts](../examples/)

## How it works
1. **Submit** an IR → your idea is hashed and signed (no content stored).
2. **Validate** with VRs → small, auditable checks add confidence.
3. **List** as an LR → **Frontier** if promising; **Gold** when checks converge.

## Privacy, by default
No inputs, outputs, or chain-of-thought.  
Hashes + length bins + timestamp signatures; transparency-anchored.

## Quick actions
- **Browse Frontier** → `../examples/`  
- **Sponsor a validation** → `../examples/`  
- **Implement the spec** → `../schemas/v0.1/`
