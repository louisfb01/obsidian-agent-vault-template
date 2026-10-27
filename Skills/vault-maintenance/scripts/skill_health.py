#!/usr/bin/env python3
"""Weekly skill health scan for the vault maintenance skill (step 8c).

Reads local Claude Code and Codex session files and the vault's skill folders, then writes:
  <out>/skill-health.json   counts, lint results and flagged sessions, with no session text
  <evidence>/<id>.md        condensed transcripts of flagged sessions, for scoring (keep outside the vault)

Local only, standard library only. Nothing is uploaded. Sessions that touch a private skill or a
private folder are counted but never excerpted. Practices adapted from Warp's skill-doctor
(https://github.com/warpdotdev/common-skills, MIT, commit 7c4eb852d); this script is our own.
"""
import argparse
import json
import re
import time
from datetime import date, datetime, timezone
from pathlib import Path

HOME = Path.home()
WRITE_TOOLS = {"Edit", "MultiEdit", "Write", "NotebookEdit"}
CORRECTION = re.compile(r"^(no\b|nope|wrong|that'?s not)|\b(not what i (asked|meant|wanted)|i (asked|wanted) (for|you to)|why did(n'?t)? you|you should(n'?t)? have|instead of|you (forgot|missed|ignored|removed))\b", re.I)
REPEAT = re.compile(r"\b(as i said|like i said|i (already )?(told|asked) you|i said (before|earlier)|never happens? again|for the (second|third) time|again\?|still (not|doesn'?t|isn'?t|wrong))\b", re.I)
TYPED_MAX = 1500  # longer user messages are pastes, not corrections
INJECTED = ("<", "# AGENTS.md", "Caveat:", "[Request interrupted", "This session is being continued", "Another Claude session sent")
MACHINE_FIRST = ("Reply with exactly", "The following is the Codex agent history", "# Shared brief")
MAX_MSG, MAX_TOOL, HEAD, TAIL = 1500, 300, 100, 40


def args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--vault", default=".")
    p.add_argument("--skills-folder", default="Skills")
    p.add_argument("--private-paths", nargs="*", default=[], help="the private folders listed in AGENT-RULES.md §1; sessions touching them are never excerpted")
    p.add_argument("--triggers", help="JSON file: skill name -> regex its job matches in a first request")
    p.add_argument("--feedback-since", default="", help="check FEEDBACK.md logging only for sessions after this date (YYYY-MM-DD); empty checks every session")
    p.add_argument("--days", type=int, default=7)
    p.add_argument("--max-flagged", type=int, default=10)
    p.add_argument("--include-subagents", action="store_true")
    p.add_argument("--status-roots", nargs="*", default=[str(HOME / "Documents"), str(HOME / "Downloads")])
    p.add_argument("--out", required=True)
    p.add_argument("--evidence", required=True)
    return p.parse_args()


def frontmatter(text):
    if not text.startswith("---"):
        return {}
    block = text.split("---", 2)[1]
    out = {}
    for key in ("name", "description", "updated", "private"):
        m = re.search(rf"^{key}:\s*(.+)$", block, re.M)
        if m:
            out[key] = m.group(1).strip().strip("\"'")
    return out


def lint_skills(skills_dir, index_text):
    rows = []
    for d in sorted(p for p in skills_dir.iterdir() if p.is_dir() and not p.name.startswith((".", "_"))):
        skill_md = d / "SKILL.md"
        if not skill_md.exists():
            rows.append({"skill": d.name, "flags": ["no SKILL.md"]})
            continue
        text = skill_md.read_text(errors="replace")
        fm = frontmatter(text)
        fb = d / "FEEDBACK.md"
        fb_text = fb.read_text(errors="replace") if fb.exists() else ""
        # An entry is a promotion candidate only when it is open and proposes a change.
        entries = re.split(r"^### ", fb_text, flags=re.M)[1:]
        candidates = [e.splitlines()[0][:80] for e in entries
                      if re.search(r"\*\*Status:\*\*\s*open", e, re.I)
                      and not re.search(r"\*\*Proposed rule change:\*\*\s*(none|n/a)\b", e, re.I)]
        block = re.search(r"^### [^\n]*\n\n\*\*File:\*\* \[\[%s/%s/SKILL" % (re.escape(skills_dir.name), re.escape(d.name)), index_text, re.M)
        fields = 0
        if block:
            seg = index_text[block.start(): index_text.find("\n### ", block.end())]
            fields = sum(f"**{f}:**" in seg for f in ("File", "Use when", "Main output", "Also load", "Do not use for", "Guardrails"))
        words = len(text.split())
        flags = []
        if fm.get("name") != d.name:
            flags.append(f"frontmatter name is {fm.get('name')!r}, folder is {d.name!r}")
        if not fm.get("description"):
            flags.append("no description")
        elif len(fm["description"]) > 1024:
            flags.append("description over 1,024 characters")
        if not fm.get("updated"):
            flags.append("no updated: date")
        if words > 5000:
            flags.append(f"{words:,} words loaded on every use")
        if not fb.exists():
            flags.append("no FEEDBACK.md")
        if not block:
            flags.append("no block in the skills index")
        elif fields < 6:
            flags.append(f"index block has {fields} of 6 fields")
        rows.append({"skill": d.name, "private": fm.get("private") == "true", "words": words,
                     "updated": fm.get("updated"), "feedback_entries": len(entries),
                     "promotion_candidates": candidates, "flags": flags})
    return rows


def user_text(rec):
    if rec.get("type") == "user":
        c = rec.get("message", {}).get("content")
        if isinstance(c, str):
            return c
        if isinstance(c, list):
            return "\n".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")
    p = rec.get("payload") or {}
    if rec.get("type") == "response_item" and p.get("type") == "message" and p.get("role") == "user":
        return "\n".join(b.get("text", "") for b in p.get("content", []) if isinstance(b, dict))
    return ""


def assistant_text(rec):
    if rec.get("type") == "assistant":
        return "\n".join(b.get("text", "") for b in rec.get("message", {}).get("content", []) or [] if isinstance(b, dict) and b.get("type") == "text")
    p = rec.get("payload") or {}
    if rec.get("type") == "response_item" and p.get("type") == "message" and p.get("role") == "assistant":
        return "\n".join(b.get("text", "") for b in p.get("content", []) if isinstance(b, dict))
    return ""


def tool_calls(rec):
    """(tool name, input text) for each tool call in one record."""
    out = []
    if rec.get("type") == "assistant":
        for b in rec.get("message", {}).get("content", []) or []:
            if isinstance(b, dict) and b.get("type") == "tool_use":
                out.append((b.get("name", ""), json.dumps(b.get("input", {}), ensure_ascii=False)))
    p = rec.get("payload") or {}
    if rec.get("type") == "response_item" and p.get("type") in ("function_call", "custom_tool_call", "local_shell_call"):
        out.append((p.get("name", "shell"), str(p.get("arguments") or p.get("input") or p.get("action") or "")))
    return out


SHELL_WRITE = re.compile(r"\*\*\* Begin Patch|(?<![0-9&])>>?\s*['\"]?[~/\w]|\btee\b|write_text\(|open\([^)]*,\s*['\"][wa]")


def is_write(name, text):
    return name in WRITE_TOOLS or name == "apply_patch" or bool(SHELL_WRITE.search(text))


def scan_session(path, harness, skills, private_skills, private_paths, triggers, include_subagents, vault):
    load_rx = re.compile(r"(%s)/+(?:SKILL\.md|scheduled-run\.md)" % "|".join(map(re.escape, skills)))
    fb_rx = re.compile(r"(%s)/+FEEDBACK\.md" % "|".join(map(re.escape, skills)))
    loaded, fb_written, entries, users = set(), set(), [], []
    touched_private, wrote_vault, wrote_log, source, cwd = False, False, False, "", ""
    first_load = None
    with path.open(errors="replace") as fh:
        for i, line in enumerate(fh):
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            if rec.get("type") == "session_meta":
                source = (rec.get("payload") or {}).get("source", "")
            payload = rec.get("payload") if isinstance(rec.get("payload"), dict) else {}
            cwd = rec.get("cwd") or payload.get("cwd") or cwd
            for name, text in tool_calls(rec):
                text = text.replace("\\'", "'")
                for m in load_rx.findall(text):
                    loaded.add(m)
                    first_load = i if first_load is None else first_load
                if any(p in text for p in private_paths):
                    touched_private = True
                if is_write(name, text):
                    fb_written.update(fb_rx.findall(text))
                    wrote_vault = wrote_vault or vault in text or str(cwd).startswith(vault)
                    wrote_log = wrote_log or "agent-log/" in text
                entries.append(("tool:" + name, text[:MAX_TOOL]))
            t = user_text(rec)
            if t and not t.lstrip().startswith(INJECTED):
                users.append((i, t.strip()))
                entries.append(("user", t.strip()[:MAX_MSG]))
            a = assistant_text(rec)
            if a.strip():
                entries.append(("assistant", a.strip()[:800]))
    # Codex approval reviewers and subagents ({"subagent": ...}), MCP and exec workers, and health pings are not the owner's sessions.
    machine = isinstance(source, dict) or source in ("mcp", "exec")
    if not users or (machine and not include_subagents) or users[0][1].startswith(MACHINE_FIRST):
        return None
    private = touched_private or bool(loaded & private_skills)
    first = users[0][1]
    scheduled = first.startswith(("Scheduled run:", "Automation:"))
    later = [t for i, t in users[1:] if first_load is None or i > first_load]
    reasons = []
    typed = [t for t in later if len(t) <= TYPED_MAX]
    corrections = sum(bool(CORRECTION.search(t)) for t in typed)
    repeats = sum(bool(REPEAT.search(t)) for t in typed)
    if repeats:
        reasons.append(f"user repeated an instruction {repeats}x")
    if corrections >= 2:
        reasons.append(f"user corrected {corrections}x")
    missed = [k for k, rx in triggers.items() if k in skills and k not in loaded and re.search(rx, first[:800], re.I)]
    if missed and not scheduled:
        reasons.append("request matched but skill not opened: " + ", ".join(missed))
    return {"id": path.stem[-36:], "file": str(path), "harness": harness, "scheduled": scheduled,
            "mtime": datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).date().isoformat(),
            "loaded": sorted(loaded), "feedback_written": sorted(fb_written), "wrote_vault": wrote_vault,
            "wrote_agent_log": wrote_log, "private": private, "user_messages": len(users),
            "corrections": corrections, "repeats": repeats, "missed": missed, "reasons": reasons,
            "_entries": entries}


def condensed(s):
    e = s["_entries"]
    if len(e) > HEAD + TAIL:
        e = e[:HEAD] + [("note", f"[... {len(e) - HEAD - TAIL} entries omitted ...]")] + e[-TAIL:]
    head = [f"# Session {s['id']} ({s['harness']}, {s['mtime']})", "",
            f"Skills opened: {', '.join(s['loaded']) or 'none'}. FEEDBACK.md written for: {', '.join(s['feedback_written']) or 'none'}.",
            f"Flagged because: {'; '.join(s['reasons'])}.", ""]
    return "\n".join(head + [f"**{role}:** {text}" for role, text in e]) + "\n"


def email_statuses(roots, days):
    cut = time.time() - days * 86400
    out = []
    for root in roots:
        for f in Path(root).rglob("email-send-status.json"):
            try:
                # Preflight, dry-run and no-send folders hold deliberate test renders.
                if f.stat().st_mtime < cut or any(w in part for part in f.parts[-3:-1] for w in ("preflight", "no-send", "dry-run")):
                    continue
                d = json.loads(f.read_text())
            except (OSError, ValueError):
                continue
            out.append({"path": str(f), "sent": bool(d.get("sent")), "has_message_id": bool(d.get("message_id"))})
    return sorted(out, key=lambda r: r["path"])


def main():
    a = args()
    vault = Path(a.vault)
    skills_dir = vault / a.skills_folder
    index_files = list(skills_dir.glob("*Skills*.md")) or list(skills_dir.glob("*.md"))
    index_text = index_files[0].read_text(errors="replace") if index_files else ""
    lint = lint_skills(skills_dir, index_text)
    skills = [r["skill"] for r in lint]
    private_skills = {r["skill"] for r in lint if r.get("private")}
    triggers = json.loads(Path(a.triggers).read_text()) if a.triggers else {}

    cut = time.time() - a.days * 86400
    files = [(f, "claude") for f in (HOME / ".claude/projects").glob("*/*.jsonl")]
    for sub in ("sessions", "archived_sessions"):
        files += [(f, "codex") for f in (HOME / ".codex" / sub).rglob("rollout-*.jsonl")]
    files = [(f, h) for f, h in files if f.stat().st_mtime >= cut]
    sessions = [s for s in (scan_session(f, h, skills, private_skills, a.private_paths, triggers, a.include_subagents, str(vault.resolve())) for f, h in files) if s]

    since = date.fromisoformat(a.feedback_since) if a.feedback_since else date.min
    for s in sessions:
        if s["loaded"] and date.fromisoformat(s["mtime"]) > since:
            unlogged = [k for k in s["loaded"] if k not in s["feedback_written"]]
            if unlogged:
                s["reasons"].append("no FEEDBACK.md entry for: " + ", ".join(unlogged))
        if s["wrote_vault"] and not s["wrote_agent_log"] and date.fromisoformat(s["mtime"]) > since:
            s["reasons"].append("wrote to the vault without an agent-log line")

    flagged = sorted((s for s in sessions if s["reasons"]), key=lambda s: (-s["repeats"], -s["corrections"], -len(s["reasons"])))
    evidence = Path(a.evidence)
    evidence.mkdir(parents=True, exist_ok=True)
    for s in flagged[: a.max_flagged]:
        if not s["private"]:
            (evidence / f"{s['id']}.md").write_text(condensed(s))

    usage = {k: {"claude": 0, "codex": 0, "feedback_written": 0} for k in skills}
    for s in sessions:
        for k in s["loaded"]:
            usage[k][s["harness"]] += 1
            usage[k]["feedback_written"] += k in s["feedback_written"]
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "window_days": a.days,
        "sessions": len(sessions),
        "sessions_with_skill": sum(1 for s in sessions if s["loaded"]),
        "skill_coverage": round(sum(1 for s in sessions if s["loaded"]) / len(sessions), 3) if sessions else 0,
        "usage": usage,
        "never_opened": [k for k, v in usage.items() if not v["claude"] and not v["codex"]],
        "lint": lint,
        "flagged": [{k: v for k, v in s.items() if k not in ("_entries", "file")} | {"evidence": None if s["private"] else f"{s['id']}.md"}
                    for s in flagged[: a.max_flagged]],
        "flagged_total": len(flagged),
        "email_statuses": email_statuses(a.status_roots, a.days),
        "evidence_dir": str(evidence),
    }
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "skill-health.json").write_text(json.dumps(report, indent=1, ensure_ascii=False))
    print(f"{report['sessions']} sessions, {report['sessions_with_skill']} opened a skill "
          f"(coverage {report['skill_coverage']:.0%}); {report['flagged_total']} flagged, "
          f"{min(len(flagged), a.max_flagged)} kept as evidence; {sum(bool(r['flags']) for r in lint)} skills with lint flags; "
          f"{sum(not e['sent'] for e in report['email_statuses'])} unsent report emails of {len(report['email_statuses'])}")


if __name__ == "__main__":
    main()
