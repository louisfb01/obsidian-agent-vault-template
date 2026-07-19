---
type: agent-rules
status: active
updated: 2026-07-19
tags:
  - agent
  - ai-os
  - rules
---

# Agent Rules

Read this file first, before doing any work in this vault. It defines how the
agent (Claude, Codex, or any assistant) should behave here, and — most
importantly — how it gets better the more you use it.

If a task genuinely needs to break a rule, say so out loud and explain why first.

---

## 1. Orientation — always start here

1. Open `Skills/Skills Index.md`. It is the map: which skill to load, what each is
   for, and which skills combine. The index is the map; each `SKILL.md` is the
   source of truth.
2. Load the skill's `SKILL.md` in full before doing the work.
3. If the task needs both content and voice, combine a **grounding** skill with an
   **output** skill (see the layered hierarchy in the index).
4. Do messy in-progress work inside `working-dir/<task>/`, never loose in the vault.
5. Finished deliverables land in the relevant **Areas/** folder, not in `working-dir/`.

---

## 2. The Feedback loop (self-improvement) — REQUIRED

Every skill owns a `FEEDBACK.md` in its own folder. This is how the vault
improves over time. It is not optional.

### After every meaningful run of a skill
Append one dated entry to that skill's `FEEDBACK.md`:

- **Task** — what was asked.
- **Worked** — what produced a good result.
- **User corrected** — every correction or "no, do it like this," captured
  clearly enough to learn from.
- **Friction** — anything slow, confusing, or repeated.
- **Proposed rule change** — a concrete edit to `SKILL.md`, or "none".

One run = one entry, newest at the top. Use the "Feedback entry" template
(hotkey: Insert template) so the shape stays consistent.

### Promotion — turn feedback into the skill
When the same lesson appears in **two or more** entries, it is a rule now:

1. Edit the skill's `SKILL.md` to encode it (a new guardrail, a changed default, a
   corrected example).
2. Bump `updated:` in the `SKILL.md` frontmatter.
3. Mark the promoted entries `→ promoted YYYY-MM-DD` so they are not re-learned.

### Never
- Never "learn" a correction only for the current chat. If it matters, it goes in
  `FEEDBACK.md`, or it is gone next session.
- Never promote a one-off preference into a hard rule. Two signals minimum.
- Never delete feedback history. Mark it promoted or superseded; keep the trail.

> `FEEDBACK.md` is the skill's memory. `SKILL.md` is what it has learned and now
> does by default. The loop moves lessons from the first into the second.

---

## 3. Code lives in an external repo (reminder)

This vault holds **notes and skills**, not code. When a task involves writing or
running code:

- Keep that code in a real **git repository outside this vault**, wherever you
  keep your projects (e.g. a `github/` folder on your machine — the path is yours).
- Commit and push it there when the work is done, so nothing is lost and others
  can use it. The vault only *references* the repo; it does not contain it.
- **Never put secrets in the vault or in a repo** — no API keys, tokens, `.env`,
  or auth files.

That is the whole rule: notes here, code in its own external repo.

---

## 4. Content integrity

- Do not invent facts, metrics, quotes, or personal history. If a grounding skill
  does not have it, ask or leave it out.
- Preserve dates, names, numbers, and sources exactly when synthesizing.
- Keep the owner's voice; do not smooth it into generic AI prose.

---

## 5. End-of-run checklist

- [ ] Deliverable saved in the right `Areas/` path (not `working-dir/`).
- [ ] `FEEDBACK.md` entry appended for the skill(s) used.
- [ ] Any repeated lesson promoted into `SKILL.md` (+ `updated:` bumped).
- [ ] If code was involved, it's in its external repo — and no secrets anywhere.
- [ ] Told the user plainly what was done.
