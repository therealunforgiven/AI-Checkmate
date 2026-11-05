#!/usr/bin/env python3
"""
AI Learning Pipeline Runner
Runs numbered scripts in order, captures output, writes reports.
"""

import os
import sys
import subprocess
import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
SCRIPTS_DIR = BASE_DIR / "scripts"
OUTPUTS_DIR = BASE_DIR / "outputs"
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"

for d in [OUTPUTS_DIR, REPORTS_DIR, LOGS_DIR]:
    d.mkdir(exist_ok=True)

def get_script_folders():
    """Get sorted list of numbered script folders."""
    folders = []
    if SCRIPTS_DIR.exists():
        for item in sorted(SCRIPTS_DIR.iterdir()):
            if item.is_dir() and item.name[:2].isdigit():
                folders.append(item)
    return folders

def run_script(script_folder):
    """Run the main script in a folder and capture results."""
    script_files = list(script_folder.glob("*.py"))
    if not script_files:
        return {"status": "error", "message": "No .py file found"}
    
    script_path = script_files[0]
    output_dir = OUTPUTS_DIR / script_folder.name
    output_dir.mkdir(exist_ok=True)
    
    start_time = datetime.now()
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=script_folder,
            capture_output=True,
            text=True,
            timeout=3600  # 1 hour default timeout
        )
        end_time = datetime.now()
        runtime = (end_time - start_time).total_seconds()
        
        # Save output
        (output_dir / "stdout.txt").write_text(result.stdout)
        (output_dir / "stderr.txt").write_text(result.stderr)
        
        report = {
            "script": script_folder.name,
            "status": "success" if result.returncode == 0 else "error",
            "returncode": result.returncode,
            "runtime_seconds": runtime,
            "start": start_time.isoformat(),
            "end": end_time.isoformat(),
            "stdout_preview": result.stdout[-500:] if result.stdout else "",
            "stderr_preview": result.stderr[-500:] if result.stderr else "",
        }
        
    except subprocess.TimeoutExpired:
        end_time = datetime.now()
        report = {
            "script": script_folder.name,
            "status": "timeout",
            "runtime_seconds": 3600,
            "message": "Script exceeded 1 hour timeout"
        }
    except Exception as e:
        report = {
            "script": script_folder.name,
            "status": "exception",
            "message": str(e)
        }
    
    # Write report
    report_path = REPORTS_DIR / f"{script_folder.name}_report.json"
    report_path.write_text(json.dumps(report, indent=2))
    
    return report

def main():
    print("AI Learning Pipeline Starting...")
    folders = get_script_folders()
    if not folders:
        print("No script folders found in scripts/")
        return
    
    print(f"Found {len(folders)} scripts to run")
    
    for folder in folders:
        print(f"\n=== Running {folder.name} ===")
        report = run_script(folder)
        print(f"Status: {report.get('status')}")
        if report.get('returncode') is not None:
            print(f"Return code: {report['returncode']}")
    
    print("\nPipeline complete. Check reports/ and outputs/ folders.")

if __name__ == "__main__":
    main()
