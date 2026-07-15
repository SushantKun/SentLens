import customtkinter as ctk
from generator import generate_scenario

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Create the main window
app = ctk.CTk()
app.title("SentLens")
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

incident = generate_scenario("brute_force")

print(f"\nScenario: {incident['name']}")
print(f"Severity: {incident['severity']}")
print("\nLogs:\n")

for log in incident["logs"]:
    print(log)
    
app.mainloop()