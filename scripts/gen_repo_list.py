#!/usr/bin/env python3
"""profile/README.md 의 <!-- REPO-LIST:START/END --> 구역을 org 저장소 목록으로 갱신."""
import json, re, pathlib

repos = json.load(open("repos.json", encoding="utf-8"))
repos = [r for r in repos if r["name"] != ".github"]
repos.sort(key=lambda r: r.get("updated_at", ""), reverse=True)

rows = ["| 저장소 | 설명 |", "| :-- | :-- |"]
for r in repos:
    lock = "🔒 " if r.get("visibility") == "private" else ""
    desc = (r.get("description") or "—").replace("|", "\\|")
    rows.append(f"| {lock}[{r['name']}]({r['html_url']}) | {desc} |")
table = "\n".join(rows) if repos else "_아직 저장소가 없습니다._"

p = pathlib.Path("profile/README.md")
md = p.read_text(encoding="utf-8")
md = re.sub(
    r"(<!-- REPO-LIST:START -->).*?(<!-- REPO-LIST:END -->)",
    lambda m: m.group(1) + "\n" + table + "\n" + m.group(2),
    md,
    flags=re.S,
)
p.write_text(md, encoding="utf-8")
print(f"갱신 완료: 저장소 {len(repos)}개")
