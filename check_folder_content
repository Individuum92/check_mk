#!/bin/bash

# Konfiguration
FOLDER="/var/html-backup/"
TIME_TRACK_FILE="/tmp/nicht_entfernen_folder_check_time"

# Schwellenwerte in Minuten (z. B. 720 Minuten = 12 Stunden, 1080 Minuten = 18 Stunden)
WARN_THRESHOLD=720  # Zeit in Minuten für WARN
CRIT_THRESHOLD=1080 # Zeit in Minuten für CRIT

DIR_COUNT=$(find "$FOLDER" -mindepth 1 -maxdepth 1 -type d | wc -l)
CURRENT_TIME=$(date +%s)

# Falls der Ordner leer ist, Zeitmessung zurücksetzen
if [ "$DIR_COUNT" -eq 0 ]; then
    rm -f "$TIME_TRACK_FILE"
    STATUS=0  # OK
    MESSAGE="Ordner $FOLDER ist leer. Zeitmessung zurückgesetzt."
else
    # Prüfe, ob eine Zeitmessung existiert
    if [ -f "$TIME_TRACK_FILE" ]; then
        START_TIME=$(cat "$TIME_TRACK_FILE")
        TIME_ELAPSED=$((CURRENT_TIME - START_TIME))
    else
        echo "$CURRENT_TIME" > "$TIME_TRACK_FILE"
        TIME_ELAPSED=0
    fi

    MINUTES_ELAPSED=$((TIME_ELAPSED / 60))

    # Eskalationslogik mit konfigurierbaren Schwellenwerten
    if [ "$MINUTES_ELAPSED" -ge "$CRIT_THRESHOLD" ]; then
        STATUS=2  # CRIT
        MESSAGE="Ordner $FOLDER ist seit $MINUTES_ELAPSED Minuten nicht leer! (Kritisch nach ${CRIT_THRESHOLD}m)"
    elif [ "$MINUTES_ELAPSED" -ge "$WARN_THRESHOLD" ]; then
        STATUS=1  # WARN
        MESSAGE="Ordner $FOLDER ist seit $MINUTES_ELAPSED Minuten nicht leer! (Warnung nach ${WARN_THRESHOLD}m)"
    else
        STATUS=0  # OK
        MESSAGE="Ordner $FOLDER enthält $DIR_COUNT Unterverzeichnisse. Dauer: $MINUTES_ELAPSED Minuten"
    fi
fi

SERVICE_NAME="Folder Check of $FOLDER"

# Ausgabe im CheckMK-Format mit dynamischen Schwellenwerten
echo "$STATUS \"$SERVICE_NAME\" count=$DIR_COUNT;$WARN_THRESHOLD;$CRIT_THRESHOLD;0 $MESSAGE"
