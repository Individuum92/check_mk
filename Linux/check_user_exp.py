#!/usr/bin/env python3
import datetime

# Präfix-Steuerung
PREFIX_ENABLED = 1  # 1 = "Serancon: " wird vorangestellt, 0 = deaktiviert

# Benutzerliste
USERS = ['test', 'backup_user_000']

# Konfiguration der Tage für die Statusbewertung
CRIT_DAYS_1 = 0   # Passwort abgelaufen (kritisch)
CRIT_DAYS_2 = 15  # Weniger als 15 Tage bis Ablauf (kritisch)
WARN_DAYS = 30    # Weniger als 30 Tage bis Ablauf (Warnung)

def get_expiry_info(username):
    """
    Liest das Ablaufdatum des Passworts für einen Benutzer aus /etc/shadow.
    Gibt None zurück, wenn das Passwort nicht abläuft.
    """
    try:
        with open("/etc/shadow", "r") as shadow_file:
            for line in shadow_file:
                parts = line.split(":")
                if parts[0] == username:
                    last_change = int(parts[2])
                    max_days = parts[4].strip()

                    # Prüfen, ob das Feld leer ist, -1 oder 99999 enthält (bedeutet: kein Ablauf)
                    if not max_days or max_days in ('-1', '99999'):
                        return None  # Passwort läuft nie ab

                    max_days = int(max_days)
                    expiry_date = datetime.datetime(1970, 1, 1) + datetime.timedelta(days=last_change + max_days)
                    return expiry_date
    except Exception:
        return None
    return None

# CheckMK erwartet eine Kopfzeile für Local Checks
print("<<<local>>>")

for user in USERS:
    expiry_date = get_expiry_info(user)

    # Servicenamen mit optionalem Präfix setzen und Unterstriche durch Leerzeichen ersetzen
    base_service_name = f"User {user.replace('_', ' ')}"
    service_name = f"Serancon: {base_service_name}" if PREFIX_ENABLED else base_service_name

    if expiry_date is None:
        print(f'0 "{service_name}" - Passwort läuft nie ab')
    else:
        delta = (expiry_date - datetime.datetime.now()).days
        if delta <= CRIT_DAYS_1:
            print(f'2 "{service_name}" - Passwort ist abgelaufen')
        elif delta <= CRIT_DAYS_2:
            print(f'2 "{service_name}" - Passwort läuft in {delta} Tagen ab (kritisch)')
        elif delta <= WARN_DAYS:
            print(f'1 "{service_name}" - Passwort läuft in {delta} Tagen ab (Warnung)')
        else:
            print(f'0 "{service_name}" - Passwort läuft in {delta} Tagen ab (OK)')
