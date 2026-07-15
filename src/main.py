import customtkinter as ctk
from generator import generate_random_scenario
from analyzer import analyze_logs

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Create the main window
app = ctk.CTk()
app.title("🛡️ SentLens")
app.geometry("900x600")

# Welcome title
title = ctk.CTkLabel(
    app,
    text="🛡️ SentLens",
    font=("Segoe UI", 28, "bold")
)
title.pack(pady=30)

subtitle = ctk.CTkLabel(
    app,
    text="Cyber Incident Investigation Platform",
    font=("Segoe UI", 16)
)
subtitle.pack()

# Generate a random incident
incident = generate_random_scenario()

# Analyze the logs
result = analyze_logs(incident["logs"])

# Display incident in terminal
print(f"\nScenario: {incident['name']}")
print(f"Severity: {incident['severity']}")

print("\nLogs:")
print("-----")

for log in incident["logs"]:
    print(log)

print("\nAnalysis Result")
print("----------------")
print(f"Attack: {result['attack']}")
print(f"Confidence: {result['confidence']}%")

print("\nEvidence:")

for reason in result["reason"]:
    print(f"- {reason}")

app.mainloop()