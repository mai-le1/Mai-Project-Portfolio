# Projects-Portfolio

Personal engineering portfolio and project documentation monorepo for **Khanh Mai Le**.

Khanh is an Electrical Engineering student at the University of Calgary, seeking an **8–16 month co-op beginning January 2027 in Metro Vancouver**.

This repository contains:

1. A **Flask portfolio website** (homepage, project pages, skills, contact)
2. A **`projects/`** documentation tree for featured engineering builds
3. An **`projects/additional-projects/`** folder for secondary builds

---

## About

I build embedded systems, electronic prototypes, and software tools that connect hardware with real-world applications. Experience areas include PCB design, embedded programming, motor control, circuit prototyping, CAD, and AI-powered software development.

**Location:** Calgary, Alberta  
**Email:** sarahlebics@gmail.com

---

## Featured engineering projects

| Project | Category | Status | Documentation |
|---------|----------|--------|---------------|
| Autonomous Delivery System | Embedded Systems / Robotics | TODO: Update status | [README](projects/autonomous-delivery-system/README.md) |
| Programmable LED Heart PCB | PCB Design / Electronics | TODO: Update status | [README](projects/led-heart-pcb/README.md) |
| Personal Quad-Motor Drone | Embedded Systems / Power Electronics | TODO: Update status | [README](projects/personal-drone/README.md) |
| Remote-Controlled Metal Detection Vehicle | Embedded Systems / Sensing | TODO: Update status | [README](projects/metal-detecting-remote-car/README.md) |

---

## Additional projects

| Project | Category | Status | Documentation |
|---------|----------|--------|---------------|
| Portable Garden | Electronics / Embedded Systems | TODO: Update status | [README](projects/additional-projects/portable-garden/README.md) |
| Dual-Mode Autonomous and Remote-Controlled Vehicle | Embedded Systems / Mechatronics | TODO: Update status | [README](projects/additional-projects/autonomous-remote-car/README.md) |
| Walkie-Talkie | Electronics / Communications | TODO: Update status | [README](projects/additional-projects/walkie-talkie/README.md) |
| AI Booking and Customer Service Agent | AI and Software Development | TODO: Update status | [README](projects/additional-projects/ai-booking-agent/README.md) |

For how to add projects, organize files, and document work, see [CONTRIBUTING_PROJECTS.md](CONTRIBUTING_PROJECTS.md).

---

## Repository structure

```text
Projects-Portfolio/
├── app.py                      # Flask application and featured project data
├── requirements.txt
├── .env.example
├── .gitignore
├── CONTRIBUTING_PROJECTS.md
├── README.md
├── static/                     # Website CSS, images, documents
├── templates/                  # Jinja HTML templates
└── projects/                   # Engineering documentation
    ├── autonomous-delivery-system/   # Featured
    ├── led-heart-pcb/                # Featured
    ├── personal-drone/               # Featured
    ├── metal-detecting-remote-car/   # Featured
    └── additional-projects/          # Secondary builds
        ├── portable-garden/
        ├── autonomous-remote-car/
        ├── walkie-talkie/
        └── ai-booking-agent/
```

Each project folder includes: `code/`, `schematics/`, `pcb/`, `cad/`, `documentation/`, `images/`, `videos/`, `bom/`, and `test-results/`.

---

## Portfolio website (Flask)

### Technology

| Layer | Choice |
|-------|--------|
| Language | Python |
| Framework | Flask |
| Templates | Jinja2 |
| Styling | Custom CSS |
| Production server | Gunicorn |
| Database | None |

### Install and run (Windows)

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

### Replace website placeholders

In `app.py`:

```python
GITHUB_URL = "YOUR_GITHUB_URL"
LINKEDIN_URL = "YOUR_LINKEDIN_URL"
RESUME_FILENAME = "YOUR_RESUME_FILENAME"
```

Place a resume PDF in `static/documents/` after updating `RESUME_FILENAME`.

Copy `.env.example` to `.env` for any local secrets — never commit `.env`.

### Deploy on Render

| Setting | Value |
|---------|--------|
| Build command | `pip install -r requirements.txt` |
| Start command | `gunicorn app:app` |

---

## Website routes

| URL | Description |
|-----|-------------|
| `/` | Portfolio homepage |
| `/projects/<slug>` | Featured project detail page |
| Unknown path / invalid slug | Custom 404 |

Featured website projects: Autonomous Delivery System, Programmable LED Heart PCB, Personal Quad-Motor Drone, and Remote-Controlled Metal Detection Vehicle. Additional builds are documented under `projects/additional-projects/`.
