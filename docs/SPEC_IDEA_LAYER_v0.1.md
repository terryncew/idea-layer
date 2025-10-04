# Idea Layer v0.1 — Specification

**One line:** Small receipts, big accountability. IR (Idea), VR (Validation), LR (Listing).

## How to read this spec
- **Sections 1–2**: Threat model & crypto primitives
- **Section 3**: The three receipt schemas (IR/VR/LR) with JSON examples
- **Sections 4–6**: Badge rules, routing logic, licensing/escrow
- **Sections 7–9**: Anti-gaming, UI hints, versioning
If you're implementing: start at Section 3. If you're auditing: start at Section 2 and Section 7.

## 1) Overview
Receipts measure structure (κ) and change (Δhol) without exposing content. Monotone hazards support triage, not truth. VRs add auditable evidence; Frontier surfaces promising under-supported claims; Gold demands convergent checks.

## 2) Threat model & privacy
- **No inputs/outputs/CoT** in receipts.
- HMAC with daily rotating pepper for `idea_hmac` / `prompt_hmac`.
- Length bins (S/M/L/XL) and ± jittered timestamps.
- Signature: HMAC-SHA256 over canonical JSON (excludes `provenance.sig`).
- Transparency anchor: default **local** Merkle log (Rekor/RFC3161 compatible).

## 3) Schemas
See `schemas/v0.1/*.schema.json` for IR/VR/LR. Required fields are minimal and portable.

## 4) Badge rules
- **Frontier** when `F = P*(1−E)*(1−k̂) ≥ τ_F`, `kappa < τ_k`, no contradictions.
- **Gold** when ≥ `N_gold` VRs with `support_score ≥ τ_S`, inter-rater agreement `≥ IRR_min`, guards clean.
- **Hold/Revoked** on disputes or guard failures.

## 5) Routing (ops)
- κ high → pause & require a VR before listing.
- Δhol attribution guides spend (prompt/tool/retrieval/model/cache).

## 6) Licensing & escrow
- Scopes: `audit-only`, `research-noncommercial`, `train-critic`, `limited-production`, `full-production`.
- Default split 70/20/10 (creator/validators/platform).
- Disputes: 30d escrow → counter-VR (+14d) → 2 expert checks (tie-break).

## 7) Anti-gaming
- Commit-reveal seeded controls (5–10%).
- Rater reputation (cold-start 0.50), ELO-like updates anchored to control agreement.
- Spam brake (rate-limit or small bond).

## 8) UI hints
- Show five numbers on LR cards: κ, Δhol (dominant), P, E, F.
- Badges: 🟦 Frontier, 🟨 Gold.

## 9) Versioning
All receipts carry `"schema_version": "idea_layer/v0.1"`. Subsequent versions MUST be backward compatible or include a migration note.
