"""Generates output/dashboard.html — single-file editorial page for Minerva.

Design language: "calm analytical instrument" — light-first (technical paper +
ink), one mineral signal accent, monospace for quantitative/identifier/label text,
confidence as ink marks, flat hairline components, no glow / no fake-live / no
floating shadows. See docs/DESIGN_TRACK.md and docs/design/dashboard.html.

Layout (unchanged from Phase 2):
  Hero → Featured (feature card) → The landscape (charts) → Runners-up (cards)
  → Explore (2-pane: compact list + light sticky detail) → How it works (pipeline)
  → Footer.

No external dependencies: HTML+CSS+JS+SVG inline, JSON inlined, openable via
file://. Self-contained by design (does not import build_site) — token values are
kept identical to build_site.py's BASE_CSS by hand so the two documents read as one
system; a stale favicon.svg reference is harmless if build_site.py hasn't run yet.

Interactivity (search/filter/sort/keyboard nav/presets) is UNCHANGED from Phase 2 —
this pass only re-skins presentation; see the `=== Bindings ===` section below.

TODO (Jinja2 templating refactor sprint): this file uses its own inline logic
to parse the markdown fiches, separate from src/fiche_schema.py. Migrate to
Fiche.from_markdown when the Jinja2 sprint is opened. For now we leave it
as-is (cf. PR #3 — feat/fiche-schema).
"""

import html
import json
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _watched_org_count() -> int:
    """Watched orgs from config — distinct from orgs that currently have fiches
    (conflating the two was an audit-flagged truth drift)."""
    try:
        cfg = json.loads((ROOT / "config" / "sources.json").read_text(encoding="utf-8"))
        return len(cfg.get("comptes_gitee", [])) + len(cfg.get("comptes_github", []))
    except Exception:
        return 0
sys.path.insert(0, str(ROOT / "src"))
from fiche_schema import confidence_tier, _is_recent_month  # noqa: E402 — shared confidence logic

STATE_FILE = ROOT / "output" / "state.json"
FICHES_DIR = ROOT / "output" / "fiches"
OUT_FILE = ROOT / "output" / "dashboard.html"


FIELD_RE = re.compile(r"^\*\*([^:*]+?)\s*:\*\*\s*(.*)$")
TITLE_RE = re.compile(r"^##\s+(.+?)(\s+\[MODIFIÉ\])?\s*$")
STARS_RE = re.compile(r"★\s*(\d+)")
FORKS_RE = re.compile(r"(\d+)\s*forks")
DATE_RE = re.compile(r"(?:updated|mis à jour) (\d{4}-\d{2})")

# EN (default) / FR label aliases, to parse either set interchangeably.
_LABELS = {
    "type": ("Type",),
    "domaine": ("Domain", "Domaine"),
    "score": ("Relevance score", "Score de pertinence"),
    "probleme": ("Problem solved", "Problème résolu"),
    "comment": ("How it works", "Comment ça marche"),
    "specificite": ("Chinese specificity", "Spécificité chinoise"),
    "equivalent": ("Western equivalent", "Équivalent occidental"),
    "maturite": ("Maturity", "Maturité"),
    "langue": ("Language", "Langue"),
    "source": ("Gitee", "GitHub"),
}


def _pick(fields: dict, key: str, default: str = "") -> str:
    for label in _LABELS[key]:
        if label in fields:
            return fields[label]
    return default


def slugify(full_name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_\-]", "_", full_name.replace("/", "_"))


def parse_fiche(path: Path) -> tuple[str | None, bool, dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    fields: dict[str, str] = {}
    title: str | None = None
    modified = False
    for line in text.splitlines():
        s = line.strip()
        if title is None:
            m = TITLE_RE.match(s)
            if m:
                title = m.group(1).strip()
                modified = bool(m.group(2))
                continue
        m = FIELD_RE.match(s)
        if m:
            fields[m.group(1).strip()] = m.group(2).strip()
    return title, modified, fields


def parse_int(s: str) -> int:
    m = re.search(r"(\d+)", s or "")
    return int(m.group(1)) if m else 0


def parse_stars(maturity: str) -> int:
    m = STARS_RE.search(maturity or "")
    return int(m.group(1)) if m else 0


def parse_forks(maturity: str) -> int:
    m = FORKS_RE.search(maturity or "")
    return int(m.group(1)) if m else 0


def parse_date(maturity: str) -> str:
    m = DATE_RE.search(maturity or "")
    return m.group(1) if m else ""


def parse_status(maturity: str) -> str:
    if not maturity:
        return ""
    return maturity.split(" (", 1)[0].strip()


def primary_domain(domaine: str) -> str:
    if not domaine:
        return ""
    return domaine.split(" / ", 1)[0].strip()


def web_slug(full_name: str) -> str:
    """Short lowercase owner-repo URL slug. Must match build_site.web_slug."""
    s = full_name.lower().replace("/", "-")
    s = re.sub(r"[^a-z0-9\-]+", "-", s)
    return s.strip("-")


def build_items(state_repos: dict[str, str],
                fiches_dir: Path = FICHES_DIR) -> tuple[list[dict], int]:
    items: list[dict] = []
    skipped = 0
    for full_name, pushed_at in state_repos.items():
        path = fiches_dir / f"{slugify(full_name)}_fiche.md"
        if not path.is_file():
            skipped += 1
            continue
        title, modified, fields = parse_fiche(path)
        if not title:
            skipped += 1
            continue
        maturity = _pick(fields, "maturite")
        owner = title.split("/", 1)[0] if "/" in title else ""
        domaine = _pick(fields, "domaine")
        comment = _pick(fields, "comment")
        prose_all = " ".join([_pick(fields, "probleme"), comment,
                              _pick(fields, "specificite"), _pick(fields, "equivalent")])
        has_meta = bool(STARS_RE.search(maturity) or DATE_RE.search(maturity))
        _dm = DATE_RE.search(maturity)
        is_recent = _is_recent_month(_dm.group(1)) if _dm else False
        confidence = confidence_tier(prose_all, len(comment), has_meta, is_recent)
        items.append({
            "full_name": title,
            "owner": owner,
            "modified": modified,
            "type": _pick(fields, "type"),
            "domaine": domaine,
            "domaine_primary": primary_domain(domaine),
            "score": parse_int(_pick(fields, "score")),
            "probleme": _pick(fields, "probleme"),
            "comment": comment,
            "confidence": confidence,
            "specificite": _pick(fields, "specificite"),
            "equivalent": _pick(fields, "equivalent"),
            "maturite": maturity,
            "status": parse_status(maturity),
            "stars": parse_stars(maturity),
            "forks": parse_forks(maturity),
            "date": parse_date(maturity),
            "langue": _pick(fields, "langue"),
            "gitee_url": _pick(fields, "source"),
            "pushed_at": pushed_at,
            "web_slug": web_slug(title),
        })
    items.sort(key=lambda x: x["score"], reverse=True)
    return items, skipped


def compute_aggregates(items: list[dict]) -> dict:
    """Pre-computes the aggregates used by the charts (4 domains + top orgs)."""
    DOMS = ["Embedded", "IoT", "Robotics", "Edge AI"]
    domain_counts: dict[str, int] = {d: 0 for d in DOMS}
    for it in items:
        for d in (it.get("domaine") or "").split(" / "):
            d = d.strip()
            if d in domain_counts:
                domain_counts[d] += 1

    owner_counts = Counter(it["owner"] for it in items if it["owner"])
    top_owners = owner_counts.most_common(12)

    total_stars = sum(it["stars"] or 0 for it in items)
    avg_score = round(sum(it["score"] for it in items) / max(1, len(items)))
    n_languages = len({"Bilingual CN-EN" if it["langue"] == "Bilingual CN-EN" else "Chinese" if it["langue"] == "Chinese" else "English" for it in items if it["langue"]})

    return {
        "domain_counts": domain_counts,
        "top_owners": top_owners,
        "total_stars": total_stars,
        "avg_score": avg_score,
        "n_languages": n_languages,
        "n_orgs": len(owner_counts),
    }


def fmt_int(n: int) -> str:
    s = f"{n:,}".replace(",", " ")
    return s


def fmt_stars(n: int) -> str:
    if n >= 10000:
        return f"{n/1000:.0f}k"
    if n >= 1000:
        return f"{n/1000:.1f}k"
    return fmt_int(n)


def conf_dm(conf: str) -> str:
    """Confidence as ink diamond marks (hue-neutral): High ◆◆◆, Medium ◆◆◇, Low ◆◇◇."""
    n = {"High": 3, "Medium": 2, "Low": 1}.get(conf, 0)
    if not n:
        return ""
    on, off = "◆" * n, "◇" * (3 - n)
    return f'{on}<span class="off">{off}</span>' if off else on


DOM_KEY = {"Embedded": "emb", "IoT": "iot", "Robotics": "rob", "Edge AI": "edge"}
DOM_HEX = {"emb": "var(--d-emb)", "edge": "var(--d-edge)", "rob": "var(--d-rob)", "iot": "var(--d-iot)"}


def render_domain_bars(domain_counts: dict[str, int]) -> str:
    """HTML rendering of the per-domain bars. Width = count / max_count."""
    if not domain_counts:
        return ""
    max_count = max(domain_counts.values()) or 1
    total = sum(domain_counts.values()) or 1
    keys = ["Embedded", "IoT", "Robotics", "Edge AI"]
    rows = []
    for k in keys:
        count = domain_counts.get(k, 0)
        pct_max = (count / max_count) * 100
        pct_total = (count / total) * 100
        rows.append(
            f'<div class="bar-row" data-domain="{html.escape(k)}">'
            f'<div class="bar-label">{html.escape(k)}</div>'
            f'<div class="bar-track">'
            f'<div class="bar-fill {DOM_KEY.get(k,"")}" style="width:{pct_max:.1f}%"></div>'
            f'</div>'
            f'<div class="bar-value tnum">{count} <span class="bar-pct">· {pct_total:.0f}%</span></div>'
            f'</div>'
        )
    return "\n".join(rows)


def render_owner_bars(top_owners: list[tuple[str, int]]) -> str:
    if not top_owners:
        return ""
    max_count = top_owners[0][1] or 1
    rows = []
    for owner, count in top_owners:
        pct = (count / max_count) * 100
        rows.append(
            f'<div class="bar-row org">'
            f'<div class="bar-label mono">{html.escape(owner)}</div>'
            f'<div class="bar-track"><div class="bar-fill signal" style="width:{pct:.1f}%"></div></div>'
            f'<div class="bar-value tnum">{count}</div>'
            f'</div>'
        )
    return "\n".join(rows)


HTML_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Minerva — Chinese open source watch</title>
<meta name="description" content="Decision-ready watch on China's open-source hardware ecosystem — __N__ fiches, __N_ORGS__ organizations, Gitee + GitHub.">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<style>
:root {
  --paper:#F5F6F4; --surface:#FFFFFF; --surface-2:#FAFBF9;
  --ink:#1B1E20; --ink-2:#565C61; --ink-3:#8A9096; --ink-4:#B9BEC2;
  --line:#E4E6E2; --line-2:#CDD0CB; --grid:rgba(27,30,32,0.028);
  --signal:#2F5A5C; --signal-2:#244748; --signal-soft:#E9EEEC;
  --d-emb:#4C6FA4; --d-edge:#8A6AA0; --d-rob:#5E8C6A; --d-iot:#B4894C;
  --sans:-apple-system,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;
  --mono:ui-monospace,"SF Mono","JetBrains Mono",Menlo,Consolas,monospace;

  /* D5 — bounded instrument register (status-line + Featured readout ONLY;
     never a page-wide theme — this is not dark mode). Mirrors build_site.py. */
  --slab:#1B1E20; --slab-2:#262B2D; --slab-ink:#F5F6F4;
  --slab-line:rgba(245,246,244,0.14); --signal-on-slab:#5B948F;
  /* D5 — flattened radius scale: kills the generic "SaaS card" 5-8px softness. */
  --r-0:0px; --r-sm:2px; --r-pill:100px;
  --tick:var(--ink-4);
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body {
  font-family: var(--sans);
  background: var(--paper);
  color: var(--ink);
  font-size: 15px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  font-feature-settings: "tnum","cv02","cv03";
  background-image: linear-gradient(var(--grid) 1px,transparent 1px),
                     linear-gradient(90deg,var(--grid) 1px,transparent 1px);
  background-size: 34px 34px;
}
a { color: inherit; text-decoration: none; }
.mono { font-family: var(--mono); }
.tnum { font-variant-numeric: tabular-nums; }
main, header, footer, section, nav { position: relative; z-index: 1; }
.wrap { max-width: 1180px; margin: 0 auto; padding: 0 28px; }

/* NAV */
nav.top { position: sticky; top: 0; z-index: 40; background: rgba(245,246,244,0.86);
  backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); border-bottom: 1px solid var(--line-2); }
nav.top .row { display: flex; align-items: center; gap: 20px; padding: 13px 0; }
.brand { display: flex; align-items: center; gap: 9px; color: var(--ink); }
.mark { width: 14px; height: 14px; border: 2px solid var(--ink); border-radius: var(--r-sm); position: relative; flex: none; }
.mark::after { content: ""; position: absolute; inset: 3px 3px auto auto; width: 4px; height: 4px; background: var(--signal); }
.brand b { font-family: var(--mono); font-size: 14.5px; font-weight: 600; letter-spacing: 0.02em; }
nav.top .links { margin-left: auto; display: flex; gap: 20px; align-items: center; }
nav.top .links a { font-size: 13.5px; color: var(--ink-2); font-weight: 500; }
nav.top .links a:hover { color: var(--ink); }
nav.top .links a.active { color: var(--signal); }
nav.top .links .pro { border: 1px solid var(--line-2); border-radius: var(--r-sm); padding: 5px 12px; color: var(--ink); }
nav.top .links .pro:hover { border-color: var(--signal); color: var(--signal); }

/* STATUS LINE — one shared, bounded instrument band under nav (D5). Slab-
   registered but confined to this strip only — not a page theme. */
.status-line { background: var(--slab); color: var(--slab-ink); }
.status-line .srow { display: flex; align-items: center; gap: 0; padding: 7px 0; font-family: var(--mono); font-size: 11px; letter-spacing: 0.02em; }
.status-line .seg { display: flex; align-items: center; gap: 7px; padding: 0 16px; position: relative; }
.status-line .seg:first-child { padding-left: 0; }
.status-line .seg:not(:last-child)::after { content: ""; position: absolute; right: 0; top: 2px; bottom: 2px; width: 1px; background: var(--slab-line); }
.status-line .dot { width: 5px; height: 5px; border-radius: var(--r-sm); background: var(--signal-on-slab); flex: none; }
.status-line .accent { color: var(--signal-on-slab); font-weight: 600; }
.status-line .ticks { margin-left: auto; display: flex; gap: 4px; }
.status-line .ticks i { display: block; width: 1px; height: 10px; background: var(--slab-line); }

/* SECTION MARKERS (01 / The landscape etc.) */
.s-marker {
  display: flex; align-items: baseline; gap: 14px;
  margin: 72px 0 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--line);
}
.s-marker .num {
  font-family: var(--mono); font-size: 12px; font-weight: 700;
  color: var(--signal); letter-spacing: 2px;
}
.s-marker h2 { font-family: var(--sans); margin: 0; font-size: 26px; font-weight: 680; letter-spacing: -0.025em; color: var(--ink); }
.s-marker .sub { margin-left: auto; font-size: 13px; color: var(--ink-3); max-width: 360px; text-align: right; }

/* HERO */
.hero { padding: 40px 0 36px; border-bottom: 1px solid var(--line); }
.badge {
  display: inline-flex; align-items: center; gap: 8px;
  font-family: var(--mono); font-size: 11.5px; color: var(--ink-2);
  background: var(--surface); border: 1px solid var(--line-2);
  border-radius: var(--r-pill); padding: 5px 12px; letter-spacing: 0.02em;
}
.badge .d { width: 6px; height: 6px; border-radius: var(--r-sm); background: var(--signal); }
.hero h1 { font-family: var(--sans); margin: 0 0 14px; font-size: clamp(30px,4vw,44px); font-weight: 700; letter-spacing: -0.03em; line-height: 1.05; max-width: 22ch; color: var(--ink); }
.hero .lede { font-size: clamp(15.5px,1.6vw,17.5px); line-height: 1.55; color: var(--ink-2); max-width: 720px; margin: 0 0 8px; font-weight: 400; }
.hero .lede strong { color: var(--ink); font-weight: 600; }
.hero-stats { display: grid; grid-template-columns: repeat(4,1fr); gap: 0; margin-top: 26px; border: 1px solid var(--line); border-radius: var(--r-0); overflow: hidden; background: var(--surface); }
.hero-stats .cell { padding: 16px 18px; border-right: 1px solid var(--line); }
.hero-stats .cell:last-child { border-right: none; }
.hero-stats .num { font-family: var(--mono); font-size: clamp(22px,2.6vw,28px); font-weight: 600; letter-spacing: -0.01em; line-height: 1; color: var(--ink); }
.hero-stats .num em { font-style: normal; font-size: 13px; color: var(--ink-3); font-weight: 500; margin-left: 3px; }
.hero-stats .lbl { margin-top: 6px; font-family: var(--mono); font-size: 11px; color: var(--ink-3); text-transform: uppercase; letter-spacing: 0.06em; }
.hero .meta-line { margin-top: 16px; font-family: var(--mono); font-size: 11.5px; color: var(--ink-3); display: flex; gap: 18px; flex-wrap: wrap; }
.hero .meta-line strong { color: var(--ink-2); font-weight: 600; }
.hero .meta-line code { background: var(--surface); padding: 0 5px; border-radius: var(--r-sm); border: 1px solid var(--line); color: var(--ink); }

/* SHARED ATOMS */
.tag { display: inline-flex; align-items: center; gap: 6px; font-family: var(--mono); font-size: 11px; font-weight: 600;
  letter-spacing: 0.02em; padding: 3px 8px; border-radius: var(--r-sm); border: 1px solid var(--line-2); color: var(--ink-2); background: var(--surface); }
.tag.type, .tag.plain { color: var(--ink-2); }
.tag.dom-Embedded { color: var(--d-emb); } .tag.dom-IoT { color: var(--d-iot); }
.tag.dom-Robotics { color: var(--d-rob); } .tag.dom-EdgeAI { color: var(--d-edge); }
.tag.st-Stable, .tag.st-Active, .tag.st-Experimental, .tag.st-Archived { color: var(--ink-2); }
.tag.conf-High, .tag.conf-Medium, .tag.conf-Low { color: var(--ink-2); font-family: var(--mono); }
.conf { font-family: var(--mono); font-size: 11px; color: var(--ink-2); display: inline-flex; align-items: center; gap: 6px; }
.conf .dm, .conf-dm { letter-spacing: 1px; color: var(--ink); } .off { color: var(--ink-4); }
.badge-mod { display: inline-block; font-family: var(--mono); font-size: 9.5px; font-weight: 700; letter-spacing: 0.06em;
  color: var(--signal-2); background: var(--signal-soft); border: 1px solid var(--line-2);
  border-radius: var(--r-sm); padding: 1px 4px; margin-left: 5px; vertical-align: 1px; }

/* READOUT — score/confidence/domain as a structural instrument panel (D5).
   The ONE readout slab for this page (inside Featured only) — do not add a
   second one elsewhere on the dashboard (stay calm; Runners-up/Explorer/
   Pipeline stay on the light surface register). */
.readout { background: var(--slab); color: var(--slab-ink); border-radius: var(--r-0);
  padding: 16px 20px; display: flex; align-items: center; gap: 26px; flex-wrap: wrap; position: relative; overflow: hidden; margin-bottom: 18px; }
.readout::before { content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 5px; background: var(--dom-color,var(--ink-4)); }
.readout .rblock { display: flex; flex-direction: column; gap: 3px; }
.readout .rlab { font-family: var(--mono); font-size: 9.5px; text-transform: uppercase; letter-spacing: 0.09em; color: var(--ink-4); }
.readout .rval { font-family: var(--mono); font-size: 24px; font-weight: 600; letter-spacing: -0.01em; color: var(--slab-ink); line-height: 1; }
.readout .rval .unit { font-size: 11px; color: var(--ink-4); font-weight: 500; margin-left: 2px; }
.readout .rval.conf { font-size: 16px; letter-spacing: 2px; }
.readout .rval.dom { font-size: 14px; letter-spacing: 0; color: var(--slab-ink); font-weight: 600; }
.readout .off { color: #4A5052; }
.readout .rmeta { margin-left: auto; font-family: var(--mono); font-size: 10.5px; color: var(--ink-4); text-align: right; }

/* FEATURED */
.feature { padding: 30px 32px; background: var(--surface);
  border: 1px solid var(--line-2); border-radius: var(--r-0); }
.feature .feat-body { display: grid; grid-template-columns: 1fr 320px; gap: 40px; }
.feature h3 { font-family: var(--mono); font-size: clamp(20px,2.6vw,28px); font-weight: 600; letter-spacing: -0.01em;
  margin: 0 0 14px; word-break: break-word; line-height: 1.15; }
.feature h3 a:hover { color: var(--signal); }
.feature .feat-tags { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 22px; }
.feature .feat-prose { font-size: 16px; color: var(--ink); line-height: 1.65; margin: 0 0 12px; max-width: 620px; }
.feature .feat-prose-secondary { font-size: 14px; color: var(--ink-2); line-height: 1.6; margin: 0 0 20px; max-width: 620px; }
.feature .feat-cta { display: inline-flex; align-items: center; gap: 8px; padding: 10px 16px; background: var(--signal);
  color: #fff; border-radius: var(--r-sm); font-size: 13.5px; font-weight: 600; width: fit-content; transition: background .14s; }
.feature .feat-cta:hover { background: var(--signal-2); }
.feature .feat-side { border-left: 1px solid var(--line); padding-left: 28px; display: flex; flex-direction: column; gap: 16px; }
.feature .feat-side .kb.hl { background: var(--signal-soft); border-radius: var(--r-0); padding: 10px 12px; margin-left: -12px; margin-right: -12px; }
.feature .kb h5 { margin: 0 0 5px; font-family: var(--mono); font-size: 10.5px; font-weight: 700; color: var(--ink-3);
  text-transform: uppercase; letter-spacing: 0.07em; }
.feature .kb.hl h5 { color: var(--signal-2); }
.feature .kb p { margin: 0; font-size: 13.5px; color: var(--ink); line-height: 1.55; }
.feature .kb.hl p { font-weight: 560; }
.feature .kb p.mono { font-family: var(--mono); font-size: 12.5px; }

/* LANDSCAPE — charts */
.charts { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.chart-card { background: var(--surface); border: 1px solid var(--line); border-radius: var(--r-0); padding: 24px; }
.chart-card h4 { margin: 0 0 4px; font-size: 15.5px; font-weight: 620; letter-spacing: -0.01em; }
.chart-card .chart-sub { margin: 0 0 20px; font-size: 12.5px; color: var(--ink-3); }
.bar-row { display: grid; grid-template-columns: 100px 1fr 66px; align-items: center; gap: 12px; padding: 7px 0; font-size: 12.5px; }
.bar-row.org { grid-template-columns: 130px 1fr 34px; }
.bar-label { color: var(--ink-2); font-weight: 500; }
.bar-row.org .bar-label { font-size: 11.5px; color: var(--ink); }
.bar-track { height: 5px; background: var(--line); border-radius: var(--r-sm); overflow: hidden; }
.bar-fill { height: 100%; border-radius: var(--r-sm); background: var(--ink-3); }
.bar-fill.emb { background: var(--d-emb); } .bar-fill.iot { background: var(--d-iot); }
.bar-fill.rob { background: var(--d-rob); } .bar-fill.edge { background: var(--d-edge); }
.bar-fill.signal { background: var(--signal); }
.bar-value { font-weight: 600; color: var(--ink); text-align: right; }
.bar-pct { color: var(--ink-3); font-weight: 400; font-size: 11.5px; }

/* RUNNERS-UP */
.runner-up { display: grid; grid-template-columns: repeat(4,1fr); gap: 14px; }
.runner { background: var(--surface); border: 1px solid var(--line); border-radius: var(--r-0); padding: 16px 18px;
  display: flex; flex-direction: column; position: relative; transition: border-color .14s; }
.runner:hover { border-color: var(--ink-4); }
.runner .rk { position: absolute; top: 14px; right: 16px; font-family: var(--mono); font-size: 11px; font-weight: 700; color: var(--ink-4); }
.runner .runner-score { display: inline-flex; align-items: center; font-family: var(--mono); font-size: 12px; font-weight: 700;
  color: var(--signal-2); background: var(--signal-soft); padding: 3px 9px; border-radius: var(--r-sm); width: fit-content; margin-bottom: 12px; }
.runner h4 { font-family: var(--mono); font-size: 13px; font-weight: 600; margin: 0 0 8px; word-break: break-word; line-height: 1.35; }
.runner h4 a:hover { color: var(--signal); }
.runner .runner-tags { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 10px; }
.runner p { font-size: 12.5px; color: var(--ink-2); line-height: 1.5; margin: 0 0 12px; flex: 1;
  display: -webkit-box; -webkit-line-clamp: 4; -webkit-box-orient: vertical; overflow: hidden; }
.runner .runner-meta { font-family: var(--mono); font-size: 11px; color: var(--ink-3); border-top: 1px solid var(--line);
  padding-top: 9px; display: flex; gap: 12px; }

/* Use-case quick views */
.presets { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 14px; }
.preset { font-family: var(--sans); font-size: 12.5px; font-weight: 600; color: var(--ink-2); background: var(--surface);
  border: 1px solid var(--line-2); border-radius: var(--r-pill); padding: 6px 13px; cursor: pointer; transition: all .14s; }
.preset:hover { border-color: var(--signal); color: var(--signal); }
.preset.active { background: var(--signal); border-color: var(--signal); color: #fff; }

/* Explorer: 2-pane (compact list + light sticky detail). Kept on the light
   register — D5 deliberately does NOT slab this surface: with 106 rows re-
   rendering on every keystroke/arrow-press, a dark panel here would flip
   constantly during fast exploration and violate "keep the slab calm". */
.explorer { display: grid; grid-template-columns: minmax(290px, 380px) 1fr; gap: 16px; align-items: start; }
.ex-list { display: flex; flex-direction: column; gap: 0; max-height: 74vh; overflow-y: auto;
  border: 1px solid var(--line); border-radius: var(--r-0); background: var(--surface); }
.ex-list::-webkit-scrollbar { width: 8px; }
.ex-list::-webkit-scrollbar-thumb { background: var(--line-2); border-radius: var(--r-sm); }
.ex-row {
  display: flex; align-items: center; gap: 10px; width: 100%;
  padding: 9px 13px; border: none; border-bottom: 1px solid var(--line); border-left: 2px solid transparent;
  background: transparent; cursor: pointer; text-align: left; font: inherit;
}
.ex-list .ex-row:last-child { border-bottom: none; }
.ex-row:hover { background: var(--surface-2); }
.ex-row.sel { background: var(--signal-soft); border-left-color: var(--signal); }
.ex-row .rscore { font-family: var(--mono); font-weight: 600; font-size: 13px; width: 24px; color: var(--ink); flex: none; }
/* Domain tick — a calm structural bar, not a decorative dot (D5). JS only sets
   the inline background-color; shape/size stay controlled here. */
.ex-row .rdot { width: 3px; height: 16px; border-radius: var(--r-sm); flex: none; }
.ex-row .rname { font-family: var(--mono); font-size: 13px; font-weight: 500; color: var(--ink); overflow: hidden;
  text-overflow: ellipsis; white-space: nowrap; flex: 1; }
.ex-row .rconf { font-family: var(--mono); font-size: 11px; letter-spacing: 1px; color: var(--ink); flex: none; }

.ex-detail { position: sticky; top: 66px; border: 1px solid var(--line-2); border-radius: var(--r-0); background: var(--surface);
  min-height: 200px; overflow: hidden; }
.ex-detail .d-top { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; padding: 15px 20px;
  border-bottom: 1px solid var(--line); background: var(--surface-2); }
.ex-detail .d-score { font-family: var(--mono); color: var(--ink); font-weight: 600; font-size: 14px; }
.ex-detail .d-name { font-family: var(--mono); font-weight: 600; font-size: 14.5px; color: var(--ink); margin-left: 4px; }
.ex-detail .d-name:hover { color: var(--signal); }
.ex-detail .d-tags { display: flex; gap: 6px; flex-wrap: wrap; margin: 12px 20px 0; }
.ex-detail .d-meta { font-family: var(--mono); font-size: 11.5px; color: var(--ink-3); display: flex; gap: 14px; flex-wrap: wrap; margin: 10px 20px 0; }
.ex-detail .d-field { padding: 12px 20px; border-top: 1px solid var(--line); margin-top: 12px; }
.ex-detail .d-field:first-of-type { margin-top: 14px; }
.ex-detail .d-field .d-lab { display: flex; gap: 8px; flex-wrap: wrap; align-items: baseline; font-family: var(--mono);
  font-size: 10.5px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--ink-3); margin-bottom: 4px; }
.ex-detail .d-field .d-lab em { font-family: var(--sans); font-style: normal; text-transform: none; letter-spacing: 0;
  font-weight: 600; color: var(--signal); font-size: 10.5px; }
.ex-detail .d-field p { margin: 0; font-size: 13.5px; line-height: 1.55; color: var(--ink); }
.ex-detail .d-field.hl { background: var(--signal-soft); margin: 12px 0 0; padding: 12px 20px; border-top: none; }
.ex-detail .d-field.hl .d-lab { color: var(--signal-2); }
.ex-detail .d-field.hl p { font-weight: 560; }
.ex-detail .d-foot { display: flex; gap: 16px; flex-wrap: wrap; margin-top: 4px; padding: 11px 20px; font-family: var(--mono);
  font-size: 11px; color: var(--ink-3); background: var(--surface-2); border-top: 1px solid var(--line); }
.ex-detail .d-foot a { color: var(--signal); font-weight: 600; }
.ex-detail .d-foot a:hover { color: var(--signal-2); }

@media (max-width: 820px) {
  .explorer { grid-template-columns: 1fr; }
  .ex-list { max-height: 340px; }
  .ex-detail { position: static; }
}

/* TOOLBAR + FILTERS */
/* top: below the sticky nav (~48px) so the toolbar never slides under it. */
.toolbar-wrap { position: sticky; top: 48px; z-index: 30; background: rgba(245,246,244,0.9);
  backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
  border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); margin-top: 24px; }
.toolbar { padding: 14px 0; display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.search { flex: 1 1 260px; min-width: 220px; position: relative; display: flex; align-items: center; gap: 8px;
  background: var(--surface); border: 1px solid var(--line-2); border-radius: var(--r-sm); padding: 8px 12px; }
.search svg { width: 14px; height: 14px; color: var(--ink-3); flex: none; }
.search input { flex: 1; border: none; outline: none; background: none; font-family: var(--mono); font-size: 13px; color: var(--ink); }
.search input::placeholder { color: var(--ink-3); }
.search kbd { font-family: var(--mono); font-size: 11px; color: var(--ink-3); border: 1px solid var(--line-2); border-radius: var(--r-sm); padding: 0 5px; flex: none; }
.search:focus-within { border-color: var(--signal); box-shadow: 0 0 0 3px var(--signal-soft); }
.search:focus-within kbd { display: none; }

.chips { display: flex; gap: 6px; flex-wrap: wrap; }
.chip { display: inline-flex; align-items: center; gap: 6px; font-family: var(--sans); background: var(--surface);
  border: 1px solid var(--line-2); color: var(--ink-2); padding: 7px 12px; border-radius: var(--r-sm); font-size: 12.5px;
  font-weight: 600; cursor: pointer; transition: all .14s; }
.chip:hover { border-color: var(--signal); color: var(--signal); }
.chip.active { background: var(--signal); border-color: var(--signal); color: #fff; }

select.minimal { font-family: var(--sans); background: var(--surface); border: 1px solid var(--line-2); color: var(--ink);
  padding: 7px 26px 7px 11px; border-radius: var(--r-sm); font-size: 12.5px; cursor: pointer;
  appearance: none; -webkit-appearance: none;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='6' viewBox='0 0 10 6' fill='none'><path d='M1 1l4 4 4-4' stroke='%23565C61' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'/></svg>");
  background-position: right 9px center; background-repeat: no-repeat; max-width: 190px; }
select.minimal:focus { outline: none; border-color: var(--signal); }

.btn-reset { font-family: var(--sans); background: var(--surface); border: 1px solid var(--line-2); color: var(--ink-2);
  padding: 7px 13px; border-radius: var(--r-sm); font-size: 12.5px; font-weight: 600; cursor: pointer; transition: all .14s; }
.btn-reset:hover { border-color: var(--signal); color: var(--signal); }

.result-info { font-family: var(--mono); font-size: 11.5px; color: var(--ink-3); padding: 14px 0 10px;
  display: flex; gap: 14px; align-items: center; flex-wrap: wrap; }
.result-info strong { color: var(--ink); }
.result-info .dot { width: 3px; height: 3px; border-radius: 50%; background: var(--ink-4); }

.empty { padding: 70px 0; text-align: center; color: var(--ink-3); }
.empty .ico { font-size: 40px; opacity: 0.4; margin-bottom: 10px; }
.empty h3 { color: var(--ink); font-weight: 620; margin: 0 0 6px; font-size: 17px; }

/* PIPELINE */
.pipeline-wrap { background: var(--surface); border: 1px solid var(--line); border-radius: var(--r-0); padding: 32px; }
.pipeline-svg { width: 100%; height: auto; margin: 10px 0 22px; }
.pipeline-text { display: grid; grid-template-columns: repeat(4,1fr); gap: 20px; margin-top: 10px; }
.pipeline-text .step h5 { margin: 0 0 5px; font-family: var(--mono); font-size: 12px; font-weight: 700; color: var(--ink); }
.pipeline-text .step p { margin: 0; font-size: 12.5px; color: var(--ink-2); line-height: 1.5; }
.pipeline-text .step code { font-family: var(--mono); font-size: 11px; background: var(--surface-2); padding: 0 5px;
  border-radius: var(--r-sm); border: 1px solid var(--line); color: var(--ink); }
.tech-stack { margin-top: 28px; padding-top: 22px; border-top: 1px solid var(--line);
  display: flex; gap: 14px 28px; flex-wrap: wrap; font-family: var(--mono); font-size: 11.5px; color: var(--ink-3); }
.tech-stack .item strong { color: var(--ink-2); font-weight: 600; }

/* FOOTER */
footer { margin-top: 60px; padding: 26px 0 40px; border-top: 1px solid var(--line); font-family: var(--mono); font-size: 11.5px; color: var(--ink-3); }
footer .row { display: flex; justify-content: space-between; gap: 16px; flex-wrap: wrap; }
footer .signature { font-family: var(--mono); }
footer a { color: var(--ink-2); } footer a:hover { color: var(--signal); }

@media (max-width: 980px) {
  .wrap { padding: 0 22px; }
  .feature { grid-template-columns: 1fr; gap: 24px; padding: 24px; }
  .feature .feat-side { border-left: none; border-top: 1px solid var(--line); padding-left: 0; padding-top: 20px; }
  .charts { grid-template-columns: 1fr; gap: 14px; }
  .runner-up { grid-template-columns: repeat(2,1fr); }
  .pipeline-text { grid-template-columns: repeat(2,1fr); }
  .hero-stats { grid-template-columns: repeat(2,1fr); }
  .hero-stats .cell:nth-child(2n) { border-right: none; }
  .hero-stats .cell:nth-child(-n+2) { border-bottom: 1px solid var(--line); }
  .s-marker { margin-top: 52px; }
  .s-marker h2 { font-size: 21px; }
  .s-marker .sub { display: none; }
}
@media (max-width: 580px) {
  .runner-up { grid-template-columns: 1fr; }
  .pipeline-text { grid-template-columns: 1fr; }
  .hero { padding: 44px 0 26px; }
  .hero-stats { grid-template-columns: 1fr; }
  .hero-stats .cell { border-right: none; border-bottom: 1px solid var(--line); }
  .hero-stats .cell:last-child { border-bottom: none; }
}
</style>
</head>
<body>

<nav class="top"><div class="wrap row">
  <a class="brand" href="index.html"><span class="mark"></span><b>MINERVA</b></a>
  <span class="links">
    <a href="dashboard.html" class="active">Dashboard</a>
    <a href="index.html#newsletter">Newsletter</a>
    <a href="pro.html" class="pro">Pro</a>
  </span>
</div></nav>

<div class="status-line"><div class="wrap srow">
  <span class="seg"><span class="dot"></span><span class="accent">Snapshot</span>&nbsp;· as of __LAST_RUN__</span>
  <span class="seg">__N__ fiches</span>
  <span class="seg">reading: dashboard</span>
  <span class="ticks"><i></i><i></i><i></i><i></i><i></i></span>
</div></div>

<header class="hero wrap">
  <h1>Decision-ready watch on China's open-source hardware ecosystem.</h1>
  <p class="lede">
    Minerva scans <strong>__N_WATCHED__ watched organizations</strong> across
    <strong>Gitee and GitHub</strong>, scores each repo across
    <strong>4 technical domains</strong>, and turns the relevant ones into
    structured EN/FR fiches — each mapped to its <strong>Western equivalent</strong>.
    <strong>__N__ projects</strong> from <strong>__N_ORGS__ orgs</strong> made the
    cut in this snapshot.
  </p>
  <div class="hero-stats">
    <div class="cell"><div class="num tnum">__N__</div><div class="lbl">Active fiches</div></div>
    <div class="cell"><div class="num tnum">__N_ORGS__</div><div class="lbl">Organizations</div></div>
    <div class="cell"><div class="num tnum">__STARS_FMT__<em>★</em></div><div class="lbl">Total stars</div></div>
    <div class="cell"><div class="num tnum">__AVG_SCORE__<em>/100</em></div><div class="lbl">Average score</div></div>
  </div>
  <div class="meta-line">
    <span><strong>Stack</strong> Python 3.10 · Claude Haiku 4.5 · Gitee + GitHub APIs</span>
    <span><strong>LLM cost</strong> ~$0.01 per bilingual fiche pair</span>
    <span><strong>Run</strong> <code>python src/pipeline.py</code></span>
    <span><strong>License</strong> Apache 2.0</span>
  </div>
</header>

<main>

<section class="wrap">
  <div class="s-marker">
    <span class="num">01</span>
    <h2>Featured</h2>
    <span class="sub">The fiche with the highest relevance score — the one to know if you only look at one.</span>
  </div>

  <article class="feature">
    <div class="readout" style="--dom-color:__FEAT_DOM_COLOR__">
      <div class="rblock"><span class="rlab" title="Coarse triage signal, 0-100 (semantic similarity + activity bonuses) — a sort key, not a measurement">Score</span><span class="rval tnum">__FEAT_SCORE__<span class="unit">/100</span></span></div>
      <div class="rblock"><span class="rlab" title="Data-quality tier: enrichment depth, metadata, recency — ◆◆◆ High / ◆◆◇ Medium / ◆◇◇ Low">Confidence</span><span class="rval conf">__FEAT_CONF_DM__</span></div>
      <div class="rblock"><span class="rlab">Domain</span><span class="rval dom">__FEAT_DOMAIN__</span></div>
      <div class="rmeta">highest-scored decision-grade fiche in this snapshot</div>
    </div>
    <div class="feat-body">
      <div class="feat-main">
        <h3><a href="__FEAT_URL__" target="_blank" rel="noopener">__FEAT_NAME__</a></h3>
        <div class="feat-tags">__FEAT_TAGS__</div>
        <p class="feat-prose">__FEAT_PROBLEME__</p>
        <p class="feat-prose-secondary">__FEAT_COMMENT__</p>
        <a class="feat-cta" href="__FEAT_URL__" target="_blank" rel="noopener">__FEAT_SRC_LABEL__ →</a>
      </div>
      <aside class="feat-side">
        <div class="kb"><h5>Chinese specificity</h5><p>__FEAT_SPEC__</p></div>
        <div class="kb hl"><h5>Western equivalent</h5><p>__FEAT_EQUIV__</p></div>
        <div class="kb"><h5>Maturity</h5><p class="mono">__FEAT_MAT__</p></div>
      </aside>
    </div>
  </article>
</section>

<section class="wrap">
  <div class="s-marker">
    <span class="num">02</span>
    <h2>The landscape</h2>
    <span class="sub">Distribution of the corpus by technical domain and by organization.</span>
  </div>
  <div class="charts">
    <div class="chart-card">
      <h4>By domain</h4>
      <p class="chart-sub">4 domains covered. A fiche can count in several domains.</p>
      __DOMAIN_BARS__
    </div>
    <div class="chart-card">
      <h4>Top 12 organizations</h4>
      <p class="chart-sub">Editorial concentration of the current corpus.</p>
      __OWNER_BARS__
    </div>
  </div>
</section>

<section class="wrap">
  <div class="s-marker">
    <span class="num">03</span>
    <h2>Runners-up</h2>
    <span class="sub">The 4 fiches right after the Featured one, by descending score.</span>
  </div>
  <div class="runner-up">
    __RUNNERS__
  </div>
</section>

<section class="wrap">
  <div class="s-marker">
    <span class="num">04</span>
    <h2>Explore the corpus</h2>
    <span class="sub">Pick a fiche on the left, read its decision layer on the right. Search, filter, or use a quick view. ↑/↓ to move.</span>
  </div>
  <div class="presets">
    <button class="preset" data-preset="edge-ai">⚡ Edge-AI benchmarking</button>
    <button class="preset" data-preset="robotics">🤖 Robotics stacks</button>
    <button class="preset" data-preset="embedded">🔧 RTOS / BSP / firmware</button>
    <button class="preset" data-preset="high-conf">◆ High-confidence only</button>
  </div>
</section>

<div class="toolbar-wrap">
  <div class="toolbar wrap">
    <div class="search">
      <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="7" cy="7" r="5"/><path d="m11 11 4 4"/></svg>
      <input type="search" id="q" placeholder="Search across __N__ fiches…" autocomplete="off">
      <kbd>/</kbd>
    </div>
    <div class="chips">
      <button class="chip" data-domain="Embedded">Embedded</button>
      <button class="chip" data-domain="IoT">IoT</button>
      <button class="chip" data-domain="Robotics">Robotics</button>
      <button class="chip" data-domain="Edge AI">Edge AI</button>
    </div>
    <select class="minimal" id="f-owner"><option value="">All accounts</option></select>
    <select class="minimal" id="f-type"><option value="">All types</option></select>
    <select class="minimal" id="f-status"><option value="">Any maturity</option></select>
    <select class="minimal" id="sort">
      <option value="score-desc">Score ↓</option>
      <option value="stars-desc">Stars ↓</option>
      <option value="date-desc">Recent push ↓</option>
      <option value="name-asc">Name A→Z</option>
    </select>
    <button class="btn-reset" id="reset">Reset</button>
  </div>
</div>

<section class="wrap">
  <div class="result-info">
    <span><strong id="r-shown">0</strong> / <span id="r-total">__N__</span> fiches shown</span>
    <span class="dot"></span>
    <span id="r-active">no active filter</span>
  </div>
  <div class="explorer" id="explorer">
    <div class="ex-list" id="ex-list"></div>
    <aside class="ex-detail" id="ex-detail"></aside>
  </div>
  <div class="empty" id="empty" style="display:none">
    <div class="ico">⌀</div>
    <h3>No fiche matches</h3>
    <p>Try loosening a filter or shortening the search.</p>
  </div>
</section>

<section class="wrap">
  <div class="s-marker">
    <span class="num">05</span>
    <h2>How it works</h2>
    <span class="sub">4-step pipeline, incremental by design — every run is dated.</span>
  </div>
  <div class="pipeline-wrap">
    <svg class="pipeline-svg" viewBox="0 0 900 140" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <defs>
        <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
          <path d="M0,0 L10,5 L0,10 Z" fill="#8A9096"/>
        </marker>
      </defs>
      <g font-family="ui-monospace, monospace" font-size="11" fill="#565C61">
        <rect x="20"  y="40" width="170" height="60" rx="6" fill="#FFFFFF" stroke="#CDD0CB" stroke-width="1.5"/>
        <text x="105" y="68" text-anchor="middle" fill="#1B1E20" font-size="13" font-weight="600">Collection</text>
        <text x="105" y="86" text-anchor="middle">Gitee + GitHub APIs</text>

        <rect x="240" y="40" width="170" height="60" rx="6" fill="#FFFFFF" stroke="#CDD0CB" stroke-width="1.5"/>
        <text x="325" y="68" text-anchor="middle" fill="#1B1E20" font-size="13" font-weight="600">Scoring</text>
        <text x="325" y="86" text-anchor="middle">4 domains · semantic + anti-noise</text>

        <rect x="460" y="40" width="170" height="60" rx="6" fill="#FFFFFF" stroke="#CDD0CB" stroke-width="1.5"/>
        <text x="545" y="68" text-anchor="middle" fill="#1B1E20" font-size="13" font-weight="600">Enrichment</text>
        <text x="545" y="86" text-anchor="middle">Claude Haiku · EN + FR</text>

        <rect x="680" y="40" width="200" height="60" rx="6" fill="#FFFFFF" stroke="#2F5A5C" stroke-width="1.5"/>
        <text x="780" y="68" text-anchor="middle" fill="#1B1E20" font-size="13" font-weight="600">Output</text>
        <text x="780" y="86" text-anchor="middle">__N__ fiches · dashboard · newsletter</text>

        <line x1="195" y1="70" x2="235" y2="70" stroke="#8A9096" stroke-width="1.5" marker-end="url(#arr)"/>
        <line x1="415" y1="70" x2="455" y2="70" stroke="#8A9096" stroke-width="1.5" marker-end="url(#arr)"/>
        <line x1="635" y1="70" x2="675" y2="70" stroke="#8A9096" stroke-width="1.5" marker-end="url(#arr)"/>
      </g>
    </svg>

    <div class="pipeline-text">
      <div class="step">
        <h5>1 · Collection</h5>
        <p>For each monitored organization, <code>list_all_repos_by_owner</code> with exponential retry on intermediate pages. Gitee token: 4500 req/h.</p>
      </div>
      <div class="step">
        <h5>2 · Scoring</h5>
        <p>Multilingual <b>semantic embeddings</b> vs 4 domain definitions + anti-noise admission (curated keywords anchor, contrastive anti-domains). Hard filters upstream (<code>third_party_*</code>, <code>mirrors/*</code>, stale &gt;2y).</p>
      </div>
      <div class="step">
        <h5>3 · Enrichment</h5>
        <p>For each selected repo: Claude Haiku 4.5 produces Problem solved, How it works, Chinese specificity, Western equivalent. Bootstrap: no call if fiche already on disk.</p>
      </div>
      <div class="step">
        <h5>4 · Incremental diff</h5>
        <p><code>state.json</code> stores <code>pushed_at</code> per repo. Diff <em>NEW / MODIFIED / UNCHANGED / DELETED</em> per run, written to <code>output/diff_YYYYMMDD.md</code>.</p>
      </div>
    </div>

    <div class="tech-stack">
      <div class="item"><strong>Corpus</strong> __N__ fiches × EN + FR</div>
      <div class="item"><strong>Tests</strong> 110 pytest, GitHub Actions CI</div>
      <div class="item"><strong>Bootstrap cost</strong> ~$1 (__N__ bilingual pairs × Haiku 4.5)</div>
      <div class="item"><strong>Incremental run cost</strong> ~$0.10-$0.50</div>
    </div>
  </div>
</section>

</main>

<footer>
  <div class="wrap row">
    <span class="signature">▮ MINERVA · Apache 2.0 · single-file dashboard</span>
    <span>Last pipeline run: <strong style="color:var(--ink)">__LAST_RUN__</strong> · <a href="legal.html" style="color:var(--ink-2)">Legal &amp; privacy</a></span>
  </div>
  <div class="wrap row" style="margin-top:8px">
    <span>Sources: official Gitee &amp; GitHub APIs · public repository metadata only · every fiche links back to its source.</span>
    <span>Enrichment: Claude Haiku 4.5 · fiches may contain "to be confirmed" — verify at the source.</span>
  </div>
</footer>

<script>
const FICHES = __FICHES_JSON__;
const RUNNER_NAMES = __RUNNER_NAMES_JSON__;  // the 4 fiches already rendered as "Runners-up" (to exclude from the main grid)
const FEAT_NAME    = __FEAT_NAME_JSON__;     // the Featured fiche (same)

const $ = (id) => document.getElementById(id);
const DOMAIN_KEY = {
  "Embedded": "Embedded",
  "IoT": "IoT",
  "Robotics": "Robotics",
  "Edge AI": "EdgeAI",
};

function escapeHtml(s) {
  return (s || "").replace(/[&<>"']/g, c => ({
    "&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"
  }[c]));
}
function uniq(arr) {
  return [...new Set(arr.filter(Boolean))].sort((a, b) => a.localeCompare(b, "fr", {sensitivity:"base"}));
}
function fmtInt(n) { return new Intl.NumberFormat("fr-FR").format(n || 0); }
function scoreClass(s) { if (s >= 35) return "high"; if (s >= 22) return "mid"; return ""; }
function statusClass(s) { return s ? "st-" + s.replace(/[^A-Za-zÀ-ÿ]/g, "") : ""; }
function domainTagClass(d) {
  const k = DOMAIN_KEY[d] || "";
  return k ? "dom-" + k : "";
}
// Confidence as ink diamond marks (hue-neutral): High ◆◆◆, Medium ◆◆◇, Low ◆◇◇ — same
// convention as build_site.py's conf_dm(). Text only, no color channel.
function confMarks(conf) {
  const n = {"High": 3, "Medium": 2, "Low": 1}[conf] || 0;
  if (!n) return "";
  const on = "◆".repeat(n), off = "◇".repeat(3 - n);
  return off ? `${on}<span class="off">${off}</span>` : on;
}

function populate(id, values) {
  const sel = $(id);
  for (const v of values) {
    const o = document.createElement("option");
    o.value = v; o.textContent = v;
    sel.appendChild(o);
  }
}
populate("f-owner",  uniq(FICHES.map(f => f.owner)));
populate("f-type",   uniq(FICHES.map(f => f.type)));
populate("f-status", uniq(FICHES.map(f => f.status)));

const state = {
  q: "", owner: "", type: "", status: "", conf: "",
  domains: new Set(),
  sort: "score-desc",
};
const DOMAIN_COLOR = {"Embedded":"var(--d-emb)","IoT":"var(--d-iot)","Robotics":"var(--d-rob)","Edge AI":"var(--d-edge)"};
let filteredItems = [];
let selIdx = 0;

function getFiltered() {
  const q = state.q.toLowerCase().trim();
  return FICHES.filter(f => {
    if (state.owner && f.owner !== state.owner) return false;
    if (state.type && f.type !== state.type) return false;
    if (state.status && f.status !== state.status) return false;
    if (state.conf && f.confidence !== state.conf) return false;
    if (state.domains.size > 0) {
      const fDoms = (f.domaine || "").split(" / ").map(s => s.trim());
      if (!fDoms.some(d => state.domains.has(d))) return false;
    }
    if (q) {
      const blob = (f.full_name + " " + f.probleme + " " + f.comment + " " +
                    f.specificite + " " + f.equivalent + " " + f.type + " " +
                    f.domaine + " " + f.owner).toLowerCase();
      if (!blob.includes(q)) return false;
    }
    return true;
  });
}

function sortItems(items) {
  const arr = [...items];
  switch (state.sort) {
    case "stars-desc": arr.sort((a,b) => (b.stars||0) - (a.stars||0)); break;
    case "date-desc":  arr.sort((a,b) => (b.date||"").localeCompare(a.date||"")); break;
    case "name-asc":   arr.sort((a,b) => a.full_name.localeCompare(b.full_name, "fr")); break;
    default:           arr.sort((a,b) => (b.score||0) - (a.score||0));
  }
  return arr;
}

function isFilterActive() {
  return state.q || state.owner || state.type || state.status || state.domains.size > 0;
}

// Compact left-list row — fast to scan.
function renderRow(f, idx) {
  const el = document.createElement("button");
  el.className = "ex-row" + (idx === selIdx ? " sel" : "");
  el.dataset.idx = idx;
  const color = DOMAIN_COLOR[f.domaine_primary] || "var(--ink-4)";
  const conf = f.confidence
    ? `<span class="rconf" title="${escapeHtml(f.confidence)} confidence">${confMarks(f.confidence)}</span>` : "";
  el.innerHTML = `
    <span class="rscore tnum">${f.score}</span>
    <span class="rdot" style="background:${color}"></span>
    <span class="rname">${escapeHtml(f.full_name)}${f.modified ? '<span class="badge-mod">UPD</span>' : ''}</span>
    ${conf}`;
  el.addEventListener("click", () => select(idx));
  return el;
}

// Light, non-invasive detail panel — the decision layer.
function renderDetail(f) {
  const d = $("ex-detail");
  if (!f) { d.innerHTML = ""; return; }
  const dKey = domainTagClass(f.domaine_primary);
  const stCls = statusClass(f.status);
  const ficheLink = f.web_slug
    ? `<a href="f/${escapeHtml(f.web_slug)}.html">Full fiche →</a>` : "";
  const srcLink = f.gitee_url
    ? `<a href="${escapeHtml(f.gitee_url)}" target="_blank" rel="noopener">View source →</a>` : "";
  d.innerHTML = `
    <div class="d-top">
      <span class="d-score tnum">${f.score}</span>
      <a class="d-name" href="${escapeHtml(f.gitee_url)}" target="_blank" rel="noopener">${escapeHtml(f.full_name)}${f.modified ? '<span class="badge-mod">UPD</span>' : ''}</a>
    </div>
    <div class="d-tags">
      ${f.type ? `<span class="tag type">${escapeHtml(f.type)}</span>` : ""}
      ${f.domaine_primary ? `<span class="tag ${dKey}">${escapeHtml(f.domaine)}</span>` : ""}
      ${f.status ? `<span class="tag ${stCls}">${escapeHtml(f.status)}</span>` : ""}
      ${f.confidence ? `<span class="conf"><span class="dm">${confMarks(f.confidence)}</span> ${escapeHtml(f.confidence)}</span>` : ""}
      ${f.langue ? `<span class="tag">${escapeHtml(f.langue)}</span>` : ""}
    </div>
    <div class="d-meta">
      ${f.stars ? `<span>★ ${fmtInt(f.stars)}</span>` : ""}
      ${f.forks ? `<span>${fmtInt(f.forks)} forks</span>` : ""}
      ${f.date  ? `<span>push ${escapeHtml(f.date)}</span>` : ""}
    </div>
    <div class="d-field"><span class="d-lab">Problem solved</span><p>${escapeHtml(f.probleme)}</p></div>
    <div class="d-field"><span class="d-lab">How it works</span><p>${escapeHtml(f.comment)}</p></div>
    <div class="d-field"><span class="d-lab">Chinese specificity</span><p>${escapeHtml(f.specificite)}</p></div>
    <div class="d-field hl"><span class="d-lab">Western equivalent <em>← the bridge</em></span><p>${escapeHtml(f.equivalent)}</p></div>
    <div class="d-foot">${ficheLink}${srcLink}</div>`;
}

function select(idx) {
  if (!filteredItems.length) return;
  selIdx = Math.max(0, Math.min(idx, filteredItems.length - 1));
  const rows = $("ex-list").children;
  for (let i = 0; i < rows.length; i++) rows[i].classList.toggle("sel", i === selIdx);
  if (rows[selIdx]) rows[selIdx].scrollIntoView({block: "nearest"});
  renderDetail(filteredItems[selIdx]);
}

function applyFilters() {
  filteredItems = sortItems(getFiltered());
  const list = $("ex-list");
  list.innerHTML = "";
  filteredItems.forEach((f, i) => list.appendChild(renderRow(f, i)));
  $("r-shown").textContent = fmtInt(filteredItems.length);

  // Description of the active filters
  const parts = [];
  if (state.domains.size) parts.push([...state.domains].join(" + "));
  if (state.owner) parts.push(state.owner);
  if (state.type) parts.push(state.type);
  if (state.status) parts.push(state.status);
  if (state.conf) parts.push(state.conf + " confidence");
  if (state.q) parts.push(`"${state.q}"`);
  $("r-active").textContent = parts.length ? "filter: " + parts.join(" · ") : "no active filter";

  const has = filteredItems.length > 0;
  $("explorer").style.display = has ? "grid" : "none";
  $("empty").style.display = has ? "none" : "block";
  if (has) { selIdx = 0; select(0); } else renderDetail(null);
}

// === Bindings ===
function clearPresets() { document.querySelectorAll(".preset.active").forEach(p => p.classList.remove("active")); }
function syncUI() {
  $("q").value = state.q; $("f-owner").value = state.owner;
  $("f-type").value = state.type; $("f-status").value = state.status;
  $("sort").value = state.sort;
  document.querySelectorAll(".chip[data-domain]").forEach(c =>
    c.classList.toggle("active", state.domains.has(c.dataset.domain)));
}

$("q").addEventListener("input", e => { state.q = e.target.value; clearPresets(); applyFilters(); });
["f-owner", "f-type", "f-status"].forEach(id => {
  $(id).addEventListener("change", e => {
    state[id.replace("f-", "")] = e.target.value; clearPresets(); applyFilters();
  });
});
$("sort").addEventListener("change", e => { state.sort = e.target.value; applyFilters(); });

document.querySelectorAll(".chip[data-domain]").forEach(chip => {
  chip.addEventListener("click", () => {
    const d = chip.dataset.domain;
    if (state.domains.has(d)) { state.domains.delete(d); chip.classList.remove("active"); }
    else { state.domains.add(d); chip.classList.add("active"); }
    clearPresets(); applyFilters();
  });
});

// Use-case quick views
const PRESETS = {
  "edge-ai":   s => { s.domains = new Set(["Edge AI"]); s.sort = "stars-desc"; },
  "robotics":  s => { s.domains = new Set(["Robotics"]); },
  "embedded":  s => { s.domains = new Set(["Embedded"]); },
  "high-conf": s => { s.conf = "High"; },
};
document.querySelectorAll(".preset[data-preset]").forEach(btn => {
  btn.addEventListener("click", () => {
    const wasActive = btn.classList.contains("active");
    state.q = ""; state.owner = ""; state.type = ""; state.status = ""; state.conf = "";
    state.domains = new Set(); state.sort = "score-desc";
    clearPresets();
    if (!wasActive) { PRESETS[btn.dataset.preset](state); btn.classList.add("active"); }
    syncUI(); applyFilters();
  });
});

$("reset").addEventListener("click", () => {
  state.q = ""; state.owner = ""; state.type = ""; state.status = ""; state.conf = "";
  state.domains.clear();
  state.sort = "score-desc";
  clearPresets(); syncUI();
  applyFilters();
});

document.addEventListener("keydown", e => {
  const typing = ["INPUT","TEXTAREA","SELECT"].includes(document.activeElement.tagName);
  if (e.key === "/" && !typing) {
    e.preventDefault();
    $("q").focus();
  }
  if (e.key === "Escape" && document.activeElement === $("q")) {
    $("q").value = ""; state.q = ""; applyFilters();
    $("q").blur();
  }
  // ↑/↓ move the selection through the list — fast exploration.
  if (!typing && (e.key === "ArrowDown" || e.key === "ArrowUp") && filteredItems.length) {
    e.preventDefault();
    select(selIdx + (e.key === "ArrowDown" ? 1 : -1));
  }
});

applyFilters();
</script>

</body>
</html>
"""


def render_tags(item: dict) -> str:
    parts = []
    dp = item.get("domaine_primary")
    if dp:
        key = {"Embedded": "Embedded", "IoT": "IoT", "Robotics": "Robotics", "Edge AI": "EdgeAI"}.get(dp, "")
        parts.append(f'<span class="tag dom-{key}">{html.escape(dp)}</span>')
    if item.get("type"):
        parts.append(f'<span class="tag type">{html.escape(item["type"])}</span>')
    if item.get("status"):
        cls = "st-" + re.sub(r"[^A-Za-zÀ-ÿ]", "", item["status"])
        parts.append(f'<span class="tag {cls}">{html.escape(item["status"])}</span>')
    if item.get("langue"):
        parts.append(f'<span class="tag">{html.escape(item["langue"])}</span>')
    return "".join(parts)


def render_runner(item: dict, rank: int) -> str:
    tags = render_tags(item)
    meta_bits = []
    if item.get("stars"):
        meta_bits.append(f'★ {fmt_int(item["stars"])}')
    if item.get("date"):
        meta_bits.append(f'push {html.escape(item["date"])}')
    meta = "".join(f"<span>{m}</span>" for m in meta_bits)
    return (
        f'<article class="runner">'
        f'<span class="rk">#{rank}</span>'
        f'<div class="runner-score">★ {item["score"]}/100</div>'
        f'<h4><a href="{html.escape(item.get("gitee_url",""))}" target="_blank" rel="noopener">{html.escape(item["full_name"])}</a></h4>'
        f'<div class="runner-tags">{tags}</div>'
        f'<p>{html.escape(item.get("probleme",""))}</p>'
        f'<div class="runner-meta">{meta}</div>'
        f'</article>'
    )


def main() -> int:
    if not STATE_FILE.is_file():
        print(f"ERROR: {STATE_FILE} not found. Run the pipeline first.", file=sys.stderr)
        return 1

    state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    repos_state = state.get("repos", {})
    last_run = state.get("last_run", "")
    last_run_short = last_run[:10] if last_run else "—"

    items, skipped = build_items(repos_state)
    if not items:
        print("ERROR: no fiche parsed.", file=sys.stderr)
        return 1

    aggs = compute_aggregates(items)

    # Hero-slot curation (D5 audit fix): Featured / Runners-up only front
    # decision-rich fiches — utility repos (docs mirrors, download-data blobs,
    # toolchain binaries, helper tools) stay in the corpus and the explorer but
    # don't carry the proof. Presentation-layer rule; score formula untouched
    # (real rework = V1.1 backlog on the fresh-run corpus).
    utility_re = re.compile(r"(docs?$|download|toolchain|tools$)")

    def vitrine_worthy(it):
        repo_part = it["full_name"].split("/", 1)[-1].lower()
        return bool(it.get("equivalent")) and not utility_re.search(repo_part)

    hero_pool = [it for it in items if vitrine_worthy(it)] or items
    feat = hero_pool[0]
    runners = hero_pool[1:5]

    feat_tags = render_tags(feat)
    # Rank shown = TRUE corpus rank (curation skips utility repos but must not
    # renumber the ranking — that would be cosmetic dishonesty).
    rank_of = {it["full_name"]: i + 1 for i, it in enumerate(items)}
    runners_html = "\n".join(render_runner(it, rank_of[it["full_name"]]) for it in runners)

    domain_bars = render_domain_bars(aggs["domain_counts"])
    owner_bars = render_owner_bars(aggs["top_owners"])

    feat_src_label = "View on GitHub" if "github.com" in (feat.get("gitee_url", "") or "").lower() else "View on Gitee"
    feat_dom_color = DOM_HEX.get(DOM_KEY.get(feat.get("domaine_primary", ""), ""), "var(--ink-4)")

    fiches_json = json.dumps(items, ensure_ascii=False, separators=(",", ":"))
    runner_names_json = json.dumps([r["full_name"] for r in runners], ensure_ascii=False)
    feat_name_json = json.dumps(feat["full_name"], ensure_ascii=False)

    replacements = {
        "__N__": fmt_int(len(items)),
        "__N_ORGS__": fmt_int(aggs["n_orgs"]),
        "__N_WATCHED__": fmt_int(_watched_org_count()),
        "__STARS_FMT__": fmt_stars(aggs["total_stars"]),
        "__AVG_SCORE__": str(aggs["avg_score"]),
        "__LAST_RUN__": html.escape(last_run_short),

        "__FEAT_NAME__": html.escape(feat["full_name"]),
        "__FEAT_URL__": html.escape(feat.get("gitee_url", "")),
        "__FEAT_SCORE__": str(feat["score"]),
        "__FEAT_TAGS__": feat_tags,
        "__FEAT_PROBLEME__": html.escape(feat.get("probleme", "")),
        "__FEAT_COMMENT__": html.escape(feat.get("comment", "")),
        "__FEAT_SPEC__": html.escape(feat.get("specificite", "")),
        "__FEAT_EQUIV__": html.escape(feat.get("equivalent", "")),
        "__FEAT_MAT__": html.escape(feat.get("maturite", "")),
        "__FEAT_SRC_LABEL__": feat_src_label,
        "__FEAT_CONF_DM__": conf_dm(feat.get("confidence", "")),
        "__FEAT_DOMAIN__": html.escape(feat.get("domaine_primary", "")),
        "__FEAT_DOM_COLOR__": feat_dom_color,

        "__DOMAIN_BARS__": domain_bars,
        "__OWNER_BARS__": owner_bars,
        "__RUNNERS__": runners_html,

        "__FICHES_JSON__": fiches_json,
        "__RUNNER_NAMES_JSON__": runner_names_json,
        "__FEAT_NAME_JSON__": feat_name_json,
    }

    out = HTML_TEMPLATE
    # Longest first so a placeholder isn't absorbed by another
    for k in sorted(replacements, key=len, reverse=True):
        out = out.replace(k, replacements[k])

    OUT_FILE.write_text(out, encoding="utf-8")
    size_kb = OUT_FILE.stat().st_size / 1024
    print(f"OK: {OUT_FILE}")
    print(f"  fiches included                          : {len(items)}")
    print(f"  fiches missing (in state but no .md)     : {skipped}")
    print(f"  Featured                                 : {feat['full_name']} (score {feat['score']})")
    print(f"  Runners-up                               : {', '.join(r['full_name'] for r in runners)}")
    print(f"  size                                     : {size_kb:.1f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
