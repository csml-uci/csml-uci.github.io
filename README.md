# Computational Solid Mechanics Lab website

Hugo site for the Computational Solid Mechanics Lab @ UCI. All content is
Markdown and YAML; the only tool needed is Hugo (`brew install hugo`).

## Preview

```bash
hugo server -D
```

Open http://localhost:1313. Pages reload as you edit. `-D` also shows news
posts marked `draft: true`. If a change does not show up after a batch of file
edits, stop the server (Ctrl+C) and start it again.

## Publish

The site is hosted on GitHub Pages at https://csml-uci.github.io/ from the
repository `csml-uci/csml-uci.github.io`. Every push to `main` triggers the
workflow in `.github/workflows/hugo.yaml`, which builds the site with Hugo and
publishes it within a couple of minutes. To publish your changes:

```bash
./publish.sh "what changed"
```

Progress and any build errors appear in the repository's Actions tab.
`deploy.sh` still builds `public/` locally for uploading to an ordinary web
server, should the site ever move.

## Where things live

| Path | What it is |
|---|---|
| `hugo.toml` | Site name, PI, email, menu |
| `content/team/` | One file per person: current members, alumni, and the PI |
| `content/research/` | One file per research project |
| `content/news/` | One file per news post |
| `content/teaching.md`, `data/courses.yml` | Teaching page text and course list |
| `publications.bib` | Publications; converted to `data/publications.yml` by `scripts/bib_to_yaml.py` |
| `static/images/` | Team photos, research images, hero image |
| `layouts/`, `static/css/main.css` | Templates and styles |
| `.github/workflows/hugo.yaml` | The GitHub Pages build |
| `public/` | Local build output from `./deploy.sh`; GitHub builds its own copy |
| `../research-lab-website-materials/` | CV, proposals, master BibTeX file, photo originals. Never published |

How to add or change content: see [MAINTENANCE_GUIDE.md](MAINTENANCE_GUIDE.md).
