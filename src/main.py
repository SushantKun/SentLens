from analyzer.analyzer import analyze_incident
from engine.generator import IncidentGenerator
from reports.report import format_incident_report


def main():
    generator = IncidentGenerator()
    incident = generator.generate()

    print("=" * 70)
    print("GENERATED INCIDENT")
    print("=" * 70)
    print(f"Attack: {incident.attack_type}")
    print(f"Severity: {incident.severity}")
    print(f"Source: {incident.source}")
    print()

    print("LOGS")
    print("-" * 70)

    for log in incident.logs:
        print(
            f"[{log.timestamp}] "
            f"[{log.level}] "
            f"[{log.source}] "
            f"{log.message}"
        )

    result = analyze_incident(incident)
    report = format_incident_report(incident, result)

    print("\n")
    print(report)


if __name__ == "__main__":
    main()