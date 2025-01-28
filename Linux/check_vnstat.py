#!/usr/bin/env python3
import subprocess
import json
import sys
import os

# Netzwerkschnittstelle anpassen (z. B. eth0, wlan0)
INTERFACE = "wlan0"  # Falls eth0 nicht genutzt wird, kann dies geändert werden
LOG_FILE = "/var/log/serancon/vnstat.log"

# Präfix-Steuerung
PREFIX_ENABLED = 1  # 1 = "Serancon: " wird vorangestellt, 0 = deaktiviert
BASE_SERVICE_NAME = "VNStat Traffic"
SERVICE_NAME = f"Serancon: {BASE_SERVICE_NAME}" if PREFIX_ENABLED else BASE_SERVICE_NAME

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

# Fehlerprotokollierung
def log_error(message):
    with open(LOG_FILE, "a") as log:
        log.write(f"[ERROR] {message}\n")

# Log schreiben
def log_info(message):
    with open(LOG_FILE, "a") as log:
        log.write(f"[INFO] {message}\n")

# Daten auswerten
def parse_vnstat(data, interface):
    try:
        traffic = data["interfaces"][0]["traffic"]["hour"]
        if not traffic:
            raise ValueError("No hourly traffic data available")

        latest_entry = traffic[-1]  # Letzter Stunden-Eintrag
        rx = round(latest_entry["rx"] / (1024 ** 2), 2)  # Empfangene Daten in GB
        tx = round(latest_entry["tx"] / (1024 ** 2), 2)  # Gesendete Daten in GB
        total = round(rx + tx, 2)  # Gesamttraffic in GB

        output = (f"0 \"{SERVICE_NAME}\" IN={rx:.2f}GB|OUT={tx:.2f}GB|TOTAL={total:.2f}GB")
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
    parse_vnstat(data, INTERFACE)

if __name__ == "__main__":
    main()
