---
type: skill-index
status: active
updated: 2026-10-27
tags: [skills, ai-os]
---

# Skills Index

The map. Use this first to pick which skill to load. Each `SKILL.md` is the source of truth; this note only points to it.

## Agent Quick Start

0. Read [[AGENT-RULES|Agent Rules]] first if you have not in this session. It says where outputs go and what to check at the end of a run.
1. Choose the task type in [[#Choose the right skill]].
2. Open the linked `SKILL.md` before doing the work. This index is only the map; the skill file is the source of truth. Read the open entries in the skill's `FEEDBACK.md` too.
3. Combine a grounding skill with an output skill when the task needs both content and voice.
4. Do not invent the owner's personal history, client stories, tool usage, metrics or opinions. Use the grounding skill.
5. After the run, add an entry to each used skill's `FEEDBACK.md` ([[AGENT-RULES]] §5). Lessons go there, not only into one agent's memory.

## Hierarchy (load lower layers to ground higher ones)

- **Grounding**: who you are, background, positioning.
- **Voice**: how things sound: [[Skills/example-voice/SKILL|Example Voice]].
- **Research**: turn sources into a plan.
- **Output**: the deliverable skills (each loads grounding and voice), for example [[Skills/html-prototypes/SKILL|HTML Prototypes]] for quick pages and tools.
- **Vault operations**: keeping the vault healthy: [[Skills/vault-maintenance/SKILL|Vault Maintenance]].
- **Scheduled tasks**: every scheduled task runs a skill, and every run also loads [[Skills/scheduled-runs/SKILL|Scheduled Runs]]. The scheduler's prompt only points to the skill (`Templates/Scheduled task prompt.md`); the task table is in [[AGENT-RULES]] §1.

## Choose the right skill

> One block per skill. Keep the six fields.

### Example Voice

**File:** [[Skills/example-voice/SKILL]]

**Use when:** a draft needs to sound like you (tone, anti-slop, first person).

**Main output:** a voice pass on an existing draft, not a first draft.

**Also load:** the output skill that wrote the draft.

**Do not use for:** generating structure from scratch.

**Guardrails:** never invent facts to make a line land better.

### Vault Maintenance

**File:** [[Skills/vault-maintenance/SKILL]]

**Use when:** the weekly scheduled run, or you ask to tidy hubs, fix broken links, link orphans, or check the vault against [[AGENT-RULES|Agent Rules]].

**Main output:** updated hub and index links, a dated entry in `working-dir/vault-maintenance/weekly-log.md`, a refreshed `state.json`, a rules-health report, and a skill-health report with drafted skill edits for you to approve.

**Also load:** [[AGENT-RULES|Agent Rules]].

**Do not use for:** reorganising folders, archiving or deleting notes, or rewriting note content.

**Guardrails:** never delete, move or rename notes. Never edit personal prose. Rule gaps are reported, not fixed, and skill edits are only drafted. Session transcripts stay outside the vault.

### HTML Prototypes

**File:** [[Skills/html-prototypes/SKILL]]

**Use when:** you ask for a page, prototype, mockup, small tool, options to compare, a visual plan, explainer or report, a diagram or a mini deck in HTML, published as a Claude artifact, a ChatGPT site from Codex or a local file.

**Main output:** one self-contained HTML file, checked at desktop and phone width, published where you want it.

**Also load:** the host's own instructions (for example the artifact tool's), and your voice skill when the page carries public copy.

**Do not use for:** production websites, or anything that needs a build step or a backend.

**Guardrails:** no secrets or API keys in the page; nothing private on a public site; sample data labelled as sample.

### Scheduled Runs

**File:** [[Skills/scheduled-runs/SKILL]]

**Use when:** any scheduled run, together with the task's own skill, or when you set up or fix a scheduled task.

**Main output:** a run that starts and ends the same way every time: no duplicate sends, one report, the tabs it opened closed, state and feedback recorded.

**Also load:** [[AGENT-RULES|Agent Rules]] and the task's skill.

**Do not use for:** interactive work, or the steps of a single task (those live in the task's skill).

**Guardrails:** the task's skill wins where they differ. Never edit a skill or a prompt during a scheduled run.

## Maintenance notes

- When a new skill is added, update [[#Hierarchy (load lower layers to ground higher ones)|Hierarchy]] and [[#Choose the right skill]], and give the skill folder a `FEEDBACK.md` (template: `Templates/Skill feedback.md`).
- Each block keeps six fields: File, Use when, Main output, Also load, Do not use for, Guardrails.
- Link to the actual `SKILL.md`; do not copy the skill body here.
- A scheduled task gets a skill and a row in the [[AGENT-RULES]] §1 task table; its procedure never lives in the scheduler's prompt.
