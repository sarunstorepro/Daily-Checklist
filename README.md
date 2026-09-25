# Daily Checklist

A tiny, serverless replacement for a paper task diary. It's one HTML page
hosted free on Cloudflare Pages; every add/check-off/delete is saved as a
git commit to `data/tasks.json` in this same (private) repo, via the
GitHub API — no server, no database, no paid plan.

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

Only the `public/` folder is ever served publicly. `data/` and `scripts/`
never leave this private repo — Cloudflare Pages is told to publish just
`public/`, and this repo is never connected to GitHub Pages (which would
require making it public).

## One-time setup

1. **Keep this repo Private** — Settings → General → Danger Zone. Nothing
   here changes that.

2. **Create a Cloudflare account and connect this repo** (free, no card
   needed):
   - Go to https://dash.cloudflare.com/ → sign up / log in.
   - Go to **Workers & Pages → Create → Pages → Connect to Git**.
   - Authorize Cloudflare's GitHub App and give it access to the
     `Daily-Checklist` repo (you can restrict it to just this repo).
   - Pick the `Daily-Checklist` repo, branch `main`.
   - Build settings: **Framework preset**: None. **Build command**:
     leave empty. **Build output directory**: `public`.
   - Deploy. Cloudflare gives you a URL like
     `https://daily-checklist-xyz.pages.dev` — that's your app. Every
     future `git push` to `main` redeploys it automatically.

3. **Create a fine-grained GitHub access token** (this is what lets the
   page save your changes as commits):
   - Go to https://github.com/settings/personal-access-tokens/new
   - **Repository access**: "Only select repositories" → choose
     `Daily-Checklist`.
   - **Permissions → Repository permissions → Contents**: set to
     **Read and write**.
   - Generate, then copy the token (starts with `github_pat_`). You won't
     be able to see it again, so keep it somewhere safe until you paste it
     in the next step.

4. **Open the Cloudflare Pages URL** from step 2. On first load it'll ask
   for:
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

- `public/index.html` — the whole app (HTML/CSS/JS, no build step, no
  dependencies). This is the only file Cloudflare Pages ever serves.
- `data/tasks.json` — your live task list. Don't edit by hand while the app
  might also be writing to it — let the app own this file.
- `data/archive/` — created automatically once anything is old enough to
  archive.
- `scripts/archive_completed.py` + `.github/workflows/archive.yml` — the
  daily housekeeping job described above. You can trigger it manually from
  this repo's **Actions** tab if you ever want to run it early.
