#!/usr/bin/env python3

import os
import datetime

# Konfiguration
LOGFILE = "/var/log/serancon/crontab.log"  # Logdatei mit den Cronjob-Ausfuehrungen
CRONTAB_FILE = "/var/spool/cron/crontabs/root"  # Benutzer-Crontab
TIME_RANGE_MINUTES = 1  # Zeitspanne fuer die Pruefung (in Minuten)
SERVICE_NAME = "Cronjob: cron_all_jobs"  # Hauptservice fuer die Gesamtbewertung


# Pruefen, ob die Logdatei existiert
if not os.path.exists(LOGFILE):
    print(f'2 {SERVICE_NAME.replace(" ", "_")} - CRITICAL: Logdatei nicht gefunden!')
    exit(2)

#️ Pruefen, ob die Crontab-Datei existiert
if not os.path.exists(CRONTAB_FILE):
    print(f'2 {SERVICE_NAME.replace(" ", "_")} - CRITICAL: Crontab-Datei nicht gefunden!')
    exit(2)

# Zeitpunkt fuer die Zeitspanne berechnen
time_threshold = datetime.datetime.now() - datetime.timedelta(minutes=TIME_RANGE_MINUTES)

# Liste der aktuellen Cronjob-Namen aus der Crontab-Datei holen
current_cronjobs = {}
with open(CRONTAB_FILE, "r") as file:
    lines = file.readlines()
    for i in range(len(lines) - 1):
        if lines[i].strip().startswith('###'):  # Erkennung ohne Leerzeichen-Probleme
            job_name = lines[i].strip().split('###')[1].strip().replace(" ", "_")  # Namen extrahieren & Unterstriche ersetzen
            cron_command = lines[i + 1].strip()  # Die darunterliegende Zeile als Job-Befehl
            current_cronjobs[job_name] = cron_command

# Daten aus der Logdatei lesen
logged_cron_jobs = {}
with open(LOGFILE, "r") as file:
    for line in file:
        parts = line.strip().split(" | ")
        if len(parts) < 3:
            continue  # Ungueltige Zeile, ignorieren

        timestamp_str, log_name, status = parts
        log_name = log_name.strip()  # Keine Ersetzung von Leerzeichen mehr

        try:
            timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue  # Falls das Datumsformat nicht stimmt, Zeile ignorieren

        # Nur Jobs uebernehmen, die auch in der Crontab stehen
        for crontab_name in current_cronjobs.keys():
            if crontab_name in log_name:  # Pruefen, ob der Log-Name den Crontab-Namen enthaelt
                logged_cron_jobs[crontab_name] = timestamp

# Pruefen, welche Jobs innerhalb des Zeitfensters gelaufen sind
ok_jobs = []
crit_jobs = []
job_statuses = []

for job in current_cronjobs.keys():
    job_var_safe = f'"Cronjob: {job.replace("_", " ")}"'  # Servicenamen ohne Leerzeichen

    if job in logged_cron_jobs:
        last_run = logged_cron_jobs[job]
        if last_run >= time_threshold:
            ok_jobs.append(job)
            job_statuses.append(f'0 {job_var_safe} - OK')
        else:
            crit_jobs.append(job)
            job_statuses.append(f'2 {job_var_safe} - CRITICAL: Job wurde zuletzt um {last_run.strftime("%Y-%m-%d %H:%M:%S")} ausgefuehrt, aelter als {TIME_RANGE_MINUTES} Minuten!')
    else:
        crit_jobs.append(job)
        job_statuses.append(f'2 {job_var_safe} - CRITICAL: Job wurde nicht innerhalb der letzten {TIME_RANGE_MINUTES} Minuten ausgefuehrt!')

# Hauptservice-Ausgabe fuer CheckMK
overall_status = 0 if not crit_jobs else 2
status_text = "OK" if overall_status == 0 else "CRITICAL"

# Ausgabe fuer den Gesamtstatus
print(f'{overall_status} "{SERVICE_NAME}" - {status_text}: {len(ok_jobs)} Jobs OK, {len(crit_jobs)} kritisch')

# Einzelne Cronjobs als eigene Services in CheckMK ausgeben
for status in job_statuses:
    print(status)

exit(overall_status)
