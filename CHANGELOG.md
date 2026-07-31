# Build changelog — MS Security Systems site

Repo: **github.com/Markley-ITSS/mssecurity** (public, org-owned, branch `master`).
Hosting has been handed to the client: the live site is served from **the client's own
Netlify account**, deploying automatically from `master`. Markley IT no longer holds a
Netlify site for this project (deleted 2026-07-31) — the CLI `netlify deploy` flow below
is retired.

**Deploy = `git push` to `master`.** Nothing goes live until pushed; the client's Netlify
build follows a minute or two later. Rollback is via git (`git revert`), not `backups/`.

---

## 2026-07-31 — Hosting handed over to the client
- **Client now hosts the site.** Steve registered the domain and pointed it at **his own Netlify account**, which builds from this repo's `master` branch. Netlify Forms submissions (the quote form) now land in his account, not Markley IT's.
- **Markley IT's duplicate Netlify site deleted** — it was a second site deploying from the same repo and served no purpose once the domain and forms moved. No data lost; the repo is the source of truth.
- **Repo deliberately retained** in the Markley-ITSS org (public, Paul is owner). Not transferred to the client's GitHub — code changes still route through Markley IT. If a full handover is wanted later it's a single GitHub repo transfer plus a Netlify reconnect on his side.
- Background: the reason the repo sits in a public org repo rather than the client's own account is Netlify's free plan, which won't deploy a **private org-owned** repo, and won't show a personal repo you're only a collaborator on. Public + org membership was the no-cost route.

## Open items for next session

- **Crime-stats refresh** — the GitHub Actions workflow exists but its schedule is disabled (commit 4db206f); manual trigger only. Decide whether to re-enable the quarterly cadence now that the site is client-hosted. A **Windows Task Scheduler job** (`MSSecurityDemo-CrimeStatsRefresh`, Paul's machine only) remains the interim fallback.
- Google star rating/count still needed for a Google stat badge (Steve).
- ICO registration/fee status + exact data-retention periods need Steve's confirmation on the Privacy Policy page.

## 2026-07-22 — Gallery overhaul (real install photos) + crime-stats automation
- **Gallery rebuilt from real WhatsApp photos** Paul supplied in `temporary screenshots/` (36 photos, sorted down to 21 genuinely usable on-site shots). Old stock/illustrative CCTV+Alarms+Equipment album replaced with 5 real-photo albums: **Installs in progress**, **Tidy workspace**, **Old & new panels**, **Reviews** (FB review screenshot), **Events** (Steve at The Security Event, NEC). New images resized/compressed (Pillow, max 1600px, q82) into `brand_assets/gallery/` as `install-*`, `workspace-*`, `panel-*`, `review-*`, `event-*`. Old gallery-only stock/install images (not used elsewhere on the page) archived, not deleted, to `brand_assets/gallery/_archived_pre-2026-07-22/`.
- **Fixed a real square-tile grid bug**: tried the classic "padding-top: 100%" aspect-ratio trick when troubleshooting a rendering report, but it's incompatible with CSS Grid auto-row sizing (percentage padding doesn't contribute to grid track intrinsic sizing — collapses to ~66px instead of square). Reverted to the original `aspect-square` + `object-cover` approach, which is correct and grid-safe. Verified square at both desktop (4-col) and mobile (2-col, 375px) widths via computed-style checks.
- **Crime stats on security-awareness.html now auto-sourced**: `scripts/update_crime_stats.py` downloads the official Home Office/ONS "Police recorded crime open data: Police Force Area tables" (quarterly ODS) and computes each force's burglary figure — Northumbria: rolling-12-month total (residential + non-residential); Durham: latest single quarter, non-residential only ("business & community burglaries"), matching what's already on the page. Writes the numbers plus a dated, sourced note back into the page. **Anti-social behaviour figures are NOT automatable** — ASB isn't a notifiable offence and ONS stopped publishing a regular ASB-by-force series after 2016; those stay manually sourced. First run: Northumbria 6,522→**6,509**, Durham 162→**163** (both closely matched the prior manually-sourced figures, confirming the methodology).
- Interim automation via a **local Windows Scheduled Task** (runs the script quarterly, 27th of Jan/Apr/Jul/Oct, only while the PC is on) — real cloud automation needs a GitHub repo first (queued for tomorrow, see Open Items above).
- **Deployed live** — both changes are on https://mshomesec-demo.netlify.app now.

## 2026-07-22 — Self-hosted fonts (removed Google Fonts)
- Fonts now served from our own domain: `brand_assets/fonts/inter-var.woff2` + `space-grotesk-var.woff2` (variable, weights 400–700, latin subset, SIL OFL, 72KB total). Google served variable fonts, so one file per family covers all weights.
- All 5 pages: `@font-face` added to the inline `<style>`; the 3 Google `<link>` lines (2 preconnect + stylesheet) replaced with 2 local `<link rel=preload>` (crossorigin). Removes the visitor-IP transfer to Google.
- **Privacy Policy updated** (§4, §6) to drop the Google Fonts disclosure and describe fonts as self-hosted.
- Verified: fonts load from localhost/live, headings=Space Grotesk, body=Inter, **0 requests to fonts.googleapis/gstatic**. Only remaining third-party request site-wide is `cdn.tailwindcss.com` (Tailwind Play CDN) — the next item if fully airtight privacy is wanted.

## 2026-07-22 — Logo marquee spacing
- More breathing room in the hero brand-logo scroller: chip gap 28px → **44px** desktop (`gap-7`→`gap-11`), 20px → **32px** mobile (`gap-5`→`gap-8`); copy-wrapper padding widened to match so the seam gap equals the chip gap and the loop stays seamless.

## 2026-07-22 — Privacy Policy page (UK GDPR) + reader accessibility
- New **privacy.html** — full UK GDPR / DPA 2018 privacy notice (11 sections: controller, data collected, lawful bases, cookies/analytics, sharing, international transfers, retention, security, rights, changes, ICO complaints) with a sticky quick-jump contents list. Matches site design + dropdown nav + footer.
- **Reader accessibility:** legal acronyms (UK GDPR, DPA 2018, PECR, IDTA, ICO, IP address) use `<abbr title="…">` accessible tooltips; a "Skip to content" link; sections have `scroll-margin-top` for the sticky header.
- **Linked** from the footer bottom-bar on all 5 pages + a line under the quote form ("See our Privacy Policy").
- **Verified:** axe-core WCAG 2.2 AA = 0 violations; responsive clean at 375/768/1024/1280 (no horizontal overflow); image `alt` audited site-wide (content images descriptive, duplicated marquee logos `alt=""`, lightbox alt set via JS).
- **Needs Steve's confirmation** (reasonable defaults used meanwhile): ICO registration/fee status (no reg number shown), exact data-retention periods (stated "up to 6 years" for financial records), and that no analytics/cookies are used anywhere. Google Fonts IP-transfer is disclosed honestly; self-hosting fonts would remove it (flagged as a follow-up).

## 2026-07-22 — Nav decluttered into dropdowns (all 4 pages)
- Top nav collapsed from 10 flat items to **5**: **About ▾** (About Us · Why Choose Us · Community) · Services · **Our Work ▾** (Recent Work · Reviews · Quality Systems) · Awareness · Contact.
- **Coverage removed** from the menu (the `#areas` section stays on the page + in the footer, just unlinked from the top nav).
- Dropdowns are an accessible disclosure pattern: hover for mouse (CSS), click/keyboard toggle with `aria-expanded`, Esc-to-close + focus-out-to-close + click-outside-to-close (JS). Active page highlights its parent (About or Awareness).
- Breakpoint for the full nav lowered **`xl` → `lg`** now that it fits — more screens get the full menu before the burger. Mobile drawer kept flat (Coverage dropped, reordered to match the new groups).
- Verified across all 4 pages: correct `index.html#` prefixes on sub-pages, no overflow at 1024px, dropdown geometry/visibility correct.

## 2026-07-22 — Day/night comparison slider + poor-footage contrast
- "See the Difference" now has an interactive **day/night before-after slider** (`.cmp`, drag + ARIA-slider keyboard) using matched FRONT-Left CCTV shots (`brand_assets/gallery/cctv-left-day-c.jpg` / `cctv-left-night-c.jpg` — cropped to strip phone-app chrome; a tiny "Live" badge remains on the day side).
- Added a "budget-camera problem" panel with the two grainy `poor-footage-*.jpg` shots.
- FRONT-Right pair also cropped and ready (`cctv-right-day-c.jpg` / `cctv-right-night-c.jpg`) for an optional second slider — not yet placed.

## 2026-07-22 — Amendments batch (client Word docs) + 2 new pages
- New pages: **our-story.html** (About Us — company history + team) and **security-awareness.html** (crime stats + prevention advice).
- Nav restructured across all 4 pages (About Us · Services · Quality Systems · Why Choose Us · Recent Work · Reviews · Community · Awareness · Coverage · Contact); shows at `xl`, burger below. Footer rebuilt (4-col, "Our Security Services", company no. + **registered office** in small print, "MS Security Systems Limited").
- Homepage copy rewrites throughout (hero, services ×5 with Access control removed, See the Difference, new **See the Upgrade** section with old/new alarm photos, Why-us, reviews/areas/quote headings). "Alarms & CCTV" → "alarms and CCTV". Brands only named in hero + logo strip.
- **Quote form redesigned** (contact.png mockup): added Address, Postcode, Budget + new service dropdown (Alarm/CCTV Installation-Upgrade-Repair, Video Doorbell, Other). Netlify re-detected fields.
- **Community** reworked: Rutherford U13 Swifts (crest) + Kibblesworth Time Capsule replace the Whickham/Mason entry; values cards rewritten, "Backing young players" removed.
- New real images in `brand_assets/gallery/` (alarm-*, poor-footage-*) and `brand_assets/community/` (rutherford-afc, kibblesworth); official brand logos already in `brand_assets/logos/`.
- **Rollback:** `backups/index_2026-07-22_pre-amendments.html` + `backups/community_2026-07-22_pre-amendments.html`.

## 2026-07-21 — Hero: video ident replaces 3-image carousel
- Replaced the 3-slide hero carousel (logo → CCTV kit → night footage) with the `ms-security-logo.mp4` brand video (1280×720, 16:9, ~7s, autoplay/muted/loop, pause control + reduced-motion aware).
- **Rollback:** `cp backups/index_2026-07-21_carousel-hero.html index.html` then redeploy. That restores the 3-image carousel hero.

## 2026-07-21 — Brand direction + logo strip
- "Alarms & CCTV" ordering throughout (alarms priority); service cards + footer reordered alarms-first.
- Hero brand line → "Hikvision, Pyronix, Ajax and HKC". From "What we do" down, copy is brand-generic.
- Scrolling text marquee → **official brand logos** (Hikvision, Pyronix, Ajax, HKC) on white chips (`brand_assets/logos/`).
- Footage line reworded to "high-quality 4K cameras".

## 2026-07-21 — Community page (real content)
- `community.html` — Whickham FC / Mason Hardy player sponsor + Hebburn Sparks (2023) dated timeline. Real photos from FB post embeds.

## 2026-07-21 — Reviews, form, a11y, mobile
- Reviews: 3 real cards (Google/Facebook/Checkatrade) with clickable platform headers + hover popout.
- Contact form wired to Netlify Forms; email notification → steve@mssecurity.uk. (Netlify `ignore_html_forms` had to be set false.)
- Accessibility brought to Lighthouse 100 / axe WCAG 2.2 AA clean.
- Mobile nav: "Free quote" button hidden on phones (was wrapping/crowding).

## 2026-07-21 — Initial build
- Single-page site (`index.html`), Tailwind CDN, brand palette from logo (teal/navy). Hero, services, footage, why-us, gallery + popup album, reviews, areas, quote form, footer.
- Assets: enhanced logo (mark + transparent), real 206px install photos, brand guide (`BRAND_GUIDE.md`).
