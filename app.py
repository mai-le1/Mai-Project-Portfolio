"""
Khanh Mai Le — Electrical Engineering Portfolio
Flask application serving homepage and dynamic project pages.
"""

from flask import Flask, abort, render_template

app = Flask(__name__)

# ---------------------------------------------------------------------------
# PLACEHOLDER LINKS — replace these with your real URLs and filenames
# ---------------------------------------------------------------------------
GITHUB_URL = "https://github.com/mai-le1"  # e.g. "https://github.com/your-username"
LINKEDIN_URL = " linkedin.com/in/khanh-mai-le-a5984b388"  # e.g. "https://www.linkedin.com/in/your-profile"
RESUME_FILENAME = "Khanh_Mai_Le_0827_Resume.pdf"  # e.g. "Khanh_Mai_Le_Resume.pdf"
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
        "title": "Heartbeat LED PCB",
        "category": "PCB Design / Electronics",
        "summary": (
            "A custom 5 V heart-shaped PCB with an ATtiny1616, two daisy-chained "
            "74HC595 shift registers, and 16 LEDs running heartbeat firmware in C."
        ),
        "technologies": [
            "ATtiny1616",
            "C",
            "74HC595",
            "KiCad",
            "UPDI",
            "Shift Registers",
            "Software PWM",
        ],
        "overview": (
            "This custom heart-shaped PCB uses an ATtiny1616 to drive two "
            "daisy-chained 74HC595 shift registers, controlling 16 LEDs with "
            "only three GPIO pins (DATA, CLK, LATCH). Power enters through an "
            "SS14 Schottky diode for reverse-polarity protection and a slide "
            "switch for on/off control. Each LED has a 1 kΩ current-limiting "
            "resistor. Firmware written in C sends 16-bit patterns to the "
            "shift registers and uses software PWM to animate a realistic "
            "double-pulse heartbeat."
        ),
        "contributions": [
            "Designed a heart-shaped PCB in KiCad with power protection, MCU, and LED driver sections.",
            "Integrated ATtiny1616 with UPDI programming and two daisy-chained 74HC595 shift registers.",
            "Controlled 16 LEDs from 3 GPIO pins using serial shift-register communication.",
            "Wrote C firmware with software PWM for smooth heartbeat animation.",
            "Implemented a double-pulse pattern: strong first beat, weaker second beat, and rest interval.",
        ],
        "challenges": (
            "Describe a key challenge here. Include: the problem, what you "
            "originally expected, how you tested it, what failed, what you "
            "changed, and what you learned."
        ),
        "results": (
            "Schematic and PCB layout are complete in KiCad. Firmware "
            "implements shift-register control, software PWM brightness, and "
            "a synchronized heartbeat animation loop."
        ),
        "next_steps": (
            "Add assembled board photos, demo video, and documented test "
            "results after fabrication."
        ),
        "status": "Completed",
        "image_placeholder": "Add PCB or assembled board image",
        "github_repo": "YOUR_PROJECT_GITHUB_URL",
        "docs_path": "projects/led-heart-pcb/README.md",
    },
    {
        "slug": "personal-drone",
        "title": "ESP32-Based Quadcopter Drone",
        "category": "Embedded Systems / Power Electronics",
        "summary": (
            "A custom quadcopter using an ESP32, four MOSFET motor drivers, "
            "MPU6050 stabilization, and LiPo charging with battery monitoring."
        ),
        "technologies": [
            "ESP32-WROOM",
            "C++",
            "PWM",
            "MPU6050",
            "I2C",
            "N-Channel MOSFETs",
            "TP4056",
            "KiCad",
            "Fusion 360",
        ],
        "overview": (
            "This custom quadcopter uses an ESP32 to output PWM signals to "
            "four N-channel MOSFET motor drivers, controlling brushed coreless "
            "motors independently for lift and stabilization. An MPU6050 IMU "
            "communicates over I2C so the ESP32 can estimate roll and pitch "
            "angles and adjust motor speeds in real time. A single-cell 3.7 V "
            "LiPo powers the motors directly while a regulated 3.3 V rail "
            "supplies the ESP32 and sensors. A voltage divider feeds the "
            "battery level to an ADC pin, and a TP4056 circuit handles USB "
            "charging with status LEDs."
        ),
        "contributions": [
            "Built an ESP32-based drone control system with four independently controlled motor driver circuits.",
            "Used PWM signals to control brushed coreless motor speed through N-channel MOSFETs.",
            "Integrated an MPU6050 gyroscope/accelerometer for motion sensing and stabilization.",
            "Designed a battery voltage divider circuit to monitor LiPo voltage safely through the ESP32 ADC.",
            "Used a TP4056 charging circuit for single-cell LiPo battery charging.",
            "Tested motor control, battery measurement, and IMU communication separately before full integration.",
            "Developed firmware for motor control, sensor reading, and basic stabilization logic.",
        ],
        "challenges": (
            "Describe a key challenge here. Include: the problem, what you "
            "originally expected, how you tested it, what failed, what you "
            "changed, and what you learned."
        ),
        "results": (
            "Motor PWM control, MPU6050 I2C communication, and ADC battery "
            "monitoring were bench-tested individually before combining into "
            "a stabilization firmware loop. PCB layout and schematic design "
            "are complete in KiCad."
        ),
        "next_steps": (
            "Complete the 3D-printed frame, tune stabilization gains during "
            "tethered testing, and add wireless control."
        ),
        "status": "In progress",
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
