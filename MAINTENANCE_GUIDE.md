# Maintenance guide

Every page is generated from files in `content/`, `data/`, and `static/`.
Edit a file, save, and the preview updates. Run `./deploy.sh` and upload
`public/` when you are done (see [README.md](README.md)).

## Team

Each person is one Markdown file in `content/team/`, named
`firstname-lastname.md`. `hugo new team/firstname-lastname.md` creates one
with the right fields.

Current member:

```yaml
---
title: "First Last"
role: "PhD Student"           # PhD Student, MS Student, Undergraduate Student,
                              # Postdoc, Project Scientist, Research Scientist ...
status: "current"
year_joined: 2025
image: "/images/team/first-last.jpg"
email: "flast@uci.edu"
research_topic: "One line describing the thesis topic"
interests:
  - "Topic one"
  - "Topic two"
---
```

Roles are grouped into sections on the team page (Research Staff, PhD
Students, MS Students, Undergraduate Students). Any other role appears under
"Other Members", so nobody disappears.

Moving someone to the alumni list: change `status` to `alumni` and add

```yaml
year_left: 2029
degrees: "MS 2026, PhD 2029"      # shown on the alumni list and the person page
current_position: "Assistant Professor at ..."
```

People with two degrees appear once, as PhD alumni, with both degrees in
`degrees`. MS-only alumni need only `year_left` and `degrees: "MS 2026"`.

Optional fields for any person: `website`, `github`, `scholar` (Google Scholar
id), `linkedin`, `thesis_title`, and a free list of links:

```yaml
links:
  - label: "Lab GitHub"
    url: "https://github.com/..."
```

The PI card links to `content/team/julian-rimoli.md`, which has
`status: "pi"` and carries the biography in its body text.

Photos: square JPG, 1000x1000 pixels, under 500 KB, saved as
`static/images/team/first-last.jpg`. A member without a photo gets an initial
in a circle.

## Research projects

One file per project in `content/research/`; `hugo new research/short-name.md`
creates the skeleton.

```yaml
---
title: "Full project title"
short_name: "Short name"
image: "/images/research/short-name.png"   # 1200x800 (3:2)
order: 3                                    # position on the research page
active: true                                # false moves it to "Past Projects"
team_members:
  - "Student Name"
  - "Prof. Collaborator (co-PI)"
funding:
  - "Agency, Jan 2026 – Dec 2028"
description: |
  Two sentences shown on the card and at the top of the project page.
---

## Abstract

One or two paragraphs.

## Related publications

- Authors, *Title*, Journal (year). [Details](/publications/#citationkey)
```

The project pages deliberately stay high level: abstract, team, funding, and
related publications. The citation key after `#` is the BibTeX key, so the link
jumps to the entry on the publications page.

## News

One file per post in `content/news/`, named `YYYY-MM-DD-short-title.md`;
`hugo new news/2026-10-01-short-title.md` creates it.

```yaml
---
title: "Headline"
date: 2026-10-01
categories: ["awards"]        # publications, people, awards, research, outreach
---

Two or three sentences. The first sentence is used as the summary on the home
page. Link to the source at the end:

Read the full story: [Title](https://...) (UCI Samueli School of Engineering).
```

The three newest posts appear on the home page. Add `draft: true` to keep a
post out of the published site; `hugo server -D` still shows it.

## Publications

Never edit `data/publications.yml` by hand. The workflow is:

1. Edit `publications.bib` (the master copy also lives in
   `../research-lab-website-materials/publications/`; keep the two identical).
2. Run, from the site folder:
   ```bash
   python3 scripts/bib_to_yaml.py
   ```
3. Check the warnings it prints (missing fields, a name written
   `Surname Initial` without a comma, duplicate keys).

The converter:

- formats authors as `F. M. Last` and shows the PI in bold;
- turns `year={submitted}` (or `in press`, `accepted`) into a
  "Submitted and in press" section at the top of the publications page,
  kept off the home page;
- turns CV-style annotations such as `year={2021 [{\bf Cover article}]}` into
  an award badge and cleans them out of the copyable BibTeX;
- shows a DOI button when `doi` is present and an arXiv button when `url`
  points to arXiv. Every entry should have a `doi` field.

## Teaching

Courses are in `data/courses.yml` (`current`, `past`, and `past_title`). The
"Student Resources" text is the body of `content/teaching.md`.

## Home page

The About text is the body of `content/_index.md`. The hero image is
`static/images/hero.jpg`. Research cards, recent news, and recent publications
fill in automatically.

## Images

| Use | Size | Format | Location |
|---|---|---|---|
| Team photo | 1000x1000 | JPG | `static/images/team/` |
| Research card | 1200x800 | PNG for diagrams, JPG for photos and renders | `static/images/research/` |
| Hero | 1920 wide or larger | JPG | `static/images/` |

Keep files under about 500 KB. On a Mac, `sips -Z 1000 photo.jpg` resizes,
and `sips -s format jpeg photo.png --out photo.jpg` converts.

## Truss Me! page

The page is `content/trussme.md` and lives at `/trussme/`. Its front matter
controls everything that changes at release time:

- `web_app`: copy the Unity WebGL build (the folder containing `index.html`,
  `Build/`, and `TemplateData/`) to `static/trussme/app/` and set
  `web_app: "/trussme/app/index.html"`. The page then shows a "Play in your
  browser" button that loads the build in place, plus a full-screen link.
- `poster`: an optional screenshot (1600x900) shown in the play area before
  the app loads, for example `/images/trussme/poster.jpg`.
- `app_store_url` and `play_store_url`: the store links. Empty values show
  "coming soon".

Build the Unity project with **Decompression Fallback** enabled (Player
Settings > Publishing Settings). The build then runs on any web server,
including `hugo server`, without special `Content-Encoding` headers. Without it,
a Brotli or gzip compressed build only works if the server is configured to
send those headers.

## Site settings

`hugo.toml` holds the lab name, university, department, PI name, PI photo,
email, description, and the menu. `baseURL` must be set to the public address
before the first deployment.

## Troubleshooting

- **A change does not appear in the preview.** Restart `hugo server`. It
  sometimes misses a burst of file changes.
- **Styles look old in the browser.** Hard-refresh (Cmd+Shift+R).
- **`./deploy.sh` refuses to run.** Stop the preview server first.
- **A person or project is missing from a list.** Check `status`, `role`, and
  `active` in the front matter, and that the file is not a draft.
- **The build fails.** Hugo prints the file and line; the usual cause is a
  YAML front-matter error such as an unclosed quote or a missing `---`.
