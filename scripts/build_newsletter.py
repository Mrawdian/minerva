"""Generates output/newsletter_YYYYMMDD.{html,txt} — a readable weekly digest of the findings.

Reads state.json (with rescored scores) and the markdown fiches.
Highlights the 8 new big-tech orgs and the new Edge AI domain.

Two formats produced:
  - .html: rich version for the browser (cards, badges, CSS).
  - .txt : plain-text version sendable by email (subject + formatted body).
"""

import html
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

STATE_FILE = ROOT / "output" / "state.json"
FICHES_DIR = ROOT / "output" / "fiches"
OUT_DIR = ROOT / "output"

from fiche_schema import Fiche, FicheParseError  # noqa: E402


NEW_BIG_TECH_OWNERS = {
    "alibaba", "bytedance", "baidu", "paddlepaddle",
    "jd-opensource", "tencent", "dongshanpi", "licheepi",
}


def slugify(full_name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_\-]", "_", full_name.replace("/", "_"))


def parse_fiche(path: Path) -> dict | None:
    """Parse a markdown fiche into the dict expected by the HTML/TXT renderers.

    Adapter over Fiche.from_markdown that flattens the Pydantic object into the
    flat structure used by fmt_card / render_text_newsletter (short keys
    'probleme', 'specificite', etc.). Keeps backward compatibility with the
    rest of the file without having to rewrite everything.
    """
    try:
        f = Fiche.from_markdown(path.read_text(encoding="utf-8"))
    except (FicheParseError, ValueError):
        return None
    return {
        "full_name": f.full_name,
        "owner": f.owner,
        "type": f.type,
        "domaine": f.domaine,
        "score": f.score_de_pertinence,
        "stars": f.stars,
        "probleme": f.probleme_resolu,
        "specificite": f.specificite_chinoise,
        "equivalent": f.equivalent_occidental,
        "maturite": f.maturite,
        "date": f.pushed_at_month,
        "gitee_url": f.gitee_url,
    }


def fmt_card(item: dict, highlight: bool = False) -> str:
    cls = "card highlight" if highlight else "card"
    score_class = "score-high" if item["score"] >= 35 else ("score-mid" if item["score"] >= 20 else "score-low")
    domain_label = html.escape(item["domaine"])
    domain_cls = "domain edge-ai" if "Edge AI" in item["domaine"] else "domain"
    return f"""
<article class="{cls}">
  <header>
    <span class="score {score_class}">{item["score"]}</span>
    <a href="{html.escape(item["gitee_url"])}" target="_blank" rel="noopener">
      <strong>{html.escape(item["full_name"])}</strong>
    </a>
  </header>
  <div class="tags">
    <span class="tag">{html.escape(item["type"])}</span>
    <span class="tag {domain_cls}">{domain_label}</span>
    {"<span class='tag stars'>★ " + str(item["stars"]) + "</span>" if item["stars"] else ""}
    {"<span class='tag date'>push " + item["date"] + "</span>" if item["date"] else ""}
  </div>
  <p class="probleme">{html.escape(item["probleme"])}</p>
  <p class="specificite"><em>{html.escape(item["specificite"])}</em></p>
</article>
"""


def _truncate(s: str, limit: int) -> str:
    s = (s or "").strip()
    if len(s) <= limit:
        return s
    return s[: limit - 1].rstrip() + "…"


def render_text_newsletter(items: list[dict], top: list[dict], edge_ai: list[dict],
                           big_tech: list[dict], domain_count: dict[str, int],
                           type_count: dict[str, int], today_human: str,
                           last_run: str) -> str:
    """Generates the plain-text version, readable in a basic mail client (Gmail, Outlook, mutt).

    No markdown or HTML: ASCII + accents + line breaks only.
    Target width ~78 columns to render without breakage in all clients.
    """
    lines: list[str] = []
    subject = f"Minerva — Open Source China Intelligence — {today_human}"

    lines.append(f"Subject: {subject}")
    lines.append("")
    lines.append("=" * 72)
    lines.append(f"  MINERVA NEWSLETTER — {today_human}")
    lines.append("  Open source China intelligence: embedded / IoT / robotics / edge-AI")
    lines.append("=" * 72)
    lines.append("")
    if last_run:
        lines.append(f"Last pipeline run: {last_run}")
        lines.append("")

    lines.append("-" * 72)
    lines.append("TOP 5 FINDINGS (by relevance score)")
    lines.append("-" * 72)
    lines.append("")
    for idx, item in enumerate(top[:5], 1):
        stars = f"★{item['stars']}" if item["stars"] else "★0"
        header = f"{idx}. [{item['score']:>3}/100] {item['full_name']}  ({stars})"
        lines.append(header)
        phrase = _truncate(item["probleme"], 200)
        if phrase:
            lines.append(f"   {phrase}")
        if item["gitee_url"]:
            lines.append(f"   {item['gitee_url']}")
        lines.append("")

    lines.append("-" * 72)
    lines.append("KEY STATS")
    lines.append("-" * 72)
    lines.append("")
    lines.append(f"  Active fiches         : {len(items)}")
    lines.append(f"  Monitored accounts    : {len(set(i['owner'] for i in items))}")
    lines.append(f"  Edge AI repos         : {len(edge_ai)}")
    lines.append(f"  Big tech repos (8 orgs): {len(big_tech)}")
    lines.append("")
    lines.append("  Distribution by domain:")
    for dom, n in sorted(domain_count.items(), key=lambda x: -x[1]):
        pct = 100 * n / len(items) if items else 0
        lines.append(f"    - {dom:<22} {n:>4}  ({pct:.1f}%)")
    lines.append("")
    lines.append("  Distribution by type:")
    for t, n in sorted(type_count.items(), key=lambda x: -x[1])[:6]:
        pct = 100 * n / len(items) if items else 0
        lines.append(f"    - {t:<22} {n:>4}  ({pct:.1f}%)")
    lines.append("")
    lines.append("-" * 72)
    lines.append("See the interactive dashboard: output/dashboard.html")
    lines.append("Rich version                 : output/newsletter_" + datetime.now().strftime("%Y%m%d") + ".html")
    lines.append("-" * 72)
    return "\n".join(lines) + "\n"


def main() -> int:
    state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    state_repos = state.get("repos", {})
    last_run = state.get("last_run", "")

    items: list[dict] = []
    for full_name in state_repos.keys():
        path = FICHES_DIR / f"{slugify(full_name)}_fiche.md"
        if not path.is_file():
            continue
        item = parse_fiche(path)
        if item:
            items.append(item)

    items.sort(key=lambda x: -x["score"])

    big_tech = [i for i in items if i["owner"].lower() in NEW_BIG_TECH_OWNERS]
    edge_ai = [i for i in items if "Edge AI" in i["domaine"]]
    top10 = items[:10]

    # Stats by domain
    domain_count: dict[str, int] = {}
    for i in items:
        for d in i["domaine"].split(" / "):
            d = d.strip()
            domain_count[d] = domain_count.get(d, 0) + 1
    type_count: dict[str, int] = {}
    for i in items:
        type_count[i["type"]] = type_count.get(i["type"], 0) + 1

    today = datetime.now().strftime("%Y%m%d")
    today_human = datetime.now().strftime("%Y-%m-%d")
    out_path = OUT_DIR / f"newsletter_{today}.html"

    body = []
    body.append(f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Minerva Newsletter — {today_human}</title>
<style>
* {{ box-sizing: border-box; }}
body {{ font-family: -apple-system, "Segoe UI", Roboto, sans-serif; max-width: 880px;
       margin: 0 auto; padding: 24px; color: #1a1a1a; line-height: 1.55; background: #fafafa; }}
h1 {{ font-size: 26px; margin: 0 0 6px; border-bottom: 3px solid #cc0000; padding-bottom: 10px; }}
.subtitle {{ color: #6b7280; font-size: 14px; margin: 0 0 26px; }}
h2 {{ font-size: 19px; margin: 32px 0 12px; padding-left: 10px; border-left: 4px solid #cc0000; }}
h3 {{ font-size: 15px; margin: 18px 0 8px; color: #374151; }}
.stats {{ display: flex; flex-wrap: wrap; gap: 12px; margin: 0 0 18px; }}
.stat {{ flex: 1 1 140px; padding: 12px 14px; background: #fff; border: 1px solid #e5e7eb;
         border-radius: 6px; }}
.stat .num {{ font-size: 26px; font-weight: 700; color: #1a1a1a; }}
.stat .lbl {{ font-size: 12px; color: #6b7280; text-transform: uppercase; }}
.card {{ background: #fff; border: 1px solid #e5e7eb; border-radius: 6px; padding: 12px 14px;
         margin: 0 0 10px; }}
.card.highlight {{ border-left: 3px solid #cc0000; }}
.card header {{ display: flex; align-items: center; gap: 10px; margin-bottom: 6px; }}
.card a {{ color: #0969da; text-decoration: none; }}
.card a:hover {{ text-decoration: underline; }}
.score {{ width: 34px; height: 34px; border-radius: 50%; display: inline-flex;
          align-items: center; justify-content: center; color: #fff; font-weight: 700;
          font-size: 12px; flex-shrink: 0; }}
.score-high {{ background: #1a7f37; }}
.score-mid  {{ background: #bf8700; }}
.score-low  {{ background: #6b7280; }}
.tags {{ display: flex; flex-wrap: wrap; gap: 5px; margin: 4px 0 6px; font-size: 11px; }}
.tag {{ padding: 2px 7px; border-radius: 3px; background: #f3f4f6; color: #374151; }}
.tag.domain {{ background: #dbeafe; color: #1e3a8a; }}
.tag.domain.edge-ai {{ background: #fef3c7; color: #78350f; font-weight: 600; }}
.tag.stars {{ background: #fff7ed; color: #9a3412; }}
.probleme {{ font-size: 13px; margin: 4px 0 4px; }}
.specificite {{ font-size: 12px; color: #6b7280; margin: 0; }}
.owner-group {{ background: #fff; border: 1px solid #e5e7eb; border-radius: 6px;
                padding: 12px 14px; margin: 0 0 10px; }}
.owner-group h3 {{ margin: 0 0 6px; font-size: 14px; }}
.owner-list {{ display: flex; flex-wrap: wrap; gap: 6px; font-size: 12px; }}
.owner-list a {{ color: #0969da; text-decoration: none; padding: 2px 6px;
                 background: #f6f8fa; border-radius: 3px; }}
.dist-row {{ display: flex; justify-content: space-between; padding: 4px 0;
             border-bottom: 1px dashed #e5e7eb; font-size: 13px; }}
.dist-row:last-child {{ border: 0; }}
footer {{ margin-top: 30px; padding-top: 16px; border-top: 1px solid #e5e7eb;
          font-size: 11px; color: #9ca3af; text-align: center; }}
</style></head><body>

<h1>Minerva Newsletter</h1>
<p class="subtitle">Open source China intelligence embedded/IoT/robotics/edge-AI · {today_human}<br>
Last pipeline run: {html.escape(last_run)}</p>

<div class="stats">
  <div class="stat"><div class="num">{len(items)}</div><div class="lbl">Active fiches</div></div>
  <div class="stat"><div class="num">{len(big_tech)}</div><div class="lbl">Big tech (8 new orgs)</div></div>
  <div class="stat"><div class="num">{len(edge_ai)}</div><div class="lbl">Edge AI repos</div></div>
  <div class="stat"><div class="num">{len(set(i["owner"] for i in items))}</div><div class="lbl">Monitored accounts</div></div>
</div>
""")

    body.append("<h2>🏆 Top 10 findings (by relevance score)</h2>")
    for i in top10:
        body.append(fmt_card(i, highlight=True))

    body.append("<h2>🤖 Spotlight: new Edge AI domain ({} repos)</h2>".format(len(edge_ai)))
    body.append("<p>The <strong>Edge AI</strong> domain was added this week to capture Chinese mobile inference frameworks, NPU, and AI hardware acceleration.</p>")
    for i in edge_ai[:10]:
        body.append(fmt_card(i, highlight=False))
    if len(edge_ai) > 10:
        body.append(f"<p><em>+{len(edge_ai) - 10} more Edge AI repos in the dashboard.</em></p>")

    body.append("<h2>🏢 Focus: 8 new big-tech orgs added ({} repos)</h2>".format(len(big_tech)))
    body.append("<p>This week, integration of the official Gitee accounts of the Chinese giants: Alibaba, ByteDance, Baidu, PaddlePaddle, Tencent, JD, plus DongshanPi and LicheePi (RISC-V boards).</p>")

    by_owner: dict[str, list[dict]] = {}
    for i in big_tech:
        by_owner.setdefault(i["owner"].lower(), []).append(i)

    for owner in sorted(by_owner.keys(), key=lambda o: -len(by_owner[o])):
        repos = sorted(by_owner[owner], key=lambda x: -x["score"])
        body.append(f'<div class="owner-group"><h3>{html.escape(owner)} ({len(repos)} fiches)</h3>')
        body.append('<div class="owner-list">')
        for r in repos[:12]:
            body.append(f'<a href="{html.escape(r["gitee_url"])}" target="_blank">{html.escape(r["full_name"].split("/", 1)[1])} ({r["score"]})</a>')
        if len(repos) > 12:
            body.append(f'<span style="color:#9ca3af">+{len(repos) - 12} more</span>')
        body.append("</div></div>")

    body.append("<h2>📊 Distribution by domain</h2>")
    for dom, n in sorted(domain_count.items(), key=lambda x: -x[1]):
        pct = 100 * n / len(items)
        bar_w = int(pct * 4)
        body.append(f'<div class="dist-row"><span>{html.escape(dom)}</span><span><strong>{n}</strong> ({pct:.1f}%)</span></div>')

    body.append("<h2>🧱 Distribution by type</h2>")
    for t, n in sorted(type_count.items(), key=lambda x: -x[1]):
        pct = 100 * n / len(items)
        body.append(f'<div class="dist-row"><span>{html.escape(t)}</span><span><strong>{n}</strong> ({pct:.1f}%)</span></div>')

    body.append("""
<footer>Generated automatically by Minerva — Chinese tech intelligence pipeline.
See the interactive dashboard: <code>output/dashboard.html</code></footer>
</body></html>""")

    out_path.write_text("\n".join(body), encoding="utf-8")

    txt_path = OUT_DIR / f"newsletter_{today}.txt"
    txt_path.write_text(
        render_text_newsletter(items, top10, edge_ai, big_tech,
                               domain_count, type_count, today_human, last_run),
        encoding="utf-8",
    )

    print(f"OK : {out_path}")
    print(f"  Fiches included        : {len(items)}")
    print(f"  Top 10 (score)         : {[i['full_name'] for i in top10[:5]]}...")
    print(f"  Big tech (8 orgs)      : {len(big_tech)}")
    print(f"  Edge AI                : {len(edge_ai)}")
    print(f"  HTML size              : {out_path.stat().st_size / 1024:.1f} KB")
    print(f"OK : {txt_path}")
    print(f"  TXT size               : {txt_path.stat().st_size / 1024:.1f} KB")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8") if hasattr(sys.stdout, "reconfigure") else None
    raise SystemExit(main())
