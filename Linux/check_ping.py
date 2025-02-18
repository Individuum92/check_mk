#!/usr/bin/env python3
import subprocess
import re

# Präfix-Steuerung
PREFIX_ENABLED = 1  # 1 = "Serancon: " wird vorangestellt, 0 = deaktiviert

# Zielhost für den Ping
TARGET = "8.8.8.8"

# Schwellwerte für WARN und CRIT (in ms)
WARN_THRESHOLD = 100
CRIT_THRESHOLD = 200

def ping_host(target):
    """
    Führt einen Ping auf den angegebenen Host aus und gibt die Antwortzeit in ms zurück.
    Falls keine Antwort kommt, wird None zurückgegeben.
    """
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-w", "2", target],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        match = re.search(r"time=([\d.]+) ms", result.stdout)
        return float(match.group(1)) if match else None
    except Exception:
        return None

# CheckMK erwartet eine Kopfzeile für Local Checks
print("<<<local>>>")

# Ping ausführen
ping_time = ping_host(TARGET)

# Servicenamen mit optionalem Präfix setzen
base_service_name = f"Ping {TARGET}"
service_name = f"Serancon: {base_service_name}" if PREFIX_ENABLED else base_service_name

# CheckMK-Ausgabe je nach Ping-Ergebnis
if ping_time is None:
    print(f'2 "{service_name}" - CRITICAL - No response from {TARGET}')
else:
    if ping_time > CRIT_THRESHOLD:
        print(f'2 "{service_name}" ping_time={ping_time}ms CRITICAL - {ping_time} ms response time')
    elif ping_time > WARN_THRESHOLD:
        print(f'1 "{service_name}" ping_time={ping_time}ms WARNING - {ping_time} ms response time')
    else:
        print(f'0 "{service_name}" ping_time={ping_time}ms OK - {ping_time} ms response time')
