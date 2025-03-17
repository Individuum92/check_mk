#!/usr/bin/env python3
import os
import re
import sys
import shutil

# Präfix-Steuerung
PREFIX_ENABLED = 1
BASE_SERVICE_NAME = "Fail2Ban"
SERVICE_NAME = f"Serancon: {BASE_SERVICE_NAME}" if PREFIX_ENABLED else BASE_SERVICE_NAME

# Log-Dateipfad
LOG_FILE = "/var/log/fail2ban.log"
JAIL_CONF = "/etc/fail2ban/jail.conf"
JAIL_LOCAL = "/etc/fail2ban/jail.local"

# Fehlerprotokollierung
def log_error(message):
    print(f"[ERROR] {message}")

# Überprüfen, ob der Dienst aktiv ist
def check_fail2ban_service():
    status_output = os.popen("systemctl -all | grep fail2ban").read()
    return "active" in status_output and "running" in status_output

# Sicherstellen, dass jail.local existiert und konfigurieren
def configure_recidive():
    if not os.path.exists(JAIL_LOCAL):
        shutil.copy(JAIL_CONF, JAIL_LOCAL)

    with open(JAIL_LOCAL, "r", encoding="utf-8") as file:
        lines = file.readlines()

    recidive_config = [
        "[recidive]\n",
        "enabled = true\n",
        "filter = recidive\n",
        "logpath = /var/log/fail2ban.log\n",
        "bantime = 86400\n",
        "findtime = 86400\n",
        "maxretry = 3\n"
    ]

    # Überprüfen, ob die Konfiguration bereits existiert
    if "[recidive]" not in "".join(lines):
        with open(JAIL_LOCAL, "a", encoding="utf-8") as file:
            file.writelines(recidive_config)

# Log-Datei analysieren
def parse_fail2ban_log():
    if not os.path.exists(LOG_FILE):
        log_error(f"Logdatei {LOG_FILE} nicht gefunden!")
        print(f"2 \"{SERVICE_NAME}\" - FAIL: Logdatei {LOG_FILE} nicht gefunden!")
        sys.exit(2)

    with open(LOG_FILE, "r", encoding="utf-8") as file:
        log_data = file.readlines()

    found_ips = set(re.findall(r'INFO\s+\[sshd\] Found (\d+\.\d+\.\d+\.\d+)', "".join(log_data)))
    banned_ips_sshd = set(re.findall(r'NOTICE\s+\[sshd\] Ban (\d+\.\d+\.\d+\.\d+)', "".join(log_data)))
    unbanned_ips_sshd = set(re.findall(r'NOTICE\s+\[sshd\] Unban (\d+\.\d+\.\d+\.\d+)', "".join(log_data)))

    banned_ips_recidive = set(re.findall(r'NOTICE\s+\[recidive\] Ban (\d+\.\d+\.\d+\.\d+)', "".join(log_data)))
    unbanned_ips_recidive = set(re.findall(r'NOTICE\s+\[recidive\] Unban (\d+\.\d+\.\d+\.\d+)', "".join(log_data)))

    all_banned_ips = banned_ips_sshd | banned_ips_recidive
    all_unbanned_ips = unbanned_ips_sshd | unbanned_ips_recidive

    return len(found_ips), len(all_banned_ips), len(all_unbanned_ips)

# Jail.local konfigurieren, falls erforderlich
configure_recidive()

# Daten abrufen
found_count, banned_count, unbanned_count = parse_fail2ban_log()
service_status = check_fail2ban_service()

# Status setzen
status_code = 0 if service_status else 2
status_text = "OK" if service_status else "FAIL: Dienst nicht aktiv"

# CheckMK-konforme Ausgabe mit mehreren Graphen
output = (
    f"{status_code} \"{SERVICE_NAME}\" "
    f"FOUND={found_count}|BANNED={banned_count}|UNBANNED={unbanned_count} "
    f"Gefunden={found_count}, Gebannt={banned_count}, Entbannt={unbanned_count}"
)

print(output)
