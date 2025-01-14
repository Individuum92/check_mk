![Logo](https://serancon.de/wp-content/uploads/2022/03/logo.png)


www.serancon.de | Michael Kraus

Aus meiner eigenen Erfahrung und der Betreuung von Kunden im Bereich Monitoring heraus habe ich beschlossen, eigene Checks zu entwickeln und hier öffentlich bereitzustellen. Mein Ziel ist es, die Skripte kontinuierlich zu aktualisieren und zu verbessern.

Falls Sie Anregungen oder spezielle Anforderungen haben, lassen Sie es mich wissen. Bei Problemen oder Fehlern können Sie gerne die Issue-Funktion nutzen:
🔗 GitHub Issues


## Skript-Downloader

Der Skript-Downloader ermöglicht es, Skripte aus dem GitHub-Repository check_mk einfach auszuwählen, herunterzuladen und ausführbar zu machen. Die Skripte werden dabei automatisch in dn richtigen Ordner verschoben. Die Skripte können nach dem Downlaod bearbeitet werden.
Ort der Skripte: `/usr/etc/check_mk/local`

### Funktionsweise
Das Skript ruft die Liste der Dateien aus dem Repository ab.
Dem Benutzer wird ein interaktives Menü zur Auswahl der Skripte angezeigt.
Das gewählte Skript wird mit wget heruntergeladen.
Nach dem Download wird es mit chmod +x ausführbar gemacht.

## Installation & Nutzung

1. **Ordnerstruktur anlegen**

Voraussetzungen für die Nutzung der Skripte ist, dass folgende Ordnerstruktur besteht:
- /etc/serancon
- /var/log/serancon
- /etc/serancon

Mit folgendem Befehl können diese angelegt werden: 
   ```bash
   mkdir -p /etc/serancon /var/log/serancon /etc/serancon
   ```

2. **Skript herunterladen und ausführbar machen:**
   ```bash
   wget https://raw.githubusercontent.com/Individuum92/check_mk/main/github_downloader.sh
   chmod +x github_downloader.sh
   ```

3. **Skript ausführen:**
   ```bash
   ./github_downloader.sh
   ```

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



## ToDo

- [ ] Ordnerstruktur überarbeiten, sodass standardisierte Parameter bestehen (für Logs, Arbeitsdateien und etc.)
- [ ] Eindeutigkeit in die Servicenamen einbinden (Serancon {SERVICE NAME}), um z.B. Gruppierungen vornehmen zu können
- [ ] Extensions an alle Skripte hängen sodass erkennbar ist, in welcher Sprache das Skript vorliegt
- [ ] Umlaute anpassen (Ä,Ö,Ü)
- [ ] Update Automatismus der README-Datei einbinden
- [ ] Die jeweiligen Voraussetzungen der Skripte beschreiben
- [ ] DE / EN Versionen




![Logo](https://serancon.de/wp-content/uploads/2022/03/logo.png)


www.serancon.de | Michael Kraus

Aus meiner eigenen Erfahrung und der Betreuung von Kunden im Bereich Monitoring heraus habe ich beschlossen, eigene Checks zu entwickeln und hier öffentlich bereitzustellen. Mein Ziel ist es, die Skripte kontinuierlich zu aktualisieren und zu verbessern.

Falls Sie Anregungen oder spezielle Anforderungen haben, lassen Sie es mich wissen. Bei Problemen oder Fehlern können Sie gerne die Issue-Funktion nutzen:
🔗 GitHub Issues


## Skript-Downloader

Der Skript-Downloader ermöglicht es, Skripte aus dem GitHub-Repository check_mk einfach auszuwählen, herunterzuladen und ausführbar zu machen. Die Skripte werden dabei automatisch in dn richtigen Ordner verschoben. Die Skripte können nach dem Downlaod bearbeitet werden.
Ort der Skripte: `/usr/etc/check_mk/local`

### Funktionsweise
Das Skript ruft die Liste der Dateien aus dem Repository ab.
Dem Benutzer wird ein interaktives Menü zur Auswahl der Skripte angezeigt.
Das gewählte Skript wird mit wget heruntergeladen.
Nach dem Download wird es mit chmod +x ausführbar gemacht.

## Installation & Nutzung
1. Ordnerstruktur anlegen
Voraussetzungen für die Nutzung der Skripte ist, dass folgende Ordnerstruktur besteht:
`/etc/serancon
/var/log/serancon
/etc/serancon`

Mit folgendem Befehl können diese angelegt werden:

mkdir -p /etc/serancon /var/log/serancon /etc/serancon

2. Skript herunterladen und ausführbar machen:

`wget https://raw.githubusercontent.com/Individuum92/check_mk/main/github_downloader.sh`
`chmod +x github_downloader.sh`

3. Skript ausführen:
`./github_downloader.sh`


