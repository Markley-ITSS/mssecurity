#!/usr/bin/env python3
"""Sync the live pages + brand_assets from repo root into public/, the Netlify publish dir."""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

PAGES = [
    "index.html",
    "community.html",
    "our-story.html",
    "security-awareness.html",
    "privacy.html",
]


def main():
    PUBLIC.mkdir(exist_ok=True)

    for page in PAGES:
        shutil.copy2(ROOT / page, PUBLIC / page)

    dest_assets = PUBLIC / "brand_assets"
    if dest_assets.exists():
        shutil.rmtree(dest_assets)
    shutil.copytree(ROOT / "brand_assets", dest_assets)

    print(f"Synced {len(PAGES)} pages + brand_assets into {PUBLIC}")


if __name__ == "__main__":
    main()
