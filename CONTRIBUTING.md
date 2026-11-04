# How to update the website

You only edit text files. The design is applied automatically.

## How it works

1. Edit a file on github.com (pencil icon) and choose **"Create a new branch and start a pull request"**.
2. After about a minute, a **preview link** is posted on the pull request. Check your change there. More edits to the same branch update the preview.
3. Your change goes live a few minutes after it is approved: changes to a profile by
   that person or the group leader, everything else by the group leader.

If something is wrong, the automatic check on the pull request shows a red ✗.

## Your profile

Edit `content/people/<your-name>/index.md`. The part between the `---` lines holds
the fields; below it is your bio (plain text, a few sentences, third person).

```yaml
title: "Jane Doe"
role: "Researcher"                 # shown under your name
status: current                    # current | former
weight: 5                          # position on the People page
photo: photo.jpg                   # square-ish photo in the same folder
email: "jane.doe@idsia.ch"
themes: ["health", "languages"]    # see list below
bib_names: ["Doe"]                 # your surname as in BibTeX; lists your papers
links:
  scholar: "https://scholar.google.com/..."
  orcid: "https://orcid.org/..."
```

To replace your photo, upload a new `photo.jpg` into your folder.

**New member:** copy an existing folder, rename it `firstname-lastname`, and edit it.
**Leaving:** set `status: former` and add `years: "2022–2026"`.

## Publications

Add a BibTeX entry to `publications.bib` (e.g. copied from ACL Anthology, DBLP or
Google Scholar). Optional extra fields:

```bibtex
  keywords = {health, languages},   % research themes (see list below)
  project  = {m2p2},                % project file name, without .md
  code     = {https://github.com/...},
  pdf      = {https://...},
  award    = {Best Paper Award},
```

The paper then appears on the Publications page, on each author's profile, on the
theme page and on the project page.

To show it on the home page, add its key to `featured_publications` in
`content/_index.md`.

## News

Create `content/news/YYYY-MM-DD-short-title.md`:

```markdown
---
title: "Paper accepted at ACL 2027"
date: 2027-05-15
---
One or two sentences. Links like [this](https://example.org) are fine.
```

## Projects

Create or edit `content/projects/<short-name>.md`. Copy an existing project as a
template. Leave `end` empty while the project runs. It moves to "Past"
automatically after its end year.

`project_type`: `research` (public research funding) or `applied` (industry,
Innosuisse, hospitals).

## Resources (code, datasets, tools)

Create `content/resources/<name>.md`, copying an existing one.

## Research themes

| id           | name                                        |
|--------------|---------------------------------------------|
| `health`     | Health and clinical text                    |
| `languages`  | Languages, dialects and multilinguality     |
| `llm-trust`  | Understanding and trusting language models  |
| `literature` | Knowledge from scientific literature        |

## Writing style

Short, plain sentences. Say what the problem is and why it matters. Avoid
acronyms without explanation, superlatives and marketing language.
