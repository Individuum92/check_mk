```
 _____                                      
/  ___|                                     
\ `--.  ___ _ __ __ _ _ __   ___ ___  _ __  
 `--. \/ _ \ '__/ _` | '_ \ / __/ _ \| '_ \ 
/\__/ /  __/ | | (_| | | | | (_| (_) | | | |
\____/ \___|_|  \__,_|_| |_|\___\___/|_| |_|
```
www.serancon.de | Michael Kraus

<br>

---
ToDo
---
- Extensions an alle Skripte hängen sodass erkennbar ist, in welcher Sprache das Skript vorliegt
- Umlaute anpassen (Ä,Ö,Ü)
- Update Automatismus der README-Datei einbinden
- Die jeweiligen Voraussetzungen der Skripte beschreiben
- ===> bei kleineren Vorraussetzunge entsprechend im Skript automatisieren (zB mkdir, touch, wget etc.)

# Skript-Downloader - Dokumentation

Der Skript-Downloader ermöglicht es, Skripte aus dem GitHub-Repository **check_mk** einfach auszuwählen, herunterzuladen und ausführbar zu machen.

## Funktionsweise

- Das Skript ruft die Liste der Dateien aus dem Repository ab.
- Dem Benutzer wird ein interaktives Menü zur Auswahl der Skripte angezeigt.
- Das gewählte Skript wird mit `wget` heruntergeladen.
- Nach dem Download wird es mit `chmod +x` ausführbar gemacht.

## Verfügbare Skripte

### check_folder_content
Überprüft den Inhalt eines Verzeichnisses und meldet Änderungen oder Abweichungen.

### check_rpi_temp
Misst die CPU-Temperatur eines Raspberry Pi und gibt Warnungen bei Überhitzung aus.

### check_user_exp.py
Prüft die Ablaufdaten von Benutzerkonten und informiert Administratoren über baldige Abläufe.

### count_sent_mails
Zählt die Anzahl der gesendeten E-Mails eines Mailservers und hilft bei der Überwachung des E-Mail-Aufkommens.

### folder_size_check
Überwacht die Größe eines Verzeichnisses und gibt Warnungen bei Überschreiten von Grenzwerten aus.

### check_blacklist.py
Überprüft, ob bestimmte IP-Adressen oder Domains auf einer Blacklist stehen

### check_cronjobs.py
Überwacht geplante Cronjobs auf einem Linux-System und meldet, ob sie erfolgreich ausgeführt wurden oder fehlschlagen.

### speedtest.py
Führt einen Internet-Speedtest durch und misst Download-, Upload-Geschwindigkeit und Latenz. Es kann genutzt werden, um die Netzwerkleistung regelmäßig zu testen.

## Installation & Nutzung

1. **Skript herunterladen und ausführbar machen:**
   ```bash
   wget https://raw.githubusercontent.com/Individuum92/check_mk/main/github_downloader.sh
   chmod +x github_downloader.sh
   ```

2. **Skript ausführen:**
   ```bash
   ./github_downloader.sh
   ```

3. **Gewünschtes Skript aus dem Menü auswählen und herunterladen.**

---
Dieses Repository wird regelmäßig aktualisiert 🚀
