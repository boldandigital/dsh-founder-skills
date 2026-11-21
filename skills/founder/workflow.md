# The Founder workflow

This is the spine of the pack. One idea goes in; a business plan with a computed
verdict comes out. Every stage writes into the same `founder/` directory, and
each stage reads what the previous ones left behind.

## The chain

```
founder-board -> founder-competitors -> founder-consumer -> founder-pricing
  -> founder-offer -> founder-cfo -> founder-marketing -> founder-brand
  -> founder-ops -> founder-launch -> founder-plan
```

Read it as a funnel. The early stages are **cheap and decisive**: the board
kills bad ideas before any research, the competitor map finds the gap, the
buyer panel finds the objections. The later stages are **expensive and
committal**: pricing, unit economics, brand, packaging, permits. If the early
stages say no, the later ones never run.

The reverse also holds: the offer is priced *after* the panel has told you what
objections exist, and the CFO runs *after* the price is set, because the price
is the CFO's biggest input. Nothing downstream is worth doing before the
upstream stage that feeds it.

## The two modes

| | Quick | Full |
| --- | --- | --- |
| simulated buyers | 20 | 100 |
| stages run | all 15 | all 15 |
| time | an hour or two of agent time | several hours |
| what it answers | "is this worth a week of my time?" | "which segment, which price, which channel?" |

**Only the panel size changes.** Every other stage runs identically, so a Quick
run is a real plan with less statistical power, not a different product. Quick
is the default; Full is for when the answer will decide a large commitment.

The panel size is set once, at `run.py new --mode quick|full`, and every
downstream number — the buy rate, the Van Westendorp range, the verdict — is
computed from the answers that came back. A Quick run and a Full run are
therefore directly comparable if they share a seed.

## The stages

### 1. founder-board — should this exist at all?
Writes `idea.md`, `board/brief.md`, three memos in `board/`, and `board.md`.
Three sub-agents read the brief through three lenses (Offers, Monopoly,
Product) and vote. Their conditions become the checklist the rest of the pack
must tick.

**Carry forward:** the conditions. Every later stage should be able to say which
condition it satisfies.

### 2. founder-competitors — who is already there?
Writes `competitors.md` and `competitors.csv` from public sources only, with a
link per fact, and ends with a positioning map and the gap.

**Carry forward:** the gap. Pricing, marketing and brand all speak to it.

### 3. founder-consumer — would they actually buy?
Writes `customer.json`, `pitch.md`, `panel/` (cards, briefs, answers) and
`panel/results.md`. This is the only stage that fans out to many sub-agents.

**Carry forward:** the objections and the four price answers per buyer.

### 4. founder-pricing — what will they pay?
Reads the panel's price answers into a Van Westendorp range, sets it against
competitor prices and the margin, and recommends a price plus a ladder.

**Carry forward:** the price, as a number in `numbers.json`.

### 5. founder-offer — what exactly is being sold?
Rebuilds the offer around the panel's objections and **re-tests it on the same
seed** so the change can be measured rather than asserted.

**Carry forward:** the offer, and the offer's buy rate before and after.

### 6. founder-cfo — does the money work?
Writes `numbers.json` (every input, checkable) and `cfo.md`: contribution,
margin at plan, break-even, year 1 by month, cash needed, payback, and what
happens if price falls, volume falls or costs rise.

**Carry forward:** the numbers. Everything downstream quotes them.

### 7-10. founder-marketing, founder-brand, founder-ops, founder-launch — making it real
Marketing turns the objections into messages and a dated campaign with a CAC
ceiling. Brand names it, promises one thing, and briefs the look. Ops works out
the day, the suppliers, the people, the SOPs, the licences and the risks.
Launch turns it into a dated plan whose first step is a cheap real test.

**Carry forward:** each one cites the stage before it. Marketing quotes the
objections; brand quotes the positioning; ops quotes the cost lines; launch
quotes the break-even.

### 11. founder-plan — the verdict
Compiles everything into `business-plan.md` with a verdict computed from the
numbers, never written by hand, plus `summary.md` and `one-pager.md`.

## Rules that hold across the chain

1. **One idea, one directory.** Use `run.py new`. Two ideas must never share
   `founder/`.
2. **No invented facts.** Every competitor price, licence rule and supplier
   price carries a source and a date. Where a fact is unavailable, say so and
   name the skill or person that can get it.
3. **The panel is not the market.** Simulated buyers surface objections. They
   never prove demand. Only a real test — a pre-sale, a paid order, a real
   delivery — proves demand.
4. **Carry conditions forward.** The board's conditions are not decoration.
   If a condition cannot be met, the verdict is "Not yet" and the summary says
   which stage changes it.
5. **The verdict is computed.** `compile.py` decides Profitable / Not yet /
   Incomplete from the numbers. No stage may soften a failing check.
6. **Never stop at a "Next:" pointer.** The specialists print a pointer for
   humans. The `founder` skill drives the chain itself.

## Running the panel

The panel is the only stage that needs many agents, and it has its own
mechanics. `--dir` is a global option and must come **before** the
subcommand:

```bash
python3 "$SKILLDIR/../founder-consumer/panel.py" --dir founder/panel init \
    --n 20 --seed 4242 --customer founder/customer.json --pitch founder/pitch.md
```

Subcommands: `init`, `prompts`, `check`, `save`, `tally`, `status`.

Launch one sub-agent per buyer, in waves of ten, each with the brief at
`founder/panel/briefs/P0NN.md` and the output path
`founder/panel/answers/P0NN.json`. Verify with `panel.py --dir founder/panel
check` — it names every missing or malformed answer. A child that reports
success but writes no file has not answered; relaunch it. Never hand-write an
answer to fill a gap.

The answers must include all four price questions (too cheap, cheap,
expensive, too expensive) as numbers. `check` passes an answer that is missing
one, and `founder-pricing` then silently drops that buyer. Ask for every field
the brief's JSON block lists, and read the files back.

## Where the numbers come from

`numbers.json` is the single source of truth. `founder-cfo` writes it,
`founder-pricing` and `founder-offer` feed it, and `compile.py` reads it. Set
`"currency"` there (`"R$"`, `"€"`, `"$"`) and the money renders in that
currency everywhere — unit economics, the plan, the panel's income bands.

## If a stage fails

Do not fill the gap from imagination, and do not skip a stage silently. If a
stage's artifacts cannot be produced — no network for competitors, a legal
question that needs a professional — record the gap as a gap, mark the
affected stage as not done, and let the verdict reflect it. `compile.py` lists
what is missing under "Not done yet"; that list is the honest state of the
plan.
