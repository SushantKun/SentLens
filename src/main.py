import customtkinter as ctk

from generator import generate_random_scenario
from analyzer import analyze_logs

# -------------------------
# Window
# -------------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🛡 SentLens")
app.geometry("900x650")

current_incident = None

# -------------------------
# Functions
# -------------------------

def generate_incident():
    global current_incident

    current_incident = generate_random_scenario()

    log_box.configure(state="normal")
    log_box.delete("1.0", "end")

    for log in current_incident["logs"]:
        log_box.insert("end", log + "\n")

    log_box.configure(state="disabled")

    analysis_label.configure(
        text="Incident generated.\nClick Analyze."
    )


def analyze_incident():
    global current_incident

    if current_incident is None:
        analysis_label.configure(
            text="Generate an incident first."
        )
        return

    result = analyze_logs(current_incident["logs"])

    evidence = ""

    for reason in result["reason"]:
        evidence += f"• {reason}\n"

    analysis_label.configure(
        text=(
            f"Attack: {result['attack']}\n"
            f"Confidence: {result['confidence']}%\n\n"
            f"Evidence:\n{evidence}"
        )
    )

# -------------------------
# Title
# -------------------------

title = ctk.CTkLabel(
    app,
    text="🛡 SentLens",
    font=("Segoe UI", 28, "bold")
)

title.pack(pady=(20, 5))

subtitle = ctk.CTkLabel(
    app,
    text="Cyber Incident Investigation Platform",
    font=("Segoe UI", 16)
)

subtitle.pack(pady=(0, 20))

# -------------------------
# Buttons
# -------------------------

button_frame = ctk.CTkFrame(app)

button_frame.pack(pady=10)

generate_button = ctk.CTkButton(
    button_frame,
    text="Generate Incident",
    command=generate_incident
)

generate_button.pack(side="left", padx=10)

analyze_button = ctk.CTkButton(
    button_frame,
    text="Analyze",
    command=analyze_incident
)

analyze_button.pack(side="left", padx=10)

# -------------------------
# Logs
# -------------------------

logs_title = ctk.CTkLabel(
    app,
    text="Logs",
    font=("Segoe UI", 18, "bold")
)

logs_title.pack(pady=(20, 5))

log_box = ctk.CTkTextbox(
    app,
    width=800,
    height=250
)

log_box.pack()

log_box.configure(state="disabled")

# -------------------------
# Analysis
# -------------------------

analysis_title = ctk.CTkLabel(
    app,
    text="Analysis",
    font=("Segoe UI", 18, "bold")
)

analysis_title.pack(pady=(20, 5))

analysis_label = ctk.CTkLabel(
    app,
    text="Waiting for incident...",
    justify="left",
    anchor="w",
    font=("Consolas", 14)
)

analysis_label.pack(fill="x", padx=50)

# -------------------------

app.mainloop()