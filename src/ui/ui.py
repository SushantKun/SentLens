import threading

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from analyzer.analyzer import analyze_incident
from engine.generator import IncidentGenerator
from intelligence.threat_intel import lookup_ip_reputation
from reports.report import get_recommendations

from response.playbook import execute_playbook

COLORS = {
    "background": "#0b0f14",
    "sidebar": "#0f151d",
    "panel": "#121820",
    "card": "#18212b",
    "card_hover": "#202c38",
    "border": "#2a3644",
    "text": "#e5e7eb",
    "muted": "#94a3b8",
    "accent": "#38bdf8",
    "success": "#22c55e",
    "warning": "#facc15",
    "critical": "#ef4444",
    "high": "#fb923c",
    "medium": "#facc15",
    "low": "#22c55e",
    "unassessed": "#475569",
}

SEVERITY_COLORS = {
    "Critical": COLORS["critical"],
    "High": COLORS["high"],
    "Medium": COLORS["medium"],
    "Low": COLORS["low"],
    "Unassessed": COLORS["unassessed"],
}

LEVEL_COLORS = {
    "Information": COLORS["accent"],
    "Warning": COLORS["warning"],
    "Critical": COLORS["critical"],
}


class SentLensApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SentLens - Cyber Incident Investigation Platform")
        self.geometry("1280x800")
        self.minsize(1080, 680)
        self.configure(fg_color=COLORS["background"])

        self.generator = IncidentGenerator()
        self.current_incident = None
        self.current_result = None
        self.threat_intel_result = None

        self.pages = {}
        self.nav_buttons = {}
        self.timeline_index = 0
        self.analysis_index = 0
        self.animation_token = 0
        self.chart_canvas = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_area()
        self.create_case_page()
        self.create_investigation_page()
        self.create_analytics_page()

        self.show_page("case")

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self,
            width=225,
            corner_radius=0,
            fg_color=COLORS["sidebar"],
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="SENTLENS",
            font=("Segoe UI", 25, "bold"),
            text_color=COLORS["accent"],
        ).pack(anchor="w", padx=22, pady=(28, 0))

        ctk.CTkLabel(
            self.sidebar,
            text="Incident investigation workspace",
            font=("Segoe UI", 12),
            text_color=COLORS["muted"],
        ).pack(anchor="w", padx=22, pady=(0, 30))

        self.generate_button = ctk.CTkButton(
            self.sidebar,
            text="Generate New Case",
            height=40,
            fg_color="#0284c7",
            hover_color="#0369a1",
            font=("Segoe UI", 13, "bold"),
            command=self.generate_case,
        )
        self.generate_button.pack(fill="x", padx=18, pady=(0, 8))

        self.analyze_button = ctk.CTkButton(
            self.sidebar,
            text="Analyze Current Case",
            height=40,
            fg_color="#334155",
            hover_color="#475569",
            font=("Segoe UI", 13, "bold"),
            command=self.start_analysis,
        )
        self.analyze_button.pack(fill="x", padx=18, pady=(0, 28))

        ctk.CTkLabel(
            self.sidebar,
            text="WORKSPACE",
            font=("Segoe UI", 10, "bold"),
            text_color=COLORS["muted"],
        ).pack(anchor="w", padx=22, pady=(0, 7))

        self.add_nav_button("case", "Case Timeline")
        self.add_nav_button("investigation", "Investigation")
        self.add_nav_button("analytics", "Analytics")

        ctk.CTkFrame(
            self.sidebar,
            height=1,
            fg_color=COLORS["border"],
        ).pack(fill="x", padx=18, pady=22)

        ctk.CTkLabel(
            self.sidebar,
            text="CURRENT CASE",
            font=("Segoe UI", 10, "bold"),
            text_color=COLORS["muted"],
        ).pack(anchor="w", padx=22)

        self.sidebar_case_label = ctk.CTkLabel(
            self.sidebar,
            text="No case loaded",
            font=("Consolas", 11),
            text_color=COLORS["muted"],
            justify="left",
        )
        self.sidebar_case_label.pack(anchor="w", padx=22, pady=(7, 10))

        self.sidebar_status = ctk.CTkLabel(
            self.sidebar,
            text="READY",
            font=("Segoe UI", 10, "bold"),
            corner_radius=7,
            fg_color=COLORS["unassessed"],
            padx=10,
            pady=5,
        )
        self.sidebar_status.pack(anchor="w", padx=22)

        spacer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        spacer.pack(fill="both", expand=True)

        self.clear_button = ctk.CTkButton(
            self.sidebar,
            text="Clear Case",
            height=33,
            fg_color="transparent",
            border_width=1,
            border_color=COLORS["border"],
            command=self.clear_case,
        )
        self.clear_button.pack(fill="x", padx=18, pady=(0, 8))

        ctk.CTkButton(
            self.sidebar,
            text="Exit SentLens",
            height=33,
            fg_color="transparent",
            border_width=1,
            border_color="#7f1d1d",
            text_color="#fca5a5",
            hover_color="#35171b",
            command=self.destroy,
        ).pack(fill="x", padx=18, pady=(0, 24))

    def add_nav_button(self, page_name, text):
        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            anchor="w",
            height=36,
            corner_radius=7,
            fg_color="transparent",
            text_color=COLORS["muted"],
            hover_color=COLORS["card_hover"],
            command=lambda: self.show_page(page_name),
        )
        button.pack(fill="x", padx=12, pady=3)
        self.nav_buttons[page_name] = button

    def create_main_area(self):
        main_area = ctk.CTkFrame(
            self,
            fg_color=COLORS["background"],
            corner_radius=0,
        )
        main_area.grid(row=0, column=1, sticky="nsew")
        main_area.grid_columnconfigure(0, weight=1)
        main_area.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(
            main_area,
            height=74,
            corner_radius=0,
            fg_color=COLORS["panel"],
        )
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        self.page_title = ctk.CTkLabel(
            header,
            text="Case Timeline",
            font=("Segoe UI", 23, "bold"),
        )
        self.page_title.grid(row=0, column=0, sticky="w", padx=26, pady=(14, 0))

        self.page_subtitle = ctk.CTkLabel(
            header,
            text="Generate a case to begin an investigation.",
            font=("Segoe UI", 12),
            text_color=COLORS["muted"],
        )
        self.page_subtitle.grid(row=1, column=0, sticky="w", padx=26, pady=(0, 14))

        self.header_status = ctk.CTkLabel(
            header,
            text="READY",
            font=("Segoe UI", 10, "bold"),
            fg_color=COLORS["unassessed"],
            corner_radius=7,
            padx=11,
            pady=6,
        )
        self.header_status.grid(row=0, column=1, rowspan=2, padx=26)

        self.page_container = ctk.CTkFrame(
            main_area,
            fg_color=COLORS["background"],
            corner_radius=0,
        )
        self.page_container.grid(row=1, column=0, sticky="nsew")
        self.page_container.grid_columnconfigure(0, weight=1)
        self.page_container.grid_rowconfigure(0, weight=1)

    def create_page(self, name):
        page = ctk.CTkFrame(
            self.page_container,
            fg_color=COLORS["background"],
            corner_radius=0,
        )
        page.grid(row=0, column=0, sticky="nsew", padx=24, pady=20)
        self.pages[name] = page
        return page

    def create_case_page(self):
        page = self.create_page("case")
        page.grid_columnconfigure(0, weight=1)
        page.grid_rowconfigure(1, weight=1)

        metrics_frame = ctk.CTkFrame(page, fg_color="transparent")
        metrics_frame.grid(row=0, column=0, sticky="ew", pady=(0, 14))

        for column in range(4):
            metrics_frame.grid_columnconfigure(column, weight=1)

        self.case_metric = self.create_metric_card(
            metrics_frame, 0, "CASE", "--"
        )
        self.window_metric = self.create_metric_card(
            metrics_frame, 1, "EVENT WINDOW", "--"
        )
        self.event_metric = self.create_metric_card(
            metrics_frame, 2, "EVENTS", "--"
        )
        self.risk_metric = self.create_metric_card(
            metrics_frame, 3, "SUSPICIOUS", "--"
        )

        timeline_panel = ctk.CTkFrame(
            page,
            fg_color=COLORS["panel"],
            corner_radius=12,
        )
        timeline_panel.grid(row=1, column=0, sticky="nsew")
        timeline_panel.grid_columnconfigure(0, weight=1)
        timeline_panel.grid_rowconfigure(1, weight=1)

        top = ctk.CTkFrame(timeline_panel, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", padx=18, pady=(14, 7))

        ctk.CTkLabel(
            top,
            text="Event Timeline",
            font=("Segoe UI", 17, "bold"),
        ).pack(side="left")

        ctk.CTkLabel(
            top,
            text="Chronological case telemetry",
            font=("Segoe UI", 12),
            text_color=COLORS["muted"],
        ).pack(side="right")

        self.timeline_scroll = ctk.CTkScrollableFrame(
            timeline_panel,
            fg_color="transparent",
            corner_radius=0,
        )
        self.timeline_scroll.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(0, 10),
        )

        self.show_timeline_empty_state()

    def create_metric_card(self, parent, column, title, value):
        card = ctk.CTkFrame(
            parent,
            fg_color=COLORS["panel"],
            corner_radius=10,
        )
        card.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=(0 if column == 0 else 5, 0 if column == 3 else 5),
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 10, "bold"),
            text_color=COLORS["muted"],
        ).pack(anchor="w", padx=14, pady=(10, 0))

        label = ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI", 16, "bold"),
        )
        label.pack(anchor="w", padx=14, pady=(0, 10))
        return label

    def create_investigation_page(self):
        page = self.create_page("investigation")

        self.investigation_scroll = ctk.CTkScrollableFrame(
            page,
            fg_color=COLORS["panel"],
            corner_radius=12,
        )
        self.investigation_scroll.pack(fill="both", expand=True)

        self.show_investigation_empty_state()

    def create_analytics_page(self):
        page = self.create_page("analytics")

        self.analytics_frame = ctk.CTkFrame(
            page,
            fg_color=COLORS["panel"],
            corner_radius=12,
        )
        self.analytics_frame.pack(fill="both", expand=True)

        self.show_analytics_empty_state()

    def show_page(self, page_name):
        titles = {
            "case": (
                "Case Timeline",
                "Review compact chronological telemetry before analysis.",
            ),
            "investigation": (
                "Investigation",
                "Review classification, evidence, indicators, and response actions.",
            ),
            "analytics": (
                "Case Analytics",
                "Understand the risk profile and telemetry coverage for this case.",
            ),
        }

        self.pages[page_name].tkraise()

        title, subtitle = titles[page_name]
        self.page_title.configure(text=title)
        self.page_subtitle.configure(text=subtitle)

        for name, button in self.nav_buttons.items():
            if name == page_name:
                button.configure(
                    fg_color="#1d4ed8",
                    text_color="#ffffff",
                )
            else:
                button.configure(
                    fg_color="transparent",
                    text_color=COLORS["muted"],
                )

    def clear_children(self, widget):
        for child in widget.winfo_children():
            child.destroy()

    def set_status(self, text, color):
        self.sidebar_status.configure(text=text, fg_color=color)
        self.header_status.configure(text=text, fg_color=color)

    def set_controls_enabled(self, enabled):
        state = "normal" if enabled else "disabled"
        self.generate_button.configure(state=state)
        self.analyze_button.configure(state=state)
        self.clear_button.configure(state=state)

    def show_timeline_empty_state(self):
        self.clear_children(self.timeline_scroll)

        ctk.CTkLabel(
            self.timeline_scroll,
            text="No case loaded",
            font=("Segoe UI", 17, "bold"),
            text_color=COLORS["muted"],
        ).pack(pady=(120, 5))

        ctk.CTkLabel(
            self.timeline_scroll,
            text="Generate a simulated incident to populate the event timeline.",
            font=("Segoe UI", 13),
            text_color=COLORS["muted"],
        ).pack()

    def show_investigation_empty_state(self):
        self.clear_children(self.investigation_scroll)

        ctk.CTkLabel(
            self.investigation_scroll,
            text="No investigation report available",
            font=("Segoe UI", 17, "bold"),
            text_color=COLORS["muted"],
        ).pack(pady=(120, 5))

        ctk.CTkLabel(
            self.investigation_scroll,
            text="Generate and analyze a case to view evidence and indicators.",
            font=("Segoe UI", 13),
            text_color=COLORS["muted"],
        ).pack()

    def show_analytics_empty_state(self):
        self.clear_children(self.analytics_frame)

        ctk.CTkLabel(
            self.analytics_frame,
            text="No analytics available",
            font=("Segoe UI", 17, "bold"),
            text_color=COLORS["muted"],
        ).pack(expand=True)

    def generate_case(self):
        self.animation_token += 1
        token = self.animation_token

        self.current_incident = self.generator.generate()
        self.current_result = None
        self.threat_intel_result = None
        self.timeline_index = 0

        self.show_investigation_empty_state()
        self.show_analytics_empty_state()

        self.case_metric.configure(
            text=f"#{self.current_incident.case_id:04d}"
        )
        self.window_metric.configure(text="Loading")
        self.event_metric.configure(
            text=str(len(self.current_incident.logs))
        )
        self.risk_metric.configure(text="Assessing")

        self.sidebar_case_label.configure(
            text=(
                f"Case #{self.current_incident.case_id:04d}\n"
                f"{self.current_incident.created_at}"
            )
        )

        self.set_status("LOADING", COLORS["accent"])
        self.set_controls_enabled(False)
        self.show_page("case")

        self.clear_children(self.timeline_scroll)

        ctk.CTkLabel(
            self.timeline_scroll,
            text="Timeline loading...",
            font=("Segoe UI", 12),
            text_color=COLORS["muted"],
        ).pack(anchor="w", padx=10, pady=(7, 4))

        self.after(100, lambda: self.animate_next_event(token))

    def animate_next_event(self, token):
        if token != self.animation_token or self.current_incident is None:
            return

        if self.timeline_index < len(self.current_incident.logs):
            log = self.current_incident.logs[self.timeline_index]
            self.add_timeline_row(log)
            self.timeline_index += 1
            self.after(95, lambda: self.animate_next_event(token))
            return

        logs = self.current_incident.logs

        if logs:
            self.window_metric.configure(
                text=f"{logs[0].timestamp} - {logs[-1].timestamp}"
            )

        self.risk_metric.configure(text="Ready")
        self.set_status("CASE READY", COLORS["warning"])
        self.set_controls_enabled(True)

    def add_timeline_row(self, log):
        color = LEVEL_COLORS.get(log.level, COLORS["muted"])

        row = ctk.CTkFrame(
            self.timeline_scroll,
            height=52,
            fg_color=COLORS["card"],
            corner_radius=7,
        )
        row.pack(fill="x", padx=4, pady=3)
        row.pack_propagate(False)

        ctk.CTkFrame(
            row,
            width=4,
            fg_color=color,
            corner_radius=3,
        ).pack(side="left", fill="y", padx=(0, 10))

        ctk.CTkLabel(
            row,
            text=log.timestamp,
            width=72,
            anchor="w",
            font=("Consolas", 11, "bold"),
            text_color=COLORS["muted"],
        ).pack(side="left")

        ctk.CTkLabel(
            row,
            text=log.source,
            width=155,
            anchor="w",
            font=("Segoe UI", 11, "bold"),
            text_color=COLORS["accent"],
        ).pack(side="left", padx=(4, 10))

        ctk.CTkLabel(
            row,
            text=log.level.upper(),
            width=88,
            font=("Segoe UI", 9, "bold"),
            text_color="#081018",
            fg_color=color,
            corner_radius=5,
        ).pack(side="left", padx=(0, 12))

        ctk.CTkLabel(
            row,
            text=log.message,
            anchor="w",
            justify="left",
            font=("Segoe UI", 12),
        ).pack(side="left", fill="x", expand=True, padx=(0, 12))

    def start_analysis(self):
        if self.current_incident is None:
            self.show_page("case")
            return

        self.animation_token += 1
        token = self.animation_token
        self.analysis_index = 0

        self.show_page("investigation")
        self.clear_children(self.investigation_scroll)

        self.set_status("ANALYZING", COLORS["accent"])
        self.set_controls_enabled(False)

        ctk.CTkLabel(
            self.investigation_scroll,
            text="SentLens Investigation Engine",
            font=("Segoe UI", 20, "bold"),
        ).pack(anchor="w", padx=22, pady=(24, 10))

        self.analysis_box = ctk.CTkFrame(
            self.investigation_scroll,
            fg_color=COLORS["card"],
            corner_radius=10,
        )
        self.analysis_box.pack(fill="x", padx=22, pady=(0, 16))

        self.analysis_steps = [
            "Reviewing event timeline",
            "Extracting indicators of compromise",
            "Testing attack-pattern rules",
            "Scoring candidate classifications",
            "Preparing response actions",
        ]

        self.after(200, lambda: self.animate_analysis(token))

    def animate_analysis(self, token):
        if token != self.animation_token:
            return

        if self.analysis_index < len(self.analysis_steps):
            ctk.CTkLabel(
                self.analysis_box,
                text=f"Completed: {self.analysis_steps[self.analysis_index]}",
                font=("Segoe UI", 12),
                text_color=COLORS["accent"],
            ).pack(anchor="w", padx=15, pady=6)

            self.analysis_index += 1
            self.after(270, lambda: self.animate_analysis(token))
            return

        self.current_result = analyze_incident(self.current_incident)
        self.render_investigation()
        self.render_analytics()

        metrics = self.current_result["metrics"]
        self.risk_metric.configure(
            text=(
                f"{metrics['suspicious_events']}/"
                f"{metrics['total_events']}"
            )
        )

        severity = self.current_result["severity"]
        self.set_status(
            f"{severity.upper()} CASE",
            SEVERITY_COLORS.get(
                severity,
                SEVERITY_COLORS["Unassessed"],
            ),
        )

        self.set_controls_enabled(True)

    def section_label(self, parent, text):
        ctk.CTkLabel(
            parent,
            text=text.upper(),
            font=("Segoe UI", 10, "bold"),
            text_color=COLORS["muted"],
        ).pack(anchor="w", padx=20, pady=(18, 7))

    def render_investigation(self):
        self.clear_children(self.investigation_scroll)

        result = self.current_result
        metrics = result["metrics"]
        indicators = result["indicators"]
        severity = result["severity"]

        summary = ctk.CTkFrame(
            self.investigation_scroll,
            fg_color=COLORS["card"],
            corner_radius=10,
        )
        summary.pack(fill="x", padx=16, pady=(16, 0))
        summary.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            summary,
            text="LIKELY CLASSIFICATION",
            font=("Segoe UI", 10, "bold"),
            text_color=COLORS["muted"],
        ).grid(row=0, column=0, sticky="w", padx=18, pady=(15, 0))

        ctk.CTkLabel(
            summary,
            text=result["attack"],
            font=("Segoe UI", 22, "bold"),
        ).grid(row=1, column=0, sticky="w", padx=18, pady=(0, 15))

        ctk.CTkLabel(
            summary,
            text=severity.upper(),
            font=("Segoe UI", 10, "bold"),
            fg_color=SEVERITY_COLORS.get(
                severity,
                SEVERITY_COLORS["Unassessed"],
            ),
            corner_radius=6,
            padx=10,
            pady=5,
        ).grid(row=0, column=1, sticky="e", padx=18, pady=(15, 0))

        confidence_panel = ctk.CTkFrame(
            summary,
            fg_color="transparent",
        )
        confidence_panel.grid(
            row=1,
            column=1,
            sticky="e",
            padx=18,
            pady=(0, 15),
        )

        self.confidence_value_label = ctk.CTkLabel(
            confidence_panel,
            text="0% confidence",
            font=("Segoe UI", 13, "bold"),
            text_color=COLORS["accent"],
        )
        self.confidence_value_label.pack(anchor="e")

        self.confidence_progress = ctk.CTkProgressBar(
            confidence_panel,
            width=180,
            height=10,
            progress_color=COLORS["accent"],
        )
        self.confidence_progress.pack(anchor="e", pady=(5, 0))
        self.confidence_progress.set(0)

        confidence_token = self.animation_token

        self.after(
            150,
            lambda: self.animate_confidence(
                0,
                result["confidence"],
                confidence_token,
            ),
        )

        metrics_row = ctk.CTkFrame(
            self.investigation_scroll,
            fg_color="transparent",
        )
        metrics_row.pack(fill="x", padx=16, pady=(10, 0))

        for column in range(4):
            metrics_row.grid_columnconfigure(column, weight=1)

        self.add_small_metric(
            metrics_row,
            0,
            "EVENT WINDOW",
            f"{metrics['first_timestamp']} - {metrics['last_timestamp']}",
        )
        self.add_small_metric(
            metrics_row,
            1,
            "SUSPICIOUS EVENTS",
            str(metrics["suspicious_events"]),
        )
        self.add_small_metric(
            metrics_row,
            2,
            "CRITICAL EVENTS",
            str(metrics["critical_events"]),
        )
        self.add_small_metric(
            metrics_row,
            3,
            "LOG SOURCES",
            str(metrics["source_count"]),
        )

        self.section_label(self.investigation_scroll, "Observed Indicators")

        indicator_frame = ctk.CTkFrame(
            self.investigation_scroll,
            fg_color=COLORS["card"],
            corner_radius=10,
        )
        indicator_frame.pack(fill="x", padx=16)

        self.add_indicator_group(
            indicator_frame,
            "IP Addresses",
            indicators["ips"],
        )
        self.add_indicator_group(
            indicator_frame,
            "Users / Accounts",
            indicators["users"],
        )
        self.add_indicator_group(
            indicator_frame,
            "Ports",
            indicators["ports"],
        )
        self.add_indicator_group(
            indicator_frame,
            "Domains",
            indicators["domains"],
        )
        self.add_indicator_group(
            indicator_frame,
            "Files",
            indicators["files"],
        )

        self.section_label(self.investigation_scroll, "Threat Intelligence")

        ti_card = ctk.CTkFrame(
            self.investigation_scroll,
            fg_color=COLORS["card"],
            corner_radius=10,
        )
        ti_card.pack(fill="x", padx=16)

        ips = indicators["ips"]

        self.ti_target_label = ctk.CTkLabel(
            ti_card,
            text=(
                f"Target indicator: {ips[0]}"
                if ips
                else "No IP indicator found in this case."
            ),
            font=("Consolas", 11),
            text_color=COLORS["muted"],
        )
        self.ti_target_label.pack(anchor="w", padx=14, pady=(12, 4))

        self.ti_result_label = ctk.CTkLabel(
            ti_card,
            text=(
                "Request a live AbuseIPDB reputation check."
                if ips
                else "Threat-intelligence lookup is unavailable for this case."
            ),
            font=("Segoe UI", 12),
            justify="left",
            wraplength=700,
        )
        self.ti_result_label.pack(anchor="w", padx=14, pady=(0, 8))

        self.ti_lookup_button = ctk.CTkButton(
            ti_card,
            text="Enrich IP Reputation",
            width=180,
            height=32,
            fg_color="#0369a1",
            hover_color="#075985",
            state="normal" if ips else "disabled",
            command=self.start_ip_enrichment,
        )
        self.ti_lookup_button.pack(anchor="w", padx=14, pady=(0, 12))

        self.section_label(self.investigation_scroll, "Detection Evidence")

        for index, evidence in enumerate(result["evidence"], start=1):
            row = ctk.CTkFrame(
                self.investigation_scroll,
                fg_color=COLORS["card"],
                corner_radius=8,
            )
            row.pack(fill="x", padx=16, pady=3)

            ctk.CTkLabel(
                row,
                text=str(index),
                width=25,
                height=25,
                fg_color=COLORS["accent"],
                text_color="#081018",
                font=("Segoe UI", 11, "bold"),
                corner_radius=13,
            ).pack(side="left", padx=12, pady=9)

            ctk.CTkLabel(
                row,
                text=evidence,
                anchor="w",
                justify="left",
                font=("Segoe UI", 12),
            ).pack(side="left", fill="x", expand=True, padx=(0, 12), pady=9)

        self.section_label(self.investigation_scroll, "MITRE ATT&CK")

        mitre = ctk.CTkFrame(
            self.investigation_scroll,
            fg_color=COLORS["card"],
            corner_radius=8,
        )
        mitre.pack(fill="x", padx=16)

        ctk.CTkLabel(
            mitre,
            text=f"{result['mitre']['id']}  |  {result['mitre']['name']}",
            font=("Consolas", 13, "bold"),
            text_color=COLORS["accent"],
        ).pack(anchor="w", padx=14, pady=(11, 2))

        ctk.CTkLabel(
            mitre,
            text=result["mitre"]["description"],
            font=("Segoe UI", 12),
            justify="left",
            wraplength=700,
            text_color=COLORS["muted"],
        ).pack(anchor="w", padx=14, pady=(0, 11))

        self.section_label(self.investigation_scroll, "Recommended Response")

        for action in get_recommendations(result["attack"]):
            ctk.CTkLabel(
                self.investigation_scroll,
                text=action,
                anchor="w",
                font=("Segoe UI", 12),
                text_color="#d1fae5",
                fg_color="#173020",
                corner_radius=7,
                padx=13,
                pady=8,
            ).pack(fill="x", padx=16, pady=3)
        
        self.section_label(
            self.investigation_scroll,
            "Containment Playbook",
        )

        self.playbook_status = ctk.CTkLabel(
            self.investigation_scroll,
            text=(
                "Simulation only. No real accounts, systems, "
                "or network rules will be changed."
            ),
            font=("Segoe UI", 12),
            text_color=COLORS["muted"],
            justify="left",
        )
        self.playbook_status.pack(
            anchor="w",
            padx=16,
            pady=(0, 8),
        )

        self.playbook_button = ctk.CTkButton(
            self.investigation_scroll,
            text="Execute Simulated Playbook",
            height=34,
            fg_color="#7c3aed",
            hover_color="#6d28d9",
            command=self.start_playbook,
        )
        self.playbook_button.pack(
            anchor="w",
            padx=16,
            pady=(0, 20),
        )

    def add_small_metric(self, parent, column, title, value):
        card = ctk.CTkFrame(
            parent,
            fg_color=COLORS["card"],
            corner_radius=8,
        )
        card.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=(0 if column == 0 else 4, 0 if column == 3 else 4),
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 9, "bold"),
            text_color=COLORS["muted"],
        ).pack(anchor="w", padx=10, pady=(8, 0))

        ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", padx=10, pady=(0, 8))

    def add_indicator_group(self, parent, label, values):
        if not values:
            return

        ctk.CTkLabel(
            parent,
            text=label,
            font=("Segoe UI", 10, "bold"),
            text_color=COLORS["muted"],
        ).pack(anchor="w", padx=14, pady=(10, 2))

        ctk.CTkLabel(
            parent,
            text="   ".join(values[:6]),
            anchor="w",
            justify="left",
            font=("Consolas", 11),
            text_color="#bae6fd",
            wraplength=700,
        ).pack(anchor="w", padx=14, pady=(0, 4))

    def start_ip_enrichment(self):
        if self.current_result is None:
            return

        ips = self.current_result["indicators"]["ips"]

        if not ips:
            self.ti_result_label.configure(
                text="No IP indicator is available for enrichment."
            )
            return

        target_ip = ips[0]

        self.ti_lookup_button.configure(
            text="Checking AbuseIPDB...",
            state="disabled",
        )

        threading.Thread(
            target=self.lookup_ip_in_background,
            args=(target_ip,),
            daemon=True,
        ).start()

    def lookup_ip_in_background(self, target_ip):
        result = lookup_ip_reputation(target_ip)

        self.after(
            0,
            lambda: self.display_ip_reputation(result),
        )

    def display_ip_reputation(self, result):
        if not hasattr(self, "ti_result_label"):
            return

        try:
            if not self.ti_result_label.winfo_exists():
                return

            self.threat_intel_result = result

            if not result["available"]:
                self.ti_result_label.configure(
                    text=result["message"],
                    text_color=COLORS["warning"],
                )
                self.ti_lookup_button.configure(
                    text="Try Again",
                    state="normal",
                )
                return

            score = result["abuse_confidence_score"]
            reports = result["total_reports"]

            if score >= 75:
                risk_text = "High-risk reputation"
                risk_color = COLORS["critical"]
            elif score >= 25:
                risk_text = "Elevated reputation risk"
                risk_color = COLORS["high"]
            else:
                risk_text = "No elevated abuse confidence"
                risk_color = COLORS["success"]

            self.ti_result_label.configure(
                text=(
                    f"{risk_text}: {score}% abuse confidence | "
                    f"{reports} historical reports | "
                    f"ISP: {result['isp']} | "
                    f"Country: {result['country_code']}"
                ),
                text_color=risk_color,
            )

            self.ti_lookup_button.configure(
                text="Recheck Reputation",
                state="normal",
            )

        except Exception:
            return
    def start_playbook(self):
        if self.current_result is None:
            return

        self.playbook_button.configure(
            text="Executing simulation...",
            state="disabled",
        )
        self.playbook_status.configure(
            text="Simulating containment actions...",
            text_color=COLORS["warning"],
        )

        self.after(650, self.complete_playbook)

    def complete_playbook(self):
        playbook = execute_playbook(self.current_result)

        actions = "\n".join(
            f"Completed: {action}"
            for action in playbook["actions"]
        )
        self.playbook_status.configure(
            text=(
                f"{playbook['mode']}\n\n"
                f"{actions}"
            ),
            text_color=COLORS["success"],
        )
        self.playbook_button.configure(
            text="Playbook Complete",
            state="disabled",
        )

    def render_analytics(self):
        self.clear_children(self.analytics_frame)

        result = self.current_result
        metrics = result["metrics"]

        ctk.CTkLabel(
            self.analytics_frame,
            text="Case Telemetry Summary",
            font=("Segoe UI", 19, "bold"),
        ).pack(anchor="w", padx=20, pady=(17, 0))

        ctk.CTkLabel(
            self.analytics_frame,
            text=(
                "These charts describe this simulated case: how much activity "
                "was flagged as suspicious and which systems produced evidence."
            ),
            font=("Segoe UI", 12),
            text_color=COLORS["muted"],
            justify="left",
        ).pack(anchor="w", padx=20, pady=(0, 5))

        meaning = ctk.CTkFrame(
            self.analytics_frame,
            fg_color=COLORS["card"],
            corner_radius=8,
        )
        meaning.pack(fill="x", padx=20, pady=(8, 8))

        ctk.CTkLabel(
            meaning,
            text=(
                f"Risk profile: {metrics['suspicious_events']} of "
                f"{metrics['total_events']} events matched suspicious-behavior "
                f"rules. This supports the {result['attack']} classification."
            ),
            font=("Segoe UI", 12),
            justify="left",
            wraplength=850,
        ).pack(anchor="w", padx=13, pady=10)

        source_counts = metrics["source_counts"]
        normal_events = metrics["normal_events"]
        suspicious_events = metrics["suspicious_events"]

        figure = Figure(
            figsize=(10, 4.2),
            dpi=100,
            facecolor=COLORS["panel"],
        )

        risk_axis = figure.add_subplot(121)
        source_axis = figure.add_subplot(122)

        risk_axis.pie(
            [normal_events, suspicious_events],
            labels=["Normal", "Suspicious"],
            autopct="%1.0f%%",
            colors=[COLORS["accent"], COLORS["critical"]],
            startangle=90,
            textprops={"color": COLORS["text"]},
        )
        risk_axis.set_title(
            "Event Risk Profile",
            color=COLORS["text"],
            pad=14,
        )
        risk_axis.set_facecolor(COLORS["panel"])

        sources = list(source_counts.keys())
        values = list(source_counts.values())

        source_axis.bar(
            range(len(sources)),
            values,
            color=COLORS["accent"],
        )
        source_axis.set_title(
            "Evidence by Log Source",
            color=COLORS["text"],
            pad=14,
        )
        source_axis.set_facecolor(COLORS["panel"])
        source_axis.set_xticks(range(len(sources)))
        source_axis.set_xticklabels(
            sources,
            rotation=28,
            ha="right",
            fontsize=8,
            color=COLORS["muted"],
        )
        source_axis.tick_params(axis="y", colors=COLORS["muted"])
        source_axis.spines["top"].set_visible(False)
        source_axis.spines["right"].set_visible(False)
        source_axis.spines["left"].set_color(COLORS["border"])
        source_axis.spines["bottom"].set_color(COLORS["border"])

        figure.tight_layout(pad=2.5)

        self.chart_canvas = FigureCanvasTkAgg(
            figure,
            master=self.analytics_frame,
        )
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 12),
        )
    def animate_confidence(self, current, target, token):
        if token != self.animation_token:
            return

        try:
            if not self.confidence_progress.winfo_exists():
                return

            if current >= target:
                self.confidence_progress.set(target / 100)
                self.confidence_value_label.configure(
                    text=f"{target}% confidence"
                )
                return

            step = max(1, (target - current) // 18)
            current = min(target, current + step)

            self.confidence_progress.set(current / 100)
            self.confidence_value_label.configure(
                text=f"{current}% confidence"
            )

            self.after(
                30,
                lambda: self.animate_confidence(
                    current,
                    target,
                    token,
                ),
            )

        except Exception:
            return

    def clear_case(self):
        self.animation_token += 1

        self.current_incident = None
        self.current_result = None
        self.threat_intel_result = None
        self.timeline_index = 0

        self.case_metric.configure(text="--")
        self.window_metric.configure(text="--")
        self.event_metric.configure(text="--")
        self.risk_metric.configure(text="--")

        self.sidebar_case_label.configure(text="No case loaded")
        self.set_status("READY", COLORS["unassessed"])
        self.set_controls_enabled(True)

        self.show_timeline_empty_state()
        self.show_investigation_empty_state()
        self.show_analytics_empty_state()
        self.show_page("case")