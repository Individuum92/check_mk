#!/usr/bin/env python3
import subprocess
import json
import sys
import os
import datetime

# Netzwerkschnittstelle
INTERFACE = "eth0"
LOG_FILE = "/var/log/serancon/vnstat.log"

# Präfix-Steuerung
PREFIX_ENABLED = 1
BASE_SERVICE_NAME = f"VNStat Traffic {INTERFACE}"
SERVICE_NAME = f"Serancon: {BASE_SERVICE_NAME}" if PREFIX_ENABLED else BASE_SERVICE_NAME

# Monatsnamen für bessere Lesbarkeit
MONTH_NAMES = {
    1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
    7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
}

# Fehlerprotokollierung
def log_error(message):
    with open(LOG_FILE, "a") as log:
        log.write(f"[ERROR] {message}\n")

def log_info(message):
    with open(LOG_FILE, "a") as log:
        log.write(f"[INFO] {message}\n")

# vnstat installieren und starten
def install_and_start_vnstat():
    subprocess.run(["sudo", "apt-get", "update", "-qq"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["sudo", "apt-get", "install", "-y", "vnstat"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["sudo", "systemctl", "enable", "vnstat"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["sudo", "systemctl", "start", "vnstat"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# vnstat-Daten abrufen
def get_vnstat_data(interface):
    try:
        result = subprocess.run(["vnstat", "--json", "-i", interface], capture_output=True, text=True)
        data = json.loads(result.stdout)
        return data
    except Exception as e:
        log_error(f"Error reading vnstat data: {e}")
        print(f"2 \"{SERVICE_NAME}\" - Error reading vnstat data: {e}")
        sys.exit(2)

# Umrechnung von Bytes in GiB
def convert_to_gib(value):
    return round(value / (1024**3), 2)

# Werte aus vnstat extrahieren
def parse_vnstat(data):
    try:
        traffic = data["interfaces"][0]["traffic"]
        months = traffic["month"]

        # Aktuelles Jahr und Monat bestimmen
        now = datetime.datetime.now()
        current_month_str = f"{now.year}-{now.month:02d}"
        current_month_name = MONTH_NAMES[now.month]  # Aktueller Monat als Name

        # Aktueller Monats-Traffic für die Graphen
        current_month = next((m for m in months if f"{m['date']['year']}-{m['date']['month']:02d}" == current_month_str), None)
        if not current_month:
            log_error(f"No data found for current month ({current_month_str})")
            print(f"2 \"{SERVICE_NAME}\" - No data available for {current_month_name}")
            sys.exit(2)

        in_month = convert_to_gib(current_month["rx"])
        out_month = convert_to_gib(current_month["tx"])

        # **CheckMK-konforme Ausgabe mit aktuellem Monatsnamen**
        output = f"0 \"{SERVICE_NAME}\" INCOMING={in_month:.2f}GiB|OUTGOING={out_month:.2f}GiB Incoming={in_month:.2f}GiB Outgoing={out_month:.2f}GiB"
        print(output)
        log_info(output)

    except Exception as e:
        log_error(f"Error parsing vnstat data: {e}")
        print(f"2 \"{SERVICE_NAME}\" - Error parsing vnstat data: {e}")
        sys.exit(2)

# Hauptfunktion
def main():
    if not os.path.exists(os.path.dirname(LOG_FILE)):
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    data = get_vnstat_data(INTERFACE)
    parse_vnstat(data)

if __name__ == "__main__":
    main()
