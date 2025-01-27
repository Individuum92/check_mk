#!/usr/bin/env python3
import socket

# Konfiguration
MAILSERVER_IP = "194.48.217.75"
BASE_SERVICE_NAME = "Blacklist Check"  # Basis-Servicename für CheckMK

# Präfix-Steuerung
PREFIX_ENABLED = 1  # 1 = "Serancon: " wird vorangestellt, 0 = deaktiviert

# Setze den Servicenamen mit optionalem Präfix
SERVICE_NAME = f"Serancon: {BASE_SERVICE_NAME}" if PREFIX_ENABLED else BASE_SERVICE_NAME

BLACKLISTS = [
    "b.barracudacentral.org",
    "bl.spamcop.net",
    "dnsbl.sorbs.net",
    "ubl.unsubscore.com",
    "psbl.surriel.com",
]

def check_blacklist(ip):
    reversed_ip = ".".join(reversed(ip.split(".")))  # IP für DNSBL-Abfrage umkehren
    blacklisted = []

    for blacklist in BLACKLISTS:
        query = f"{reversed_ip}.{blacklist}"
        try:
            socket.gethostbyname(query)
            blacklisted.append(blacklist)
        except socket.gaierror:
            pass  # Kein Eintrag → nicht auf der Blacklist

    return blacklisted

# Prüfung ausführen
blacklisted_on = check_blacklist(MAILSERVER_IP)

# Status und CheckMK-konforme Ausgabe
if blacklisted_on:
    STATUS = 2  # CRITICAL
    MESSAGE = f"Mailserver {MAILSERVER_IP} steht auf {len(blacklisted_on)} Blacklists: {', '.join(blacklisted_on)}"
else:
    STATUS = 0  # OK
    MESSAGE = f"Mailserver {MAILSERVER_IP} steht auf keiner Blacklist"

# CheckMK-Ausgabe im korrekten Format
print(f'{STATUS} "{SERVICE_NAME}" - {MESSAGE}')
