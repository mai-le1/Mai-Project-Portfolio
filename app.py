"""
Khanh Mai Le — Electrical Engineering Portfolio
Flask application serving homepage and dynamic project pages.
"""

from flask import Flask, abort, render_template

app = Flask(__name__)

# ---------------------------------------------------------------------------
# PLACEHOLDER LINKS — replace these with your real URLs and filenames
# ---------------------------------------------------------------------------
GITHUB_URL = "YOUR_GITHUB_URL"  # e.g. "https://github.com/your-username"
LINKEDIN_URL = "YOUR_LINKEDIN_URL"  # e.g. "https://www.linkedin.com/in/your-profile"
RESUME_FILENAME = "YOUR_RESUME_FILENAME"  # e.g. "Khanh_Mai_Le_Resume.pdf"
# ---------------------------------------------------------------------------

# Featured projects shown on the portfolio homepage (main engineering builds).
# Additional projects live under projects/additional-projects/ and are documented
# in the root README — add them here only if you want them on the website too.
PROJECTS = [
    {
        "slug": "autonomous-delivery-system",
        "title": "Autonomous Delivery System",
        "category": "Embedded Systems / Robotics",
        "summary": (
            "A university engineering project combining PCB design, "
            "microcontroller programming, motor control, CAD, and 3D printing."
        ),
        "technologies": [
            "ESP32",
            "Raspberry Pi Pico",
            "C",
            "C++",
            "KiCad",
            "Autodesk Fusion 360",
            "Motor Control",
            "3D Printing",
        ],
        "overview": (
            "This university project involved designing and testing an "
            "autonomous delivery-system prototype and remote-controlled vehicle "
            "through several hardware iterations."
        ),
        "contributions": [
            "Designed PCB layouts and electrical schematics in KiCad.",
            "Programmed ESP32 and Raspberry Pi Pico microcontrollers.",
            "Integrated motors, sensors, and mechanical components.",
            "Created CAD models and components in Autodesk Fusion 360.",
            "Tested hardware and identified wiring, power-delivery, and firmware issues.",
            "Documented design changes, test results, and unresolved technical risks.",
            "Coordinated tasks and design decisions with a multidisciplinary team.",
        ],
        "challenges": (
            "Describe a key challenge here. Include: the problem, what you "
            "originally expected, how you tested it, what failed, what you "
            "changed, and what you learned."
        ),
        "results": (
            "Completed university engineering project. Add concrete results "
            "here when ready — without inventing measurements."
        ),
        "next_steps": (
            "TODO: Add next steps for this project."
        ),
        "status": "TODO: Update status",
        "image_placeholder": "Add PCB or prototype image",
        "github_repo": "YOUR_PROJECT_GITHUB_URL",
        "docs_path": "projects/autonomous-delivery-system/README.md",
    },
    {
        "slug": "led-heart-pcb",
        "title": "Programmable LED Heart PCB",
        "category": "PCB Design / Electronics",
        "summary": (
            "TODO: Add a short summary of the programmable LED heart PCB."
        ),
        "technologies": [
            "TODO: Add technologies used",
        ],
        "overview": (
            "TODO: Add project overview. See projects/led-heart-pcb/README.md "
            "for the full documentation template."
        ),
        "contributions": [
            "TODO: List your contributions.",
        ],
        "challenges": (
            "Describe a key challenge here. Include: the problem, what you "
            "originally expected, how you tested it, what failed, what you "
            "changed, and what you learned."
        ),
        "results": (
            "TODO: Add results once verified — do not invent measurements."
        ),
        "next_steps": (
            "TODO: Add next steps."
        ),
        "status": "TODO: Update status",
        "image_placeholder": "Add PCB or assembled board image",
        "github_repo": "YOUR_PROJECT_GITHUB_URL",
        "docs_path": "projects/led-heart-pcb/README.md",
    },
    {
        "slug": "personal-drone",
        "title": "Personal Quad-Motor Drone",
        "category": "Embedded Systems / Power Electronics",
        "summary": (
            "A quad-motor drone prototype using an ESP32 and MOSFET-based "
            "motor-driver circuits."
        ),
        "technologies": [
            "ESP32-WROOM",
            "C++",
            "PWM",
            "N-Channel MOSFETs",
            "Flyback Diodes",
            "716 Coreless Motors",
            "Breadboarding",
            "Fusion 360",
        ],
        "overview": (
            "I am developing a lightweight drone platform to learn motor "
            "control, power electronics, embedded programming, hardware "
            "debugging, and flight stabilization."
        ),
        "contributions": [
            "Designed four N-channel MOSFET low-side motor-driver circuits.",
            "Added flyback diodes, gate resistors, pull-down resistors, and filtering components.",
            "Programmed PWM control for four coreless DC motors.",
            "Tested simultaneous operation of all four motors.",
            "Diagnosed motor, wiring, and power-supply issues.",
            "Began designing a lightweight 3D-printed frame.",
            "Planned future sensor-based stabilization and wireless control.",
        ],
        "challenges": (
            "Describe a key challenge here. Include: the problem, what you "
            "originally expected, how you tested it, what failed, what you "
            "changed, and what you learned."
        ),
        "results": (
            "Project is in progress. Add results as milestones are reached — "
            "without claiming flight performance that has not been measured."
        ),
        "next_steps": (
            "Complete the 3D-printed frame, add IMU-based stabilization, and "
            "implement wireless control."
        ),
        "status": "In progress.",
        "image_placeholder": "Add drone circuit or frame image",
        "github_repo": "YOUR_PROJECT_GITHUB_URL",
        "docs_path": "projects/personal-drone/README.md",
    },
    {
        "slug": "metal-detecting-remote-car",
        "title": "Remote-Controlled Metal Detection Vehicle",
        "category": "Embedded Systems / Sensing",
        "summary": (
            "TODO: Add a short summary of the remote-controlled metal "
            "detection vehicle."
        ),
        "technologies": [
            "TODO: Add technologies used",
        ],
        "overview": (
            "TODO: Add project overview. See "
            "projects/metal-detecting-remote-car/README.md for the full "
            "documentation template."
        ),
        "contributions": [
            "TODO: List your contributions.",
        ],
        "challenges": (
            "Describe a key challenge here. Include: the problem, what you "
            "originally expected, how you tested it, what failed, what you "
            "changed, and what you learned."
        ),
        "results": (
            "TODO: Add results once verified — do not invent measurements."
        ),
        "next_steps": (
            "TODO: Add next steps."
        ),
        "status": "TODO: Update status",
        "image_placeholder": "Add vehicle or metal-detector prototype image",
        "github_repo": "YOUR_PROJECT_GITHUB_URL",
        "docs_path": "projects/metal-detecting-remote-car/README.md",
    },
]

SKILLS = {
    "Programming": [
        "C",
        "C++",
        "Python",
        "TypeScript",
        "JavaScript",
        "MATLAB",
    ],
    "Embedded Systems": [
        "ESP32",
        "Raspberry Pi Pico",
        "ATtiny1616",
        "Arduino IDE",
        "PWM",
        "ADC",
        "UART",
        "Sensor integration",
    ],
    "Electronics": [
        "Circuit prototyping",
        "Motor control",
        "MOSFET switching",
        "Op-amps",
        "Breadboarding",
        "Soldering",
        "Hardware troubleshooting",
        "PCB design",
    ],
    "Design and Engineering Tools": [
        "KiCad",
        "Altium Designer",
        "Autodesk Fusion 360",
        "Git",
        "GitHub",
    ],
    "Software and Backend": [
        "Flask",
        "Next.js",
        "Prisma",
        "Redis",
        "BullMQ",
        "REST APIs",
        "Webhooks",
    ],
}


def get_project_by_slug(slug):
    """Return the project dict matching slug, or None if not found."""
    for project in PROJECTS:
        if project["slug"] == slug:
            return project
    return None


@app.context_processor
def inject_globals():
    """Make placeholder links available in every template."""
    return {
        "github_url": GITHUB_URL,
        "linkedin_url": LINKEDIN_URL,
        "resume_filename": RESUME_FILENAME,
    }


@app.route("/")
def index():
    """Homepage with hero, about, projects, skills, and contact."""
    return render_template(
        "index.html",
        projects=PROJECTS,
        skills=SKILLS,
    )


@app.route("/projects/<slug>")
def project_detail(slug):
    """Dynamic project detail page. Returns 404 if slug is unknown."""
    project = get_project_by_slug(slug)
    if project is None:
        abort(404)
    return render_template("project.html", project=project)


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page for missing routes and invalid project slugs."""
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
