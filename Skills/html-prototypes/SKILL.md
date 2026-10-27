---
name: html-prototypes
description: "Build a quick HTML page when the owner asks for one: a prototype, a small tool, options to compare side by side, a plan, explainer or report, a diagram, a mini deck, or an editor that exports its result. One self-contained file, no build step, checked at desktop and phone width, then published as a Claude artifact, as a ChatGPT site from Codex, or opened locally. Use for any request for a page, prototype, mockup, tool, dashboard-like view or visual explainer in HTML."
updated: 2026-10-27
---

# HTML Prototypes

How to build quick HTML pages, whichever agent builds them and wherever they are published. The page is the same single file on every host; only the publishing step changes.

Sources (read 2026-10-27): the 31 example pages of "HTML effectiveness" (https://thariqs.github.io/html-effectiveness/, including its "Know your unknowns" series) and Simon Willison's "Useful patterns for building HTML tools" (https://simonwillison.net/2025/Dec/10/html-tools/, examples at https://tools.simonwillison.net/). Quotes below are from those pages.

## When a page beats Markdown

Make an HTML page instead of a Markdown answer when:

- the reader will skim, not read, and structure and color will get it read (recurring reports, status, incidents);
- the information is spatial: diffs, call graphs, flows, timelines. Markdown "flattens" them;
- there are several options to compare: "Reacting is easier than imagining", so show them side by side;
- motion or interaction is the point: a prototype shows in "five seconds" what "a paragraph of prose never could";
- the reader has to decide or edit something and paste the result back.

For anything that must keep running, update itself or carry real users, it is no longer a prototype: give it its own repo ([[AGENT-RULES]] §7).

## Build rules

1. **One self-contained file.** Inline CSS and JavaScript in a single `index.html`: "the least hassle in hosting or distributing them". Images as inline SVG or small data URIs.
2. **No build step and no React.** Plain HTML, CSS and DOM events ("I prompt “no react” and skip that whole rabbit hole entirely"). Most interactions need 20 to 40 lines of JavaScript.
3. **Small.** A few hundred lines, so the next agent can read and rewrite the whole file.
4. **Libraries only when needed,** from a CDN with an exact pinned version (for example `.../chart.js@4.4.1/...`). On a Claude artifact only the allowed CDNs work (below).
5. **Phone first.** It works at 390 px wide with 16 px side gutters and no horizontal scroll, and at desktop width. Many readers open pages on a phone.
6. **Color as tokens** on `:root`, with a dark version, and an explicit `body` background. A light/dark toggle is worth adding when comparing visual options.
7. **Real data, or clearly fake data.** Use the real numbers and sources when they exist. A mock uses labelled sample data ("Before wiring anything up, make a single HTML file mocking [feature] with fake data"). Numbers on the page must agree with each other, and every link must go somewhere real (no `href="#"`).
8. **State.** Shareable state goes in the URL ("you can store a _lot_ of state directly in the URL"). Per-viewer conveniences can use `localStorage`, wrapped in `try/catch`, and the page must still work when it is empty. A prototype may simply say "Refresh to reset."
9. **Input and output without a server.** Copy and paste is "one of the most useful input/output mechanisms"; read files with a file input instead of uploading them; build downloads in the browser.
10. **APIs from the browser** only when they send open CORS headers. Never put an API key in the page ("if you bake that key into your visible HTML anyone can steal it"); if the viewer must supply one, take it in an input and keep it in `localStorage`.
11. **Every editor ends with an export.** "Copy as markdown", "Copy diff", "Copy full JSON", "Copy prompt" or "Copy reply", plus "Reset" and a live "N changed" count. A page that changes something but cannot hand the change back is unfinished.
12. **Show where it came from.** Sources, files read, and a "generated YYYY-MM-DD" line at the foot.
13. **Accessible basics.** Real buttons and labels, visible focus, text contrast that holds in both themes, and a keyboard path for anything draggable (or list it as an open question).

## Patterns by job

- **Options to choose from.** Three or four directions side by side, all rendered from the same data so only the design varies. Each gets a label (A to D), a one-line stance, pros and cons, a "best for" note and a small metrics row; end with a recommendation. Let the reader tap chips to keep or skip details, and assemble the picks into a "Copy reply" to paste back to the agent.
- **Plan, explainer or pitch.** TL;DR first, then numbered sections, one idea each. A sticky "On this page" contents list with a unique anchor per section. Header chips for scope (effort, files touched, risk). A risk table tagged high, medium or low. Open questions, each with who decides. In a plan, put the judgment calls first (with alternatives and "pick this if"), then the build order, then the mechanical work collapsed. In an explainer, lead with the problem and a short answer, then the mechanism, a comparison table, a short glossary and one live demo with a caption saying what to notice.
- **Report.** A row of key numbers first, highlights as bold outcomes, a table with a risk or status column, one simple chart with a caption, then items grouped by status. An incident adds the header facts (severity, status, duration, owner), a timestamped timeline including the wrong guesses, the root cause, and action items with an owner and a date.
- **Code review or walkthrough.** A per-file risk map ("safe", "worth a look", "needs attention") linking to each file, labelled comments ("Blocking", "Nit"), and collapsible source per step with its file path and line range.
- **Interaction or animation prototype.** Native events, one class toggle per state, a shared easing token as a CSS custom property, small controls to tune it (for example linear, ease-out, spring), a "Copy CSS" block, and open questions at the end.
- **Diagram.** Inline SVG, each with its own `<style>` so a download stands alone, and a "Download SVG" button. Flat fills, one stroke width for normal lines and a heavier one for emphasis, a legend (solid for request and response, dashed for async). Clicking a node can reveal what it does.
- **Mini deck.** One `<section>` per slide, arrow keys to move, a "1 / 6" counter, about twenty lines of JavaScript.
- **Custom editor.** Drag between columns, click a tag to filter, a live preview beside the input, and the export from rule 11.
- **Quiz or review gate.** Scenario questions, a live score, and a checklist that unlocks only at a passing score. Check every file path and line number it cites; generated ones are often invented.

## Hosts

### Claude artifact (Claude Code or claude.ai)

Use when the owner is working with Claude and wants a link, or a private page to look at or share. It is private until they share it.

- In Claude Code, the Artifact tool's own instructions win over this section. Before writing, run its quickstart or load the `artifact-design` skill; load `artifact-capabilities` before using any runtime feature (saved data, shared state, asking Claude).
- The page contract (as of 2026-10-27): a `<title>` of two to four words; colors as tokens on `:root`, redefined for dark mode under `@media (prefers-color-scheme: dark)` with `:root:not([data-theme="light"])` and again under `:root[data-theme="dark"]`; an explicit `body` background; scripts only from cdnjs.cloudflare.com, cdn.jsdelivr.net/npm, unpkg.com, cdn.tailwindcss.com or code.jquery.com, each at an exact version at least two weeks old; stylesheets only from Google Fonts; 16 MB at most, data URIs included.
- Write the file in the session's scratchpad (or the task's `working-dir/<task>/` if it should be kept), publish it, and republish from the same file path to keep the same link.
- Never make a page that imitates a real company, person or record.

### ChatGPT site from Codex

Use when the page should live at a stable URL that Codex (or a scheduled task) updates, under `https://<name>.<account>.chatgpt.site`.

- The site is a folder of static files, usually `dist/`, in its own git repo (§1, outside the vault), with `.openai/hosting.json` at the repo root: `{"static": {"directory": "dist"}, "project_id": "appgprj_..."}`. Access is either public or owner-only.
- Publish with Codex's Sites hosting workflow: package the exact validated commit, save a new version, deploy it to the existing project with its existing access, poll until it reaches a final state, then open the live URL and check it for console and data errors.
- Reuse the project named in `hosting.json`; never create a duplicate. A new site is owner-only unless the owner says it should be public.
- Keep the page working when opened straight from disk, so it can be checked without deploying.

### Local only

For a throwaway, write `working-dir/<task>/index.html` and open it in the browser. Move it to a host only if the owner wants to share it.

## Check before handing over

1. Open it for real: Chrome, or headless Chrome or Playwright from a coding agent ("can test the code themselves while they work on it"). Look at desktop width and at 390 px.
2. Nothing overlaps or overflows, the console is clean, every anchor is unique, every link resolves, and the numbers agree with each other and with their source.
3. Every button works, especially the export and reset.
4. On a host, check the published page, not only the local file.
5. Hand over the link (or the path) with one line on what it shows, and a screenshot in the chat when the owner is reviewing a visual.

## Guardrails

- No secrets in the page, the repo or the vault.
- Nothing from private notes ([[AGENT-RULES]] §1) on a public site.
- Do not invent facts, file paths or numbers to fill a page; mark sample data as sample.
- A ChatGPT site is deployed to its existing project only; nothing goes public without the owner saying so.

## Feedback log

After each run, add an entry to [[Skills/html-prototypes/FEEDBACK|FEEDBACK]]. When a lesson repeats, promote it into this file. Rules: [[AGENT-RULES]] §5.
