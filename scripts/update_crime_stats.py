"""
Refreshes the burglary figures on security-awareness.html from the official
Home Office / ONS "Police recorded crime open data: Police Force Area tables"
(quarterly, notifiable offences only).

Source: https://www.gov.uk/government/statistical-data-sets/police-recorded-crime-and-outcomes-open-data-tables
This is the *only* figure on the page that's safely automatable from a stable
open dataset. Anti-social behaviour incidents are NOT notifiable offences and
are not in this file (the ONS/Home Office series covering them stopped being
published in ~2016) -- ASB numbers on the page remain manually sourced and are
left untouched by this script. It prints a reminder to check them by hand.

Usage:
    python scripts/update_crime_stats.py [--apply]

Without --apply it just prints what it found (dry run). With --apply it
rewrites the burglary numbers + "data as of" line in security-awareness.html.
"""
import argparse
import datetime
import re
import shutil
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "scripts" / ".cache"
CACHE.mkdir(parents=True, exist_ok=True)
ODS_PATH = CACHE / "prc-pfa.ods"
HTML_PATH = ROOT / "security-awareness.html"

SOURCE_LISTING_URL = "https://www.gov.uk/government/statistical-data-sets/police-recorded-crime-and-outcomes-open-data-tables"
BURGLARY_SUBGROUPS = {"Residential burglary", "Non-residential burglary"}

# Each force reports a different stat on the page, matching what it publishes
# most readily -- Northumbria: rolling-12-month total burglaries (residential +
# non-residential). Durham: latest single quarter, non-residential ("business &
# community") burglaries only, matching the wording already on the page.
FORCE_STATS = {
    "Northumbria": {"subgroups": {"Residential burglary", "Non-residential burglary"}, "window": "rolling12"},
    "Durham": {"subgroups": {"Non-residential burglary"}, "window": "latest_quarter"},
}

# Financial quarters, in calendar order: Q4 (Jan-Mar), Q1 (Apr-Jun), Q2 (Jul-Sep), Q3 (Oct-Dec)
Q_MONTHS = {1: (4, 6), 2: (7, 9), 3: (10, 12), 4: (1, 3)}


REQUEST_TIMEOUT = 30
# GOV.UK / Home Office asset hosts have been observed stalling or silently
# blocking requests with no User-Agent, especially from datacenter/CI IPs
# (Azure, etc.) -- a browser-like UA avoids that; the timeout ensures a
# hung connection fails loudly instead of running until the CI runner
# itself kills the job with no diagnostic output.
REQUEST_HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; MSSecurityCrimeStatsBot/1.0)"}


def find_ods_url() -> str:
    import re as _re

    req = urllib.request.Request(SOURCE_LISTING_URL, headers=REQUEST_HEADERS)
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
        html = resp.read().decode("utf-8", "ignore")
    m = _re.search(r'href="(https://assets\.publishing\.service\.gov\.uk/media/[^"]*prc-pfa-mar2013-onwards[^"]*\.ods)"', html)
    if not m:
        raise RuntimeError("Could not find the PFA .ods download link on the GOV.UK page")
    return m.group(1)


def download_ods(force: bool = False) -> Path:
    if ODS_PATH.exists() and not force:
        return ODS_PATH
    url = find_ods_url()
    print(f"Downloading {url}")
    req = urllib.request.Request(url, headers=REQUEST_HEADERS)
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp, open(ODS_PATH, "wb") as out:
        shutil.copyfileobj(resp, out)
    return ODS_PATH


def rolling_12_months_ending(year: int, month: int):
    """Return list of (financial_year_sheet, financial_quarter) covering the
    12 months ending at the given year/month (month is the LAST month, e.g.
    12 for 'year ending December')."""
    quarters = []
    y, m = year, month
    for _ in range(4):
        # which financial quarter does month m fall in, and which FY sheet
        if 4 <= m <= 6:
            fq, fy_start = 1, y
        elif 7 <= m <= 9:
            fq, fy_start = 2, y
        elif 10 <= m <= 12:
            fq, fy_start = 3, y
        else:  # Jan-Mar
            fq, fy_start = 4, y - 1
        sheet = f"{fy_start}_{str(fy_start + 1)[-2:]}"
        quarters.append((sheet, fq))
        m -= 3
        if m < 1:
            m += 12
            y -= 1
    return quarters


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Write the new figures into security-awareness.html")
    parser.add_argument("--refresh-download", action="store_true", help="Re-download the source file even if cached")
    parser.add_argument("--as-of-year", type=int, default=None, help="Year for 'year ending <month>' window (default: most recent full quarter)")
    parser.add_argument("--as-of-month", type=int, default=None, help="Month (1-12) for 'year ending <month>' window")
    args = parser.parse_args()

    import pandas as pd  # deferred import so --help works without pandas installed

    ods = download_ods(force=args.refresh_download)

    today = datetime.date.today()
    if args.as_of_year and args.as_of_month:
        end_year, end_month = args.as_of_year, args.as_of_month
    else:
        # Default: auto-detect the latest (financial year, quarter) actually
        # present in the workbook, and end the rolling 12-month window there.
        xls_probe = pd.ExcelFile(ods, engine="odf")
        fy_sheets = sorted(s for s in xls_probe.sheet_names if re.match(r"^\d{4}_\d{2}$", s))
        latest_sheet = fy_sheets[-1]
        latest_df = pd.read_excel(ods, engine="odf", sheet_name=latest_sheet, usecols=["Financial Quarter"])
        latest_fq = int(latest_df["Financial Quarter"].dropna().max())
        fy_start = int(latest_sheet[:4])
        end_month = Q_MONTHS[latest_fq][1]
        end_year = fy_start if latest_fq in (1, 2, 3) else fy_start + 1

    month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    rolling_quarters = rolling_12_months_ending(end_year, end_month)
    latest_sheet_label, latest_fq = rolling_quarters[0]  # most recent quarter = window end
    all_sheets_needed = sorted({s for s, _ in rolling_quarters})
    print(f"12 months ending {end_year}-{end_month:02d}: {rolling_quarters}")

    xls = pd.ExcelFile(ods, engine="odf")
    frames = []
    for sheet in all_sheets_needed:
        if sheet not in xls.sheet_names:
            raise RuntimeError(f"Sheet {sheet} not found in workbook (have: {xls.sheet_names})")
        frames.append(pd.read_excel(ods, engine="odf", sheet_name=sheet))
    df = pd.concat(frames, ignore_index=True)

    def quarter_total(force_label, subgroups, sheet, fq):
        fy_label = sheet[:4] + "/" + sheet[5:]
        mask = (
            (df["Force Name"] == force_label)
            & (df["Financial Year"] == fy_label)
            & (df["Financial Quarter"] == fq)
            & (df["Offence Subgroup"].isin(subgroups))
        )
        return int(df.loc[mask, "Number of Offences"].sum())

    results = {}
    for force_label, cfg in FORCE_STATS.items():
        if cfg["window"] == "rolling12":
            total = sum(quarter_total(force_label, cfg["subgroups"], s, fq) for s, fq in rolling_quarters)
            period_label = f"12 months to {month_names[end_month-1]} {end_year}"
        else:  # latest_quarter
            total = quarter_total(force_label, cfg["subgroups"], latest_sheet_label, latest_fq)
            q_start_month, q_end_month = Q_MONTHS[latest_fq]
            q_year = int(latest_sheet_label[:4]) if latest_fq != 4 else int(latest_sheet_label[:4]) + 1
            period_label = f"{month_names[q_start_month-1]}–{month_names[q_end_month-1]} {q_year}"
        results[force_label] = {"total": total, "period_label": period_label}

    print("\nBurglary figures:")
    for force_label, r in results.items():
        print(f"  {force_label}: {r['total']:,}  ({r['period_label']})")

    print(
        "\nReminder: anti-social behaviour figures are NOT in this dataset "
        "(ASB isn't a notifiable offence, and ONS stopped publishing a "
        "regular ASB-by-force series after 2016). Check those by hand against "
        "each force's own performance dashboard, e.g.:\n"
        "  https://northumbria-pcc.gov.uk/your-priorities/scrutiny-and-performance/crime-data/\n"
        "  https://www.durham.police.uk/About-Us/Our-Performance/Our-Performance.aspx"
    )

    if not args.apply:
        print("\n(dry run - pass --apply to write these into security-awareness.html)")
        return

    html = HTML_PATH.read_text(encoding="utf-8")
    today_str = today.strftime("%d %B %Y")

    # Northumbria: rolling-12-month total burglary figure + its period label.
    n = results["Northumbria"]
    html = re.sub(
        r'(Northumbria Police area · )[^<]*',
        f'\\g<1>{n["period_label"]}',
        html, count=1,
    )
    html = re.sub(
        r'(Northumbria Police area.*?)(\d[\d,]*)(</div><p class="text-sm text-slate-600 mt-1">burglaries recorded)',
        lambda m: m.group(1) + f'{n["total"]:,}' + m.group(3),
        html, count=1, flags=re.DOTALL,
    )

    # Durham: latest-quarter non-residential ("business & community") burglary
    # figure only -- the ASB figure alongside it is NOT touched (manual, see below).
    d = results["Durham"]
    html = re.sub(
        r'(\d[\d,]*)(</div><p class="text-sm text-slate-600 mt-1">business &amp; community burglaries \()[^)]*(\))',
        lambda m: f'{d["total"]:,}' + m.group(2) + d["period_label"] + m.group(3),
        html, count=1,
    )

    marker_start = "<!-- CRIME-STATS-SOURCE-NOTE -->"
    marker_end = "<!-- /CRIME-STATS-SOURCE-NOTE -->"
    note_html = (
        f'{marker_start}<p class="mt-2 text-xs text-slate-500 reveal">Burglary figures updated automatically on '
        f'{today_str} from the Home Office / ONS official <a href="{SOURCE_LISTING_URL}" '
        f'class="underline hover:text-teal-500" target="_blank" rel="noopener">Police recorded crime open data</a> '
        f'(Police Force Area tables; Northumbria {n["period_label"]}, Durham {d["period_label"]}). '
        f"Anti-social behaviour figures are sourced and dated separately "
        f"and checked by hand, as no equivalent open dataset is currently published.</p>{marker_end}"
    )
    if marker_start in html:
        html = re.sub(re.escape(marker_start) + r".*?" + re.escape(marker_end), note_html, html, flags=re.DOTALL)
    else:
        html = html.replace(
            "</p>\n  </div>\n</section>\n\n<!-- HARDER TARGET -->",
            f"</p>\n    {note_html}\n  </div>\n</section>\n\n<!-- HARDER TARGET -->",
            1,
        )

    HTML_PATH.write_text(html, encoding="utf-8")
    print(f"\nWrote updated figures into {HTML_PATH}")


if __name__ == "__main__":
    sys.exit(main())
