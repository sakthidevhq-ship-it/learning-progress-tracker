# End-of-day learning routine

Runs once a day (T3 scheduled task). Turns the day's local Claude conversations into vault changes, then saves
once. Work in the main checkout `/Users/sakthi/learning-progress-tracker` and use `.venv/bin/lpt` from there.

## 1. Read the day

`.venv/bin/lpt day-log` (today; pass `--date YYYY-MM-DD` to redo another day). It prints user prompts and assistant
replies per session, without tool calls. If it prints nothing, stop and report "nothing today".

Also run `.venv/bin/lpt ls` and `.venv/bin/lpt ls --state picked` so you know what's already in the library.

## 2. Decide what to record

Only things about *learning*: how something works, a concept understood, a paper/doc/repo/video worth keeping.
Ignore routine ops (fixing a laptop, Slack, git chores, one-off data pulls) unless a real concept came out of it.

- **New item**: a URL, paper, doc, repo or project that came up and is worth coming back to. Check `lpt ls` (titles
  match fuzzily) first; never add a duplicate.
  `.venv/bin/lpt add "<url or title>" --note "<why, in the context it came up>" [--type project|practice|article]`
- **Learning update**: one or two sentences, in the user's voice, on what was understood that day. Attach to the
  closest existing item (a new one is fine).
  `.venv/bin/lpt learn "<item>" "<what was learned>"`
- **Progress on an existing item**, only when the conversation states it explicitly: `lpt check "<item>" --toggle N`,
  `lpt done "<item>"`, `lpt pick "<item>"`. Log time (`lpt time`) only when a duration was actually stated.
  When unsure, write a learning update instead of changing state.

Never set or change `my-priority`, never drop or `back` an item, never edit Notes, and never touch `planned`.
Keep it short: a typical day is 0–5 changes. Zero is a fine answer.

## 3. File the new items

For each new item, follow "Filing Unsorted items" in `CLAUDE.md`: `lpt enrich` lists them, read the source, write the
result JSON to a temp file, `lpt enrich <id> --from <file>`. Use existing domains only; if nothing fits, leave it
Unsorted. Only file items you added in this run.

## 4. Save once

If anything changed: `.venv/bin/lpt save -m "Daily learning: <YYYY-MM-DD>"`. If save refuses (code commits not on
the target, or a conflict), don't force it; leave the changes and say so.

## 5. Report

A short list: items added (and where they were filed), learning updates, progress changes, and whether the save
went through. Mention anything skipped as unclear, so the user can add it by hand.

Running twice on the same day is safe: `lpt learn` ignores an identical line, and step 2's duplicate check
covers adds.
