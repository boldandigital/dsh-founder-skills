---
name: founder
description: Run the full Founder business-idea assessment in DeepSeek Harness, from idea and competitors through a simulated buyer panel, pricing, operations, launch, and a compiled plan. Use for "test my business idea", "validate my startup", or "run the whole Founder pack". Quick uses 20 simulated buyers; Full uses 100. Both cover every aspect.
---

# Founder — run the whole assessment

Use this entry point for a broad business-idea test, even if a specialist also matches. A request explicitly limited to one aspect can use that specialist alone. Quick and Full use the same stages.

1. Confirm the idea and target market only when missing. Use Quick (20 buyers) unless the user asks for Full (100) or already states the size. Ask one compact batch of questions if necessary. Do not block on unknown pricing or costs; carry those as hypotheses or missing inputs.
2. Read `workflow.md` next to this file using its actual Base directory. Create an isolated run directory using `run.py`. Do not use a previous idea's artifacts. If asked to resume, use the existing run directory and its status rather than initializing again.
3. Follow the stages in order. Load each specialist with `skill` when needed, but resolve its `founder/` outputs beneath this run directory. The same lead owns the handoffs. Do not stop at the specialists' printed “Next” pointers or ask the user to invoke them. If the specialist tool is unavailable, read the sibling `SKILL.md`; if artifacts cannot be produced, name the missing stage explicitly.
4. Launch DSH buyer subagents in bounded batches. Verify the saved output, not the child's completion claim. Do not fabricate a response or convert an absent answer into a pass. The panel represents simulated objections, not actual buyers or demand.
5. Compile the final business plan and validate the run. Present the verdict, assumptions and evidence gaps, then one practical real-world test. Share the one-pager and the full plan. A complete run is not permission to launch or spend money.
