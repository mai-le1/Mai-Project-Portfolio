# Contributing project documentation

This guide explains how to add and maintain engineering project folders in this monorepo.

The portfolio website (`app.py`, `templates/`, `static/`) and the `projects/` documentation tree are related but separate.

- **Featured projects** live directly under `projects/` and appear on the Flask homepage.
- **Additional projects** live under `projects/additional-projects/` and are listed in the root README only (unless you also add them to `app.py`).

---

## How to add a new project

1. Choose where it belongs:

   - Featured (main portfolio): `projects/my-new-project/`
   - Additional / secondary: `projects/additional-projects/my-new-project/`

   Use a short, lowercase, hyphenated slug.

2. Add the standard subfolders:

   ```text
   code/
   schematics/
   pcb/
   cad/
   documentation/
   images/
   videos/
   bom/
   test-results/
   ```

3. Put a `.gitkeep` file in any empty folder so Git tracks it.

4. Copy an existing project `README.md` template and replace the title, category, and all `TODO:` sections with real information only.

5. Add a row to the correct table in the root [`README.md`](README.md):

   - **Featured engineering projects** or **Additional projects**
   - Include project name, technical category, status, and relative README link

6. If the project is featured, add an entry to the `PROJECTS` list in `app.py` so it appears on the website.

---

## How to organize files

| Folder | Put here |
|--------|----------|
| `code/` | Firmware, scripts, notebooks, and application source |
| `schematics/` | Schematic sources and exported PDF/SVG drawings |
| `pcb/` | PCB layouts, Gerbers, drill files, fabrication notes |
| `cad/` | Mechanical models, STEP/STL exports, drawings |
| `documentation/` | Design notes, reports, meeting notes, write-ups |
| `images/` | Photos, screenshots, diagrams used in the README |
| `videos/` | Short demos, or a text file with external video links |
| `bom/` | Bills of materials (CSV/XLSX/PDF) |
| `test-results/` | Test logs, tables, scope captures, observation notes |

Prefer descriptive filenames:

```text
motor-driver-rev2.kicad_sch
frame-v3.step
bench-test-2026-07-15.md
```

---

## Naming conventions

- **Project folder slugs:** `lowercase-with-hyphens` (example: `led-heart-pcb`)
- **Files:** lowercase or clear TitleCase; avoid spaces — use hyphens or underscores
- **Revisions:** include revision or date when useful (`rev2`, `v3`, `2026-07-15`)
- **README images:** store under `images/` and link with relative paths
- Do not use special characters that break URLs or Windows paths

---

## How to document team contributions

Be specific and honest about what you owned versus what teammates owned.

In the project README **My role** section:

- List your personal contributions as bullet points
- Note the team size and context (course team, family business, personal)
- Credit teammates by name only with their permission
- Do not claim sole ownership of shared work

Example pattern:

```markdown
## My role

Team of 4 — university design course.

- Designed PCB layout in KiCad
- Wrote motor-control firmware for the ESP32
- Teammate A owned mechanical CAD
- Teammate B owned sensor bring-up
```

---

## How to avoid committing private information

Never commit:

- Passwords, API keys, tokens, or webhook secrets
- `.env` files with real values (use `.env.example` placeholders only)
- Private customer data, phone numbers, or personal messages
- Private academic grades or unpublished exam material (unless allowed)
- Licensed vendor IP you are not allowed to redistribute
- Home addresses or other sensitive personal details

Before every commit, review `git status` and `git diff`. If a secret was committed accidentally, rotate the credential and remove it from history.

---

## How to add images

1. Export or copy the image into the project’s `images/` folder.
2. Use a descriptive filename (`prototype-top-view.jpg`).
3. Link it from the project README with a relative path:

   ```markdown
   ![Prototype top view](images/prototype-top-view.jpg)
   ```

4. Add useful alt text.
5. Do **not** reference image files that do not exist yet — keep a text placeholder until the file is present.
6. Prefer compressed JPG/WebP for photos and PNG for diagrams.

Website images for the Flask app belong in `static/images/`, not under `projects/`.

---

## How to handle large videos

Git is a poor fit for large video files.

Recommended approach:

1. Upload demos to a stable external host (unlisted YouTube, Google Drive, OneDrive, etc.).
2. In `videos/`, add a short markdown or text file with the link and a description:

   ```markdown
   # Demo video

   - Description: TODO
   - Link: TODO_URL
   - Date recorded: TODO
   ```

3. If a short clip must live in the repo, keep it small and note the size in the README.
4. Do not commit multi-hundred-megabyte raw recordings.

---

## How to document testing results

1. Create a dated note in `test-results/` (example: `test-results/2026-07-15-motor-bench.md`).
2. Record:

   - what was tested
   - equipment / setup
   - expected behaviour
   - observed behaviour
   - pass/fail
   - next actions

3. Summarize key results in the project README **Testing and results** table.
4. Only include measurements you actually took — never invent numbers.
5. Attach supporting photos or logs next to the test note when useful.

---

## Checklist before opening a pull request or pushing

- [ ] Project folder uses the standard structure
- [ ] README `TODO:` items replaced only where real info exists
- [ ] Root README project table updated
- [ ] No secrets or `.env` files included
- [ ] Image links point to files that exist
- [ ] Large videos are linked, not force-committed
- [ ] Team contributions are credited accurately
