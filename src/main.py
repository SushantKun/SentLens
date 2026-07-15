import customtkinter as ctk

from generator import generate_random_scenario
from analyzer import analyze_logs

# -------------------------------------------------
# App Configuration
# -------------------------------------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🛡 SentLens")
app.geometry("1100x700")

current_incident = None

# -------------------------------------------------
# Functions
# -------------------------------------------------

def generate_incident():
    global current_incident

    current_incident = generate_random_scenario()

    log_box.configure(state="normal")
    log_box.delete("1.0", "end")

    for log in current_incident["logs"]:
        log_box.insert("end", log + "\n")

    log_box.configure(state="disabled")

    status_label.configure(
        text="Incident Ready\n\nClick Analyze."
    )


def analyze_incident():
    global current_incident

    if current_incident is None:
        status_label.configure(
            text="Generate an incident first."
        )
        return

    result = analyze_logs(current_incident["logs"])

    evidence = ""

    for reason in result["reason"]:
        evidence += f"• {reason}\n"

    report = (
        "Investigation Summary\n\n"
        f"Attack:\n{result['attack']}\n\n"
        f"Confidence:\n{result['confidence']}%\n\n"
        f"Severity:\n{current_incident['severity']}\n\n"
        "Evidence:\n"
        f"{evidence}"
    )

    status_label.configure(text=report)

# -------------------------------------------------
# Header
# -------------------------------------------------

title = ctk.CTkLabel(
    app,
    text="🛡 SentLens",
    font=("Segoe UI", 30, "bold")
)

title.pack(pady=(20, 5))

subtitle = ctk.CTkLabel(
    app,
    text="Cyber Incident Investigation Platform",
    font=("Segoe UI", 16)
)

subtitle.pack(pady=(0, 20))

# -------------------------------------------------
# Buttons
# -------------------------------------------------

button_frame = ctk.CTkFrame(app)

button_frame.pack(pady=10)

generate_button = ctk.CTkButton(
    button_frame,
    text="Generate Incident",
    width=180,
    command=generate_incident
)

generate_button.pack(side="left", padx=10)

analyze_button = ctk.CTkButton(
    button_frame,
    text="Analyze",
    width=180,
    command=analyze_incident
)

analyze_button.pack(side="left", padx=10)

# -------------------------------------------------
# Main Area
# -------------------------------------------------

main_frame = ctk.CTkFrame(app)

main_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)

main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)

# -------------------------------------------------
# LEFT PANEL
# -------------------------------------------------

logs_frame = ctk.CTkFrame(main_frame)

logs_frame.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=(0,10)
)

logs_title = ctk.CTkLabel(
    logs_frame,
    text="Logs",
    font=("Segoe UI", 22, "bold")
)

logs_title.pack(pady=15)

log_box = ctk.CTkTextbox(
    logs_frame,
    width=450,
    height=450,
    font=("Consolas",13)
)

log_box.pack(
    padx=15,
    pady=(0,15),
    fill="both",
    expand=True
)

log_box.configure(state="disabled")

# -------------------------------------------------
# RIGHT PANEL
# -------------------------------------------------

analysis_frame = ctk.CTkFrame(main_frame)

analysis_frame.grid(
    row=0,
    column=1,
    sticky="nsew",
    padx=(10,0)
)

analysis_title = ctk.CTkLabel(
    analysis_frame,
    text="Investigation",
    font=("Segoe UI",22,"bold")
)

analysis_title.pack(pady=15)

status_label = ctk.CTkLabel(
    analysis_frame,
    text="Waiting for incident...",
    justify="left",
    anchor="nw",
    font=("Consolas",14)
)

status_label.pack(
    padx=20,
    pady=10,
    anchor="nw"
)

# -------------------------------------------------

app.mainloop()