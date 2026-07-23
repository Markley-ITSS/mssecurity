# MS Security Systems Ltd — Brand Guide

Drawn from the colours in the existing logo (`ms_security_logo.jpg`). Sampled directly from the artwork, then organised into a usable system for the website and future collateral.

---

## 1. Logo

- **Primary logo:** the shield + house + camera-eye mark with the "MS Home Security" wordmark.
- **Transparent version:** `brand_assets/ms_security_logo_transparent_cropped.png` — background removed by flood-fill (interior white line-work preserved). Works on both light and dark backgrounds.
- **Clear space:** keep at least the height of the "M" clear on all sides.
- **Minimum size:** ~40px tall for the mark alone; ~110px wide when the wordmark is included (so "Security" stays legible).
- **Don't:** recolour it, add drop shadows, stretch it, or place the light-background JPEG on a dark panel (use the transparent PNG instead).

> Note on names: the **logo/Facebook** brand is "MS Home Security"; the **legal / display name** on the site is **MS Security Systems Ltd**. Worth deciding long-term whether the logo wordmark should be updated to match, or kept as a friendly consumer brand.

---

## 2. Colour palette

### Teal family — signature / energy
| Token | Hex | Use |
|---|---|---|
| Teal 500 (**brand**) | `#007884` | Primary brand colour, icons, links, section eyebrows |
| Teal 400 | `#0CA8B4` | Bright teal, gradients |
| Cyan 400 (**accent**) | `#12BAC6` | CTAs, highlights, animated glow |
| Cyan 300 | `#35D0DB` | Brightest glow / hover accents |

### Navy family — trust / structure
| Token | Hex | Use |
|---|---|---|
| Navy 600 (**brand navy**) | `#003C60` | Headings, primary buttons |
| Navy 700 | `#002B47` | Darker surfaces |
| Navy 800 | `#001C33` | Dark section backgrounds |
| Navy 900 (deepest) | `#00121F` | Hero / footer background, deepest ink |

### Neutrals
| Token | Hex | Use |
|---|---|---|
| Paper | `#F5F6F4` | Page background (matches logo backdrop) |
| Ink | `#0A1722` | Body text |
| Slate 600 | `#475569` | Secondary text |

**Accessibility:** Navy 600 and Teal 500 both pass on white for text and buttons. **Cyan 400 / Cyan 300 are too light for body text on white** — use them only for large elements, buttons *with dark navy text*, borders, and glows.

**Signature combinations**
- Dark hero: Navy 900 background + Teal→Cyan radial glow + white text + Cyan CTA.
- Light section: Paper/white + Navy headings + Teal eyebrows + Teal icons.
- Gradient: `linear-gradient(100deg, #35D0DB, #0CA8B4 40%, #12BAC6)` for accent text/fills.

---

## 3. Typography

- **Display / headings:** **Space Grotesk** (600–700). Tight tracking (`-0.03em`) on large headings.
- **Body:** **Inter** (400–600). Line-height `1.7` for readability.
- Never set headings and body in the same font.

---

## 4. Motion & feel

Modern, "alive" but not tacky:
- Animated gradient blobs drifting behind dark sections.
- Live "REC" pulse dots, scanline over CCTV monitors, scrolling brand marquee.
- Scroll-reveal (fade + rise) on content blocks.
- Every interactive element has hover + focus-visible + active states.
- All motion respects `prefers-reduced-motion`.

---

## 5. Voice

Straight-talking, local, reassuring. "Done properly." "No pushy sales." Emphasise: local/North East, director-led (Steve Brown), genuine kit (Hikvision®, Pyronix®), tidy installs, real aftercare.

---

## 6. Partner brands (nominative use)

Show **Hikvision®**, **Pyronix®**, **Gallagher®** and **ColorVu™** as styled text word-marks with ®/™ stamps to signal "we install genuine kit" — not by copying their logo artwork. Always pair with a footer disclaimer that these are trademarks of their respective owners and MS Security is an independent installer.
