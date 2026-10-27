---
name: vault-maintenance
description: "Weekly maintenance of this Obsidian vault: inventory and diff against the last snapshot, keep hub and index notes current, check wiki links and orphans, report where AGENT-RULES.md is not followed, and log the run. Run it from any scheduler, or on request."
updated: 2026-10-27
---

# Vault Maintenance

Keeps the vault navigable as it grows. It is careful and local: it updates links and hub lists, and reports everything else. It never rewrites personal prose, reorganises folders, or deletes anything.

Steps 9, 11 and 12 are optional slots for steps that depend on your machine, such as closing browser tabs a run opened or sending a recap. Leave them out, or fill them in your own vault. When a scheduler runs this skill, it also loads [[Skills/scheduled-runs/SKILL|Scheduled Runs]].

## Run sequence

0. Read `AGENT-RULES.md` at the vault root, then the open entries in this skill's `FEEDBACK.md`. The rules bind this run; this skill adds the maintenance steps.
1. Inventory the vault, excluding `.obsidian/`, `.git/`, `.DS_Store` and generated OS cruft. Count Markdown files and major asset types.
2. Load or create `working-dir/vault-maintenance/state.json` and `working-dir/vault-maintenance/weekly-log.md`. The state file tracks file paths, mtimes, sizes, and a content hash for Markdown files. On the first run, create a baseline but still do a full index health pass.
3. Compare the current inventory with the prior state and classify:
   - added notes and assets
   - removed notes and assets
   - likely renamed notes and assets, inferred from matching basename, content hash or nearby path
   - recently modified notes, especially new files without inbound links
4. Read the relevant hub notes before editing and keep their style. Update only the list items or sections that need it. Keep wikilinks valid and readable.
5. Maintain the hubs named in the `AGENT-RULES.md` §1 folder map:
   - `START-HERE.md`: keep its hub links valid. It links hubs only, never single notes.
   - Each area hub (for example `Areas/Professional/Professional.md`): link sub-hubs and active project folders. Do not dump every generated asset into a hub.
   - The skills index: update only when a skill `SKILL.md` is added, removed or renamed. Do not rewrite skill instructions.
   - Project front notes and `working-dir/**/index.md`: update only when files inside that same folder were added, removed or renamed. Skip files marked as generated.
6. Run a wiki-link health check. Resolve links by vault-relative path, source-relative path, basename and extensionless match. Fix a broken link only when the intended target is clear; otherwise list it in the weekly log.
7. Find orphan notes outside `_archive/`, `raw/` folders and generated research sources. Link genuinely active orphans from the right hub. Report ambiguous or scratch notes instead of forcing them into a hub.
8. Note lightweight cleanup opportunities in the weekly log: duplicate or raw/cleaned meeting pairs, stale TODO lists, unreferenced assets, high-value notes with no inbound links, broken links with no obvious target.
8b. Rules health (report only; never rewrite notes to fix these). Check the vault against `AGENT-RULES.md` and record the results in the weekly log:
   - Skill folders without `FEEDBACK.md`, skill folders missing from the skills index, and index links to a `SKILL.md` that does not exist.
   - `FEEDBACK.md` files where two or more open entries propose the same rule change: list them as promotion candidates. Do not edit `SKILL.md`.
   - Project folders added since the last run that have no front note or are not linked from their hub.
   - Markdown notes added since the last run that have no frontmatter, excluding raw imports, `raw/` and `wiki/sources/` folders, generated files and private folders. Give the count and up to 20 paths; mark the ones named in this week's agent log as agent-written.
   - Root-level files or folders that are not in the `AGENT-RULES.md` §1 folder map.
   - Possible secrets: files named `.env*`, `*.pem`, `*.key`, `credentials*.json` or `token*.json`, and Markdown lines that look like API keys (`sk-`, `AIza`, `ghp_`, `xoxb-`). Report the path and line number only; never copy the value.
   - Agent log: whether `working-dir/agent-log/` has lines for this week, and which agents wrote them.
   - Scheduled tasks: if your scheduler keeps its prompts in files, check that each active task's prompt is a short pointer to a skill that exists (`Templates/Scheduled task prompt.md`) and that the task has a row in the `AGENT-RULES.md` §1 "Scheduled tasks" table. List the ones that fail.
9. Optional host housekeeping, for example closing stale browser tabs. Leave this out unless your setup needs it.
10. Save the updated state after successful edits. The weekly log entry includes the date, counts, changed hub files, added/removed/renamed files, broken links fixed and left, orphans linked and left, rules health findings, and 3 to 5 suggested next improvements. Add one line for this run to `working-dir/agent-log/YYYY-MM.md`.
11. Optional recap. If your scheduler can notify you (email, chat), send a short summary of the weekly log entry. Never put credentials in the vault.
12. Close or clean up anything this run opened (browser tabs, temporary files) and record it.

## Guardrails

- Do not delete, move or rename notes or assets.
- Do not edit private or personal content except to update links or add and remove index references.
- Keep existing headings and tone.
- Keep changes small, reviewable and focused on navigation health.
- Rules health (step 8b) is report-only: never add frontmatter, create FEEDBACK.md files, move folders or edit skills to fix a finding.
- If a change is ambiguous, write it to the weekly log instead of guessing.
- Local maintenance only: no web search.

## Final response format

- Whether the run completed.
- Hub and index files updated.
- Added, removed and renamed files found.
- Broken links fixed and left unresolved.
- Rules health findings in one or two lines.
- Top 3 suggested improvements.
- Link to `working-dir/vault-maintenance/weekly-log.md`.

## Feedback log

After each run, add an entry to [[Skills/vault-maintenance/FEEDBACK|FEEDBACK]] only when something about the procedure itself went wrong or should change. Routine results go in `working-dir/vault-maintenance/weekly-log.md`. Rules: [[AGENT-RULES]] §5.
