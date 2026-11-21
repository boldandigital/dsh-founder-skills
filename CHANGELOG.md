# Changelog

## 1.0.1 — 2026-11-21

Hardened the panel's operational mechanics after running both modes for real.

### Changed

- **`workflow.md` states the harness's eight-active-child cap** and tells the
  agent to launch six to eight buyers per batch. The previous guidance said
  "waves of ten", which fails with `subagent limit reached (active child
  limit: 8)`.
- **`workflow.md` documents the loop that works**: `check` → launch → `wait_agent`
  → `check`, plus the two failure modes seen in practice — a child that reports
  success without writing its answer file, and a child that omits the four
  price fields.
- **`founder/SKILL.md`** repeats the eight-child cap in its own instructions.
- **`run.py` gains `check-customer`**, which validates a customer profile
  against `panel.py`'s own rules and exits non-zero before the panel is set up,
  instead of failing half-way through a run.
- **`README.md`** documents the wave count and wall time for each mode.

### Verified

Full mode deals 100 buyers into 10 waves and generates 100 briefs; three real
sub-agents produced complete, valid answers with all four price fields in the
run's currency; the upstream test suite still passes.

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
