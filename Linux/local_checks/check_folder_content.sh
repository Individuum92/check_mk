#!/bin/bash

# Konfiguration
FOLDER="/check_mk_backups/"
TIME_TRACK_FILE="/tmp/nicht_entfernen_folder_check_time"

# Schwellenwerte in Minuten (z. B. 720 Minuten = 12 Stunden, 1080 Minuten = 18 Stunden)
WARN_THRESHOLD=60  # Zeit in Minuten für WARN
CRIT_THRESHOLD=180 # Zeit in Minuten für CRIT

# Präfix-Steuerung
PREFIX_ENABLED=1  # 1 = "Serancon: " wird vorangestellt, 0 = deaktiviert

DIR_COUNT=$(find "$FOLDER" -mindepth 1 -maxdepth 1 -type d | wc -l)
CURRENT_TIME=$(date +%s)

# Falls der Ordner leer ist, Zeitmessung zurücksetzen
if [ "$DIR_COUNT" -eq 0 ]; then
    rm -f "$TIME_TRACK_FILE"
    STATUS=0  # OK
    MESSAGE="Folder $FOLDER is empty. Time measurement reset."
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

# Servicenamen setzen mit optionalem Präfix
BASE_SERVICE_NAME="Folder content check"
if [ "$PREFIX_ENABLED" -eq 1 ]; then
    SERVICE_NAME="Serancon: $BASE_SERVICE_NAME"
else
    SERVICE_NAME="$BASE_SERVICE_NAME"
fi

# Ausgabe im CheckMK-Format mit dynamischen Schwellenwerten
echo "$STATUS \"$SERVICE_NAME\" count=$DIR_COUNT;$WARN_THRESHOLD;$CRIT_THRESHOLD;0 $MESSAGE"
