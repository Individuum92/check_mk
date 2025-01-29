#!/usr/bin/env python3

import subprocess
import sys
import os
from collections import Counter

# CheckMK Local Check - APT Updates with Thresholds

# Define thresholds
WARN_THRESHOLD = 20
CRIT_THRESHOLD = 35

# Toggle for adding prefix
PREFIX_ENABLED = True  # True = Prefix "Serancon: " enabled, False = Prefix disabled

# Run apt update to refresh package lists and capture errors
try:
    result = subprocess.run(["apt", "update"], capture_output=True, text=True, timeout=60)
    apt_update_output = result.stdout + result.stderr
    apt_update_status = result.returncode
except subprocess.TimeoutExpired:
    print("2 \"APT Update Check\" updates=0;20;35 APT update timed out | Repository check failed")
    sys.exit(2)

# Initialize variables
updates = 0
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

# Check for duplicate sources in /etc/apt/sources.list and sources.list.d
source_files = ["/etc/apt/sources.list"]
sources_dir = "/etc/apt/sources.list.d/"
if os.path.isdir(sources_dir):
    source_files.extend([os.path.join(sources_dir, f) for f in os.listdir(sources_dir) if f.endswith(".list")])

sources = []
for source_file in source_files:
    if os.path.exists(source_file):
        with open(source_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    sources.append(line)

# Find duplicate sources
duplicates = [item for item, count in Counter(sources).items() if count > 1]
if duplicates:
    repo_status = max(repo_status, 1)  # Ensure WARN status for duplicates
    repo_message += " | Duplicate sources detected: " + ", ".join(duplicates[:3])  # Show up to 3 duplicates

# Always try to count available updates, even if apt update failed
try:
    result = subprocess.run(["apt", "list", "--upgradable"], capture_output=True, text=True)
    upgradable_packages = [line.split('/')[0] for line in result.stdout.split('\n') if "/" in line]
    updates = len(upgradable_packages)
except Exception:
    updates = 0

# Determine the status based on thresholds
if updates >= CRIT_THRESHOLD:
    status = 2  # CRIT
elif updates >= WARN_THRESHOLD:
    status = 1  # WARN

# Define service name with optional prefix
base_service_name = "APT Update Check"
service_name = f"Serancon: {base_service_name}" if PREFIX_ENABLED else base_service_name

# Output in CheckMK Local Check format
print("<<<local>>>")
print(f"{max(status, repo_status)} \"{service_name}\" updates={updates};{WARN_THRESHOLD};{CRIT_THRESHOLD} Updates available: {updates} | {repo_message}")
