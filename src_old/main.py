import customtkinter as ctk

from engine.generator import generate_random_scenario
from analyzer.analyzer import analyze_logs
from ui.ui import create_ui

# -------------------------------------------------
# App Configuration
# -------------------------------------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🛡 SentLens")
app.geometry("1100x700")

# -------------------------------------------------
# Create UI
# -------------------------------------------------

ui = create_ui(app)

current_incident = None

# -------------------------------------------------
# Functions
# -------------------------------------------------

def generate_incident():

    global current_incident

    current_incident = generate_random_scenario()

    ui["log_box"].configure(state="normal")
    ui["log_box"].delete("1.0", "end")

    for log in current_incident.logs:
        ui["log_box"].insert("end", log + "\n")

    ui["log_box"].configure(state="disabled")

    ui["status_label"].configure(
        text="Incident Ready\n\nClick Analyze."
    )


def analyze_incident():

    global current_incident

    if current_incident is None:

        ui["status_label"].configure(
            text="Generate an incident first."
        )

        return

    result = analyze_logs(current_incident.logs)

    evidence = ""

    for reason in result["reason"]:
        evidence += f"• {reason}\n"

    report = (
        "Investigation Summary\n\n"
        f"Attack:\n{result['attack']}\n\n"
        f"Confidence:\n{result['confidence']}%\n\n"
        f"Severity:\n{current_incident.severity}\n\n"
        "Evidence:\n"
        f"{evidence}"
    )

    ui["status_label"].configure(text=report)


# -------------------------------------------------
# Connect Buttons
# -------------------------------------------------

ui["generate_button"].configure(
    command=generate_incident
)

ui["analyze_button"].configure(
    command=analyze_incident
)

app.mainloop()