---
type: reference
status: active
created: 2026-10-27
updated: 2026-10-27
summary: "Step 8c of the weekly vault maintenance run: grade how the skills did in the week's Claude Code and Codex sessions and draft skill edits for the owner to approve. Adapted from Warp's skill-doctor skill; the scan script and thresholds may need tuning after the first runs."
tags:
  - reference
  - skills
  - maintenance
---

# Skill health review (step 8c)

Every week the maintenance run grades how the skills did in the past week's real sessions, then drafts the smallest skill edits that would have prevented the failures it found. It never edits a skill. The owner approves or rejects the drafts in a session.

## Source

Adapted from Warp's skill-doctor skill: https://github.com/warpdotdev/common-skills/blob/main/.agents/skills/skill-doctor/SKILL.md (MIT licence, commit `7c4eb852d` of 2026-10-09), read in full from the raw files on 2026-10-27 with its `references/skill-improvements.md` and its four `scorers/*.md`. What we kept:

- Grade from real conversations, not from how the skill files look.
- Four scores per session (efficiency, procedure compliance, verbosity, output quality) plus skill coverage.
- Propose a change only when the evidence clears a strict bar, and draft it as a full file plus a diff without touching the real skill.
- Transcripts never leave the machine.

What we changed:

- The scan is our own script, `scripts/skill_health.py`, so the run does not execute downloaded code. It also checks this vault's rules (`FEEDBACK.md` logging, the agent log, the skills index).
- Warp's code-quality score becomes output quality, since many agent sessions produce writing, posts or pages, not code.
- The vault's own `FEEDBACK.md` entries count as evidence too.
- No Warp report page and no link to Warp's product.

## 1. Scan

```bash
python3 Skills/vault-maintenance/scripts/skill_health.py \
  --days 7 \
  --triggers Skills/vault-maintenance/references/skill-triggers.json \
  --private-paths <private folders from AGENT-RULES.md §1> \
  --out "working-dir/vault-maintenance/skill-health/YYYY-MM-DD" \
  --evidence "$HOME/.local/state/vault-skill-health/YYYY-MM-DD"
```

Run it from the vault root. It reads `~/.claude/projects/*/*.jsonl` and `~/.codex/sessions/**/rollout-*.jsonl` from the last 7 days and skips machine sessions: Codex approval reviewers and subagents, MCP and exec workers, and health pings. It writes:

- `skill-health.json` (in the vault):
  - which skills each session opened, skill coverage, and skills nobody opened;
  - lint flags per skill: name versus folder, description, `updated:`, size, `FEEDBACK.md`, index block;
  - promotion candidates: open entries that propose a change;
  - report emails found and whether they were sent;
  - the flagged sessions, with no session text.
- Condensed transcripts of up to 10 flagged sessions, written **outside the vault**. Sessions that touch a private skill or private folder are counted but never excerpted.

A session is flagged when:

- the owner repeated an instruction or corrected the agent twice or more;
- the first request matched a skill in `skill-triggers.json` that was never opened (edit that file to list your skills);
- it opened a skill but wrote no `FEEDBACK.md` entry for it (sessions after `--feedback-since`, the day your feedback logs started);
- or it wrote to the vault without an agent-log line.

The patterns are rough. Read each flagged session before scoring it, and drop false flags.

## 2. Score each flagged session

Read the condensed transcript and give each score a label and one to three sentences that cite the moment. The label tables are Warp's.

| Score | Labels (score) | What it asks |
|---|---|---|
| Efficiency | highly_efficient (1), mostly_efficient (0.8), mostly_inefficient (0.4), highly_inefficient (0.2) | "Whether the agent worked directly toward its result, or wasted effort on redundant steps, avoidable rework, or unnecessary back-and-forth." Repeated correction from the owner is the most expensive waste. Routine steps done the long way count extra, because they recur every run until a skill fixes them. |
| Procedure compliance | fully_compliant (1), mostly_compliant (0.8), noncompliant (0.2) | Whether the agent followed `AGENT-RULES.md` and every skill its task triggered, to the end. Here that means: §0 (rules read, skill and open `FEEDBACK.md` entries loaded), the skill's own steps and checks, its approval rules, and §9 (`FEEDBACK.md` entry, agent-log line). A breach of a protective rule (delete, send or publish without approval, secrets, private content) is disqualifying on its own. |
| Verbosity | proportionate (1), verbose (0.2), terse (0.1) | Whether the agent's messages matched the work: no padding or restated summaries, and nothing the owner needed left out. |
| Output quality | approve (1), block (0.2), insufficient_evidence (0.5) | Our version of Warp's code quality: would the owner accept what was produced (post, email, page, deck, code) without a fix? A defect they had to point out counts against it even if it was fixed later. Use `insufficient_evidence` when the output is not in the transcript; it is left out of the average. |

## 3. Aggregate

- Raw score: the mean of each score across the scored sessions.
- Report score: `0.5 + 0.5 × raw` (Warp's curve).
- `overall = 0.25 × efficiency + 0.25 × output quality + 0.2 × procedure compliance + 0.15 × verbosity + 0.15 × skill coverage` (Warp's weights).
- A session **failed** when any raw score is below 0.5. Only failed sessions can justify a skill edit.
- Add one row to `working-dir/vault-maintenance/skill-health/trend.md` (create it with a header the first time): date, sessions, skill coverage, the four report scores, overall, failed sessions, edits proposed. The trend matters more than one week's grade.

## 4. Decide what to propose

Warp's rules, kept close to their wording:

- Cluster the failures by root cause, then rank them by how often and how badly they happened.
- **Verify first.** Open the current `SKILL.md` and `FEEDBACK.md` of the skill involved. Many corrections are already written in, sometimes by the same session. Drop what is already covered.
- **Propose a change only when all of these are true:**
  - a missing, wrong or underspecified instruction in a named skill (or in `AGENT-RULES.md`) caused the failure;
  - you can state the one reusable rule it should have had;
  - with that rule followed, the failure would not have happened;
  - the same gap shows up in more than one session, or once but badly enough to prove the gap.
- **Do not propose when:**
  - the instruction already existed and the agent ignored it (note it as a compliance failure instead);
  - it was one-off model variance;
  - the only possible edit restates, hedges or adds examples from these sessions;
  - the real fix is in a tool, a script or a repo, not in the skill (say where it is).
- Prefer **replacing** a line over adding a paragraph. Make the smallest edit that expresses the rule, and state that rule in one sentence first.
- A skill whose job came up but which was never opened usually has a description problem: propose a description edit.
- When nothing clears the bar, propose nothing, and say per finding why not. "A speculative change is worse than none."

## 5. Write it up

In `working-dir/vault-maintenance/skill-health/YYYY-MM-DD/`:

- `report.md`, with frontmatter (`type: review`):
  - the scores;
  - the three most important findings, in plain words;
  - each proposal: skill, the one-sentence rule, the evidence (session id, score and moment, in your own words), and the path of its draft;
  - the findings that did not clear the bar, with the reason;
  - the lint flags and promotion candidates from the scan, as a short list.
- `proposed/<skill>/SKILL.md`: the full proposed file. `proposed/<skill>.diff`: `diff -u` against the current file. For a proposed new skill, the full new file.

In the recap (step 11, if you send one), `skill_health` is a short list: the overall score and trend, the three findings, the number of proposals and the folder path. No transcript text.

## Applying proposals

Only in a session with the owner. When they say which proposals to apply ("apply the skill-health proposals from <date>", or a subset), the agent:

1. checks that the skill has not changed since the draft;
2. applies the edit;
3. bumps `updated:`;
4. adds a `FEEDBACK.md` entry marked `promoted YYYY-MM-DD` that cites the report;
5. ticks the proposal in `report.md`.

Rejected proposals are marked rejected there, with the reason, so the next run does not propose them again.

## Privacy

- Transcripts and excerpts stay in the evidence folder outside the vault. The vault and the recap get scores, session ids and findings in our own words, never pasted session text.
- Never copy a secret, password, key or personal detail seen in a transcript anywhere, not even into the report as an example.
- Private skills and private folders (`AGENT-RULES.md` §1): count only.
