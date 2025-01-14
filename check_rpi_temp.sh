#!/bin/bash

# Schwellwerte für Warnung und Kritisch (anpassen nach Bedarf)
WARN_TEMP=70.0
CRIT_TEMP=85.0

# Service Name für CheckMK
SERVICE_NAME="Raspberry Pi Temperature"

# Temperatur abrufen
TEMP_OUTPUT=$(vcgencmd measure_temp)
TEMP_VALUE=$(echo "$TEMP_OUTPUT" | grep -oP '(?<=temp=)[0-9]+(\.[0-9]+)?')

# Prüfen, ob die Temperatur korrekt ausgelesen wurde
if [[ -z "$TEMP_VALUE" ]]; then
    echo "2 \"$SERVICE_NAME\" temperature=U;;;; UNKNOWN - Unable to read temperature"
    exit 2
fi

# Standardausgabe für CheckMK
STATUS=0
MESSAGE="OK - ${TEMP_VALUE}°C"

# Temperatur gegen Schwellenwerte prüfen und Status setzen
if (( $(echo "$TEMP_VALUE >= $CRIT_TEMP" | bc -l) )); then
    STATUS=2
    MESSAGE="CRITICAL - ${TEMP_VALUE}°C (Threshold: ${CRIT_TEMP}°C)"
elif (( $(echo "$TEMP_VALUE >= $WARN_TEMP" | bc -l) )); then
    STATUS=1
    MESSAGE="WARNING - ${TEMP_VALUE}°C (Threshold: ${WARN_TEMP}°C)"
fi

# CheckMK-Format mit Performance-Daten für Graphen
echo "$STATUS \"$SERVICE_NAME\" temperature=${TEMP_VALUE};$WARN_TEMP;$CRIT_TEMP;0;100 $MESSAGE"
