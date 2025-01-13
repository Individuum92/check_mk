#!/usr/bin/env python3

import json
import subprocess

# Modul-Steuerung (1 = aktiv, 0 = deaktiviert)
CHECK_DOWNLOAD = 1
CHECK_UPLOAD = 1
CHECK_PING = 1
CHECK_PACKETLOSS = 1
CHECK_EXTERNAL_IP = 1
CHECK_INTERNAL_IP = 1
CHECK_VPN_STATUS = 1
CHECK_SERVER_INFO = 1
CHECK_RESULT_URL = 1

# Schwellwerte für Warnung & Kritisch
DOWNLOAD_WARN = 10
DOWNLOAD_CRIT = 5

UPLOAD_WARN = 5
UPLOAD_CRIT = 2

PING_WARN = 50
PING_CRIT = 100

PACKETLOSS_WARN = 5  # Warnung bei >1% Paketverlust
PACKETLOSS_CRIT = 10  # Kritisch bei >5% Paketverlust

def run_speedtest():
    try:
        # Speedtest ausführen und JSON-Ergebnis abrufen
        result = subprocess.run(["speedtest", "--format=json"], capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)

        # Variablen für Ergebnisse (initial leer)
        download, upload, ping, packet_loss = None, None, None, None
        external_ip, internal_ip, vpn_status = None, None, None
        server_name, server_location, server_ip = None, None, None
        result_url = None

        # Werte nur berechnen, wenn aktiv
        if CHECK_DOWNLOAD:
            download = round(data["download"]["bandwidth"] / 125000, 2)
        if CHECK_UPLOAD:
            upload = round(data["upload"]["bandwidth"] / 125000, 2)
        if CHECK_PING:
            ping = round(data["ping"]["latency"], 2)
        if CHECK_PACKETLOSS:
            packet_loss = data.get("packetLoss", 0)
        if CHECK_EXTERNAL_IP:
            external_ip = data["interface"]["externalIp"]
        if CHECK_INTERNAL_IP:
            internal_ip = data["interface"]["internalIp"]
        if CHECK_VPN_STATUS:
            vpn_status = "Yes" if data["interface"]["isVpn"] else "No"
        if CHECK_SERVER_INFO:
            server_name = data["server"]["name"]
            server_location = data["server"]["location"]
            server_ip = data["server"]["ip"]
        if CHECK_RESULT_URL:
            result_url = data["result"]["url"]

        # Statuscodes berechnen (0=OK, 1=Warnung, 2=Kritisch)
        if CHECK_DOWNLOAD:
            download_state = 2 if download < DOWNLOAD_CRIT else (1 if download < DOWNLOAD_WARN else 0)
            print(f"{download_state} Speedtest_Download download={download}MBps;{DOWNLOAD_WARN};{DOWNLOAD_CRIT} Download Speed: {download} MBps")

        if CHECK_UPLOAD:
            upload_state = 2 if upload < UPLOAD_CRIT else (1 if upload < UPLOAD_WARN else 0)
            print(f"{upload_state} Speedtest_Upload upload={upload}MBps;{UPLOAD_WARN};{UPLOAD_CRIT} Upload Speed: {upload} MBps")

        if CHECK_PING:
            ping_state = 2 if ping > PING_CRIT else (1 if ping > PING_WARN else 0)
            print(f"{ping_state} Speedtest_Ping ping={ping}ms;{PING_WARN};{PING_CRIT} Ping: {ping} ms")

        if CHECK_PACKETLOSS:
            packet_loss_state = 2 if packet_loss > PACKETLOSS_CRIT else (1 if packet_loss > PACKETLOSS_WARN else 0)
            print(f"{packet_loss_state} Speedtest_PacketLoss packetloss={packet_loss}%;{PACKETLOSS_WARN};{PACKETLOSS_CRIT} Packet Loss: {packet_loss}%")

        # Info-Meldungen (immer Status 0, da keine Schwellwerte)
        if CHECK_EXTERNAL_IP:
            print(f"0 Speedtest_ExternalIP - External IP: {external_ip}")
        if CHECK_INTERNAL_IP:
            print(f"0 Speedtest_InternalIP - Internal IP: {internal_ip}")
        if CHECK_VPN_STATUS:
            print(f"0 Speedtest_VPN - VPN detected: {vpn_status}")
        if CHECK_SERVER_INFO:
            print(f"0 Speedtest_Server - Server: {server_name}, Location: {server_location}, IP: {server_ip}")
        if CHECK_RESULT_URL:
            print(f"0 Speedtest_ResultURL - Test URL: {result_url}")

    except subprocess.CalledProcessError as e:
        print("2 Speedtest_Error - Speedtest konnte nicht ausgeführt werden:", str(e))

    except json.JSONDecodeError:
        print("2 Speedtest_Error - Ungültige JSON-Antwort von Speedtest")

if __name__ == "__main__":
    run_speedtest()
