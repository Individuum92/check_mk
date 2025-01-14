#!/bin/bash

GITHUB_USER="Individuum92"
REPO="check_mk"
GITHUB_API="https://api.github.com/repos/$GITHUB_USER/$REPO/contents"
METADATA_URL="https://raw.githubusercontent.com/$GITHUB_USER/$REPO/main/metadaten.json"
TARGET_DIR="/usr/lib/check_mk_agent/local"

# Verzeichnisse prüfen und ggf. anlegen
REQUIRED_DIRS=("/etc/serancon" "/var/log/serancon" "/tmp/serancon")
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        sudo mkdir -p "$dir"
    fi
done

# Prüfe und installiere Abhängigkeiten, falls sie fehlen
echo "Prüfe erforderliche Pakete..."

MISSING_DEPS=()
for pkg in curl jq grep wget; do
    if ! command -v $pkg &> /dev/null; then
        MISSING_DEPS+=($pkg)
    fi
done

if [ ${#MISSING_DEPS[@]} -ne 0 ]; then
    echo "Fehlende Abhängigkeiten: ${MISSING_DEPS[*]}"
    read -p "Möchtest du sie jetzt installieren? (y/n) " confirm
    if [[ "$confirm" == "y" ]]; then
        sudo apt update && sudo apt install -y "${MISSING_DEPS[@]}"
    else
        echo "Fehlende Abhängigkeiten! Das Skript kann möglicherweise nicht korrekt ausgeführt werden."
        exit 1
    fi
else
    echo "Alle erforderlichen Pakete sind installiert."
fi

# Stelle sicher, dass das Zielverzeichnis existiert
if [ ! -d "$TARGET_DIR" ]; then
    echo "Erstelle Zielverzeichnis: $TARGET_DIR"
    sudo mkdir -p "$TARGET_DIR"
fi

echo "Zielverzeichnis: $TARGET_DIR"

# Lade Metadaten herunter und prüfe, ob es erfolgreich war
metadata=$(curl -s $METADATA_URL)
if [[ -z "$metadata" || "$metadata" == "404: Not Found" ]]; then
    echo "⚠ Fehler: Metadaten konnten nicht geladen werden! Stelle sicher, dass metadaten.json existiert."
    exit 1
fi

display_menu() {
    while true; do
        clear
        echo "========================================"
        echo "Verfügbare Skripte im Repository $REPO"
        echo "========================================"

        scripts=($(curl -s $GITHUB_API | jq -r '.[] | select(.type=="file") | .name' | grep -vE 'README.md|metadaten.json|github_downloader.sh|\.gitattributes'))

        if [ ${#scripts[@]} -eq 0 ]; then
            echo "Keine Skripte gefunden."
            sleep 2
            continue
        fi

        for i in "${!scripts[@]}"; do
            echo "$((i+1)). ${scripts[i]}"
        done
        echo "$(( ${#scripts[@]} + 1 )). Beenden"

        read -p "Wähle eine Nummer: " selection

        if [[ "$selection" -eq "$(( ${#scripts[@]} + 1 ))" ]]; then
            echo "Beenden..."
            exit 0
        elif [[ "$selection" =~ ^[0-9]+$ ]] && (( selection > 0 && selection <= ${#scripts[@]} )); then
            script="${scripts[$((selection-1))]}"
            description=$(echo "$metadata" | jq -r --arg key "$script" '.[$key] // "Keine Beschreibung verfügbar."')

            clear
            echo "========================================"
            echo "Skript: $script"
            echo "========================================"
            echo "Beschreibung: $description"
            echo ""
            read -p "Möchtest du das Skript herunterladen? (y/n) " confirm
            if [[ "$confirm" == "y" ]]; then
                download_script "$script"
            fi
        else
            echo "Ungültige Auswahl, bitte erneut versuchen."
            sleep 2
        fi
    done
}

download_script() {
    local script_name="$1"
    local script_url="https://raw.githubusercontent.com/$GITHUB_USER/$REPO/main/$script_name"
    local temp_file="/tmp/$script_name"

    echo "Herunterladen von $script_name..."
    wget -q "$script_url" -O "$temp_file"

    if [ $? -eq 0 ]; then
        chmod +x "$temp_file"
        sudo mv "$temp_file" "$TARGET_DIR/$script_name"
        echo "$script_name erfolgreich heruntergeladen, ausführbar gemacht und nach $TARGET_DIR verschoben."
    else
        echo "Fehler beim Herunterladen von $script_name."
    fi
    sleep 2
}

display_menu
