# Projects-Portfolio

Personal engineering portfolio and project documentation monorepo for **Khanh Mai Le**.

I am an Electrical Engineering student at the University of Calgary.

What this repository contains:

1. A **Flask portfolio website** (homepage, project pages, skills, contact)
2. A **`projects/`** documentation tree for featured engineering projects (University + Personal)
3. An **`projects/additional-projects/`** folder for smaller fun projects

---

## About

I am a third-year Electrical Engineering student who enjoys turning ideas into real, working systems. I am especially interested in hands-on design, embedded systems, and software that connects hardware with real-world applications. My main areas of interest include electrical system design, custom PCB development, embedded programming, and hardware-software integration.

**Location:** Calgary, Alberta  
**Email:** sarahlebics@gmail.com

---

## Featured engineering projects

| Project | Category | Status | Documentation |
|---------|----------|--------|---------------|
| Autonomous Delivery System | Embedded Systems / Robotics | [README](projects/autonomous-delivery-system/README.md) |
| Heartbeat LED PCB | PCB Design / Electronics | [README](projects/led-heart-pcb/README.md) |
| ESP32-Based Quadcopter Drone | Embedded Systems / Power Electronics | [README](projects/personal-drone/README.md) |
| Remote-Controlled Metal Detection Vehicle | Embedded Systems / Sensing | [README](projects/metal-detecting-remote-car/README.md) |

---

## Additional projects

| Project | Category | Status | Documentation |
|---------|----------|--------|---------------|
| Portable Garden | Electronics / Embedded Systems| [README](projects/additional-projects/portable-garden/README.md) |
| Walkie-Talkie | Electronics / Communications | TODO: Update status | [README](projects/additional-projects/walkie-talkie/README.md) |
| AI Booking and Customer Service Agent | AI and Software Development | [README](projects/additional-projects/ai-booking-agent/README.md) |

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

Featured website projects: Autonomous Delivery System, Heartbeat LED PCB, ESP32-Based Quadcopter Drone, and Remote-Controlled Metal Detection Vehicle. Additional builds are documented under `projects/additional-projects/`.
