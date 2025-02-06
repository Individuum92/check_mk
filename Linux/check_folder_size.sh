#!/bin/bash

# Ordnerpfad anpassen
FOLDER="/path/"

# Toggle fuer Prefix
PREFIX_ENABLED=1  # 1 = Prefix "Serancon: " aktiviert, 0 = Prefix deaktiviert

# Berechne die Groesse des Ordners in GB (2 Nachkommastellen)
SIZE_GB=$(du -s "$FOLDER" | awk '{printf "%.2f", $1 / 1024 / 1024}')

# Status immer 0 (OK), da keine Warnungen/Kritischen Werte benoetigt werden
STATUS=0
BASE_SERVICE_NAME="Folder Size of $FOLDER"

# Prefix-Logik
if [ "$PREFIX_ENABLED" -eq 1 ]; then
    SERVICE_NAME="Serancon: $BASE_SERVICE_NAME"
else
    SERVICE_NAME="$BASE_SERVICE_NAME"
fi

# Ausgabe im CheckMK-Format
echo "$STATUS \"$SERVICE_NAME\" size=$SIZE_GB Folder size: $SIZE_GB GB"
