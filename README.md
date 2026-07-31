# MS Security Systems — website

Static marketing site for MS Security Systems (alarms, CCTV, video doorbells).
Built and maintained by **Markley IT**; hosting is owned by the client.

## Hosting & deploy

- **Repo:** `github.com/Markley-ITSS/mssecurity` — public, branch `master`.
- **Live site:** served from the **client's own Netlify account**, which builds
  automatically from `master`. Markley IT holds no Netlify site for this project.
- **To deploy:** commit and `git push` to `master`. Nothing goes live until pushed;
  the Netlify build lands a minute or two later.
- **To roll back:** `git revert` the offending commit and push. (The `backups/` folder
  is a pre-git relic, not the rollback path.)
- **Forms:** the quote form on `index.html` uses Netlify Forms (`data-netlify="true"`)
  with a honeypot field. Submissions and email notifications go to the client's
  Netlify account.

The repo is public because Netlify's free plan won't deploy a private org-owned repo.
**Never commit secrets** — anything sensitive belongs in Netlify's environment variables.

## Layout

| Path | What it is |
|---|---|
| `*.html` | The site's pages — `index`, `community`, `our-story`, `privacy`, `security-awareness`. **Edit these.** |
| `public/` | Auto-generated mirror of the root pages + `brand_assets/`. **Never hand-edit** — a git pre-commit hook syncs it via `scripts/sync_public.py`. |
| `brand_assets/` | Logos, palette, gallery photos. See `BRAND_GUIDE.md`. |
| `scripts/` | `sync_public.py` (the hook) and `update_crime_stats.py` (refreshes the community crime figures). |
| `.github/workflows/` | `crime-stats-refresh.yml` — scheduled run currently disabled, manual trigger only. |
| `backups/` | Timestamped page copies from before this was a git repo. Historical. |
| `CHANGELOG.md` | Dated build log and open items. Keep current. |
| `webCLAUDE.md` | Frontend conventions for AI-assisted work on this site. |

## Local preview

Serve the project root over localhost (not `file:///`, which breaks relative paths):

```bash
python -m http.server 3000
```

Then open <http://localhost:3000>. The same config is wired up as the `mssecurity`
entry in `.claude/launch.json`.
