import re
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
import requests

# ---- Settings ---------------------------------------------------------------
DOWNLOAD = True             # True: check the portal and download new/changed files; False: skip
START_YEAR = 2016
RAW_DIR = Path("data/raw")
MANIFEST = RAW_DIR / "manifest.csv"
TABLES = ["Crashes", "Parties", "InjuredWitnessPassengers"]
REFRESH_RECENT_YEARS = 2    # fallback only: used when a resource has no last_modified date

CKAN = "https://data.ca.gov/api/3/action/package_show"
HEADERS = {"User-Agent": "Napa County traffic safety EDA (CCRS research notebook)"}

RAW_DIR.mkdir(parents=True, exist_ok=True)


def list_ccrs_resources():
    """List every yearly Crashes / Parties / InjuredWitnessPassengers resource from START_YEAR on."""
    r = requests.get(CKAN, params={"id": "ccrs"}, headers=HEADERS, timeout=60)
    r.raise_for_status()
    pattern = re.compile(rf"({'|'.join(TABLES)})[_\s-]*(\d{{4}})", re.IGNORECASE)
    rows = []
    for res in r.json()["result"]["resources"]:
        m = pattern.fullmatch(res.get("name", "").strip())
        if not m or int(m.group(2)) < START_YEAR:
            continue
        table = next(t for t in TABLES if t.lower() == m.group(1).lower())
        rows.append({
            "table": table,
            "year": int(m.group(2)),
            "resource_id": res["id"],
            "url": res["url"],
            "last_modified": res.get("last_modified") or res.get("metadata_modified"),
        })

    if not rows:
        raise RuntimeError("No CCRS resources matched. Check the resource names on data.ca.gov.")
    resources = pd.DataFrame(rows).sort_values(["table", "year"]).reset_index(drop=True)
    years = range(START_YEAR, resources["year"].max() + 1)
    expected = {(t, y) for t in TABLES for y in years}
    missing = sorted(expected - set(zip(resources["table"], resources["year"])))
    if missing:
        raise RuntimeError(f"Missing resources: {missing}")
    return resources


def download(url, dest):
    """Stream to a .part file, then rename, so an interrupted download never looks complete."""
    tmp = dest.with_suffix(".part")
    with requests.get(url, headers=HEADERS, stream=True, timeout=600) as r:
        r.raise_for_status()
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 20):
                f.write(chunk)
    tmp.replace(dest)


def count_data_lines(path):
    """Approximate row count (lines minus header). Quoted line breaks would inflate it slightly."""
    with open(path, "rb") as f:
        return sum(1 for _ in f) - 1


def load_manifest():
    if MANIFEST.exists():
        return pd.read_csv(MANIFEST, dtype=str).set_index("file")
    return pd.DataFrame(columns=["table", "year", "resource_id", "last_modified",
                                 "downloaded_at", "bytes", "data_lines"]).rename_axis("file")


if DOWNLOAD:
    resources = list_ccrs_resources()
    END_YEAR = int(resources["year"].max())  
    print(f"Found {len(resources)} resources covering {START_YEAR}–{END_YEAR}.")

    manifest = load_manifest()
    for row in resources.itertuples():
        name = f"{row.table.lower()}_{row.year}.csv"
        dest = RAW_DIR / name
        prev = manifest.loc[name] if name in manifest.index else None

        # re-download only when the portal says the file changed
        if not dest.exists() or prev is None:
            reason = "new"
        elif row.last_modified and str(prev["last_modified"]) != str(row.last_modified):
            reason = "updated on portal"
        elif not row.last_modified and row.year > END_YEAR - REFRESH_RECENT_YEARS:
            reason = "recent year, no last_modified"
        else:
            continue

        print(f"Downloading {name} ({reason}) ...")
        download(row.url, dest)

        # record what was downloaded and when
        manifest.loc[name] = {
            "table": row.table,
            "year": row.year,
            "resource_id": row.resource_id,
            "last_modified": row.last_modified,
            "downloaded_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "bytes": dest.stat().st_size,
            "data_lines": count_data_lines(dest),
        }
        manifest.sort_index().to_csv(MANIFEST)  # save after each file in case a later one fails

    print("Done.")
    print(manifest.sort_index())
