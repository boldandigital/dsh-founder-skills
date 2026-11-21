# Changelog

## 1.0.0 — 2026-11-21

First release of the Founder pack for DeepSeek Harness.

Ported from [Jakeschincariol/founder-skill](https://github.com/Jakeschincariol/founder-skill)
(MIT). Twelve skills: the eleven upstream specialists plus one new entry point.

### Added

- **`founder`** — the chained entry point. One request runs all fifteen stages
  in order (board → competitors → consumer → pricing → offer → cfo →
  marketing → brand → ops → launch → plan). Upstream expects a human to invoke
  each skill in turn; this drives the chain itself and never stops at a
  stage's printed "Next:" pointer.
- **`founder/run.py`** — creates and inspects isolated run directories, so two
  ideas never share `founder/` and a resumed run knows what is left.
- **`founder/workflow.md`** — the chain, the rules that hold across it, and the
  panel's operating mechanics.
- **`install.sh`** — no-build installer for the skill roots. Idempotent, and
  reversible with `--uninstall`.
- **Currency support.** `"currency"` in `numbers.json` now drives the unit
  economics, the compiled plan, the Van Westendorp curve and the panel's
  income bands and persona briefs. The default is `$`.
- **CI.** The upstream test suite is vendored in `tests/` and runs against this
  port, so an upstream merge that breaks the port fails here first.

### Changed from upstream

- `${CLAUDE_SKILL_DIR}` → `$SKILLDIR`, the path DeepSeek Harness prints in the
  skill header.
- The Claude `Agent` tool → the DSH `subagent` tool.
- `/founder-x` slash commands → skill-name references.
- `$ARGUMENTS` and `argument-hint` removed; instructions are plain prose.
- Unit pluralisation fixed: `%ss` produced "10 boxs a day"; it now produces
  "10 boxes", "10 orders", "10 washes".

### Known limitations

- `compile.py` still prints "run /founder-cfo" in its missing-section list.
  The upstream test suite asserts that exact string, so changing it is an
  upstream decision rather than a local one.
- Sub-agent fan-out is unreliable in constrained environments. The panel
  survives it because `check` names every missing answer, but a Full
  (100-buyer) run may need several waves and relaunches.
- The competitor and operations stages need working web research. Where it
  fails, those stages record the gap rather than inventing facts.

### Upstream

MIT licensed. The upstream notice is preserved in `LICENSE`.
