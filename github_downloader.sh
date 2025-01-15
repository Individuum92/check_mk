#!/bin/bash

GITHUB_USER="Individuum92"
REPO="check_mk"
GITHUB_API="https://api.github.com/repos/$GITHUB_USER/$REPO/contents"
METADATA_URL="https://raw.githubusercontent.com/$GITHUB_USER/$REPO/main/metadaten.json"
TARGET_BASE="/usr/lib/check_mk_agent/local"

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

# Lade Metadaten herunter und prüfe, ob es erfolgreich war
metadata=$(curl -s $METADATA_URL)
if [[ -z "$metadata" || "$metadata" == "404: Not Found" ]]; then
    echo "⚠ Fehler: Metadaten konnten nicht geladen werden! Stelle sicher, dass metadaten.json existiert."
    exit 1
fi

display_menu() {
    while true; do
        clear
        echo "=================================================="
        echo "Verfügbare Kategorien im Repository $REPO"
        echo "=================================================="
        echo "1. Linux"
        echo "2. Raspberry-Pi"
        echo "3. Beenden"

        read -p "Wähle eine Kategorie: " category_selection

        case "$category_selection" in
            1) download_category "Linux" ;;
            2) download_category "Raspberry-Pi" ;;
            3) echo "Beenden..."; exit 0 ;;
            *) echo "Ungültige Auswahl, bitte erneut versuchen."; sleep 2 ;;
        esac
    done
}

download_category() {
    local category="$1"
    local category_api="$GITHUB_API/$category"

    clear
    echo "=================================================="
    echo "Verfügbare Skripte in $category"
    echo "=================================================="

    scripts=($(curl -s "$category_api" | jq -r '.[] | select(.type=="dir") | .name'))

    if [ ${#scripts[@]} -eq 0 ]; then
        echo "Keine Skripte gefunden."
        sleep 2
        return
    fi

    for i in "${!scripts[@]}"; do
        echo "$((i+1)). ${scripts[i]}"
    done
    echo "$(( ${#scripts[@]} + 1 )). Zurück zum Hauptmenü"

    read -p "Wähle einen Unterordner: " sub_selection

    if [[ "$sub_selection" -eq "$(( ${#scripts[@]} + 1 ))" ]]; then
        return
    elif [[ "$sub_selection" =~ ^[0-9]+$ ]] && (( sub_selection > 0 && sub_selection <= ${#scripts[@]} )); then
        sub_folder="${scripts[$((sub_selection-1))]}"
        download_scripts "$category/$sub_folder"
    else
        echo "Ungültige Auswahl, bitte erneut versuchen."
        sleep 2
    fi
}


download_scripts() {
    local script_path="$1"
    local script_api="$GITHUB_API/$script_path"

    clear
    echo "=================================================="
    echo "Verfügbare Skripte in $script_path"
    echo "=================================================="

    # Lade Liste der Skripte, filtere Verzeichnisse & ignoriere versteckte Dateien (die mit '.' beginnen)
    scripts=($(curl -s "$script_api" | jq -r '.[] | select(.type=="file") | .name' | grep -vE '^\..*'))

    if [ ${#scripts[@]} -eq 0 ]; then
        echo "Keine Skripte gefunden."
        sleep 2
        return
    fi

    # Skripte nummeriert auflisten
    for i in "${!scripts[@]}"; do
        echo "$((i+1)). ${scripts[i]}"
    done
    echo "$(( ${#scripts[@]} + 1 )). Zurück zum vorherigen Menü"

    # Nutzereingabe abfragen
    read -p "Wähle ein Skript zum Herunterladen: " script_selection

    if [[ "$script_selection" -eq "$(( ${#scripts[@]} + 1 ))" ]]; then
        return
    elif [[ "$script_selection" =~ ^[0-9]+$ ]] && (( script_selection > 0 && script_selection <= ${#scripts[@]} )); then
        script_name="${scripts[$((script_selection-1))]}"
        description=$(echo "$metadata" | jq -r --arg key "$script_name" '.[$key] // "Keine Beschreibung verfügbar."')

        clear
        echo "=================================================="
        echo "Skript: $script_name"
        echo "=================================================="
        echo "Beschreibung: $description"
        echo ""
        read -p "Möchtest du das Skript herunterladen? (y/n) " confirm
        if [[ "$confirm" == "y" ]]; then
            download_script "$script_path" "$script_name"
        fi
    else
        echo "Ungültige Auswahl, bitte erneut versuchen."
        sleep 2
    fi
}


download_script() {
    local script_path="$1"
    local script_name="$2"
    local target_dir="$3"
    local script_url="https://raw.githubusercontent.com/$GITHUB_USER/$REPO/main/$script_path/$script_name"
    local temp_file="/tmp/$script_name"

    echo "Herunterladen von $script_name..."
    wget -q "$script_url" -O "$temp_file"

    if [ $? -eq 0 ]; then
        chmod +x "$temp_file"
        sudo mv "$temp_file" "$target_dir/$script_name"
        echo "$script_name erfolgreich heruntergeladen, ausführbar gemacht und nach $target_dir verschoben."
    else
        echo "Fehler beim Herunterladen von $script_name."
    fi
    sleep 2
}

display_menu
