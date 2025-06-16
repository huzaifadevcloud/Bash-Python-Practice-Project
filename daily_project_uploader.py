	#!/usr/bin/env python3

import os
import subprocess
import sys
from datetime import datetime

# === USER CONFIGURATION ===
GITHUB_USERNAME = "huzaifadevcloud"
REPO_NAME = "Bash-Python-Practice-Project"
PROJECTS_DIR = "/home/huzaifa/devOps/bash_practice_projects"
STATE_FILE = os.path.expanduser("~/.last_uploaded_project.txt")
LOG_FILE = os.path.expanduser("~/.project_upload_log.txt")
GIT_REMOTE_URL = f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
SCRIPT_PATH = os.path.abspath(__file__)

# === Configure Git default branch ===
subprocess.run(["git", "config", "--global", "init.defaultBranch", "main"])

# === Load all project folders ===
all_projects = sorted([
    f for f in os.listdir(PROJECTS_DIR)
    if os.path.isdir(os.path.join(PROJECTS_DIR, f))
])

# === Determine the next project to upload ===
if os.path.exists(STATE_FILE):
    with open(STATE_FILE) as f:
        last = f.read().strip()
        try:
            last_index = all_projects.index(last)
            next_index = last_index + 1
        except ValueError:
            next_index = 0
else:
    next_index = 0

# === If all uploaded, clean up and exit ===
if next_index >= len(all_projects):
    print("✅ All projects have been uploaded.")
    bashrc_path = os.path.expanduser("~/.bashrc")
    if os.path.exists(bashrc_path):
        with open(bashrc_path, "r") as file:
            lines = file.readlines()
        with open(bashrc_path, "w") as file:
            for line in lines:
                if SCRIPT_PATH not in line:
                    file.write(line)
        print("🧹 Auto-run disabled: script removed from .bashrc.")
    else:
        print("⚠️ .bashrc not found.")
    sys.exit(0)

# === Start Uploading Next Project ===
next_project = all_projects[next_index]
project_path = os.path.join(PROJECTS_DIR, next_project)
print(f"🚀 Preparing to upload: {next_project}")
os.chdir(project_path)

# === Git Setup ===
if not os.path.isdir(".git"):
    subprocess.run(["git", "init"], check=True)
    subprocess.run(["git", "remote", "add", "origin", GIT_REMOTE_URL], check=True)
else:
    remotes = subprocess.run(["git", "remote"], capture_output=True, text=True)
    if "origin" not in remotes.stdout:
        subprocess.run(["git", "remote", "add", "origin", GIT_REMOTE_URL])

# === Pull from remote to avoid push errors ===
print("🔄 Pulling from remote to sync...")
pull = subprocess.run(["git", "pull", "origin", "main"], capture_output=True, text=True)
if pull.returncode != 0 and "couldn't find remote ref main" not in pull.stderr:
    print("❌ Pull failed:\n", pull.stderr)
    sys.exit(1)

# === Add all files ===
subprocess.run(["git", "add", "."], check=True)

# === Get commit message ===
commit_msg = input("📝 Enter your commit message: ").strip()
if not commit_msg:
    print("❌ Commit message required. Aborting.")
    sys.exit(1)

# === Commit and check result ===
commit = subprocess.run(["git", "commit", "-m", commit_msg])
if commit.returncode != 0:
    print("⚠️ Nothing to commit. Skipping push.")
else:
    push = subprocess.run(["git", "push", "-u", "origin", "main"])
    if push.returncode != 0:
        print("❌ Push failed.")
        sys.exit(1)

# === Log the upload ===
now = datetime.now().strftime("%Y-%m-%d")
with open(LOG_FILE, "a") as log:
    log.write(f"[{now}] Uploaded {next_project} - Commit: \"{commit_msg}\"\n")

# === Update state ===
with open(STATE_FILE, "w") as f:
    f.write(next_project)

print(f"✅ {next_project} uploaded and logged.")

