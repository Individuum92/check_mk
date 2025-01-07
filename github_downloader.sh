#!/bin/bash

GITHUB_USER="Individuum92"
REPO="check_mk"
GITHUB_API="https://api.github.com/repos/$GITHUB_USER/$REPO/contents"
METADATA_URL="https://raw.githubusercontent.com/$GITHUB_USER/$REPO/main/metadata.json"

# Lade Metadaten herunter
metadata=$(curl -s $METADATA_URL)

display_menu() {
    clear
    echo "========================================"
    echo "  Verfügbare Skripte im Repository $REPO"
    echo "========================================"
    
    scripts=($(curl -s $GITHUB_API | jq -r '.[] | select(.type=="file") | .name'))

    if [ ${#scripts[@]} -eq 0 ]; then
        echo "Keine Skripte gefunden."
        exit 1
    fi

    select script in "${scripts[@]}" "Beenden"; do
        if [[ "$script" == "Beenden" ]]; then
            echo "Beenden..."
            exit 0
        elif [[ -n "$script" ]]; then
            description=$(echo "$metadata" | jq -r --arg key "$script" '.[$key] // "Keine Beschreibung verfügbar."')
            clear
            echo "========================================"
            echo "  Skript: $script"
            echo "========================================"
            echo "Beschreibung: $description"
            echo ""
            read -p "Möchtest du das Skript herunterladen? (y/n) " confirm
            if [[ "$confirm" == "y" ]]; then
                download_script "$script"
            fi
        else
            echo "Ungültige Auswahl, bitte erneut versuchen."
        fi
    done
}

download_script() {
    local script_name="$1"
    local script_url="https://raw.githubusercontent.com/$GITHUB_USER/$REPO/main/$script_name"

    echo "Herunterladen von $script_name..."
    wget -q "$script_url" -O "$script_name"

    if [ $? -eq 0 ]; then
        chmod +x "$script_name"
        echo "$script_name erfolgreich heruntergeladen und ausführbar gemacht."
    else
        echo "Fehler beim Herunterladen von $script_name."
    fi
}

display_menu
