#!/usr/bin/env python3

import os
import datetime

# Konfiguration
LOGFILE = "/var/log/serancon/crontab.log"  # Logdatei mit den Cronjob-Ausführungen
CRONTAB_FILE = "/var/spool/cron/crontabs/root"  # Benutzer-Crontab
TIME_RANGE_MINUTES = 1  # Zeitspanne für die Prüfung (in Minuten)
BASE_SERVICE_NAME = "Cronjob Overview"  # Hauptservice für die Gesamtbewertung

# Präfix-Steuerung
PREFIX_ENABLED = 1  # 1 = "Serancon: " wird vorangestellt, 0 = deaktiviert

# Setze den Servicenamen mit optionalem Präfix
SERVICE_NAME = f"Serancon: {BASE_SERVICE_NAME}" if PREFIX_ENABLED else BASE_SERVICE_NAME

# Prüfen, ob die Logdatei existiert
if not os.path.exists(LOGFILE):
    print(f'2 "{SERVICE_NAME.replace(" ", "_")}" - CRITICAL: Logdatei nicht gefunden!')
    exit(2)

# Prüfen, ob die Crontab-Datei existiert
if not os.path.exists(CRONTAB_FILE):
    print(f'2 "{SERVICE_NAME.replace(" ", "_")}" - CRITICAL: Crontab-Datei nicht gefunden!')
    exit(2)

# Zeitpunkt für die Zeitspanne berechnen
time_threshold = datetime.datetime.now() - datetime.timedelta(minutes=TIME_RANGE_MINUTES)

# Liste der aktuellen Cronjob-Namen aus der Crontab-Datei holen
current_cronjobs = {}
with open(CRONTAB_FILE, "r") as file:
    lines = file.readlines()
    for i in range(len(lines) - 1):
        if lines[i].strip().startswith('###'):
            job_name = lines[i].strip().split('###')[1].strip().replace(" ", "_")
            cron_command = lines[i + 1].strip()
            current_cronjobs[job_name] = cron_command

# Daten aus der Logdatei lesen
logged_cron_jobs = {}
with open(LOGFILE, "r") as file:
    for line in file:
        parts = line.strip().split(" | ")
        if len(parts) < 3:
            continue  # Ungültige Zeile, ignorieren

        timestamp_str, log_name, status = parts
        log_name = log_name.strip()

        try:
            timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue  # Falls das Datumsformat nicht stimmt, Zeile ignorieren

        # Nur Jobs übernehmen, die auch in der Crontab stehen
        for crontab_name in current_cronjobs.keys():
            if crontab_name in log_name:
                logged_cron_jobs[crontab_name] = timestamp

# Prüfen, welche Jobs innerhalb des Zeitfensters gelaufen sind
ok_jobs = []
crit_jobs = []
job_statuses = []

for job in current_cronjobs.keys():
    base_job_name = f'Cronjob {job.replace("_", " ")}'
    job_var_safe = f'"Serancon: {base_job_name}"' if PREFIX_ENABLED else f'"{base_job_name}"'

    if job in logged_cron_jobs:
        last_run = logged_cron_jobs[job]
        if last_run >= time_threshold:
            ok_jobs.append(job)
            job_statuses.append(f'0 {job_var_safe} - OK')
        else:
            crit_jobs.append(job)
            job_statuses.append(f'2 {job_var_safe} - CRITICAL: Job wurde zuletzt um {last_run.strftime("%Y-%m-%d %H:%M:%S")} ausgeführt, älter als {TIME_RANGE_MINUTES} Minuten!')
    else:
        crit_jobs.append(job)
        job_statuses.append(f'2 {job_var_safe} - CRITICAL: Job wurde nicht innerhalb der letzten {TIME_RANGE_MINUTES} Minuten ausgeführt!')

# Hauptservice-Ausgabe für CheckMK
overall_status = 0 if not crit_jobs else 2
status_text = "OK" if overall_status == 0 else "CRITICAL"

# Ausgabe für den Gesamtstatus
print(f'{overall_status} "{SERVICE_NAME}" - {status_text}: {len(ok_jobs)} Jobs OK, {len(crit_jobs)} kritisch')

# Einzelne Cronjobs als eigene Services in CheckMK ausgeben
for status in job_statuses:
    print(status)

exit(overall_status)
