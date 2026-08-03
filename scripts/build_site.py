"""Generates Minerva's multi-page static site from the existing fiches.

Design language: "calm analytical instrument" — light-first (technical paper +
ink), one mineral signal accent, monospace for quantitative/identifier/label text,
confidence as ink marks, flat hairline components, no glow / no fake-live / no
floating shadows. See docs/DESIGN_TRACK.md and docs/design/*.html.

TODO (Jinja2 templating refactor sprint): this file uses its own inline logic
to parse the markdown fiches, separate from src/fiche_schema.py. Migrate to
Fiche.from_markdown when the Jinja2 sprint is opened.

Outputs (all self-contained, openable via file:// or deployable as-is):

  output/
    index.html              ← landing: proof → trust → conversion
    pro.html                ← 3-tier pricing + Pro waitlist
    f/<slug>.html           ← one page per fiche (SEO + social sharing)
    favicon.svg             ← brand mark
    og.svg                  ← social card (rasterize to og.png at deploy — see below)
    sitemap.xml             ← one entry per static page + per fiche (real domain only)
    robots.txt

Set MINERVA_SITE_URL to the final domain (used in canonical + sitemap + OpenGraph);
until then the build degrades to ship no fake absolute URLs. MINERVA_CONTACT sets
the Enterprise contact address.

OG image note: og:image needs a raster PNG. This build ships og.svg (the design);
og:image is only emitted with a real domain, pointing at /og.png — generate that PNG
from og.svg at deploy time (headless Chrome, rsvg-convert, or cairosvg). Documented
in docs/DEPLOYMENT.md.
"""

import html
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from fiche_schema import confidence_tier, _is_recent_month  # noqa: E402 — shared confidence logic

STATE_FILE = ROOT / "output" / "state.json"
FICHES_DIR = ROOT / "output" / "fiches"
FICHES_FR_DIR = ROOT / "output" / "fiches_fr"
OUT_DIR = ROOT / "output"
F_DIR = OUT_DIR / "f"
SOURCES_FILE = ROOT / "config" / "sources.json"


def watched_org_count() -> int:
    """Watched orgs from config (Gitee + GitHub accounts) — distinct from the
    number of orgs that currently HAVE fiches. Conflating the two was an
    audit-flagged truth drift; keep them separate everywhere."""
    try:
        cfg = json.loads(SOURCES_FILE.read_text(encoding="utf-8"))
        return len(cfg.get("comptes_gitee", [])) + len(cfg.get("comptes_github", []))
    except Exception:
        return 0

SITE_URL = os.environ.get("MINERVA_SITE_URL", "https://minerva.example").rstrip("/")
# Newsletter handle (buttondown.email/<handle>). No default: an unset handle is a
# PLACEHOLDER state and the email form degrades to a disabled, honest stub — a
# live-looking form posting to an account we don't own would silently ship
# visitors' emails to a stranger (worse than a fake URL). Set MINERVA_NEWSLETTER
# to the real, owner-controlled handle to activate capture.
NEWSLETTER_HANDLE = os.environ.get("MINERVA_NEWSLETTER", "").strip()
IS_PLACEHOLDER_NEWSLETTER = not NEWSLETTER_HANDLE

# Cadence rule (owner doctrine, 2026-07-31): the copy follows the REAL operator,
# not the intention. By default no cadence is promised anywhere ("after each
# corpus run"). "Weekly" wording appears ONLY when MINERVA_CADENCE=weekly — and
# the only thing that sets that is the weekly CI workflow's own rebuild step.
# The promise is literally produced by its operator; a manual/local build can
# never over-promise.
IS_WEEKLY = os.environ.get("MINERVA_CADENCE", "").strip().lower() == "weekly"
BRIEF_EN = "Every week, the flagship new & updated fiches in your inbox." if IS_WEEKLY \
    else "The flagship new & updated fiches, in your inbox after each corpus run."
BRIEF_SHORT_EN = "Free weekly brief." if IS_WEEKLY else "The free brief."
BRIEF_CTA_EN = "Get the weekly brief" if IS_WEEKLY else "Get the brief"
BRIEF_FICHE_EN = ("Get the flagship new &amp; updated fiches every week. Free, unsubscribe in one click."
                  if IS_WEEKLY else
                  "Get the flagship new &amp; updated fiches after each corpus run. Free, unsubscribe in one click.")
BRIEF_FICHE_FR = ("Recevez chaque semaine les fiches nouvelles et mises à jour. Gratuit, désinscription en un clic."
                  if IS_WEEKLY else
                  "Recevez les fiches nouvelles et mises à jour après chaque run du corpus. Gratuit, désinscription en un clic.")
# Until a real domain is set, MINERVA_SITE_URL is a placeholder. In that mode the
# build degrades gracefully: it ships NO fake absolute URLs (no canonical, no
# og:url, no og:image, no sitemap entries, no robots Sitemap line). Set
# MINERVA_SITE_URL to a real domain to re-enable them. See the note in main().
IS_PLACEHOLDER_URL = "minerva.example" in SITE_URL
CONTACT_EMAIL = os.environ.get("MINERVA_CONTACT", "").strip()


# ============================================================================
# PARSING (data layer — unchanged)
# ============================================================================

FIELD_RE = re.compile(r"^\*\*([^:*]+?)\s*:\*\*\s*(.*)$")
TITLE_RE = re.compile(r"^##\s+(.+?)(\s+\[MODIFIÉ\])?\s*$")
STARS_RE = re.compile(r"★\s*(\d+)")
FORKS_RE = re.compile(r"(\d+)\s*forks")
DATE_RE = re.compile(r"(?:updated|mis à jour) (\d{4}-\d{2})")


def md_slug(full_name: str) -> str:
    """Slug for the existing markdown file name."""
    return re.sub(r"[^A-Za-z0-9_\-]", "_", full_name.replace("/", "_"))


def web_slug(full_name: str) -> str:
    """Short URL slug: owner/repo → owner-repo, lowercase, no exotic characters."""
    s = full_name.lower().replace("/", "-")
    s = re.sub(r"[^a-z0-9\-]+", "-", s)
    return s.strip("-")


def parse_int(s: str) -> int:
    m = re.search(r"(\d+)", s or "")
    return int(m.group(1)) if m else 0


def parse_status(maturity: str) -> str:
    return maturity.split(" (", 1)[0].strip() if maturity else ""


def primary_domain(domaine: str) -> str:
    return domaine.split(" / ", 1)[0].strip() if domaine else ""


def parse_fiche(path: Path):
    text = path.read_text(encoding="utf-8")
    fields, title, modified = {}, None, False
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


def build_items(state_repos, fiches_dir=None):
    """Parse the fiche corpus into presentation items. fiches_dir defaults to the
    EN set; pass FICHES_FR_DIR for the French twin corpus (the field parser is
    already bilingual — EN and FR labels both resolve)."""
    fiches_dir = fiches_dir or FICHES_DIR
    items, skipped = [], 0
    for full_name, pushed_at in state_repos.items():
        path = fiches_dir / f"{md_slug(full_name)}_fiche.md"
        if not path.is_file():
            skipped += 1
            continue
        title, modified, fields = parse_fiche(path)
        if not title:
            skipped += 1
            continue
        maturity = fields.get("Maturity") or fields.get("Maturité", "")
        owner = title.split("/", 1)[0] if "/" in title else ""
        domaine = fields.get("Domain") or fields.get("Domaine", "")
        m_stars = STARS_RE.search(maturity)
        m_forks = FORKS_RE.search(maturity)
        m_date = DATE_RE.search(maturity)
        comment = fields.get("How it works") or fields.get("Comment ça marche", "")
        _prose = " ".join([
            fields.get("Problem solved") or fields.get("Problème résolu", ""), comment,
            fields.get("Chinese specificity") or fields.get("Spécificité chinoise", ""),
            fields.get("Western equivalent") or fields.get("Équivalent occidental", ""),
        ])
        _has_meta = bool(m_stars or m_date)
        _recent = _is_recent_month(m_date.group(1)) if m_date else False
        confidence = confidence_tier(_prose, len(comment), _has_meta, _recent)
        items.append({
            "confidence": confidence,
            "full_name": title,
            "owner": owner,
            "modified": modified,
            "type": fields.get("Type", ""),
            "domaine": domaine,
            "domaine_primary": primary_domain(domaine),
            "score": parse_int(fields.get("Relevance score") or fields.get("Score de pertinence", "")),
            "probleme": fields.get("Problem solved") or fields.get("Problème résolu", ""),
            "comment": fields.get("How it works") or fields.get("Comment ça marche", ""),
            "specificite": fields.get("Chinese specificity") or fields.get("Spécificité chinoise", ""),
            "equivalent": fields.get("Western equivalent") or fields.get("Équivalent occidental", ""),
            "maturite": maturity,
            "status": parse_status(maturity),
            "stars": int(m_stars.group(1)) if m_stars else 0,
            "forks": int(m_forks.group(1)) if m_forks else 0,
            "date": m_date.group(1) if m_date else "",
            "langue": fields.get("Language") or fields.get("Langue", ""),
            "gitee_url": fields.get("Gitee") or fields.get("GitHub", ""),
            "pushed_at": pushed_at,
            "web_slug": web_slug(title),
        })
    items.sort(key=lambda x: x["score"], reverse=True)
    return items, skipped


def fmt_int(n):
    return f"{n:,}".replace(",", " ")


def fmt_stars(n):
    if n >= 10000:
        return f"{n/1000:.0f}k"
    if n >= 1000:
        return f"{n/1000:.1f}k"
    return fmt_int(n)


def trunc(s, n):
    s = (s or "").strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def src_label(it):
    return "View on GitHub" if "github.com" in (it.get("gitee_url") or "").lower() else "View on Gitee"


def conf_dm(conf):
    """Confidence as ink diamond marks (hue-neutral): High ◆◆◆, Medium ◆◆◇, Low ◆◇◇."""
    n = {"High": 3, "Medium": 2, "Low": 1}.get(conf, 2)
    on, off = "◆" * n, "◇" * (3 - n)
    return f'{on}<span class="off">{off}</span>' if off else on


# ============================================================================
# DESIGN SYSTEM — shared tokens + chrome (light-first "calm analytical instrument")
# ============================================================================

BASE_CSS = r"""
:root{
  --paper:#F5F6F4; --surface:#FFFFFF; --surface-2:#FAFBF9;
  --ink:#1B1E20; --ink-2:#565C61; --ink-3:#8A9096; --ink-4:#B9BEC2;
  --line:#E4E6E2; --line-2:#CDD0CB; --grid:rgba(27,30,32,0.028);
  --signal:#2F5A5C; --signal-2:#244748; --signal-soft:#E9EEEC;
  --d-emb:#4C6FA4; --d-edge:#8A6AA0; --d-rob:#5E8C6A; --d-iot:#B4894C;
  --sans:-apple-system,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;
  --mono:ui-monospace,"SF Mono","JetBrains Mono",Menlo,Consolas,monospace;

  /* D5 — bounded instrument register (status-line + readout panels ONLY;
     never a page-wide theme — this is not dark mode). */
  --slab:#1B1E20; --slab-2:#262B2D; --slab-ink:#F5F6F4;
  --slab-line:rgba(245,246,244,0.14); --signal-on-slab:#5B948F;
  /* D5 — flattened radius scale: kills the generic "SaaS card" 5-8px softness. */
  --r-0:0px; --r-sm:2px; --r-pill:100px;
  --tick:var(--ink-4);
}
*{box-sizing:border-box} html,body{margin:0}
body{
  background:var(--paper); color:var(--ink); font-family:var(--sans);
  font-size:15px; line-height:1.6; -webkit-font-smoothing:antialiased;
  font-feature-settings:"tnum","cv02","cv03";
  background-image:linear-gradient(var(--grid) 1px,transparent 1px),
                   linear-gradient(90deg,var(--grid) 1px,transparent 1px);
  background-size:34px 34px;
}
a{color:inherit;text-decoration:none}
.wrap{max-width:1060px;margin:0 auto;padding:0 28px}
.mono{font-family:var(--mono)} .tnum{font-variant-numeric:tabular-nums}

/* NAV */
nav{position:sticky;top:0;z-index:30;background:rgba(245,246,244,0.86);
  backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border-bottom:1px solid var(--line-2)}
nav .row{display:flex;align-items:center;gap:20px;padding:13px 0}
.brand{display:flex;align-items:center;gap:9px;color:var(--ink)}
.mark{width:14px;height:14px;border:2px solid var(--ink);border-radius:var(--r-sm);position:relative;flex:none}
.mark::after{content:"";position:absolute;inset:3px 3px auto auto;width:4px;height:4px;background:var(--signal)}
.brand b{font-family:var(--mono);font-size:14.5px;font-weight:600;letter-spacing:0.02em}
nav .links{margin-left:auto;display:flex;gap:20px;align-items:center}
nav .links a{font-size:13.5px;color:var(--ink-2);font-weight:500}
nav .links a:hover{color:var(--ink)}
nav .links a.active{color:var(--signal)}
nav .links .pro{border:1px solid var(--line-2);border-radius:var(--r-sm);padding:5px 12px;color:var(--ink)}
nav .links .pro:hover{border-color:var(--signal);color:var(--signal)}

/* STATUS LINE — one shared, bounded instrument band under nav, on every page.
   Slab-registered (ink bg) but confined to this strip only — not a page theme. */
.status-line{background:var(--slab);color:var(--slab-ink)}
.status-line .srow{display:flex;align-items:center;gap:0;padding:7px 0;font-family:var(--mono);font-size:11px;letter-spacing:0.02em}
.status-line .seg{display:flex;align-items:center;gap:7px;padding:0 16px;position:relative}
.status-line .seg:first-child{padding-left:0}
.status-line .seg:not(:last-child)::after{content:"";position:absolute;right:0;top:2px;bottom:2px;width:1px;background:var(--slab-line)}
.status-line .dot{width:5px;height:5px;border-radius:var(--r-sm);background:var(--signal-on-slab);flex:none}
.status-line .accent{color:var(--signal-on-slab);font-weight:600}
.status-line .ticks{margin-left:auto;display:flex;gap:4px}
.status-line .ticks i{display:block;width:1px;height:10px;background:var(--slab-line)}

/* SHARED ATOMS */
.seclabel{font-family:var(--mono);font-size:12px;text-transform:uppercase;letter-spacing:0.09em;
  color:var(--ink-3);font-weight:600;margin:0 0 18px}
.seclabel .n{color:var(--signal);margin-right:8px}
.btn{display:inline-flex;align-items:center;gap:7px;font-family:var(--sans);font-size:14px;font-weight:600;
  padding:11px 18px;border-radius:var(--r-sm);border:1px solid transparent;cursor:pointer;
  transition:background .14s,border-color .14s,color .14s}
.btn-primary{background:var(--signal);color:#fff;border-color:var(--signal)}
.btn-primary:hover{background:var(--signal-2);border-color:var(--signal-2)}
.btn-ghost{background:var(--surface);color:var(--ink);border-color:var(--line-2)}
.btn-ghost:hover{border-color:var(--signal);color:var(--signal)}
.btn-link{color:var(--signal);font-weight:600;font-size:14px;border-bottom:1px solid var(--line-2);padding-bottom:2px}
.btn-link:hover{border-color:var(--signal)}
.tag{display:inline-flex;align-items:center;gap:6px;font-family:var(--mono);font-size:11px;font-weight:600;
  letter-spacing:0.02em;padding:3px 8px;border-radius:var(--r-sm);border:1px solid var(--line-2);color:var(--ink-2);background:var(--surface)}
.tag .d{width:7px;height:7px;border-radius:var(--r-sm);display:inline-block}
.tag.emb .d{background:var(--d-emb)} .tag.edge .d{background:var(--d-edge)}
.tag.rob .d{background:var(--d-rob)} .tag.iot .d{background:var(--d-iot)}
.tag.plain{color:var(--ink-2)}
.conf{font-family:var(--mono);font-size:11px;color:var(--ink-2);display:inline-flex;align-items:center;gap:6px}
.conf .dm{letter-spacing:1px;color:var(--ink)} .conf .off{color:var(--ink-4)}
.score{display:flex;align-items:center;gap:9px}
.score .n{font-family:var(--mono);font-size:14px;font-weight:600}
.meter{width:96px;height:4px;background:var(--line);border-radius:var(--r-sm);overflow:hidden}
.meter i{display:block;height:100%;background:var(--signal)}
.badge{display:inline-flex;align-items:center;gap:8px;font-family:var(--mono);font-size:11.5px;color:var(--ink-2);
  background:var(--surface);border:1px solid var(--line-2);border-radius:var(--r-pill);padding:5px 12px;letter-spacing:0.02em}
.badge .d{width:6px;height:6px;border-radius:var(--r-sm);background:var(--signal)}
.form{display:flex;gap:8px;max-width:440px;flex-wrap:wrap}
.form input{flex:1 1 200px;background:var(--surface);border:1px solid var(--line-2);border-radius:var(--r-sm);
  padding:11px 14px;font-family:var(--sans);font-size:14px;color:var(--ink)}
.form input:focus{outline:none;border-color:var(--signal);box-shadow:0 0 0 3px var(--signal-soft)}
.form .btn{flex:0 0 auto}
.fine{font-family:var(--mono);font-size:11.5px;color:var(--ink-3);margin-top:12px}

/* READOUT — score/confidence/domain as a structural instrument panel (D5).
   Shared by the landing proof-fiche and the fiche page. This is the ONE readout
   slab per surface — do not add a second one on the same page (stay calm). */
.readout{background:var(--slab);color:var(--slab-ink);border-radius:var(--r-0);
  padding:18px 22px;display:flex;align-items:center;gap:28px;flex-wrap:wrap;position:relative;overflow:hidden}
.readout::before{content:"";position:absolute;left:0;top:0;bottom:0;width:5px;background:var(--dom-color,var(--ink-4))}
.readout .rblock{display:flex;flex-direction:column;gap:3px}
.readout .rlab{font-family:var(--mono);font-size:9.5px;text-transform:uppercase;letter-spacing:0.09em;color:var(--ink-4)}
.readout .rval{font-family:var(--mono);font-size:26px;font-weight:600;letter-spacing:-0.01em;color:var(--slab-ink);line-height:1}
.readout .rval .unit{font-size:12px;color:var(--ink-4);font-weight:500;margin-left:2px}
.readout .rval.conf{font-size:18px;letter-spacing:2px}
.readout .rval.dom{font-size:15px;letter-spacing:0;color:var(--slab-ink);font-weight:600}
.readout .off{color:#4A5052}
.readout .rmeta{margin-left:auto;font-family:var(--mono);font-size:10.5px;color:var(--ink-4);text-align:right;line-height:1.5}
/* Legend — an instrument without a legend is a decorative number (audit fix). */
.rlegend{font-family:var(--mono);font-size:10.5px;color:var(--ink-3);margin-top:8px;line-height:1.5}
.rlegend b{color:var(--ink-2);font-weight:600}

/* FOOTER */
footer{padding:28px 0 44px;border-top:1px solid var(--line);margin-top:16px}
footer .frow{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;font-family:var(--mono);font-size:12px;color:var(--ink-3)}
footer a{color:var(--ink-2)} footer a:hover{color:var(--signal)}
"""


def nav_html(active: str = "", prefix: str = "") -> str:
    def cls(name):
        return ' class="active"' if active == name else ''
    return f"""<nav><div class="wrap row">
  <a class="brand" href="{prefix}index.html"><span class="mark"></span><b>MINERVA</b></a>
  <span class="links">
    <a href="{prefix}dashboard.html"{cls('dashboard')}>Dashboard</a>
    <a href="{prefix}index.html#newsletter">Newsletter</a>
    <a href="{prefix}pro.html" class="pro">Pro</a>
  </span>
</div></nav>"""


def status_line_html(last_run: str, n_fiches: int, reading: str = "") -> str:
    """One shared, bounded instrument band under nav — present identically on
    every page. This is the ONLY other slab surface besides a page's single
    readout panel (fiche/proof-fiche/featured); it must stay a single calm strip,
    never multiplied."""
    last_run_short = last_run[:10] if last_run else "n/a"
    reading_seg = f'<span class="seg">reading: {html.escape(reading)}</span>' if reading else ""
    return f"""<div class="status-line"><div class="wrap srow">
  <span class="seg"><span class="dot"></span><span class="accent">Snapshot</span>&nbsp;· as of {html.escape(last_run_short)}</span>
  <span class="seg">{n_fiches} fiches</span>
  {reading_seg}
  <span class="ticks"><i></i><i></i><i></i><i></i><i></i></span>
</div></div>"""


def footer_html(prefix: str = "") -> str:
    return f"""<footer><div class="wrap frow">
  <span>▮ MINERVA · Apache 2.0 · open source</span>
  <span><a href="{prefix}index.html">Home</a> · <a href="{prefix}dashboard.html">Dashboard</a> · <a href="{prefix}pro.html">Pro</a> · <a href="{prefix}legal.html">Legal &amp; privacy</a></span>
</div></footer>"""


def newsletter_form(button_text: str = "Subscribe", note: bool = True, prefix: str = "") -> str:
    tail = (f'<p class="fine">No spam. Unsubscribe in one click. · <a href="{prefix}legal.html">Privacy</a></p>'
            if note else "")
    if IS_PLACEHOLDER_NEWSLETTER:
        # Placeholder mode: no live form. A disabled, clearly-labeled stub — never
        # a working form posting to an account we don't control.
        return f"""<form class="form" onsubmit="return false">
  <input type="email" placeholder="you@email.com" disabled>
  <button class="btn btn-primary" type="button" disabled style="opacity:.55;cursor:not-allowed">{html.escape(button_text)}</button>
</form><p class="fine">Email sign-up opens at launch.</p>"""
    return f"""<form class="form" action="https://buttondown.email/api/emails/embed-subscribe/{NEWSLETTER_HANDLE}" method="post" target="popupwindow">
  <input type="email" name="email" placeholder="you@email.com" required>
  <input type="hidden" value="1" name="embed">
  <button class="btn btn-primary" type="submit">{html.escape(button_text)}</button>
</form>{tail}"""


def page_shell(title: str, description: str, canonical_path: str, body: str,
               page_css: str = "", active_nav: str = "", og_type: str = "website",
               last_run: str = "", n_fiches: int = 0, reading: str = "",
               alternate=None, lang: str = "en") -> str:
    """Common HTML shell. canonical_path starts with /. page_css is this page's
    scoped stylesheet (plain string, injected after the shared BASE_CSS)."""
    prefix = "../" if canonical_path.startswith("/f/") else ""
    canonical = f"{SITE_URL}{canonical_path}"
    canonical_tag = "" if IS_PLACEHOLDER_URL else f'<link rel="canonical" href="{html.escape(canonical)}">'
    ogurl_tag = "" if IS_PLACEHOLDER_URL else f'<meta property="og:url" content="{html.escape(canonical)}">'
    ogimg_tag = "" if IS_PLACEHOLDER_URL else f'<meta property="og:image" content="{html.escape(SITE_URL)}/og.png">'
    alt_tag = ""
    if alternate and not IS_PLACEHOLDER_URL:
        alt_lang, alt_path = alternate
        alt_tag = (f'<link rel="alternate" hreflang="{alt_lang}" href="{html.escape(SITE_URL + alt_path)}">'
                   f'<link rel="alternate" hreflang="{lang}" href="{html.escape(canonical)}">')
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="icon" type="image/svg+xml" href="{prefix}favicon.svg">
{canonical_tag}{alt_tag}
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
{ogurl_tag}
{ogimg_tag}
<meta property="og:site_name" content="Minerva">
<meta property="og:locale" content="{'fr_FR' if lang == 'fr' else 'en_US'}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(description)}">
<style>{BASE_CSS}{page_css}</style>
</head>
<body>
{nav_html(active_nav, prefix)}
{status_line_html(last_run, n_fiches, reading)}
{body}
{footer_html(prefix)}
</body>
</html>
"""


# ============================================================================
# AGGREGATES (data layer — unchanged)
# ============================================================================

def compute_aggregates(items):
    DOMS = ["Embedded", "IoT", "Robotics", "Edge AI"]
    domain_counts = {d: 0 for d in DOMS}
    for it in items:
        for d in (it.get("domaine") or "").split(" / "):
            d = d.strip()
            if d in domain_counts:
                domain_counts[d] += 1
    owner_counts = Counter(it["owner"] for it in items if it["owner"])
    return {
        "domain_counts": domain_counts,
        "n_orgs": len(owner_counts),
        "total_stars": sum(it["stars"] or 0 for it in items),
        "avg_score": round(sum(it["score"] for it in items) / max(1, len(items))),
        "top_owners": owner_counts.most_common(8),
    }


DOM_KEY = {"Embedded": "emb", "IoT": "iot", "Robotics": "rob", "Edge AI": "edge",
           # FR fiche corpus uses localized domain names — same color keys.
           "Embarqué": "emb", "Robotique": "rob"}
DOM_HEX = {"emb": "var(--d-emb)", "edge": "var(--d-edge)", "rob": "var(--d-rob)", "iot": "var(--d-iot)"}

# Localized strings for the fiche page (EN default, FR twin pages). Chrome
# (nav / status-line / footer) intentionally stays EN in V1 — the decision
# surface (headings, labels, legend) is what must read natively.
FICHE_L = {
    "en": {
        "problem": "Problem solved", "how": "How it works",
        "spec": "Chinese specificity", "equiv": "Western equivalent",
        "hint": "← the bridge a directory never gives you",
        "score": "Score", "conf": "Confidence", "dom": "Domain",
        "legend": "<b>score</b> = a coarse triage signal, 0–100 (semantic similarity to the embedded/IoT/robotics/edge-AI wedge + activity bonuses) — a sort key, not a measurement of the ecosystem · <b>◆ marks</b> = confidence tier (data-quality: enrichment depth, metadata, recency) — method in docs/SCORING.md",
        "type": "Type", "lang": "Language", "stars": "Stars", "forks": "Forks",
        "push": "Last push", "view_gh": "View on GitHub", "view_ge": "View on Gitee",
        "related": "Other fiches in {dom}", "read": "fiche",
        "nl_h": "Enjoyed this fiche?",
        "nl_p": BRIEF_FICHE_EN,
        "nl_btn": "Subscribe", "other_lang": "FR →", "title_tag": "",
    },
    "fr": {
        "problem": "Problème résolu", "how": "Comment ça marche",
        "spec": "Spécificité chinoise", "equiv": "Équivalent occidental",
        "hint": "← le pont qu'un annuaire ne vous donnera jamais",
        "score": "Score", "conf": "Confiance", "dom": "Domaine",
        "legend": "<b>score</b> = un signal de tri grossier, 0–100 (similarité sémantique au créneau embarqué/IoT/robotique/edge-AI + bonus d'activité) — une clé de tri, pas une mesure de l'écosystème · <b>marques ◆</b> = niveau de confiance (qualité des données : profondeur d'enrichissement, métadonnées, récence) — méthode dans docs/SCORING.md",
        "type": "Type", "lang": "Langage", "stars": "Étoiles", "forks": "Forks",
        "push": "Dernier push", "view_gh": "Voir sur GitHub", "view_ge": "Voir sur Gitee",
        "related": "Autres fiches en {dom}", "read": "fiche · FR",
        "nl_h": "Cette fiche vous a été utile ?",
        "nl_p": BRIEF_FICHE_FR,
        "nl_btn": "S'abonner", "other_lang": "EN →", "title_tag": " (FR)",
    },
}


def render_tag(it):
    parts = []
    dp = it.get("domaine_primary")
    if dp:
        parts.append(f'<span class="tag {DOM_KEY.get(dp, "")}"><span class="d"></span>{html.escape(dp)}</span>')
    if it.get("type"):
        parts.append(f'<span class="tag plain">{html.escape(it["type"])}</span>')
    if it.get("status"):
        parts.append(f'<span class="tag plain">{html.escape(it["status"])}</span>')
    return "".join(parts)


# ============================================================================
# PAGE: LANDING
# ============================================================================

_UTILITY_RE = re.compile(r"(docs?$|download|toolchain|tools$)")


def is_vitrine_worthy(it) -> bool:
    """Hero-slot curation (Featured / Runners-up / proof fiche): only
    decision-rich fiches carry the vitrine. Utility repos (docs mirrors,
    download-data blobs, toolchain binaries, helper tools) stay IN the corpus
    and the explorer — they just don't front the proof. Presentation-layer
    rule only: the score formula is untouched (real rework = V1.1 backlog,
    calibrated on the fresh-run corpus)."""
    repo_part = (it["full_name"].split("/", 1)[-1] if it.get("full_name") else "").lower()
    return bool(it.get("equivalent")) and not _UTILITY_RE.search(repo_part)


def _pick_proof_fiche(items):
    """Selects a real, recognizable, decision-rich fiche to stage on the landing."""
    priority = ["sophgo/tpu-mlir", "Tencent/ncnn", "kendryte/nncase",
                "unitreerobotics/xr_teleoperate", "alibaba/MNN"]
    by_name = {it["full_name"]: it for it in items}
    for s in priority:
        if s in by_name and is_vitrine_worthy(by_name[s]):
            return by_name[s]
    worthy = [it for it in items if is_vitrine_worthy(it)]
    return max(worthy or items, key=lambda it: it["score"])


def _render_proof_fiche(it) -> str:
    dp = it.get("domaine_primary", "")
    dom_color = DOM_HEX.get(DOM_KEY.get(dp, ""), "var(--ink-4)")
    return f"""<article class="fiche">
  <div class="readout" style="--dom-color:{dom_color}">
    <div class="rblock"><span class="rlab">Score</span><span class="rval tnum">{it['score']}<span class="unit">/100</span></span></div>
    <div class="rblock"><span class="rlab">Confidence</span><span class="rval conf">{conf_dm(it.get('confidence',''))}</span></div>
    <div class="rblock"><span class="rlab">Domain</span><span class="rval dom">{html.escape(dp)}</span></div>
    <div class="rmeta">{html.escape(it['maturite'])}</div>
  </div>
  <div class="fnamerow">
    <a class="fname" href="f/{it['web_slug']}.html">{html.escape(it['full_name'])}</a>
    <span class="tag {DOM_KEY.get(dp, '')}"><span class="d"></span>{html.escape(dp)}</span>
  </div>
  <div class="field"><div class="k">Problem solved</div><div class="v">{html.escape(trunc(it['probleme'], 230))}</div></div>
  <div class="field"><div class="k">How it works</div><div class="v">{html.escape(trunc(it['comment'], 280))}</div></div>
  <div class="field"><div class="k">Chinese specificity</div><div class="v">{html.escape(trunc(it['specificite'], 220))}</div></div>
  <div class="field key"><div class="k">Western equivalent <span class="hint">← the bridge a directory never gives you</span></div><div class="v">{html.escape(it['equivalent'])}</div></div>
  <div class="prov"><span>Maturity: {html.escape(it['maturite'])}</span><a href="{html.escape(it['gitee_url'])}" target="_blank" rel="noopener">{src_label(it)} →</a></div>
</article>"""


USE_CASES = [
    ("Tech scouting", "Find the Chinese counterpart to a Western framework", "Edge AI",
     '“Is there a Chinese ncnn/TVM?” — the <b>Western-equivalent</b> field maps each project to what you already know.'),
    ("Competitive intelligence", "Watch a competitor's open-source footprint", "Robotics",
     "Track what a vendor (Sophgo, Unitree, Bouffalo…) ships and how mature it is — before it lands in a product."),
    ("Sourcing / BOM", "De-risk a chipset SDK before you design it in", "Embedded",
     "Read the maturity, activity and real scope of a vendor's RTOS/BSP/SDK, not a marketing page."),
    ("Edge-AI benchmarking", "Line up inference runtimes on Chinese silicon", "Edge AI",
     "ncnn vs MNN vs tpu-mlir vs nncase — targets, quantization and Western equivalents side by side."),
]


LANDING_CSS = r"""
.hero{padding:56px 0 56px}
.hero h1{font-family:var(--sans);font-size:clamp(34px,5vw,52px);letter-spacing:-0.03em;line-height:1.05;margin:20px 0 20px;font-weight:700;max-width:16ch}
.hero .lede{font-size:clamp(16px,1.7vw,19px);color:var(--ink-2);max-width:640px;margin:0 0 30px}
.hero .lede b{color:var(--ink);font-weight:600}
.cta{display:flex;gap:14px;align-items:center;flex-wrap:wrap}
.trust{margin-top:30px;display:flex;gap:24px;flex-wrap:wrap;font-family:var(--mono);font-size:12.5px;color:var(--ink-3)}
.trust b{color:var(--ink);font-weight:600}
section{border-bottom:1px solid var(--line)}
.sec{padding:52px 0}
h2{font-family:var(--sans);font-size:26px;letter-spacing:-0.02em;margin:0 0 8px;font-weight:680}
.lead{font-size:15px;color:var(--ink-2);max-width:620px;margin:0}
.fiche{background:var(--surface);border:1px solid var(--ink-4);border-radius:var(--r-0);max-width:720px;overflow:hidden;margin-top:24px}
.fiche .fnamerow{display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding:15px 20px;border-bottom:1px solid var(--line);background:var(--surface-2)}
.fiche .fname{font-family:var(--mono);font-weight:600;font-size:15px;color:var(--ink)}
.fiche .fname:hover{color:var(--signal)}
.field{padding:14px 20px;border-bottom:1px solid var(--line)}
.field .k{font-family:var(--mono);font-size:11px;text-transform:uppercase;letter-spacing:0.08em;color:var(--ink-3);margin-bottom:5px;display:flex;gap:8px;flex-wrap:wrap;align-items:baseline}
.field .v{font-size:14.5px;line-height:1.55}
.field.key{background:var(--signal-soft)} .field.key .k{color:var(--signal-2)} .field.key .v{font-weight:560}
.field .k .hint{font-family:var(--sans);text-transform:none;letter-spacing:0;color:var(--signal);font-weight:600;font-size:11px}
.prov{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;padding:12px 20px;font-family:var(--mono);font-size:11.5px;color:var(--ink-3);background:var(--surface-2)}
.prov a{color:var(--signal)}
.uc-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:24px}
.uc{display:block;background:var(--surface);border:1px solid var(--line);border-radius:var(--r-0);padding:18px 20px;transition:border-color .14s}
.uc:hover{border-color:var(--ink-4)}
.uc .h{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:8px}
.uc .h b{font-size:15.5px}
.uc .job{font-size:14px;font-weight:560;margin:0 0 6px} .uc .ex{font-size:13px;color:var(--ink-2);margin:0;line-height:1.5} .uc .ex b{color:var(--ink)}
.how{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:24px}
.step{background:var(--surface);border:1px solid var(--line);border-radius:var(--r-0);padding:18px}
.step .num{font-family:var(--mono);font-size:11px;color:var(--signal);font-weight:700;letter-spacing:0.08em}
.step h4{margin:8px 0 6px;font-size:14.5px;font-weight:620} .step p{margin:0;font-size:12.5px;color:var(--ink-2);line-height:1.5}
.step code{font-family:var(--mono);font-size:11.5px;background:var(--surface-2);border:1px solid var(--line);border-radius:var(--r-sm);padding:0 5px;color:var(--ink)}
.dom{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:24px}
.cell{background:var(--surface);border:1px solid var(--line);border-radius:var(--r-0);padding:16px 18px}
.cell .top{display:flex;align-items:center;gap:8px;margin-bottom:8px}
.cell .dot{width:8px;height:8px;border-radius:var(--r-sm)} .cell .top b{font-size:14.5px} .cell .top .c{margin-left:auto;font-family:var(--mono);font-weight:600;color:var(--ink)}
.cell .bar{height:3px;background:var(--line);border-radius:var(--r-sm);overflow:hidden;margin-bottom:8px} .cell .bar i{display:block;height:100%}
.cell p{margin:0;font-size:12px;color:var(--ink-2);line-height:1.45}
.trustband ul{list-style:none;padding:0;margin:20px 0 0;display:grid;grid-template-columns:1fr 1fr;gap:10px 28px}
.trustband li{font-size:13.5px;color:var(--ink-2);padding-left:22px;position:relative}
.trustband li::before{content:"✓";position:absolute;left:0;color:var(--signal);font-weight:700}
.capture{padding:64px 0;text-align:center}
.capture h2{margin-bottom:10px} .capture .lead{margin:0 auto 24px}
.capture .form{margin:0 auto;justify-content:center} .capture .fine{text-align:center}
@media(max-width:780px){.uc-grid,.how,.dom,.trustband ul{grid-template-columns:1fr 1fr}}
@media(max-width:520px){.how,.dom{grid-template-columns:1fr 1fr}.uc-grid{grid-template-columns:1fr}}
"""


def build_landing(items, aggs, last_run: str = "") -> str:
    n = len(items)
    dc = aggs["domain_counts"]
    GEN = {"alibaba", "bytedance", "baidu", "tencent", "jd-opensource", "paddlepaddle"}
    vendor_share = round(100 * sum(1 for it in items if it["owner"].lower() not in GEN) / max(1, n))
    proof_html = _render_proof_fiche(_pick_proof_fiche(items))
    usecase_html = "\n".join(
        f"""<a class="uc" href="dashboard.html"><div class="h"><b>{title}</b><span class="tag {DOM_KEY.get(dom, '')}"><span class="d"></span>{dom}</span></div>
  <p class="job">{job}</p><p class="ex">{ex}</p></a>""" for title, job, dom, ex in USE_CASES)

    DOM_DESCS = [
        ("Embedded", "var(--d-emb)", "RTOS, BSP, drivers, bare-metal firmware."),
        ("Edge AI", "var(--d-edge)", "NPU/TPU inference, quantization, OCR, vision."),
        ("Robotics", "var(--d-rob)", "ROS, SLAM, teleop, motor control, quadrupeds."),
        ("IoT", "var(--d-iot)", "MQTT/CoAP stacks, cellular modules, device OSes."),
    ]
    max_dc = max(dc.values()) or 1
    domain_blocks = ""
    for label, color, desc in DOM_DESCS:
        c = dc.get(label, 0)
        pct = round(100 * c / max_dc)
        domain_blocks += f"""<div class="cell"><div class="top"><span class="dot" style="background:{color}"></span><b>{label}</b><span class="c tnum">{c}</span></div>
  <div class="bar"><i style="width:{pct}%;background:{color}"></i></div><p>{desc}</p></div>"""

    body = f"""
<header class="hero wrap">
  <h1>Decision-ready intelligence on China's open-source hardware.</h1>
  <p class="lede">The Chinese embedded / IoT / robotics / edge-AI ecosystem ships fast — in
  Mandarin, split across Gitee and GitHub. Minerva turns it into <b>structured EN/FR fiches
  you can act on</b>: what a project does, how mature it is, and its <b>Western equivalent</b>.
  Intelligence, not a repo directory.</p>
  <div class="cta">
    <a class="btn btn-primary" href="dashboard.html">Explore the dashboard →</a>
    <a class="btn-link" href="#newsletter">{BRIEF_CTA_EN}</a>
  </div>
  <div class="trust">
    <span><b>{n}</b> fiches</span>
    <span><b>{aggs['n_orgs']}</b> orgs · Gitee + GitHub</span>
    <span><b>{vendor_share}%</b> hardware vendors</span>
    <span><b>EN + FR</b></span>
    <span>Apache 2.0</span>
  </div>
</header>

<section><div class="wrap sec">
  <p class="seclabel"><span class="n">01</span>What one fiche looks like</p>
  <h2>Not a link and a star count — the decision layer.</h2>
  <p class="lead">Generated from the description and README, mapped to what you already know.
  This is the anti-directory proof.</p>
  {proof_html}
</div></section>

<section><div class="wrap sec">
  <p class="seclabel"><span class="n">02</span>What you'd use it for</p>
  <h2>Four jobs, each wired to a real view.</h2>
  <div class="uc-grid">
    {usecase_html}
  </div>
</div></section>

<section><div class="wrap sec">
  <p class="seclabel"><span class="n">03</span>How it works</p>
  <h2>A monitoring engine, not a one-shot scrape.</h2>
  <div class="how">
    <div class="step"><div class="num">01 · COLLECT</div><h4>Collect</h4><p>Official <b>Gitee</b> &amp; <b>GitHub</b> APIs across {watched_org_count() or "the"} watched orgs; {aggs['n_orgs']} currently yield fiches. Public metadata &amp; READMEs only.</p></div>
    <div class="step"><div class="num">02 · SCORE</div><h4>Score</h4><p>Multilingual <b>semantic embeddings</b> vs 4 domains, plus an anti-noise filter that keeps vendors and drops generic big-tech repos.</p></div>
    <div class="step"><div class="num">03 · ENRICH</div><h4>Enrich</h4><p><code>Claude Haiku 4.5</code> writes problem, how-it-works, Chinese specificity and <b>Western equivalent</b> — in EN &amp; FR.</p></div>
    <div class="step"><div class="num">04 · TRACK</div><h4>Track</h4><p>Incremental <b>NEW / MODIFIED / REMOVED</b> diff via persisted state — dated to each run, not a one-shot scrape.</p></div>
  </div>
</div></section>

<section><div class="wrap sec">
  <p class="seclabel"><span class="n">04</span>The corpus, honestly</p>
  <h2>{n} fiches, {aggs['n_orgs']} orgs, {vendor_share}% from hardware vendors.</h2>
  <p class="lead">Generic big-tech deliberately filtered down. Quality over quantity.</p>
  <div class="dom">
    {domain_blocks}
  </div>
</div></section>

<section><div class="wrap sec trustband">
  <p class="seclabel"><span class="n">05</span>Sources &amp; method you can trust</p>
  <h2>Auditable by design.</h2>
  <ul>
    <li>Official Gitee &amp; GitHub APIs only — no scraping, within published rate limits</li>
    <li>Public repository metadata &amp; READMEs only — no private or personal data</li>
    <li>No code redistributed — original summaries + a link back to every source</li>
    <li>Transparent relevance &amp; confidence scoring — every fiche is auditable</li>
  </ul>
</div></section>

<section><div class="wrap capture" id="newsletter">
  <h2>{BRIEF_SHORT_EN}</h2>
  <p class="lead">{BRIEF_EN} No tracking, unsubscribe in one click.</p>
  {newsletter_form()}
  <p class="fine">Need always-fresh data, history or a custom competitor watch? <a href="pro.html" style="color:var(--signal)">See Pro &amp; Enterprise →</a></p>
</div></section>
"""
    return page_shell(
        title="Minerva — Decision-ready intelligence on China's open-source hardware",
        description=f"{n} decision-ready EN/FR fiches on Chinese embedded, IoT, robotics and "
                    f"edge-AI open source (Gitee + GitHub) — with Western-equivalent mapping, "
                    f"maturity and confidence. Tech scouting, competitive intelligence, sourcing.",
        canonical_path="/",
        body=body,
        page_css=LANDING_CSS,
        active_nav="",
        last_run=last_run,
        n_fiches=n,
    )


# ============================================================================
# PAGE: PRO (PRICING)
# ============================================================================

PRO_CSS = r"""
.phero{padding:56px 0 30px;text-align:center}
.phero h1{font-family:var(--sans);font-size:clamp(30px,4vw,42px);letter-spacing:-0.03em;line-height:1.05;margin:16px 0 12px;font-weight:700}
.phero p{font-size:17px;color:var(--ink-2);max-width:560px;margin:0 auto}
.tiers{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;padding:24px 0 44px}
.tier{background:var(--surface);border:1px solid var(--line);border-radius:var(--r-0);padding:26px 24px;display:flex;flex-direction:column;position:relative}
.tier.feat{border-color:var(--signal);box-shadow:inset 0 2px 0 var(--signal)}
.tier .pop{position:absolute;top:-10px;left:24px;font-family:var(--mono);font-size:10px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:#fff;background:var(--signal);border-radius:var(--r-sm);padding:2px 8px}
.tier h3{margin:0 0 4px;font-size:17px} .tier .ttag{font-size:12.5px;color:var(--ink-3);margin-bottom:16px}
.tier .price{font-family:var(--mono);font-size:40px;font-weight:600;letter-spacing:-0.02em;line-height:1;color:var(--ink)}
.tier .price .per{font-size:13px;color:var(--ink-3);font-weight:500;margin-left:3px} .tier .price.muted{color:var(--ink-2)}
.tier ul{list-style:none;padding:0;margin:20px 0;flex:1}
.tier li{position:relative;padding:6px 0 6px 22px;font-size:13.5px;color:var(--ink-2);line-height:1.5}
.tier li::before{content:"✓";position:absolute;left:0;color:var(--signal);font-weight:700}
.tier li.off{color:var(--ink-4)} .tier li.off::before{content:"✕";color:var(--ink-4)}
.tier .btn{justify-content:center;text-align:center}
section{border-top:1px solid var(--line)} .sec{padding:48px 0}
.road{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.ri{background:var(--surface);border:1px solid var(--line);border-radius:var(--r-0);padding:16px 18px}
.ri .when{font-family:var(--mono);font-size:10.5px;font-weight:700;letter-spacing:0.07em;text-transform:uppercase;color:var(--signal);margin-bottom:6px}
.ri h4{margin:0 0 5px;font-size:14px;font-weight:620} .ri p{margin:0;font-size:12.5px;color:var(--ink-2);line-height:1.5}
.waitlist{margin:40px 0;padding:34px;background:var(--surface);border:1px solid var(--line-2);border-radius:var(--r-0);text-align:center}
.waitlist h3{margin:0 0 10px;font-size:22px} .waitlist p{color:var(--ink-2);max-width:480px;margin:0 auto 20px}
.waitlist .form{margin:0 auto;justify-content:center} .waitlist .fine{text-align:center}
.perk{display:inline-block;margin-top:12px;font-family:var(--mono);font-size:11px;color:var(--signal-2);background:var(--signal-soft);border:1px solid var(--line-2);border-radius:var(--r-pill);padding:4px 11px}
.faq details{border-bottom:1px solid var(--line);padding:16px 0}
.faq summary{cursor:pointer;list-style:none;font-size:15.5px;font-weight:600;display:flex;justify-content:space-between;align-items:center}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";color:var(--ink-3);font-size:20px;font-weight:400}
.faq details[open] summary::after{content:"–"}
.faq p{margin:12px 0 0;font-size:14px;color:var(--ink-2);line-height:1.6}
@media(max-width:820px){.tiers{grid-template-columns:1fr}.tier.feat{order:-1}.road{grid-template-columns:1fr 1fr}}
"""


def build_pro(items, aggs, last_run: str = "") -> str:
    n = len(items)
    contact_href = f"mailto:{html.escape(CONTACT_EMAIL)}" if CONTACT_EMAIL else "index.html#newsletter"
    body = f"""
<header class="phero wrap">
  <span class="badge"><span class="d"></span>Waitlist open — launch when it's ready, not before</span>
  <h1>Minerva Pro</h1>
  <p>For R&amp;D teams and consultants who need to go faster and further than the free newsletter.</p>
</header>

<section style="border-top:none"><div class="wrap">
  <div class="tiers">
    <div class="tier">
      <h3>Free</h3><p class="ttag">To discover the corpus. Live today.</p>
      <div class="price muted">€0</div>
      <ul>
        <li>Public read-only dashboard</li>
        <li>{n} browsable fiches (EN + FR)</li>
        <li>{'Weekly email brief (3 flagship fiches)' if IS_WEEKLY else 'Email brief after each corpus run (3 flagship fiches)'}</li>
        <li>Shareable fiche pages</li>
        <li class="off">Keyword alerts</li>
        <li class="off">CSV / JSON exports</li>
        <li class="off">API access</li>
      </ul>
      <a class="btn btn-ghost" href="index.html#newsletter">Subscribe for free</a>
    </div>
    <div class="tier feat">
      <span class="pop">Most popular</span>
      <h3>Pro</h3><p class="ttag">For individual engineers &amp; consultants. <b>Planned scope — not built yet; may change before launch.</b></p>
      <div class="price">€19<span class="per">/month</span></div>
      <ul>
        <li>Everything in Free</li>
        <li>Per-run brief with the full NEW + MODIFIED diff</li>
        <li>Email / Slack alerts by keyword or account</li>
        <li>Personal watchlist</li>
        <li>CSV / JSON / Markdown exports</li>
        <li>Read API</li>
        <li>Full diff archives</li>
      </ul>
      <a class="btn btn-primary" href="#waitlist">Join the waitlist</a>
    </div>
    <div class="tier">
      <h3>Enterprise</h3><p class="ttag">Intelligence teams, structured R&amp;D. <b>Planned scope — shaped with first customers.</b></p>
      <div class="price muted">Custom</div>
      <ul>
        <li>Everything in Pro</li>
        <li>Unlimited watchlists + teams</li>
        <li>Slack / Teams / Webhook integrations</li>
        <li>Quarterly analysis report (PDF)</li>
        <li>Bespoke monitored domain</li>
        <li>Dedicated support</li>
        <li>Optional on-premise hosting</li>
      </ul>
      <a class="btn btn-ghost" href="{contact_href}">Contact us</a>
    </div>
  </div>
</div></section>

<section><div class="wrap sec">
  <p class="seclabel"><span class="n">01</span>Public roadmap</p>
  <div class="road">
    <div class="ri"><div class="when">Now</div><h4>Newsletter + dashboard</h4><p>Free, OSS, open to all. {n} published fiches{', weekly refresh' if IS_WEEKLY else ', refreshed per corpus run'}.</p></div>
    <div class="ri"><div class="when">Next</div><h4>Pro launch</h4><p>Alerts, exports, basic API. Launch pricing −30% for the waitlist.</p></div>
    <div class="ri"><div class="when">Later</div><h4>Integrations</h4><p>Slack, Teams, webhooks. Team-shared watchlists.</p></div>
    <div class="ri"><div class="when">Exploring</div><h4>Vertical reports</h4><p>Quarterly PDFs by domain (robotics, edge-AI, RISC-V…).</p></div>
  </div>
</div></section>

<section><div class="wrap" id="waitlist">
  <div class="waitlist">
    <h3>Pro waitlist</h3>
    <p>No launch date promised until it's real. Waitlist signups get <b>−30%</b> for their first six months at launch.</p>
    {newsletter_form(button_text="Join the waitlist", note=False)}
    <span class="perk">−30% launch pricing for the waitlist</span>
  </div>
</div></section>

<section><div class="wrap sec faq">
  <p class="seclabel"><span class="n">02</span>FAQ</p>
  <details><summary>Is it really free?</summary><p>Yes. The email brief and the dashboard are free, no sign-up required. The source is Apache 2.0 on GitHub. Pro is an optional paid layer for alerts, exports and the API — planned, not built yet.</p></details>
  <details><summary>Why such a low price for Pro?</summary><p>€19/month is the price of a lunch — affordable on a personal card without approval. Enterprise is for structured teams with a dedicated tech-intelligence budget.</p></details>
  <details><summary>Gitee only, or GitHub too?</summary><p>Both. Gitee is the priority source; a GitHub connector additionally captures Chinese vendors that publish only on GitHub — Bouffalo, Sophgo, Unitree, Kendryte and Allwinner are already covered.</p></details>
  <details><summary>Data stored? GDPR?</summary><p>Free newsletter: just your email, processed by Buttondown (a US-based newsletter service) solely to send the brief. No third-party analytics, no cookies on this site. Pro (when it exists): email + watchlists. Unsubscribe and deletion in one click. Details on the <a href="legal.html" style="color:var(--signal)">legal &amp; privacy page</a>.</p></details>
</div></section>
"""
    return page_shell(
        title="Minerva Pro — Alerts, exports and API for open source China intelligence",
        description="For R&D teams and consultants: keyword alerts, CSV/JSON exports, API access. "
                    "Waitlist open.",
        canonical_path="/pro.html",
        body=body,
        page_css=PRO_CSS,
        active_nav="pro",
        last_run=last_run,
        n_fiches=len(items),
    )


# ============================================================================
# PAGE: FICHE
# ============================================================================

FICHE_CSS = r"""
.crumb{font-family:var(--mono);font-size:11.5px;color:var(--ink-3);padding:20px 0 0;display:flex;gap:8px;flex-wrap:wrap}
.crumb a{color:var(--ink-2)} .crumb a:hover{color:var(--signal)} .crumb .sep{color:var(--ink-4)}
.fhead{padding:18px 0 24px;border-bottom:1px solid var(--line)}
.fhead h1{font-family:var(--mono);font-size:clamp(24px,4vw,34px);letter-spacing:-0.01em;line-height:1.12;margin:0 0 14px;font-weight:600;word-break:break-word}
.tags{display:flex;gap:6px;flex-wrap:wrap}
.grid{display:grid;grid-template-columns:1fr 264px;gap:44px;padding:28px 0 54px}
.main h2{font-family:var(--mono);font-size:11.5px;text-transform:uppercase;letter-spacing:0.09em;color:var(--ink-3);margin:26px 0 8px;font-weight:650}
.main h2:first-child{margin-top:0} .main h2.key{color:var(--signal-2)}
.main p{font-size:16px;line-height:1.7;margin:0 0 4px;color:var(--ink)} .main p.lede{font-size:17px}
.keyblock{background:var(--signal-soft);border-radius:var(--r-0);padding:14px 16px;margin:6px 0 4px}
.keyblock .hint{font-family:var(--mono);font-size:11px;color:var(--signal);margin-top:8px}
aside{align-self:start;border:1px solid var(--ink-4);border-radius:var(--r-0);background:var(--surface);overflow:hidden}
aside .r{display:flex;justify-content:space-between;gap:12px;padding:11px 16px;border-bottom:1px solid var(--line);font-size:13px}
aside .r dt{font-family:var(--mono);font-size:11px;text-transform:uppercase;letter-spacing:0.06em;color:var(--ink-3)}
aside .r dd{margin:0;font-family:var(--mono);text-align:right;color:var(--ink);font-weight:500}
aside .src{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:13px 16px;background:var(--signal);color:#fff;font-weight:600;font-size:13.5px}
aside .src:hover{background:var(--signal-2)}
.related{padding:36px 0;border-top:1px solid var(--line)}
.related .lbl{font-family:var(--mono);font-size:11.5px;text-transform:uppercase;letter-spacing:0.09em;color:var(--ink-3);margin-bottom:16px;font-weight:650}
.rel-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.rc{display:block;background:var(--surface);border:1px solid var(--line);border-radius:var(--r-0);padding:14px 16px;transition:border-color .14s}
.rc:hover{border-color:var(--ink-4)}
.rc .t{display:flex;align-items:center;gap:8px;margin-bottom:8px} .rc .t .s{font-family:var(--mono);font-size:12px;font-weight:600;color:var(--signal-2)}
.rc h4{font-family:var(--mono);font-size:13px;margin:0 0 8px;word-break:break-word;font-weight:600}
.rc p{margin:0;font-size:12.5px;color:var(--ink-2);line-height:1.5;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.nlbox{margin:32px 0 0;padding:24px;background:var(--surface);border:1px solid var(--line-2);border-radius:var(--r-0);text-align:center}
.nlbox h3{margin:0 0 8px;font-size:18px} .nlbox p{margin:0 auto 16px;color:var(--ink-2);max-width:440px;font-size:14px}
.nlbox .form{margin:0 auto;justify-content:center}
@media(max-width:820px){.grid{grid-template-columns:1fr;gap:24px}.rel-grid{grid-template-columns:1fr}}
"""

def build_fiche(it, related, n_total, rank, last_run: str = "", lang: str = "en") -> str:
    L = FICHE_L[lang]
    ext = ".html" if lang == "en" else ".fr.html"
    other_ext = ".fr.html" if lang == "en" else ".html"
    dp = it.get("domaine_primary", "")
    dom_color = DOM_HEX.get(DOM_KEY.get(dp, ""), "var(--ink-4)")
    repo_short = it['full_name'].split('/', 1)[1] if '/' in it['full_name'] else it['full_name']
    view_label = L["view_gh"] if "github.com" in (it.get("gitee_url") or "").lower() else L["view_ge"]
    related_html = "\n".join(
        f"""<a class="rc" href="{r['web_slug']}{ext}"><div class="t"><span class="s tnum">★ {r['score']}</span><span class="tag {DOM_KEY.get(r.get('domaine_primary',''), '')}"><span class="d"></span>{html.escape(r.get('domaine_primary',''))}</span></div>
  <h4>{html.escape(r['full_name'])}</h4><p>{html.escape(r['probleme'])}</p></a>"""
        for r in related)
    related_block = (f"""<section class="related"><div class="lbl">{html.escape(L['related'].format(dom=dp))}</div>
    <div class="rel-grid">{related_html}</div></section>""" if related else "")

    body = f"""
<div class="wrap">
  <div class="crumb"><a href="../index.html">Home</a><span class="sep">/</span><a href="../dashboard.html">Dashboard</a><span class="sep">/</span><a href="../dashboard.html?owner={html.escape(it['owner'])}">{html.escape(it['owner'])}</a><span class="sep">/</span><span>{html.escape(repo_short)}</span><span style="margin-left:auto"><a href="{it['web_slug']}{other_ext}" style="color:var(--signal);font-weight:600">{L['other_lang']}</a></span></div>

  <div class="readout" style="--dom-color:{dom_color};margin-top:16px">
    <div class="rblock"><span class="rlab">{L['score']}</span><span class="rval tnum">{it['score']}<span class="unit">/100</span></span></div>
    <div class="rblock"><span class="rlab">{L['conf']}</span><span class="rval conf">{conf_dm(it.get('confidence',''))}</span></div>
    <div class="rblock"><span class="rlab">{L['dom']}</span><span class="rval dom">{html.escape(dp)}</span></div>
    <div class="rmeta">{html.escape(it['type'])} · {html.escape(it['status'] or '—')}</div>
  </div>
  <div class="rlegend">{L['legend']}</div>

  <header class="fhead">
    <h1>{html.escape(it['full_name'])}</h1>
    <div class="tags">{render_tag(it)}</div>
  </header>

  <div class="grid">
    <div class="main">
      <h2>{L['problem']}</h2>
      <p class="lede">{html.escape(it['probleme'])}</p>
      <h2>{L['how']}</h2>
      <p>{html.escape(it['comment'])}</p>
      <h2>{L['spec']}</h2>
      <p>{html.escape(it['specificite'])}</p>
      <h2 class="key">{L['equiv']}</h2>
      <div class="keyblock"><p style="margin:0">{html.escape(it['equivalent'])}</p><div class="hint">{L['hint']}</div></div>
    </div>
    <aside>
      <div class="r"><dt>{L['type']}</dt><dd>{html.escape(it['type'])}</dd></div>
      <div class="r"><dt>{L['lang']}</dt><dd>{html.escape(it['langue'] or '—')}</dd></div>
      <div class="r"><dt>{L['stars']}</dt><dd>{fmt_int(it['stars'])} ★</dd></div>
      <div class="r"><dt>{L['forks']}</dt><dd>{fmt_int(it['forks'])}</dd></div>
      <div class="r"><dt>{L['push']}</dt><dd>{html.escape(it['date'] or '—')}</dd></div>
      <a class="src" href="{html.escape(it['gitee_url'])}" target="_blank" rel="noopener">{view_label} →</a>
    </aside>
  </div>

  {related_block}

  <div class="nlbox">
    <h3>{L['nl_h']}</h3>
    <p>{L['nl_p']}</p>
    {newsletter_form(button_text=L['nl_btn'], note=False)}
  </div>
</div>
"""
    return page_shell(
        title=f"{it['full_name']} — Minerva{L['title_tag']}",
        description=trunc(it["probleme"], 200),
        canonical_path=f"/f/{it['web_slug']}{ext}",
        body=body,
        page_css=FICHE_CSS,
        active_nav="dashboard",
        og_type="article",
        last_run=last_run,
        n_fiches=n_total,
        reading=L["read"],
        alternate=(("fr" if lang == "en" else "en"), f"/f/{it['web_slug']}{other_ext}"),
        lang=lang,
    )


# ============================================================================
# BRAND ASSETS (written to output/ so the site is self-contained)
# ============================================================================

FAVICON_SVG = """<svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Minerva">
  <rect x="0" y="0" width="32" height="32" rx="7" fill="#F5F6F4"/>
  <rect x="8" y="8" width="16" height="16" rx="3.5" fill="none" stroke="#1B1E20" stroke-width="3"/>
  <rect x="17.5" y="6.5" width="6" height="6" rx="1.6" fill="#2F5A5C"/>
</svg>
"""

# ============================================================================
# PAGE: LEGAL & PRIVACY
# ============================================================================

LEGAL_CSS = r"""
.lhero{padding:48px 0 8px}
.lhero h1{font-family:var(--sans);font-size:clamp(26px,3.4vw,36px);letter-spacing:-0.03em;line-height:1.05;margin:0 0 10px;font-weight:700}
.lhero p{color:var(--ink-2);max-width:640px;margin:0}
.lsec{padding:26px 0;border-bottom:1px solid var(--line);max-width:720px}
.lsec:last-of-type{border-bottom:none}
.lsec h2{font-family:var(--mono);font-size:11.5px;text-transform:uppercase;letter-spacing:0.09em;color:var(--ink-3);margin:0 0 10px;font-weight:650}
.lsec p{font-size:14.5px;line-height:1.65;color:var(--ink);margin:0 0 10px;max-width:66ch}
.lsec p:last-child{margin-bottom:0}
.lsec a{color:var(--signal);font-weight:600}
.lsec ul{margin:0 0 10px;padding-left:20px}
.lsec li{font-size:14px;color:var(--ink-2);margin:4px 0;line-height:1.6}
"""


def build_legal(items, last_run: str = "") -> str:
    contact_line = (f'Email: <a href="mailto:{html.escape(CONTACT_EMAIL)}">{html.escape(CONTACT_EMAIL)}</a>.'
                    if CONTACT_EMAIL else
                    "Contact: via the project's GitHub issues (link in the footer once the repository is public).")
    body = f"""
<div class="wrap">
  <header class="lhero">
    <h1>Legal &amp; privacy.</h1>
    <p>Minerva is an open-source technology-watch project. This page states, plainly,
    what data this site touches and where its content comes from.</p>
  </header>

  <section class="lsec">
    <h2>01 · What this site collects</h2>
    <p><b>Nothing, by default.</b> This is a static site: no cookies, no third-party
    analytics, no tracking pixels, no fingerprinting. Reading Minerva leaves no trace
    with us.</p>
    <p>The <b>only</b> personal data we ever process is your email address, and only
    if you deliberately subscribe to the brief. It is stored and processed by
    <a href="https://buttondown.com" target="_blank" rel="noopener">Buttondown</a>,
    a US-based newsletter service, solely to send you the brief. We see your address;
    we never share, sell or enrich it. Every email includes a one-click unsubscribe,
    which also deletes your address from the list. For any further deletion request: see contact below.</p>
  </section>

  <section class="lsec">
    <h2>02 · Where the content comes from</h2>
    <p>Fiches are built exclusively from <b>public repository metadata and READMEs</b>,
    fetched via the official Gitee and GitHub APIs, within their published rate limits.
    No private data, no personal data of repository authors, no scraping.</p>
    <p>The analytical prose (problem solved, how it works, Chinese specificity, Western
    equivalent) is <b>generated by a large language model</b> and may contain errors —
    fiches carry a confidence tier and may say "to be confirmed". Always verify at the
    source; every fiche links back to the original repository. No source code is
    redistributed.</p>
  </section>

  <section class="lsec">
    <h2>03 · If your project is featured</h2>
    <p>If you maintain a repository covered by a fiche and want a correction — or want
    the fiche removed — contact us (below). We correct factual errors quickly and
    honor reasonable removal requests from maintainers.</p>
  </section>

  <section class="lsec">
    <h2>04 · Licensing</h2>
    <p>Minerva's <b>source code</b> is Apache-2.0. Repository names, descriptions and
    metadata belong to their respective owners. The generated fiche text is provided
    as-is, for reading and sharing with attribution; it is analysis, not advice.</p>
  </section>

  <section class="lsec">
    <h2>05 · Contact</h2>
    <p>{contact_line}</p>
  </section>
</div>
"""
    return page_shell(
        title="Legal & privacy — Minerva",
        description="What data this site touches (almost none), where the fiche content "
                    "comes from, and how to reach us — corrections and removals honored.",
        canonical_path="/legal.html",
        body=body,
        page_css=LEGAL_CSS,
        active_nav="",
        last_run=last_run,
        n_fiches=len(items),
        reading="legal",
    )


OG_SVG = """<svg viewBox="0 0 1200 630" width="1200" height="630" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="g" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0V40" fill="none" stroke="#1B1E20" stroke-opacity="0.035" stroke-width="1"/>
    </pattern>
  </defs>
  <rect width="1200" height="630" fill="#F5F6F4"/>
  <rect width="1200" height="630" fill="url(#g)"/>
  <g transform="translate(80,84)">
    <rect x="0" y="0" width="46" height="46" rx="9" fill="none" stroke="#1B1E20" stroke-width="5"/>
    <rect x="30" y="-6" width="16" height="16" rx="3.5" fill="#2F5A5C"/>
    <text x="66" y="34" font-family="Segoe UI,Helvetica,Arial,sans-serif" font-size="30" font-weight="700" fill="#1B1E20" letter-spacing="0.5">MINERVA</text>
  </g>
  <text x="80" y="250" font-family="Segoe UI,Helvetica,Arial,sans-serif" font-size="58" font-weight="700" fill="#1B1E20" letter-spacing="-1.5">Decision-ready intelligence</text>
  <text x="80" y="318" font-family="Segoe UI,Helvetica,Arial,sans-serif" font-size="58" font-weight="700" fill="#1B1E20" letter-spacing="-1.5">on China's open-source hardware.</text>
  <line x1="80" y1="372" x2="1120" y2="372" stroke="#CDD0CB" stroke-width="1"/>
  <g font-family="Consolas,ui-monospace,monospace" font-size="24" fill="#565C61">
    <text x="80" y="432"><tspan fill="#1B1E20" font-weight="700">__OG_N__</tspan> fiches</text>
    <text x="300" y="432">Gitee + GitHub</text>
    <text x="580" y="432"><tspan fill="#1B1E20" font-weight="700">EN / FR</tspan></text>
    <text x="760" y="432">Western-equivalent mapping</text>
  </g>
  <g transform="translate(80,478)">
    <rect x="0" y="0" width="1040" height="72" rx="8" fill="#E9EEEC"/>
    <text x="22" y="30" font-family="Consolas,ui-monospace,monospace" font-size="15" fill="#244748" letter-spacing="1">WESTERN EQUIVALENT</text>
    <text x="22" y="56" font-family="Segoe UI,Helvetica,Arial,sans-serif" font-size="20" fill="#1B1E20" font-weight="600">sophgo/tpu-mlir  →  Apache TVM + a vendor toolchain (a la TensorRT / OpenVINO)</text>
  </g>
</svg>
"""


# ============================================================================
# SITEMAP + ROBOTS (data layer — unchanged)
# ============================================================================

def build_sitemap(items, last_run: str) -> str:
    if IS_PLACEHOLDER_URL:
        # No real domain yet → emit a valid but empty sitemap rather than fake
        # absolute URLs. Regenerated with real <loc>s once MINERVA_SITE_URL is set.
        return ("""<?xml version="1.0" encoding="UTF-8"?>\n"""
                "<!-- Placeholder build: URLs omitted until MINERVA_SITE_URL is a real "
                "domain. Re-run build_site.py with the real domain before deploy. -->\n"
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n</urlset>\n')
    lastmod = last_run[:10] if last_run else ""
    urls = []
    static_urls = ["/", "/dashboard.html", "/pro.html", "/legal.html"]
    for u in static_urls:
        urls.append(f"  <url><loc>{SITE_URL}{u}</loc>"
                    + (f"<lastmod>{lastmod}</lastmod>" if lastmod else "")
                    + "<changefreq>weekly</changefreq>"
                    + ("<priority>1.0</priority>" if u == "/" else "<priority>0.8</priority>")
                    + "</url>")
    for it in items:
        for ext in (".html", ".fr.html"):
            urls.append(
                f"  <url><loc>{SITE_URL}/f/{it['web_slug']}{ext}</loc>"
                + (f"<lastmod>{lastmod}</lastmod>" if lastmod else "")
                + "<changefreq>monthly</changefreq><priority>0.6</priority></url>"
            )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>
"""


def build_robots() -> str:
    # Omit the Sitemap: line while the domain is a placeholder (it requires an
    # absolute URL); it is added back automatically once MINERVA_SITE_URL is real.
    sitemap_line = "" if IS_PLACEHOLDER_URL else f"\nSitemap: {SITE_URL}/sitemap.xml\n"
    return f"""User-agent: *
Allow: /
Disallow: /fiches/
Disallow: /fiches_fr/
Disallow: /logs/
{sitemap_line}"""


# ============================================================================
# MAIN
# ============================================================================

def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    if not STATE_FILE.is_file():
        print(f"ERROR: {STATE_FILE} not found", file=sys.stderr)
        return 1

    state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    repos_state = state.get("repos", {})
    last_run = state.get("last_run", "")

    items, skipped = build_items(repos_state)
    if not items:
        print("ERROR: no fiche", file=sys.stderr)
        return 1

    aggs = compute_aggregates(items)

    # 1. Landing
    (OUT_DIR / "index.html").write_text(build_landing(items, aggs, last_run), encoding="utf-8")
    sz_index = (OUT_DIR / "index.html").stat().st_size / 1024
    print(f"OK : index.html              ({sz_index:.1f} KB)")

    # 2. Pro
    (OUT_DIR / "pro.html").write_text(build_pro(items, aggs, last_run), encoding="utf-8")
    sz_pro = (OUT_DIR / "pro.html").stat().st_size / 1024
    print(f"OK : pro.html                ({sz_pro:.1f} KB)")

    # 2b. Legal & privacy
    (OUT_DIR / "legal.html").write_text(build_legal(items, last_run), encoding="utf-8")
    print(f"OK : legal.html              ({(OUT_DIR / 'legal.html').stat().st_size / 1024:.1f} KB)")

    # 3. Fiches — EN pages + FR twin pages (the "EN + FR" promise must be
    # verifiable on the site, not just true in the repo).
    items_fr, skipped_fr = build_items(repos_state, FICHES_FR_DIR)
    fr_by_name = {it["full_name"]: it for it in items_fr}

    F_DIR.mkdir(exist_ok=True)
    by_domain: dict[str, list[dict]] = {}
    for it in items:
        by_domain.setdefault(it["domaine_primary"], []).append(it)
    by_domain_fr: dict[str, list[dict]] = {}
    for it in items_fr:
        by_domain_fr.setdefault(it["domaine_primary"], []).append(it)

    def _related(pool_by_dom, it):
        same = [x for x in pool_by_dom.get(it["domaine_primary"], []) if x["full_name"] != it["full_name"]]
        same.sort(key=lambda x: abs(x["score"] - it["score"]))
        return same[:3]

    n_total = len(items)
    n_fiches = n_fr = 0
    for rank, it in enumerate(items, start=1):
        (F_DIR / f"{it['web_slug']}.html").write_text(
            build_fiche(it, _related(by_domain, it), n_total, rank, last_run), encoding="utf-8")
        n_fiches += 1
        fr = fr_by_name.get(it["full_name"])
        if fr:
            (F_DIR / f"{it['web_slug']}.fr.html").write_text(
                build_fiche(fr, _related(by_domain_fr, fr), n_total, rank, last_run, lang="fr"),
                encoding="utf-8")
            n_fr += 1
    avg_size_kb = sum((F_DIR / f"{it['web_slug']}.html").stat().st_size for it in items) / 1024 / max(1, n_fiches)
    print(f"OK : f/{n_fiches} EN + {n_fr} FR fiches (~{avg_size_kb:.1f} KB each)")
    if n_fr < n_fiches:
        print(f"     WARNING: {n_fiches - n_fr} fiche(s) missing their FR twin page")

    # 3b. Purge orphan fiche pages (old-corpus leftovers). The sitemap and the
    # public site must reflect ONLY the current corpus — never stale pages.
    live_slugs = ({f"{it['web_slug']}.html" for it in items}
                  | {f"{it['web_slug']}.fr.html" for it in items})
    orphans = [p for p in F_DIR.glob("*.html") if p.name not in live_slugs]
    for p in orphans:
        p.unlink()
    if orphans:
        print(f"     purged {len(orphans)} orphan fiche page(s)")

    # 4. Brand assets (self-contained site)
    (OUT_DIR / "favicon.svg").write_text(FAVICON_SVG, encoding="utf-8")
    (OUT_DIR / "og.svg").write_text(OG_SVG.replace("__OG_N__", str(n_total)), encoding="utf-8")
    print("OK : favicon.svg · og.svg")

    # 5. Sitemap
    (OUT_DIR / "sitemap.xml").write_text(build_sitemap(items, last_run), encoding="utf-8")
    n_urls = 0 if IS_PLACEHOLDER_URL else 4 + 2 * len(items)
    print(f"OK : sitemap.xml             ({(OUT_DIR / 'sitemap.xml').stat().st_size} bytes, {n_urls} URLs)")

    # 6. robots.txt
    (OUT_DIR / "robots.txt").write_text(build_robots(), encoding="utf-8")
    print(f"OK : robots.txt              ({(OUT_DIR / 'robots.txt').stat().st_size} bytes)")

    print()
    print("=" * 64)
    print(f"Configured site URL : {SITE_URL}  (override via env MINERVA_SITE_URL)")
    print(f"Newsletter handle   : {NEWSLETTER_HANDLE or '(unset — form disabled)'}  (override via env MINERVA_NEWSLETTER)")
    print(f"Total site size     : ~{(sz_index + sz_pro + avg_size_kb * n_fiches + 5):.0f} KB")
    print("=" * 64)
    if IS_PLACEHOLDER_NEWSLETTER:
        print("⚠️  PUBLICATION BLOCKER: MINERVA_NEWSLETTER is unset. Email forms are")
        print("    rendered DISABLED ('sign-up opens at launch') — a live form posting")
        print("    to an unowned Buttondown account would leak visitors' emails. Create")
        print("    the owner-controlled account, then rebuild with the real handle.")
    if IS_PLACEHOLDER_URL:
        print("⚠️  PUBLICATION BLOCKER: MINERVA_SITE_URL is still the placeholder")
        print("    'https://minerva.example'. The build has DEGRADED GRACEFULLY —")
        print("    no canonical, og:url, og:image, sitemap entries or robots Sitemap")
        print("    line are emitted, so nothing fake ships. Set the real domain:")
        print("      MINERVA_SITE_URL=https://your-domain python scripts/build_site.py")
        if not CONTACT_EMAIL:
            print("    (Optional: set MINERVA_CONTACT=you@domain for the Enterprise CTA.)")
    print("    OG image: og.svg shipped — rasterize to og.png before deploy (see")
    print("    docs/DEPLOYMENT.md); og:image is emitted only with a real domain.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
