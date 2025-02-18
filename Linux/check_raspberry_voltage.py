#!/bin/bash

# CheckMK Local Check - Raspberry Pi Unterspannung überwachen (nur Graph)
# Ohne Alarmierungen, nur für die Visualisierung der Werte in CheckMK

# Toggle für Prefix
PREFIX_ENABLED=1  # 1 = Prefix aktivieren, 0 = deaktivieren

# Aktuellen Unterspannungsstatus abrufen
STATUS=$(vcgencmd get_throttled)
TIMESTAMP=$(date +"%s")

# Standardwerte für CheckMK (keine Zustände, nur Werte)
VOLTAGE=1.0  # Normalspannung = 1V (Dummy-Wert für den Graphen)

# Logik zur Bestimmung der Unterspannungsstufe (nur Werte, keine WARN/CRIT)
case "$STATUS" in
    "throttled=0x0")
        VOLTAGE=1.0  # Keine Unterspannung
        MESSAGE="Keine Unterspannung erkannt"
        ;;
    "throttled=0x50000")
        VOLTAGE=0.5  # Vergangene Unterspannung
        MESSAGE="Vergangene Unterspannung erkannt"
        ;;
    "throttled=0x50005")
        VOLTAGE=0.2  # Aktuelle Unterspannung
        MESSAGE="Aktuelle Unterspannung erkannt"
        ;;
    *)
        VOLTAGE=0.7  # Unbekannter Status
        MESSAGE="Unbekannter Status: $STATUS"
        ;;
esac

# Basis-Service-Name
BASE_SERVICE_NAME="Spannung externe SSD"

# Prefix-Logik anwenden, falls aktiviert
if [ "$PREFIX_ENABLED" -eq 1 ]; then
    SERVICE_NAME="Serancon: $BASE_SERVICE_NAME"
else
    SERVICE_NAME="$BASE_SERVICE_NAME"
fi

# CheckMK-konforme Ausgabe ohne WARN/CRIT-Schwellenwerte, nur für den Graphen
echo "0 \"$SERVICE_NAME\" voltage=$VOLTAGE V;;;0;1 $MESSAGE"
