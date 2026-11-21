# Review of the Founder port for DeepSeek Harness

Reviewed 2026-11-21, against DSH 0.2.2-rc.5 and the upstream MIT pack at
`Jakeschincariol/founder-skill`. This is the honest state of the port: what was
broken, what was fixed, what was added, and what is still not right.

## Published

Released 2026-11-21 as `dsh-founder-skills@1.0.0`.

| channel | address |
| --- | --- |
| npm | https://www.npmjs.com/package/dsh-founder-skills (tagged `latest`, 27 files, 42.6 kB) |
| GitHub | https://github.com/boldandigital/dsh-founder-skills (public, `main`) |

Both verified by downloading the published tarball and installing it into a
clean DSH home: 12 skills installed, `run.py new` worked in both Quick and
Full mode, and the panel dealt 100 buyers in Full. GitHub CI is green on the
published commit.

Install with `npm install -g dsh-founder-skills` and then `./install.sh` from
the installed directory, or clone the repo and run `./install.sh` directly.

## Verdict

**Shippable.** The pack runs end to end in DSH, the verdict is computed from
the numbers, and the eleven specialists still work individually. The one design
gap in the upstream pack — it expects a human to invoke each skill in turn — is
now closed by a `founder` entry point.

## What was wrong with the upstream pack in DSH

| # | Problem | Severity | Status |
| --- | --- | --- | --- |
| 1 | It is written for Claude Code: `${CLAUDE_SKILL_DIR}`, `$ARGUMENTS`, `argument-hint`, the Claude `Agent` tool, `/founder-x` slash commands. None of these exist in DSH. | **blocking** | fixed — replaced with `$SKILLDIR`, the DSH `subagent` tool, and plain prose references |
| 2 | The chain only advances if a human runs the next skill. An agent that stops at the printed "Next:" pointer has done nothing. | **blocking for agents** | fixed — new `founder` skill drives the chain itself |
| 3 | Every skill reads and writes one shared `founder/` directory. Two ideas in one workspace overwrite each other. | high | fixed — new `run.py` gives each idea an isolated run directory |
| 4 | Money is hardcoded to `$`. A run in Brazil or Europe prints wrong currency in the unit economics, the price curve and the plan. | high | fixed — `currency` in `numbers.json`, threaded through all four scripts |
| 5 | Units are pluralised as `%ss`: "10 boxs a day". | medium | fixed — proper pluralisation ("10 boxes", "10 orders", "10 washes") |
| 6 | The panel's income bands and persona briefs hardcoded `$`, so a euro run showed dollar incomes next to euro prices. | medium | fixed — same currency mechanism |
| 7 | The compiled plan's missing-section list says `run /founder-cfo`, a Claude slash command. | low | **open by choice** — the upstream test suite asserts that exact string (`test_compile.py:36` and `:46`), so changing it breaks the upstream contract. It is a hint in a generated report, not an instruction to the agent. Fixing it properly means changing an upstream test assertion, which is a decision for the upstream repo, not a silent local change. |
| 8 | The board skill assumes three sub-agents launched in one message. | low | works, but the harness caps active children at 8; launch in waves and verify files, not completion claims |
| 9 | `panel.py --dir` is a global option that must precede the subcommand. | low | **misuse trap** — `panel.py init --dir panel` fails with a confusing argparse error. Documented prominently in `workflow.md`. |

## What was added

### `founder` — the chained entry point

The upstream pack has no entry point. You ask for a board review and you get a
board review. This adds one skill that runs **all fifteen stages** in order:

```
board → competitors → consumer → pricing → offer → cfo
      → marketing → brand → ops → launch → plan
```

It reads `workflow.md` (the chain, the rules, the panel mechanics) and
`run.py` (the run directory). It is written so an agent can follow it without
human intervention: it never stops at a "Next:" pointer, it verifies each
stage's files rather than trusting a sub-agent's claim, and it reports missing
stages honestly instead of filling them.

### `run.py` — isolated, resumable runs

```bash
python3 run.py new --name my-idea --root runs --mode quick --seed 4242 --currency '€'
python3 run.py status --dir runs/my-idea
```

`new` refuses to overwrite an existing run. `status` prints which of the
fifteen stages have produced their artifacts and what is next — so a resumed
run knows where it stopped without guessing.

### Packaging

Two routes, both supported:

- **`./install.sh`** — copies the skill folders into `~/.dsh/skills` (or
  `~/.dsh/profiles/<name>/skills`). No plugin, no build, no network. Verified
  working, idempotent, and cleanly reversible with `--uninstall`.
- **`package.json` + `cordis.patch.yml`** — for `dsh plugin install`, if you
  publish to npm.

The discovery contract was read from DSH's own source
(`dsh-skill-filesystem/src/index.ts`), not guessed: `<name>/SKILL.md` under the
skill root, ranked by directory depth, with `customSkillDirs` available for
extra roots.

## How it was verified

| check | result |
| --- | --- |
| upstream tool tests (22) against the installed tree | **pass** |
| all Python compiles | **pass** |
| every `$SKILLDIR/…` and `../…` reference in every SKILL.md resolves | **pass** |
| no Claude residue (`CLAUDE_SKILL_DIR`, `$ARGUMENTS`, `argument-hint`, `subagent_type`) | **pass** |
| `run.py new` → `status` → `path` | **pass** |
| installer idempotency and uninstall | **pass** |
| packaged panel: real sub-agent wrote a valid answer with all four price fields, `check` accepted it | **pass** |
| full chain: `panel init` → `prompts` → `check` → `tally` → `van_westendorp` → `unit_economics` → `compile.py` | **pass**, verdict computed |
| currency in euros end to end (briefs, income bands, price curve, unit economics, plan) | **pass** — `€53,000`, `€45.00`, "3 washes a day" |
| the skill appears in DSH's catalogue after install | **pass** — `founder` listed |

The end-to-end run used a throwaway idea in `/tmp` with synthetic panel
answers to exercise the machinery. It proved the pipeline, not a business
finding — no conclusion about that idea should be drawn from it.

## Known limitations

1. **Sub-agent fan-out is unreliable in this environment.** Launching 7
   children at once, most failed without writing a file. The panel survived it
   because `check` names every missing answer and the agent relaunches. The
   workflow documents waves of ten, `check` between waves, and verifying the
   file rather than the completion message.
2. **The panel needs a real `customer.json`.** The schema wants segments with
   income bands, behaviours with shares and objections. A malformed file fails
   with `every segment needs a name and an income [low, high]` — correct, but
   the error arrives after `run.py new`, so the entry point should validate the
   customer file before calling `init`.
3. **`compile.py` still prints slash-command pointers** (issue 7).
4. **The pack assumes web research works.** `founder-competitors` and
   `founder-ops` need public sources. In an environment without working search,
   those stages produce gaps rather than results, and the plan says so. That is
   correct behaviour, but it means the pack is only as good as the network.
5. **One panel seed per idea.** Two runs with the same seed deal the same
   cards, which is what makes the offer re-test comparable. Two runs with
   different seeds are not comparable — the numbers will move for reasons that
   have nothing to do with the business.

## Before publishing publicly

Done, except the two items that need an upstream decision:

1. Issue 7 is open by choice — replacing `run /founder-cfo` means changing two
   upstream test assertions, which belongs in the upstream repo.
2. The package name is now `dsh-founder-skills` (unscoped, matching the sibling
   DSH packages), CI is in place, and `CHANGELOG.md` documents the release.

## Upstream

Ported from [Jakeschincariol/founder-skill](https://github.com/Jakeschincariol/founder-skill),
MIT licensed. The upstream notice is preserved in `LICENSE`.
