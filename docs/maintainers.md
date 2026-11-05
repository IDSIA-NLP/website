# Maintainer notes

For admins of the repository and the IDSIA web server. Contributors don't need this.

## Folder overview

| Path                     | What                                            |
|--------------------------|-------------------------------------------------|
| `content/`               | All text: people, projects, news, themes, pages |
| `publications.bib`       | All publications (BibTeX)                       |
| `hugo.toml`              | Site settings, menu, contact, theme names       |
| `scripts/bib2json.py`    | Turns the BibTeX file into data for Hugo        |
| `.github/workflows/`     | Automatic build on GitHub                       |
| `.github/CODEOWNERS`     | Who approves changes to which profile           |
| `deploy/pull-site.sh`    | Script the IDSIA server runs to fetch the site  |
| `layouts/`, `assets/`    | Design: HTML templates, CSS, JavaScript         |

## Preview locally (optional)

Install Hugo (a single file: https://github.com/gohugoio/hugo/releases, version 0.145.0), then:

```bash
python3 scripts/bib2json.py
hugo server
```

Open http://localhost:1313.

## How publishing works

1. Someone proposes a change (pull request). GitHub checks that it builds and
   posts a **preview link** on the pull request
   (`https://idsia-nlp.github.io/website/pr-<number>/`).
2. The right person approves it (see `.github/CODEOWNERS`) and it is merged into `main`.
3. On the IDSIA server, a cron job runs `deploy/pull-site.sh` every 5 minutes. If `main`
   changed, it builds the site and copies it to the web folder. The official site is
   only ever built from approved content.

### Server setup (once)

```bash
# 1. Back up the current site.
# 2. Copy deploy/pull-site.sh to the server and set WEBROOT inside it.
# 3. Run it once by hand to check, then add to crontab (crontab -e):
*/5 * * * * flock -n /tmp/nlp-site.lock /path/to/pull-site.sh >> $HOME/nlp-site-deploy.log 2>&1
```

The server needs `git`, `python3`, `rsync`, `curl` and outgoing HTTPS to github.com.
Hugo is downloaded automatically by the script.

### GitHub settings (once, by an admin)

- **Settings → Pages:** Source "Deploy from a branch", branch `gh-pages`, folder `/ (root)`.
  (The branch appears after the first pull request.)
- **Settings → Rules → Rulesets → New branch ruleset** for `main`:
  require a pull request before merging, with 1 approval and
  "Require review from Code Owners"; block force pushes;
  add the group leader (Repository admin role) to the bypass list.
- **Settings → Actions → General:** "Workflow permissions" → Read and write;
  keep "Allow GitHub Actions to create and approve pull requests" **off**.
- **Settings → Collaborators and teams:** give group members the **Write** role.

### Adding a collaborator

1. Give them Write access (Settings → Collaborators and teams).
2. Add a line for their profile folder in `.github/CODEOWNERS`.
