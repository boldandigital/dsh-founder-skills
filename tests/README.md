# Upstream test suite

These are the tests from
[Jakeschincariol/founder-skill](https://github.com/Jakeschincariol/founder-skill)
(MIT), vendored unchanged so this port's CI can prove it still works.

They load the skills from `../skills` — that is, **this port**, not the upstream
tree. If a future upstream merge breaks the port, these fail here first.

`test_repo.py` is excluded: it asserts on the upstream repository layout
(`.claude-plugin/plugin.json`, a README with Claude-specific copy), which does
not apply to a DSH port.

To refresh against upstream:

```bash
git clone --depth 1 https://github.com/Jakeschincariol/founder-skill.git /tmp/upstream
cp /tmp/upstream/tests/{_load.py,test_compile.py,test_panel.py,test_pricing.py,test_unit_economics.py} tests/
```

Then run:

```bash
cd tests && python3 -m unittest test_compile test_panel test_pricing test_unit_economics
```
