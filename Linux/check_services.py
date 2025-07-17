#!/usr/bin/env python3
import subprocess
import sys
import os
import datetime

# Schalter, um das Präfix für den Check-Namen zu aktivieren (1) oder zu deaktivieren (0).
PREFIX_ENABLED = 1
# Das Präfix, das verwendet wird, wenn es aktiviert ist.
PREFIX_TAG = "Serancon"

# Der Basis-Anzeigename für den Sammel-Check in Checkmk.
BASE_CHECK_NAME = "Systemd Service Check"

# Die zuüberwachendes Services
SERVICES_TO_MONITOR = {
    "ssh.service": "SSH Daemon",
    "cron.service": "Cron Scheduler",
    "apache2.service": "Apache Webserver",
    "postgresql.service": "PostgreSQL Database",
    "duftkorb.service": "Duftkorb Service",
}

# Pfad zur Log-Datei für dieses Skript
LOG_FILE = "/var/log/serancon/systemd_status.log"


def log_message(message):
    try:
        log_dir = os.path.dirname(LOG_FILE)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        with open(LOG_FILE, "a") as log:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log.write(f"[{timestamp}] --- New Check Run ---\n{message}\n")
    except IOError as e:
        print(f"CRITICAL - Log-Datei konnte nicht geschrieben werden {LOG_FILE}: {e}", file=sys.stderr)


def get_service_status(systemd_name):
    try:
        subprocess.run(
            ["systemctl", "is-active", "--quiet", systemd_name],
            check=True,
            capture_output=True,
            text=True
        )
        return (0, "Service is active and running.") # OK

    except FileNotFoundError:
        return (3, "Command 'systemctl' not found.") # UNKNOWN

    except subprocess.CalledProcessError:
        try:
            result = subprocess.run(
                ["systemctl", "show", systemd_name, "--property=ActiveState", "--property=SubState", "--value"],
                capture_output=True,
                text=True,
                check=True
            )
            states = result.stdout.strip().split('\n')
            active_state = states[0]
            sub_state = states[1]
            return (2, f"Service is not active. State: {active_state} ({sub_state})") # CRITICAL
        except (subprocess.CalledProcessError, FileNotFoundError):
            return (2, f"Service '{systemd_name}' could not be found or queried.") # CRITICAL

    except Exception as e:
        return (3, f"An unexpected error occurred: {e}") # UNKNOWN


def main():
    # Baue den finalen Check-Namen basierend auf der Konfiguration zusammen.
    if PREFIX_ENABLED:
        final_check_name = f"{PREFIX_TAG}: {BASE_CHECK_NAME}"
    else:
        final_check_name = BASE_CHECK_NAME

    if not isinstance(SERVICES_TO_MONITOR, dict) or not SERVICES_TO_MONITOR:
        msg = "CRITICAL - SERVICES_TO_MONITOR is not a valid, non-empty dictionary."
        log_message(msg)
        print(f"3 \"{final_check_name}\" - Configuration error: Please check the script.")
        sys.exit(3)

    results = []
    for systemd_name, display_name in SERVICES_TO_MONITOR.items():
        status_code, summary = get_service_status(systemd_name)
        results.append({
            'display_name': display_name,
            'status_code': status_code,
            'summary': summary
        })

    # Sortiere die Ergebnisse nach Status
    critical_services = [res for res in results if res['status_code'] == 2]
    unknown_services = [res for res in results if res['status_code'] == 3]
    ok_services = [res for res in results if res['status_code'] == 0]

    # Bestimme den Gesamtstatus (der höchste Status-Code gewinnt)
    if critical_services:
        overall_status = 2
    elif unknown_services:
        overall_status = 3
    else:
        overall_status = 0

    # Erstelle die neue, verbesserte einzeilige Zusammenfassung
    total_services = len(SERVICES_TO_MONITOR)
    ok_count = len(ok_services)

    if critical_services:
        crit_names = [res['display_name'] for res in critical_services]
        short_summary = f"{len(critical_services)} critical: {', '.join(crit_names)}. ({ok_count}/{total_services} running)"
    elif unknown_services:
        unkn_names = [res['display_name'] for res in unknown_services]
        short_summary = f"{len(unknown_services)} unknown: {', '.join(unkn_names)}. ({ok_count}/{total_services} running)"
    else:
        short_summary = f"All {total_services} services running."

    # Erstelle die sortierte Detailansicht (CRIT -> UNKN -> OK)
    detailed_lines = []
    for res in critical_services:
        detailed_lines.append(f"CRIT - {res['display_name']}: {res['summary']}")
    for res in unknown_services:
        detailed_lines.append(f"UNKN - {res['display_name']}: {res['summary']}")
    for res in ok_services:
        detailed_lines.append(f"OK   - {res['display_name']}: {res['summary']}")

    # Kombiniere die kurze Zusammenfassung mit den Details für die finale Ausgabe
    final_output = f"{overall_status} \"{final_check_name}\" - {short_summary}\n" + "\n".join(detailed_lines)

    print(final_output)
    log_message(final_output)


if __name__ == "__main__":
    main()
