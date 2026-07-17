import customtkinter as ctk

from analyzer.analyzer import analyze_incident
from engine.generator import IncidentGenerator
from reports.report import format_incident_report


class SentLensApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SentLens")
        self.geometry("1200x760")
        self.minsize(950, 650)

        self.generator = IncidentGenerator()
        self.current_incident = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_workspace()

    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=240)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        sidebar.grid_propagate(False)

        ctk.CTkLabel(
            sidebar,
            text="🛡 SentLens",
            font=("Segoe UI", 28, "bold"),
        ).pack(pady=(30, 5))

        ctk.CTkLabel(
            sidebar,
            text="Cyber Incident\nInvestigation Platform",
            font=("Segoe UI", 14),
            justify="center",
        ).pack(pady=(0, 35))

        ctk.CTkButton(
            sidebar,
            text="Generate Incident",
            height=42,
            command=self.generate_incident,
        ).pack(fill="x", padx=20, pady=8)

        ctk.CTkButton(
            sidebar,
            text="Analyze Incident",
            height=42,
            command=self.analyze_current_incident,
        ).pack(fill="x", padx=20, pady=8)

        ctk.CTkButton(
            sidebar,
            text="Clear Case",
            height=42,
            fg_color="transparent",
            border_width=1,
            command=self.clear_case,
        ).pack(fill="x", padx=20, pady=8)

        ctk.CTkLabel(
            sidebar,
            text="CASE STATUS",
            font=("Segoe UI", 14, "bold"),
        ).pack(pady=(45, 8))

        self.status_label = ctk.CTkLabel(
            sidebar,
            text="● Ready",
            font=("Segoe UI", 15),
        )
        self.status_label.pack()

        self.case_label = ctk.CTkLabel(
            sidebar,
            text="No case loaded",
            font=("Consolas", 12),
            justify="center",
        )
        self.case_label.pack(pady=18)

    def create_workspace(self):
        workspace = ctk.CTkFrame(self)
        workspace.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=15)

        workspace.grid_columnconfigure(0, weight=1)
        workspace.grid_columnconfigure(1, weight=1)
        workspace.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            workspace,
            text="Investigation Workspace",
            font=("Segoe UI", 26, "bold"),
        ).grid(row=0, column=0, columnspan=2, pady=(22, 15))

        logs_frame = ctk.CTkFrame(workspace)
        logs_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(20, 10),
            pady=(0, 20),
        )

        ctk.CTkLabel(
            logs_frame,
            text="Event Logs",
            font=("Segoe UI", 19, "bold"),
        ).pack(pady=(15, 8))

        self.log_box = ctk.CTkTextbox(
            logs_frame,
            font=("Consolas", 12),
            wrap="word",
        )
        self.log_box.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.log_box.configure(state="disabled")

        report_frame = ctk.CTkFrame(workspace)
        report_frame.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(10, 20),
            pady=(0, 20),
        )

        ctk.CTkLabel(
            report_frame,
            text="Investigation Report",
            font=("Segoe UI", 19, "bold"),
        ).pack(pady=(15, 8))

        self.report_box = ctk.CTkTextbox(
            report_frame,
            font=("Consolas", 12),
            wrap="word",
        )
        self.report_box.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.set_text(
            self.report_box,
            "Generate an incident to begin an investigation."
        )

    def set_text(self, text_box, content):
        text_box.configure(state="normal")
        text_box.delete("1.0", "end")
        text_box.insert("end", content)
        text_box.configure(state="disabled")

    def generate_incident(self):
        self.current_incident = self.generator.generate()

        formatted_logs = []

        for log in self.current_incident.logs:
            formatted_logs.append(
                f"[{log.timestamp}] [{log.level}] "
                f"[{log.source}]\n{log.message}\n"
            )

        self.set_text(self.log_box, "\n".join(formatted_logs))
        self.set_text(
            self.report_box,
            "Incident generated.\n\n"
            "Review the logs, then click “Analyze Incident” "
            "to produce the investigation report."
        )

        self.status_label.configure(text="● Awaiting analysis")
        self.case_label.configure(
            text=(
                f"Case #{self.current_incident.case_id:04d}\n"
                f"Severity: {self.current_incident.severity}\n\n"
                f"{self.current_incident.created_at}"
            )
        )

    def analyze_current_incident(self):
        if self.current_incident is None:
            self.set_text(
                self.report_box,
                "No incident loaded.\n\nGenerate an incident first."
            )
            return

        result = analyze_incident(self.current_incident)
        report = format_incident_report(self.current_incident, result)

        self.set_text(self.report_box, report)
        self.status_label.configure(text="● Investigation complete")

    def clear_case(self):
        self.current_incident = None
        self.set_text(self.log_box, "")
        self.set_text(
            self.report_box,
            "Generate an incident to begin an investigation."
        )

        self.status_label.configure(text="● Ready")
        self.case_label.configure(text="No case loaded")