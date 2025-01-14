<div align="center">
    <img src="https://serancon.de/wp-content/uploads/2022/03/logo.png" alt="Logo" style="width:50%;">
</div>



<div align="center">
   
### 👋 Willkommen in meinem eigenen Check_MK Repo!  

[![Website](https://img.shields.io/badge/Website-Visit-blue?style=for-the-badge)](https://serancon.de) [![GitHub](https://img.shields.io/badge/GitHub-Profile-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Individuum92)

</div>

Aus meiner eigenen Erfahrung und der Betreuung von Kunden im Bereich Monitoring heraus habe ich beschlossen, eigene Checks zu entwickeln und hier öffentlich bereitzustellen. Mein Ziel ist es, die Skripte kontinuierlich zu aktualisieren und zu verbessern.

Falls Sie Anregungen oder spezielle Anforderungen haben, lassen Sie es mich wissen. Bei Problemen oder Fehlern können Sie gerne die Issue-Funktion nutzen.

[![GitHub issues](https://img.shields.io/github/issues/Individuum92/check_mk?style=for-the-badge)](https://github.com/Individuum92/check_mk/issues)

<br>

<details>
  <summary>📚 Inhaltsverzeichnis</summary>

- [Sprachen und Technologien](#Sprachen-und-Technologien)
- [Skript-Downloader](#Skript-Downloader)

</details>

<br>

## Sprachen und Technologien

![Bash](https://img.shields.io/badge/Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) 

![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black) ![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=raspberry-pi&logoColor=white)

<br>

## Skript-Downloader

Der Skript-Downloader ermöglicht es, Skripte aus dem GitHub-Repository *check_mk* einfach auszuwählen, herunterzuladen und ausführbar zu machen. Die Skripte werden dabei automatisch in den richtigen Ordner verschoben und können bearbeitet werden.  
Das Skript ruft die Liste der Dateien aus dem Repository ab. Dem Benutzer wird ein interaktives Menü zur Auswahl der Skripte angezeigt.  
**Ort der Skripte:** `/usr/etc/check_mk/local`



<br>

### Installation & Nutzung

#### Ordnerstruktur anlegen

Voraussetzungen für die Nutzung der Skripte ist, dass folgende Ordnerstruktur besteht:
- /etc/serancon
- /var/log/serancon
- /etc/serancon

Diese Struktur wird automatisch bei Ausführung des Skript-Downloader's angelegt. Alternativ mit folgendem Befehl: 
   ```bash
   mkdir -p /etc/serancon /var/log/serancon /etc/serancon
   ```

#### Skript herunterladen und ausführbar machen
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

<br>

## Statistiken

[![GitHub stars](https://img.shields.io/github/stars/Individuum92/check_mk?style=for-the-badge)](https://github.com/Individuum92/check_mk/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Individuum92/check_mk?style=for-the-badge)](https://github.com/Individuum92/check_mk/network/members)
[![GitHub watchers](https://img.shields.io/github/watchers/Individuum92/check_mk?style=for-the-badge)](https://github.com/Individuum92/check_mk/watchers)

<br>

## ToDo

- [ ] Ordnerstruktur überarbeiten, sodass standardisierte Parameter bestehen (für Logs, Arbeitsdateien und etc.)
- [ ] Eindeutigkeit in die Servicenamen einbinden (Serancon {SERVICE NAME}), um z.B. Gruppierungen vornehmen zu können
- [ ] Extensions an alle Skripte hängen sodass erkennbar ist, in welcher Sprache das Skript vorliegt
- [ ] Umlaute anpassen (Ä,Ö,Ü)
- [ ] Update Automatismus der README-Datei einbinden
- [ ] Die jeweiligen Voraussetzungen der Skripte beschreiben
- [ ] DE / EN Versionen

