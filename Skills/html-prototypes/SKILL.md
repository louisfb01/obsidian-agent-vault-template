---
name: html-prototypes
description: "Build a quick HTML page when the owner asks for one: a prototype, a small tool, options to compare side by side, a plan, explainer or report, a diagram, a mini deck, or an editor that exports its result. One self-contained file, no build step, checked at desktop and phone width, then published as a Claude artifact, as a ChatGPT site from Codex, or opened locally. Use for any request for a page, prototype, mockup, tool or visual explainer in HTML."
updated: 2026-10-27
---

# HTML Prototypes

How to build quick HTML pages, whichever agent builds them and wherever they are published. The page is the same single file on every host; only the publishing step changes.

**Sources**, read from their raw HTML on 2026-10-27 (every quote below was checked against that text):

- "The unreasonable effectiveness of HTML": https://thariqs.github.io/html-effectiveness/ , its 20 examples, and the 11 examples of "Know your unknowns" (https://thariqs.github.io/html-effectiveness/unknowns/index.html).
- Simon Willison, "Useful patterns for building HTML tools" (10 December 2025): https://simonwillison.net/2025/Dec/10/html-tools/ , with his collection at https://tools.simonwillison.net/.

When you update this skill from those pages, read the pages themselves (download the HTML), never a tool's summary of them ([[AGENT-RULES]] §4).

## When a page beats Markdown

Make an HTML page instead of a Markdown answer when one of these is true:

- **Several options to choose from.** "Ask the agent to fan out across several directions and lay them next to each other so you can point at one — instead of reading three sequential walls of text". "Reacting is easier than imagining."
- **The information is spatial.** "Diffs and call-graphs are spatial information; markdown flattens them."
- **Motion or interaction is the question.** "Motion and interaction can't be described, only felt." A throwaway page "tells you in five seconds what a paragraph of prose never could."
- **A recurring document should get read.** Status updates and post-mortems "benefit most from a bit of structure and color."
- **A new topic needs navigating.** Collapsible sections, tabbed code and a glossary read "very differently from the same words dumped linearly."
- **The reader has to decide or edit something** and hand the result back (see Editors below).

Anything that must keep running, update itself or carry real users is no longer a prototype: give it its own repo ([[AGENT-RULES]] §7).

## How the source pages are built

All 33 pages of the html-effectiveness site (as of 2026-10-27) follow the same recipe. Copy it:

- **Nothing external.** No external scripts, no external stylesheets, no web fonts: "Each one trades a document you'd skim for one you'd actually read — open any of them directly in a browser."
- **System font stacks as tokens** on `:root`: `--serif: ui-serif, Georgia, "Times New Roman", Times, serif`, `--sans: system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`, `--mono: ui-monospace, "SF Mono", Menlo, Monaco, Consolas, monospace`. Serif for headings and reading text, mono for code, paths, labels and numbers.
- **A small palette as tokens** on `:root` (one warm accent, one success color, a ladder of neutrals), named by role or color, never hard-coded in rules.
- **A viewport meta tag, CSS grid layouts, a reading column of about 640 to 980 px, and one or two `@media (max-width: …)` breakpoints between about 560 and 900 px** so the page reflows on a phone. `clamp()` for type that scales.
- **Native elements first:** `<details>` for collapsible steps, `position: sticky` for an "On this page" list, real `<button>`s, `<table>` for tables, inline `<svg>` for figures, `data-` attributes as JavaScript hooks.
- **A copy helper on every page that hands text back:** `navigator.clipboard.writeText`, a hidden-textarea fallback, and the button reading "Copied" for about 1.6 seconds.
- **Little JavaScript.** The slide deck is 27 lines (arrow keys plus an `IntersectionObserver` that updates the "1 / 6" counter); the drag-to-reorder prototype is "~40 lines of JS, no libraries".
- **No saved state.** The prototypes say so: "Order persists in the DOM only — refresh to reset."
- **The request at the top.** Most examples open with a "Prompt" block, and every "Know your unknowns" page "shows the exact prompt at the top and the artifact Claude produced below it: paste the prompt, get something like the page."

## Build rules

1. **One self-contained file.** "A single file: inline JavaScript and CSS in a single HTML file means the least hassle in hosting or distributing them". Images as inline SVG or small data URIs.
2. **No React, no build step.** "I prompt “no react” and skip that whole rabbit hole entirely." Attempts with React "take longer to display" and "are more likely to contain crashing bugs".
3. **Keep it small.** "A few hundred lines means the maintainability of the code doesn't matter too much: any good LLM can read them and understand what they're doing".
4. **Libraries only when they earn it,** from a CDN with the version in the URL: "The fewer dependencies the better", and CDNs are trustworthy "especially for URLs that include the package version". On a Claude artifact only the allowed CDNs load (Hosts, below).
5. **Phone and desktop.** It works at 390 px wide with 16 px side gutters and no horizontal scroll, and at desktop width. Many readers open pages on a phone; one example asks to "Make it easy to skim on a phone".
6. **Tokens for color and type** (above). The source pages are light only; on a Claude artifact also define the dark tokens the host requires, and when comparing visual options add a light/dark switch as the empty-state example does.
7. **Real data, or labelled sample data.** Use real numbers and sources when they exist. A mock says it is one: "Everything above is fake data in one static file". Numbers on the page must agree with each other, and every link must go somewhere real.
8. **Copy and paste as the main input and output.** "One of the most useful input/output mechanisms for HTML tools comes in the form of copy and paste." Add "Copy to clipboard" buttons, because "Copy and paste on mobile phones is fiddly".
9. **Every editor ends with an export.** "Always end with an export button that turns whatever you did in the UI back into something you can paste into the agent or commit." The examples use "Copy as markdown", "Copy diff", "Copy full JSON", "Copy prompt" and "copy reply", next to "Reset" and a live "0 changed" count.
10. **State only when it helps.** For a page someone will bookmark or share, "you can store a lot of state directly in the URL". For larger state, `localStorage` ("without exposing that data to the server"), wrapped in `try/catch`, and the page must still work when it is empty.
11. **Files in and out without a server.** "You don't need to upload a file to a server in order to make use of the <input type="file"> element." "An HTML tool can generate a file for download without needing help from a server."
12. **Browser APIs only with open CORS.** "APIs that provide open CORS headers are a goldmine for HTML tools" (for example GitHub raw files, PyPI, Bluesky). An LLM API key never goes in the page: "if you bake that key into your visible HTML anyone can steal it"; ask the viewer for theirs and keep it in `localStorage`.
13. **Heavier compute stays in the browser** when needed: Pyodide ("a distribution of Python that's compiled to WebAssembly"), or a WebAssembly port such as Tesseract.js for OCR.
14. **Start from a working example.** "An LLM with one or two existing tools in their context is much more likely to produce working code." Look for an earlier page of yours, or an example in the sources, before writing from scratch.
15. **Say where it came from.** The request at the top, and a footer with the sources and the date, like the status report's "Sources: git log main..HEAD · CI dashboard · deploy log".
16. **Accessible basics.** Real buttons and labels, visible focus, contrast that holds in every theme, and a keyboard path for anything draggable. The drag prototype lists its own as an open question: "Keyboard path: is Alt + Arrow to move the focused row enough for the first ship?"

## Patterns by job

Each pattern names the example to open for the real thing.

- **Options to choose from** (01, 02, unknowns 03). Three or four directions side by side, rendered from the same data: "Same data, four philosophies" and "the only variable is the design". Each gets a label ("A — Minimal"), a one-line stance ("Show everything, waste nothing, let the anomalies pop."), pros and cons, a metrics row ("Bundle impact", "Testability", "Reuse") and a "best for" note, then a recommendation. Chips to "steal" or "skip" details assemble a reply: "your picks assemble a reply at the bottom of the page."
- **Brainstorm** (unknowns 05). Ten options "from cheapest to most ambitious", placed on a scale from "Ship this afternoon" to "Quarter-long bet", each with its size (S, M, L), the evidence it rests on ("Found in code"), its impact, and a "This resonates" box that feeds the reply.
- **Mock before you wire** (08, unknowns 04). "Before wiring anything up, make a single HTML file mocking Acme's new frame-annotation toolbar with fake data." Switch between layouts with buttons, list the design decisions baked in under "What you're feeling" ("so you can push back on them"), and end with open questions answered by chips: "Tap a chip to record your pick — the reply template below fills itself in."
- **Animation sandbox** (07). The motion in isolation, driven by one class toggle and a shared `--ease` custom property, with buttons to swap the easing ("Swaps --ease across every transition so you can feel the difference"), the keyframe timings listed, and a "Copy-paste CSS" block.
- **Plan** (16, unknowns 08). Header chips for the scope ("Effort", "Surfaces touched", "New tables", "Feature flag"), milestones, a data-flow diagram with its legend in a sentence ("Solid = request/response path. Dashed clay = realtime fan-out."), rough mockups ("Not pixel-final"), the key code ("The two pieces most likely to be done wrong"), and a risk table. A plan for review is "sorted by likelihood-of-tweaking, not execution order": decisions first, each with its alternative and "Pick this if:", then the build order, then the mechanical work collapsed.
- **Explainer** (14, 15, unknowns 02). A TL;DR first, the "Files read", expandable steps with file and line, tabbed snippets, "Gotchas" and an FAQ. For a concept: the problem in two sentences, one live demo with buttons and a caption saying what to notice ("every dot outside that arc keeps its color. That's the whole idea."), a comparison table and a short glossary. To teach a domain: a vocabulary ladder with a sample phrase per term, "What good looks like", and "Prompts you couldn't have written an hour ago".
- **Report** (11, 12). Key numbers first ("14 PRs merged"), highlights as bold outcomes, a table with a risk column, one small chart with a caption, carryover grouped by status, sources and the date in the footer. An incident adds "On this page", a header with severity, status, duration and owner, a TL;DR, a timestamped timeline that keeps the wrong first guess, the root cause with the diff, an impact table, and action items with an owner and a date.
- **Code review and walkthroughs** (03, 04, 17). A risk map per file ("safe", "worth a look", "needs attention"), comments labelled "Blocking" or "Nit" on the exact line, collapsible source per step with its file path and lines, a "Gotchas" list, before and after, and a file-by-file tour "Ordered for reading, not alphabetically."
- **Diagram** (10, 13). Inline SVG with its own rules: "Each SVG carries its own <style> block so the download stands alone", a "Download SVG" button, flat fills ("no drop shadows or gradients"), "Strokes are 1.5px for neutral boxes, 2px for emphasised containers", and a legend. In a flowchart, "Click any step to see what runs, how long it usually takes, and where it can short-circuit."
- **Mini deck** (09). "A handful of <section> tags and twenty lines of JS is a slide deck": arrow keys, a "1 / 6" counter, one decision slide with the options spelled out.
- **Editors** (18, 19, 20). The exact thing being edited, with drag between columns and filters (triage board), toggles with dependency warnings (feature flags: "1 flag is enabled without its prerequisite"), or a template with live previews and unknown slots flagged (prompt tuner), each ending in its copy-out button.
- **Before, during and after the work** (unknowns 01, 06, 07, 09, 10, 11). A blindspot pass with one card per gap, "Why it bites" and a copyable corrective prompt; an interview "one question at a time", "ordered by architectural blast radius"; a semantics map before a port ("Nothing gets implemented until you sign off on this page."); a running log of deviations with the "Conservative choice" made; a pitch that leads with the demo and answers reviewers' questions with references; a quiz that is "Not trivia — each one is a decision you'd have to make correctly during an incident or a review."

## Hosts

### Claude artifact (Claude Code or claude.ai)

Use when the owner is working with Claude and wants a link or a private page to look at or share. It is private until they share it. Simon Willison's caution applies to every chat host: they "run the tools inside a tight sandbox with a lot of restrictions" and are "often unable to load data or images from external URLs", so keep the page self-contained.

- In Claude Code, the Artifact tool's own instructions win over this section. Before writing, run its quickstart or load the `artifact-design` skill; load `artifact-capabilities` before using any runtime feature (saved data, shared state, asking Claude).
- The page contract (as of 2026-10-27): a `<title>` of two to four words; colors as tokens on `:root`, redefined for dark mode under `@media (prefers-color-scheme: dark)` with `:root:not([data-theme="light"])` and again under `:root[data-theme="dark"]`; an explicit `body` background; scripts only from cdnjs.cloudflare.com, cdn.jsdelivr.net/npm, unpkg.com, cdn.tailwindcss.com or code.jquery.com, each at an exact version at least two weeks old; stylesheets only from Google Fonts; 16 MB at most, data URIs included.
- Write the file in the session's scratchpad (or the task's `working-dir/<task>/` if it should be kept), publish it, and republish from the same file path to keep the same link.
- Never make a page that imitates a real company, person or record.

### ChatGPT site from Codex

Use when the page should live at a stable URL that Codex, or a scheduled task, keeps updating, under `https://<name>.<account>.chatgpt.site`.

- The site is a folder of static files, usually `dist/`, in its own git repo (§1, outside the vault), with `.openai/hosting.json` at the repo root: `{"static": {"directory": "dist"}, "project_id": "appgprj_..."}`. Access is either public or owner-only.
- Publish with Codex's Sites hosting workflow: package the exact validated commit, save a new version, deploy it to the existing project with its existing access, poll until it reaches a final state, then open the live URL and check it for console and data errors.
- Reuse the project named in `hosting.json`; never create a duplicate. A new site is owner-only unless the owner says it should be public.
- Keep the page working when opened straight from disk, so it can be checked without deploying.

### Local only

For a throwaway, write `working-dir/<task>/index.html` and open it in the browser. Move it to a host only if the owner wants to share it.

## Check before handing over

1. Open it for real: Chrome, or headless Chrome or Playwright from a coding agent, which "can test the code themselves while they work on it". Look at desktop width and at 390 px.
2. Nothing overlaps or overflows, the console is clean, every anchor is unique, every link resolves, and the numbers agree with each other and with their source.
3. Every button works, especially the export, copy and reset.
4. On a host, check the published page, not only the local file.
5. Hand over the link (or the path) with one line on what it shows, and a screenshot in the chat when the owner is reviewing a visual.

## Guardrails

- No secrets or API keys in the page, the repo or the vault.
- Nothing from private notes ([[AGENT-RULES]] §1) on a public site.
- Do not invent facts, file paths or numbers to fill a page; mark sample data as sample.
- A ChatGPT site is deployed to its existing project only; nothing goes public without the owner saying so.

## Feedback log

After each run, add an entry to [[Skills/html-prototypes/FEEDBACK|FEEDBACK]]. When a lesson repeats, promote it into this file. Rules: [[AGENT-RULES]] §5.
