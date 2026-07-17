import customtkinter as ctk

from generator import generate_random_scenario
from analyzer import analyze_logs


class SentLensApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("🛡 SentLens")
        self.geometry("1200x750")

        self.current_incident = None

        self.setup_window()
        self.create_sidebar()
        self.create_workspace()


    # -------------------------------------------------
    # Window Setup
    # -------------------------------------------------

    def setup_window(self):

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)


    # -------------------------------------------------
    # Sidebar
    # -------------------------------------------------

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=250
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=15,
            pady=15
        )

        self.sidebar.grid_rowconfigure(8, weight=1)


        title = ctk.CTkLabel(
            self.sidebar,
            text="🛡 SentLens",
            font=("Segoe UI", 28, "bold")
        )

        title.pack(
            pady=(25,5)
        )


        subtitle = ctk.CTkLabel(
            self.sidebar,
            text="Cyber Investigation\nPlatform",
            font=("Segoe UI",14)
        )

        subtitle.pack(
            pady=(0,30)
        )


        self.generate_button = ctk.CTkButton(
            self.sidebar,
            text="Generate Incident",
            height=40,
            command=self.generate_incident
        )

        self.generate_button.pack(
            padx=20,
            pady=10,
            fill="x"
        )


        self.analyze_button = ctk.CTkButton(
            self.sidebar,
            text="Analyze",
            height=40,
            command=self.analyze_incident
        )

        self.analyze_button.pack(
            padx=20,
            pady=10,
            fill="x"
        )


        self.clear_button = ctk.CTkButton(
            self.sidebar,
            text="Clear",
            height=40,
            command=self.clear_screen
        )

        self.clear_button.pack(
            padx=20,
            pady=10,
            fill="x"
        )


        status_title = ctk.CTkLabel(
            self.sidebar,
            text="Case Status",
            font=("Segoe UI",18,"bold")
        )

        status_title.pack(
            pady=(40,5)
        )


        self.status_label = ctk.CTkLabel(
            self.sidebar,
            text="🟡 Ready",
            font=("Segoe UI",14)
        )

        self.status_label.pack()


        self.case_label = ctk.CTkLabel(
            self.sidebar,
            text="No case loaded",
            font=("Consolas",12)
        )

        self.case_label.pack(
            pady=20
        )


    # -------------------------------------------------
    # Main Workspace
    # -------------------------------------------------

    def create_workspace(self):

        self.workspace = ctk.CTkFrame(
            self
        )

        self.workspace.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(0,15),
            pady=15
        )

        self.workspace.grid_rowconfigure(1, weight=1)
        self.workspace.grid_columnconfigure(0, weight=1)


        header = ctk.CTkLabel(
            self.workspace,
            text="Investigation Workspace",
            font=("Segoe UI",26,"bold")
        )

        header.grid(
            row=0,
            column=0,
            pady=20
        )


        content = ctk.CTkFrame(
            self.workspace
        )

        content.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=15,
            pady=10
        )


        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(1, weight=1)


        # Logs

        logs_title = ctk.CTkLabel(
            content,
            text="Logs",
            font=("Segoe UI",20,"bold")
        )

        logs_title.grid(
            row=0,
            column=0,
            pady=10
        )


        self.log_box = ctk.CTkTextbox(
            content,
            font=("Consolas",13)
        )

        self.log_box.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10
        )


        # Investigation

        result_title = ctk.CTkLabel(
            content,
            text="Investigation",
            font=("Segoe UI",20,"bold")
        )

        result_title.grid(
            row=0,
            column=1,
            pady=10
        )


        self.result_box = ctk.CTkTextbox(
            content,
            font=("Consolas",13)
        )

        self.result_box.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=10
        )


    # -------------------------------------------------
    # Actions
    # -------------------------------------------------

    def generate_incident(self):

        self.current_incident = generate_random_scenario()


        self.log_box.delete(
            "1.0",
            "end"
        )


        for log in self.current_incident.logs:
            self.log_box.insert(
                "end",
                log + "\n"
            )


        self.result_box.delete(
            "1.0",
            "end"
        )


        self.status_label.configure(
            text="🟡 Waiting Analysis"
        )


        self.case_label.configure(
            text=f"Case #{self.current_incident.case_id:04d}\n"
                 f"{self.current_incident.created_at}"
        )


    def analyze_incident(self):

        if self.current_incident is None:

            self.result_box.insert(
                "end",
                "No incident loaded."
            )

            return


        result = analyze_logs(
            self.current_incident
        )


        report = (
            "Investigation Summary\n\n"
            f"Attack:\n{result['attack']}\n\n"
            f"Confidence:\n{result['confidence']}%\n\n"
            f"Severity:\n{self.current_incident.severity}\n\n"
            "Evidence:\n"
        )


        for item in result["reason"]:
            report += f"\n• {item}"


        self.result_box.delete(
            "1.0",
            "end"
        )

        self.result_box.insert(
            "end",
            report
        )


        self.status_label.configure(
            text="🟢 Investigation Complete"
        )


    def clear_screen(self):

        self.current_incident = None

        self.log_box.delete(
            "1.0",
            "end"
        )

        self.result_box.delete(
            "1.0",
            "end"
        )

        self.case_label.configure(
            text="No case loaded"
        )

        self.status_label.configure(
            text="🟡 Ready"
        )