#!/usr/bin/env python3
"""Fetch only selected op-amp folders from the LOADBench Zenodo archives, without downloading
the multi-GB zips: HTTP range requests through `remotezip` read the zip index, then only the
requested members.  Dataset: LOADBench (MLCAD'26), Zenodo 10.5281/zenodo.21759759, CC BY 4.0.

usage (inside layout-s0s3, venv /opt/venv-tools):
  index:  /opt/venv-tools/bin/python scripts/loadbench_fetch.py index TwoStageOpAmps.zip
  fetch:  /opt/venv-tools/bin/python scripts/loadbench_fetch.py fetch TwoStageOpAmps.zip <folder-prefix> [...] [--max-bytes N]
Output: runs/loadbench/<zip>.index.tsv  and  circuits/loadbench/<member paths>
"""
import argparse
import collections
import sys
from pathlib import Path

from remotezip import RemoteZip

RECORD = "https://zenodo.org/records/21759759/files/{name}?download=1"
REPO = Path(__file__).resolve().parents[1]


def index(name: str) -> None:
    out = REPO / "runs" / "loadbench"
    out.mkdir(parents=True, exist_ok=True)
    with RemoteZip(RECORD.format(name=name)) as z:
        infos = z.infolist()
    (out / f"{name}.index.tsv").write_text("\n".join(f"{i.file_size}\t{i.compress_size}\t{i.filename}" for i in infos) + "\n")
    tops = collections.Counter()
    sizes = collections.Counter()
    for i in infos:
        parts = i.filename.split("/")
        key = "/".join(parts[:2]) if len(parts) > 2 else parts[0]
        tops[key] += 1
        sizes[key] += i.compress_size
    print(f"{name}: {len(infos)} entries, {sum(i.compress_size for i in infos)/1e9:.2f} GB compressed")
    for k, n in sorted(tops.items()):
        print(f"{n:7d} files {sizes[k]/1e6:9.1f} MB  {k}")


def fetch(name: str, prefixes: list, max_bytes: int, exclude: list) -> None:
    dest = REPO / "circuits" / "loadbench"
    with RemoteZip(RECORD.format(name=name)) as z:
        members = [i for i in z.infolist() if any(i.filename.startswith(p) for p in prefixes) and not i.is_dir()
                   and not any(x in i.filename for x in exclude)]
        total = sum(i.compress_size for i in members)
        print(f"{len(members)} members, {total/1e6:.1f} MB compressed")
        if total > max_bytes:
            sys.exit(f"refusing: {total} bytes > --max-bytes {max_bytes}; narrow the prefixes")
        for i in members:
            z.extract(i, dest)
    print("extracted to", dest)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["index", "fetch"])
    ap.add_argument("zip")
    ap.add_argument("prefixes", nargs="*")
    ap.add_argument("--max-bytes", type=int, default=200_000_000)
    ap.add_argument("--exclude", nargs="*", default=["all_sims.zip"], help="substrings to skip (default: the 350 MB per-topology simulation dump)")
    a = ap.parse_args()
    index(a.zip) if a.cmd == "index" else fetch(a.zip, a.prefixes, a.max_bytes, a.exclude)
