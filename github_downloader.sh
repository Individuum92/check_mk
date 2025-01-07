#!/bin/bash

GITHUB_USER="Individuum92"
REPO="check_mk"
GITHUB_API="https://api.github.com/repos/$GITHUB_USER/$REPO/contents"

# Menü-Funktion anzeigen
display_menu() {
    while true; do
        clear
        echo "========================================"
        echo "  Verfügbare Skripte im Repository $REPO"
        echo "  von $GITHUB_USER"
        echo "========================================"
        echo ""
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
                download_script "$script"
                break
            else
                echo "Ungültige Auswahl, bitte erneut versuchen."
            fi
        done
    done
}

# Funktion zum Herunterladen und ausführbar machen
download_script() {
    local script_name="$1"
    local script_url="https://raw.githubusercontent.com/$GITHUB_USER/$REPO/main/$script_name"
    
    clear
    echo "=================================================="
    echo "  Herunterladen von $script_name..."
    echo "=================================================="
    
    wget -q "$script_url" -O "$script_name"
    
    if [ $? -eq 0 ]; then
        chmod +x "$script_name"
        echo "$script_name erfolgreich heruntergeladen und ausführbar gemacht."
    else
        echo "Fehler beim Herunterladen von $script_name."
    fi
    
    echo "Drücke eine beliebige Taste, um fortzufahren..."
    read -n 1 -s
}

# Hauptprogramm starten
display_menu
