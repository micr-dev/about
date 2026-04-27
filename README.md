# about

<p align="center">
  <a href="https://about.micr.dev"><strong>about.micr.dev</strong></a> · desktop-only personal archive
</p>

Personal portfolio/about page for [micr.dev](https://about.micr.dev). Part portfolio, part personal archive — a static site listing interests, tastes, and references in a two-column layout.

## Tech Stack

- **HTML/CSS/JS** — vanilla, no frameworks, no build tools
- **Custom font** — DecimaMono (self-hosted)
- **Data-driven** — all content lives in `data.json`, rendered client-side
- **Hosted on** [Netlify](https://netlify.com)

## Browser Support

Desktop browsers only. The site uses a fixed two-column layout at ≥1024px width. Mobile visitors see a blocker overlay with a message to visit on desktop.

## Project Structure

```
.
├── index.html          # Main page (skeleton loader, two-column layout)
├── script.js           # Fetches data.json, renders all content sections
├── style.css           # Layout, skeleton shimmer, grids, custom cursor
├── data.json           # All profile content (intro, series, music, etc.)
├── fonts/
│   └── DecimaMono.ttf  # Primary monospace font (preloaded)
├── images/             # Game covers, album art, designer logos, hero image
├── .claude/
│   └── skills/         # Claude Code skill constraints for UI work
├── favicon.png
├── robots.txt
├── sitemap.xml
└── netlify.toml        # Netlify build config (publish = ".")
```

## How It Works

1. `index.html` loads with skeleton placeholder UI (shimmer animation while content loads).
2. `script.js` waits for fonts and the hero image, then fetches `data.json`.
3. Content is rendered dynamically based on each section's `type`:
   - **`intro`** — bio text with name header
   - **`T`** — timed items (title + year), sorted by year
   - **`R`** — rows with dot leaders (title·········right), optional links
   - **`P`** — picture grid (album art, game covers), optional Spotify links
   - **`designerImages`** — fashion designer logo grid
   - **`colours`** — hex values with inline color swatches
   - **`fonts`** — font name rows with dot leaders
   - **`runways`** — runway show rows
   - **`lastUpdated`** — footer timestamp
4. A custom floating cursor shows labels on image hover.
5. Desktop-only — mobile visitors see a blocker overlay.

## Local Development

No build step required. Serve the directory with any static file server:

```bash
# Python
python3 -m http.server 8000

# Node (if npx available)
npx serve .

# PHP
php -S localhost:8000
```

Open `http://localhost:8000` in your browser.

## Customization

All content is in **`data.json`**. Edit it directly to add, remove, or reorder sections. The file is a JSON object where each top-level key is a section. The `displayName` field controls the section heading (defaults to the key name).

### Section types

| Type | Fields | Display |
|------|--------|---------|
| `intro` | `text` | Bio paragraph |
| `T` | `items[].title`, `items[].year` | Title·········Year |
| `R` | `items[].title`, `items[].right?`, `items[].spotify?`, `items[].link?` | Title·········Right |
| `P` | `items[].name`, `items[].image?`, `items[].spotify?` | Image grid |
| `designerImages` | `items[].name`, `items[].image?` | Logo grid |
| `colours` | `items[].title` (hex) | Hex·········[swatch] |
| `fonts` | `items[].title`, `items[].right` | Font·········Right |
| `runways` | `items[].runway`, `items[].designer` | Runway·········Designer |
| `lastUpdated` | `text` | Small footer text |

Each section uses `displayName` for its heading (defaults to the object key). Add new images to `images/` and reference them by filename.

### Styling

CSS variables in `style.css` (`:root`) control column widths and positioning:

```css
--left-col-min: 480px;
--left-col-ideal: 36vw;
--left-col-max: 880px;
```

## Deployment

Configured via `netlify.toml`:

```toml
[build]
  publish = "."
```

Push to the repository's main branch — Netlify auto-deploys from the root directory with no build command.

## AI-Assisted Development

This project includes a [Claude Code skill](./.claude/skills/ui-skills/SKILL.md) (`ui-skills`) that enforces opinionated UI constraints when working with AI coding agents. Invoke it with `/ui-skills` in Claude Code to apply layout, animation, typography, and accessibility rules to any changes.

## License

All rights reserved.
