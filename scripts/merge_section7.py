#!/usr/bin/env python3
"""Copy docs/flow_record_section7_draft.md into docs/flow_record.md between the section-7 markers
(the draft is where section 7 is edited while the plan-v2 runs are in progress)."""
from pathlib import Path
REPO = Path(__file__).resolve().parents[1]
rec, draft = REPO / "docs" / "flow_record.md", REPO / "docs" / "flow_record_section7_draft.md"
t = rec.read_text()
a, b = "<!-- section7:start -->", "<!-- section7:end -->"
i, j = t.index(a) + len(a), t.index(b)
rec.write_text(t[:i] + "\n" + draft.read_text().rstrip() + "\n" + t[j:])
print("section 7 merged:", len(draft.read_text().splitlines()), "lines")
