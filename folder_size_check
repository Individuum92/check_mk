#!/bin/bash

# Ordnerpfad anpassen
FOLDER="/var/"

# Berechne die Größe des Ordners in GB (2 Nachkommastellen)
SIZE_GB=$(du -s "$FOLDER" | awk '{printf "%.2f", $1 / 1024 / 1024}')

# Status immer 0 (OK), da keine Warnungen/Kritischen Werte benötigt werden
STATUS=0
SERVICE_NAME="Folder Size of $FOLDER"

# Ausgabe im CheckMK-Format
echo "$STATUS \"$SERVICE_NAME\" size=$SIZE_GB GB - Folder size: $SIZE_GB GB"
