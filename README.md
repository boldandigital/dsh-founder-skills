# Founder for DeepSeek Harness

Eleven specialist skills and one entry point that runs **all of them**, end to
end, on one business idea. Give it an idea; get a business plan with a verdict
that is computed from the numbers rather than written by hand.

Ported from [Jakeschincariol/founder-skill](https://github.com/Jakeschincariol/founder-skill)
(MIT) and adapted to DeepSeek Harness.

## Install

```bash
git clone <this-repo> && cd founder-dsh
./install.sh                    # into ~/.dsh/skills
./install.sh --profile work     # into ~/.dsh/profiles/work/skills
./install.sh --uninstall        # remove it
```

No plugin, no build step, no network. DSH's skill-filesystem provider discovers
each `skills/<name>/SKILL.md` automatically.

## Use it

```
test this idea: a mobile dog-wash service in Lisbon
```

That one request runs the whole chain. The `founder` skill creates an isolated
run directory, drives each stage in order, and finishes with the compiled plan.

| say | you get |
| --- | --- |
| "test this idea" | Quick — the full pack, 20 simulated buyers |
| "test this idea, full run" | Full — the same pack, 100 simulated buyers |
| "how much should I charge for…" | just `founder-pricing` |
| "would people buy this…" | just `founder-consumer` |

**Quick and Full are the same product.** Every stage runs identically; only the
panel size changes. A Quick run is a real business plan with less statistical
power, not a stripped-down one. Both write the same files.

## What comes out

One directory per idea, so two ideas never share state:

```
runs/my-idea/founder/
├── idea.md          board.md        competitors.md   competitors.csv
├── customer.json    pitch.md        panel/{panel.json,personas.json,briefs/,answers/,results.md}
├── pricing.md       pricing-curve.md offer.md        numbers.json
├── cfo.md           cfo-sources.md  marketing.md     brand.md
├── ops.md           launch.md
└── summary.md       business-plan.md one-pager.md
```

`business-plan.md` opens with a verdict — **Profitable**, **Not yet** or
**Incomplete** — computed by `compile.py` from four checks:

1. each unit earns money before fixed costs,
2. year 1 makes an operating profit,
3. break-even fits inside capacity,
4. enough simulated buyers buy (default bar 25%).

A failing check is never rounded into a passing one, and the plan lists which
stages are still missing.

## The chain

```
founder-board → founder-competitors → founder-consumer → founder-pricing
  → founder-offer → founder-cfo → founder-marketing → founder-brand
  → founder-ops → founder-launch → founder-plan
```

The early stages are cheap and decisive; the late ones are expensive and
committal. Pricing comes after the panel, because the panel's objections set
the price. The CFO comes after the price, because the price is the CFO's
biggest input.

Each specialist still works alone. `founder-plan` reads whatever the others
wrote and tells you what is missing.

## What is honest about it

- **The panel is simulated.** It surfaces objections and price reactions. It
  never proves demand. Only a real test — a pre-sale, a paid order — proves
  demand, and `founder-launch` puts a real test first, with a number written
  down before it runs.
- **No invented facts.** Every competitor price, licence rule and supplier
  price carries a source and a date. Where evidence is missing, the stage says
  so instead of filling the gap.
- **The verdict is computed.** `compile.py` decides. No stage may soften a
  failing check.

## Currency

Set `"currency"` in `numbers.json` and the money renders in it everywhere —
unit economics, the compiled plan, the panel's income bands:

```json
{ "currency": "R$", "price": 24.00, "unit": "order" }
```

Supported by `unit_economics.py`, `compile.py`, `van_westendorp.py` and
`panel.py`. The default is `$`, and the upstream test suite passes unchanged.

## Layout

```
founder-dsh/
├── install.sh              installer
├── package.json            bundle manifest for `dsh plugin install`
├── cordis.patch.yml        patch layer for the bundle route
├── LICENSE                 MIT (upstream)
├── README.md
└── skills/
    ├── founder/            the entry point: SKILL.md, workflow.md, run.py
    ├── founder-board/      SKILL.md, lenses.md
    ├── founder-brand/      SKILL.md
    ├── founder-cfo/        SKILL.md, unit_economics.py, example.json
    ├── founder-competitors/SKILL.md
    ├── founder-consumer/   SKILL.md, panel.py, customer.example.json
    ├── founder-launch/     SKILL.md
    ├── founder-marketing/  SKILL.md
    ├── founder-offer/      SKILL.md
    ├── founder-ops/        SKILL.md
    ├── founder-plan/       SKILL.md, compile.py
    └── founder-pricing/    SKILL.md, van_westendorp.py
```

## Adapting it to DSH

The upstream pack is written for Claude Code. The port changed:

- **No `${CLAUDE_SKILL_DIR}`.** Each skill refers to its own directory as
  `$SKILLDIR`, the path DeepSeek Harness prints in the skill header.
- **No `/founder-x` slash commands.** Skills refer to each other by name.
- **No `$ARGUMENTS` or `argument-hint`.** Instructions are plain prose.
- **The Claude agent tool is the DSH `subagent` tool.**
- **New: the `founder` entry point.** The upstream pack expects a human to
  invoke each skill in turn. That is the wrong shape for an agent, so the
  entry point drives the chain itself and never stops at a stage's printed
  "Next:" pointer.
- **New: `run.py`.** Creates and inspects isolated run directories, so two
  ideas never share `founder/`, and a resumed run knows what is left.
- **New: currency support** in the four scripts that print money.

## Not legal, financial or tax advice

The licence and permits section points at official pages and says plainly that
rules differ by place and change. Confirm each one with the authority.
