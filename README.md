# about

<p align="center">
  <a href="https://about.micr.dev"><strong>about.micr.dev</strong></a> - personal archive
</p>

Personal portfolio/about page for [micr.dev](https://about.micr.dev). Part portfolio, part personal archive - a static site listing interests, tastes, and references in a responsive archive layout.

## Tech Stack

- **HTML/CSS/JS** - vanilla, no frameworks, no build tools
- **Custom font** - DecimaMono (self-hosted)
- **Data-driven** - all content lives in `data.json`, rendered client-side
- **Hosted on** [Netlify](https://netlify.com)

## Browser Support

Modern desktop and mobile browsers. Desktop keeps the fixed two-column archive layout, while mobile collapses into a single scrollable column with the hero image below the content.

## Project Structure

```
.
+-- index.html          # Main page (skeleton loader, two-column layout)
+-- script.js           # Fetches data.json, renders all content sections
+-- style.css           # Layout, skeleton shimmer, grids, custom cursor
+-- data.json           # All profile content (intro, series, music, etc.)
+-- fonts/
|   +-- DecimaMono.ttf             # Original manual-processing input
|   +-- decima-mono-core.woff2     # Preloaded ASCII and common punctuation
|   +-- decima-mono-extended.woff2 # Latin extension, loaded on demand
+-- scripts/subset-fonts.py       # Manual font generation, never a build step
+-- docs/fonts.md                # Rerun instructions, measurements, pixel proof
+-- images/             # Game covers, album art, designer logos, hero image
+-- .claude/
|   +-- skills/         # Claude Code skill constraints for UI work
+-- favicon.png
+-- robots.txt
+-- sitemap.xml
+-- netlify.toml        # Netlify build config (publish = ".")
```

## How It Works

1. `index.html` loads with skeleton placeholder UI (shimmer animation while content loads).
2. `script.js` waits for fonts before fetching `data.json`. The hero image loads independently.
3. Content is rendered dynamically based on each section's `type`:
   - **`intro`** - bio text with name header
   - **`T`** - timed items (title + year), sorted by year
   - **`R`** - rows with dot leaders (title...right), optional links
   - **`P`** - picture grid (album art, game covers), optional Spotify links
   - **`designerImages`** - fashion designer logo grid
   - **`colours`** - hex values with inline color swatches
   - **`fonts`** - font name rows with dot leaders
   - **`runways`** - runway show rows
   - **`lastUpdated`** - footer timestamp
4. A custom floating cursor shows labels on image hover.
5. Mobile visitors get the same archive content in a single-column layout.

### Loading states

The initial page contains only decorative skeletons, not an "About Microck" heading. The intro skeleton includes the name/pronoun row; text rows follow the content line height, and mobile image tiles use the same grid tracks as the loaded images.

Content stays `aria-busy="true"` until rendering finishes or the load-error message appears. Text skeletons and the hero placeholder resolve independently. The hero placeholder overlays a reserved image area, disappears completely when ready, and does not leave an invisible shimmer running. Its link stays hidden until the image is ready. Reduced-motion preferences disable shimmer and the image fade.

The hero's `width`/`height` attributes and desktop CSS height cap match its 2000×2407 source dimensions. Update both if replacing that image.

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

### Font maintenance

Run `scripts/subset-fonts.py` by hand after content or font/style changes and commit its two WOFF2 outputs and generated CSS. Deployment does not process fonts. See [font maintenance and pixel proof](docs/fonts.md) for the pinned Python tools, rendering constraints, byte measurements, and before/after screenshots.

## Customization

All content is in **`data.json`**. Edit it directly to add, remove, or reorder sections. The file is a JSON object where each top-level key is a section. The `displayName` field controls the section heading (defaults to the key name).

### Section types

| Type | Fields | Display |
|------|--------|---------|
| `intro` | `text` | Bio paragraph |
| `T` | `items[].title`, `items[].year` | Title...Year |
| `R` | `items[].title`, `items[].right?`, `items[].spotify?`, `items[].link?` | Title...Right |
| `P` | `items[].name`, `items[].image?`, `items[].spotify?` | Image grid |
| `designerImages` | `items[].name`, `items[].image?` | Logo grid |
| `colours` | `items[].title` (hex) | Hex...[swatch] |
| `fonts` | `items[].title`, `items[].right` | Font...Right |
| `runways` | `items[].runway`, `items[].designer` | Runway...Designer |
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

Push to the repository's main branch - Netlify auto-deploys from the root directory with no build command.

## AI-Assisted Development

This project includes a [Claude Code skill](./.claude/skills/ui-skills/SKILL.md) (`ui-skills`) that enforces opinionated UI constraints when working with AI coding agents. Invoke it with `/ui-skills` in Claude Code to apply layout, animation, typography, and accessibility rules to any changes.

## License

All rights reserved.
