#!/usr/bin/env python3

import subprocess
import sys
import os
import time
from collections import deque
from datetime import datetime

# CheckMK Local Check - APT Updates with Lock Handling & Execution Interval

# Define thresholds
WARN_THRESHOLD = 20
CRIT_THRESHOLD = 35

# Toggle for adding prefix
PREFIX_ENABLED = True  # True = Prefix "Serancon: " enabled, False = Prefix disabled

# Execution interval in minutes (Default: 1 Minute für Debugging)
INTERVAL_MINUTES = 1

# Lock file for apt updates
APT_LOCK_FILE = "/var/lib/apt/lists/lock"

# Log directory and files
LOG_DIR = "/var/log/serancon"
LOCK_HISTORY_FILE = os.path.join(LOG_DIR, "apt_lock_history.log")
LAST_RUN_FILE = os.path.join(LOG_DIR, "apt_check_last_run.log")

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Function to check if another apt process is running
def is_apt_running():
    try:
        result = subprocess.run(["lsof", APT_LOCK_FILE], capture_output=True, text=True)
        return bool(result.stdout.strip())  # Wenn Ausgabe existiert, ist apt noch aktiv
    except FileNotFoundError:
        return False  # Falls lsof nicht existiert, ignorieren

# Function to get last execution time
def get_last_run_time():
    try:
        with open(LAST_RUN_FILE, "r") as f:
            return float(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0  # Falls Datei nicht existiert oder fehlerhaft ist

# Function to save current execution time
def update_last_run_time():
    with open(LAST_RUN_FILE, "w") as f:
        f.write(str(time.time()))

# Function to save lock history
def save_lock_history():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lock_entries = deque()

    try:
        with open(LOCK_HISTORY_FILE, "r") as f:
            lock_entries.extend(f.read().strip().split("\n"))
    except FileNotFoundError:
        pass  # Falls Datei nicht existiert, ignorieren

    lock_entries.appendleft(now)  # Neuen Eintrag vorne hinzufügen

    while len(lock_entries) > 5:
        lock_entries.pop()  # Nur die letzten 5 Einträge behalten

    with open(LOCK_HISTORY_FILE, "w") as f:
        f.write("\n".join(lock_entries))

# Check if the script was executed too recently
last_run_time = get_last_run_time()
time_since_last_run = time.time() - last_run_time
should_skip_check = time_since_last_run < (INTERVAL_MINUTES * 60)

# Run apt list --upgradable to check for available updates
try:
    result = subprocess.run(["apt", "list", "--upgradable"], capture_output=True, text=True)
    upgradable_packages = [line.split('/')[0] for line in result.stdout.split('\n') if "/" in line]
    updates = len(upgradable_packages)
except Exception:
    updates = 0

# Falls das Prüfintervall noch nicht erreicht ist, aber Updates vorhanden sind -> trotzdem ausführen
if should_skip_check and updates == 0:
    print(f"0 \"APT Update Check\" updates=0;{WARN_THRESHOLD};{CRIT_THRESHOLD} Skipping check: Execution interval not reached | No updates counted")
    sys.exit(0)

# Wait for lock to be released (max 30s)
wait_time = 0
while is_apt_running() and wait_time < 30:
    time.sleep(3)
    wait_time += 3

lock_history_summary = ""
if is_apt_running():
    save_lock_history()  # Speichert den Zeitstempel, wann apt blockiert war
    try:
        with open(LOCK_HISTORY_FILE, "r") as f:
            lock_timestamps = f.read().strip().split("\n")
    except FileNotFoundError:
        lock_timestamps = []

    lock_history_summary = f"Last 5 lock timestamps: {' | '.join(lock_timestamps)}" if lock_timestamps else "No recent lock events"

    print(f"1 \"APT Update Check\" updates={updates};{WARN_THRESHOLD};{CRIT_THRESHOLD} APT update skipped: Lock file still held | {lock_history_summary}")
    sys.exit(1)  # WARN, da das Problem temporär sein könnte

# Run apt update to refresh package lists and capture errors
try:
    result = subprocess.run(["apt", "update"], capture_output=True, text=True, timeout=60)
    apt_update_output = result.stdout + result.stderr
    apt_update_status = result.returncode
except subprocess.TimeoutExpired:
    print(f"2 \"APT Update Check\" updates={updates};{WARN_THRESHOLD};{CRIT_THRESHOLD} APT update timed out | Repository check failed")
    sys.exit(2)

# Initialize status
status = 0
repo_status = 0
repo_message = "Repositories OK"
warning_messages = []

# Check if apt update failed
if apt_update_status != 0:
    repo_message = f"APT update failed with exit code {apt_update_status}: "
    first_error_line = next((line for line in apt_update_output.split('\n') if "E:" in line), "Unknown Error")
    repo_message += first_error_line
    repo_status = 2  # Repository error should be shown as critical
    status = 2  # Ensure overall check is critical if repo fails

# Check for warnings in apt update output
for line in apt_update_output.split('\n'):
    if line.startswith("W:"):
        warning_messages.append(line)

if warning_messages:
    repo_status = max(repo_status, 1)  # At least WARN if warnings exist
    repo_message += " | " + " | ".join(warning_messages[:3])  # Show up to 3 warnings

# Determine the status based on thresholds
if updates >= CRIT_THRESHOLD:
    status = 2  # CRIT
elif updates >= WARN_THRESHOLD:
    status = 1  # WARN

# Load last 5 lock timestamps
try:
    with open(LOCK_HISTORY_FILE, "r") as f:
        lock_timestamps = f.read().strip().split("\n")
except FileNotFoundError:
    lock_timestamps = []

lock_history_summary = f"Last 5 lock timestamps: {' | '.join(lock_timestamps)}" if lock_timestamps else "No recent lock events"

# Define service name with optional prefix
base_service_name = "APT Update Check"
service_name = f"Serancon: {base_service_name}" if PREFIX_ENABLED else base_service_name

# Save execution time
update_last_run_time()

# ✅ **Finale CheckMK-konforme Ausgabe in EINER Zeile**
print("<<<local>>>")
print(f"{max(status, repo_status)} \"{service_name}\" updates={updates};{WARN_THRESHOLD};{CRIT_THRESHOLD} Updates available: {updates} | {repo_message} | {lock_history_summary}")
