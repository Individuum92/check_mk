#!/usr/bin/env python3
import datetime

def get_expiry_info(username):
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

users = ['test', 'backup_user_000']
for user in users:
    expiry_date = get_expiry_info(user)
    if expiry_date is None:
        status = f"0 user_expire_{user} - Passwort läuft nie ab"
    else:
        delta = (expiry_date - datetime.datetime.now()).days
        if delta <= 0:
            status = f"2 user_expire_{user} - Passwort ist abgelaufen"
        elif delta <= 15:
            status = f"2 user_expire_{user} - Passwort läuft in {delta} Tagen ab"
        elif delta <= 30:
            status = f"1 user_expire_{user} - Passwort läuft in {delta} Tagen ab"
        else:
            status = f"0 user_expire_{user} - Passwort läuft in {delta} Tagen ab"
    print(status)
