#!/usr/bin/env python3
"""
Continuous AI Learning Pipeline
Runs numbered scripts in order, then loops.
Reports after each script.
"""
import os
import sys
import json
import subprocess
import time
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
SCRIPT_ROOT = os.path.join(BASE, "scripts")
OUTPUT_DIR = os.path.join(BASE, "outputs")
REPORT_DIR = os.path.join(BASE, "reports")
LOG_DIR = os.path.join(BASE, "logs")

for d in (OUTPUT_DIR, REPORT_DIR, LOG_DIR):
    os.makedirs(d, exist_ok=True)

def get_script_folders():
    if not os.path.isdir(SCRIPT_ROOT):
        return []
    folders = []
    for name in sorted(os.listdir(SCRIPT_ROOT)):
        path = os.path.join(SCRIPT_ROOT, name)
        script = os.path.join(path, "script.py")
        if os.path.isdir(path) and os.path.isfile(script):
            folders.append((name, script))
    return folders

def run_script(name, script_path):
    print(f"=== Running {name} ===")
    start = time.time()
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=300,  # 5 min per script
            cwd=os.path.dirname(script_path)
        )
        elapsed = time.time() - start
        status = "success" if result.returncode == 0 else "error"
        report = {
            "script": name,
            "status": status,
            "return_code": result.returncode,
            "elapsed_sec": round(elapsed, 2),
            "stdout": result.stdout[-2000:],
            "stderr": result.stderr[-1000:],
            "timestamp": datetime.now().isoformat()
        }
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        report = {
            "script": name,
            "status": "timeout",
            "elapsed_sec": round(elapsed, 2),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        report = {
            "script": name,
            "status": "exception",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

    report_path = os.path.join(REPORT_DIR, f"{name}_{int(time.time())}.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Status: {report.get('status')}  ({report.get('elapsed_sec', 0)}s)")
    return report

def main():
    continuous = "--once" not in sys.argv
    folders = get_script_folders()
    if not folders:
        print("No script folders found in scripts/")
        return

    print(f"AI Learning Pipeline Starting... ({len(folders)} scripts)")
    if continuous:
        print("Continuous mode. Press Ctrl+C to stop.")

    cycle = 0
    try:
        while True:
            cycle += 1
            print(f"\n--- Cycle {cycle} ---")
            for name, path in folders:
                run_script(name, path)
                time.sleep(1)  # short pause between scripts
            if not continuous:
                break
            print("Cycle complete. Sleeping 30s before next pass...")
            time.sleep(30)
    except KeyboardInterrupt:
        print("\nStopped by user.")

    print("Pipeline complete. Check reports/ and outputs/ folders.")

if __name__ == "__main__":
    main()
