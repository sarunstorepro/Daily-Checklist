# Daily Checklist

A tiny, serverless replacement for a paper task diary. It's one HTML page
hosted free on GitHub Pages; every add/check-off/delete is saved as a git
commit to `data/tasks.json` in this same (private) repo, via the GitHub
API — no server, no database, no paid plan.

- **Pending tasks never disappear until you finish or delete them** — that's
  what makes them "carry over" to the next day automatically: there's no
  separate rollover step, they just stay in the one Pending list, and each
  one shows how many days old it is.
- **Completed tasks** show under "Completed today" and then move into the
  **History** tab, grouped by the day you finished them.
- A scheduled GitHub Action (`.github/workflows/archive.yml`) tidies the
  data file once a day, moving anything completed more than 30 days ago
  into `data/archive/YYYY-MM.json` so the live file stays small forever.
  You never need to touch this yourself.

## One-time setup

1. **Make sure this repo is Private.** Settings → General → Danger Zone →
   "Change repository visibility", if it isn't already. (Your task text is
   only ever read via the GitHub API using your own token — it is never
   included in the published Pages site, but Private is still the right
   default since this is your day-to-day work list.)

2. **Enable GitHub Pages.**
   Settings → Pages → under "Build and deployment", set **Source** to
   "Deploy from a branch", branch `main`, folder `/ (root)`. Save. GitHub
   will give you a URL like `https://sarunstorepro.github.io/Daily-Checklist/`
   — that's the app.

3. **Create a fine-grained personal access token** (this is what lets the
   page save your changes as commits):
   - Go to https://github.com/settings/personal-access-tokens/new
   - **Repository access**: "Only select repositories" → choose
     `Daily-Checklist`.
   - **Permissions → Repository permissions → Contents**: set to
     **Read and write**.
   - Generate, then copy the token (starts with `github_pat_`). You won't
     be able to see it again, so keep it somewhere safe until you paste it
     in the next step.

4. **Open the Pages URL** from step 2. On first load it'll ask for:
   - GitHub username: `sarunstorepro`
   - Repo name: `Daily-Checklist`
   - Branch: `main`
   - The token from step 3

   This is saved only in that browser's local storage — it's never written
   back to the repo. If you use the checklist from another device or
   browser, you'll do this same one-time setup there too (you can reuse
   the same token, or make a new one).

5. Start typing tasks. Every add, check-off, or delete shows up as a commit
   in this repo's history within a couple of seconds.

## Files

- `index.html` — the whole app (HTML/CSS/JS, no build step, no dependencies).
- `data/tasks.json` — your live task list. Don't edit by hand while the app
  might also be writing to it — let the app own this file.
- `data/archive/` — created automatically once anything is old enough to
  archive.
- `scripts/archive_completed.py` + `.github/workflows/archive.yml` — the
  daily housekeeping job described above. You can trigger it manually from
  this repo's **Actions** tab if you ever want to run it early.
- `_config.yml` — tells GitHub Pages' Jekyll build to leave `data/` and
  `scripts/` out of the published site.
