#!/usr/bin/env python3
"""Create and inspect an isolated Founder run directory.

Standard library only, no network. Every stage of the pack writes beneath one
run directory, so two ideas never share state:

    python3 run.py new --name my-idea --root runs
    python3 run.py status --dir runs/my-idea
    python3 run.py path --dir runs/my-idea

`new` refuses to overwrite an existing run. `status` prints which stages have
produced their artifacts, so a resumed run knows what is left without guessing.
"""

import argparse
import datetime
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# (stage, skill that writes it, artifact relative to the founder/ directory)
STAGES = [
    ("idea", "founder-board", "idea.md"),
    ("board", "founder-board", "board.md"),
    ("competitors", "founder-competitors", "competitors.md"),
    ("panel", "founder-consumer", "panel/results.json"),
    ("pricing", "founder-pricing", "pricing.md"),
    ("offer", "founder-offer", "offer.md"),
    ("numbers", "founder-cfo", "numbers.json"),
    ("cfo", "founder-cfo", "cfo.md"),
    ("marketing", "founder-marketing", "marketing.md"),
    ("brand", "founder-brand", "brand.md"),
    ("ops", "founder-ops", "ops.md"),
    ("launch", "founder-launch", "launch.md"),
    ("summary", "founder-plan", "summary.md"),
    ("plan", "founder-plan", "business-plan.md"),
    ("one-pager", "founder-plan", "one-pager.md"),
]

SLUG = re.compile(r"[^a-z0-9]+")


def slugify(text):
    slug = SLUG.sub("-", str(text).strip().lower()).strip("-")
    return slug or "idea"


def cmd_new(args):
    root = os.path.abspath(args.root)
    name = slugify(args.name)
    run = os.path.join(root, name)
    if os.path.exists(run):
        raise SystemExit("run directory already exists: %s (resume it, or pick another name)" % run)
    founder = os.path.join(run, "founder")
    os.makedirs(os.path.join(founder, "panel"), exist_ok=True)
    meta = {
        "name": name,
        "created": datetime.datetime.now().isoformat(timespec="seconds"),
        "mode": args.mode,
        "panel_size": 20 if args.mode == "quick" else 100,
        "seed": args.seed,
        "currency": args.currency,
    }
    with open(os.path.join(run, "run.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    print(run)
    print("founder directory: %s" % founder)


def cmd_status(args):
    run = os.path.abspath(args.dir)
    founder = os.path.join(run, "founder")
    meta = {}
    meta_path = os.path.join(run, "run.json")
    if os.path.exists(meta_path):
        with open(meta_path, encoding="utf-8") as fh:
            meta = json.load(fh)
    print("run: %s" % run)
    if meta:
        print("mode: %s (panel size %s, seed %s, currency %s)"
              % (meta.get("mode"), meta.get("panel_size"), meta.get("seed"), meta.get("currency")))
    done, todo = [], []
    for stage, skill, artifact in STAGES:
        path = os.path.join(founder, artifact)
        if os.path.exists(path) and os.path.getsize(path) > 0:
            done.append((stage, skill))
        else:
            todo.append((stage, skill, artifact))
    print("done (%d/%d): %s" % (len(done), len(STAGES), ", ".join(s for s, _ in done) or "none"))
    if todo:
        print("next:")
        for stage, skill, artifact in todo:
            print("  %-12s %-18s -> founder/%s" % (stage, skill, artifact))
    else:
        print("next: compile the plan (founder-plan) and present the verdict")
    return 0


def cmd_path(args):
    print(os.path.join(os.path.abspath(args.dir), "founder"))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--dir", help="run directory (used by status and path)")
    sub = ap.add_subparsers(dest="cmd")
    p_new = sub.add_parser("new", help="create an isolated run directory")
    p_new.add_argument("--name", required=True)
    p_new.add_argument("--root", default="runs")
    p_new.add_argument("--mode", choices=["quick", "full"], default="quick")
    p_new.add_argument("--seed", type=int, default=4242)
    p_new.add_argument("--currency", default="$")
    p_status = sub.add_parser("status", help="which stages are done")
    p_status.add_argument("--dir", required=True)
    sub.add_parser("path", help="print the founder/ directory").add_argument("--dir", required=True)
    args = ap.parse_args(argv)
    if args.cmd == "new":
        cmd_new(args)
    elif args.cmd == "status":
        return cmd_status(args)
    elif args.cmd == "path":
        cmd_path(args)
    else:
        ap.print_help()
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
