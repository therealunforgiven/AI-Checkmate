import os
import re
import csv
import sys
import base64
import shutil
import datetime
import requests

WAVE_DIR = os.path.expanduser("~/AI-Checkmate/waveforms")
KNOWLEDGE_DIR = os.path.expanduser("~/AI-Checkmate/knowledge")
os.makedirs(WAVE_DIR, exist_ok=True)
os.makedirs(KNOWLEDGE_DIR, exist_ok=True)

OLLAMA_URL = "http://localhost:11434/api/generate"
TEXT_MODEL = "dolphin-llama3:8b"
VISION_MODEL = "minicpm-v"

def analyze_csv_waveform(csv_path: str) -> str:
    """
    Parses a Micsig / oscilloscope CSV export (Time, CH1, optional CH2),
    computes exact voltage levels, and diagnoses CAN / LIN / BSD bus health.
    """
    ch1_vals = list()
    ch2_vals = list()

    with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        for row in reader:
            nums = list()
            for cell in row:
                clean = cell.strip().replace("V", "").replace("v", "")
                try:
                    nums.append(float(clean))
                except ValueError:
                    pass
            # Typical scope CSV: [Time, CH1] or [Time, CH1, CH2]
            if len(nums) >= 2:
                it = iter(nums)
                next(it, None)  # skip timestamp column
                v1 = next(it, None)
                v2 = next(it, None)
                if v1 is not None and -50.0 <= v1 <= 100.0:
                    ch1_vals.append(v1)
                if v2 is not None and -50.0 <= v2 <= 100.0:
                    ch2_vals.append(v2)

    if len(ch1_vals) < 10:
        return "Could not extract enough voltage samples from CSV. Check that CSV has numeric Time and Voltage columns."

    c1_min, c1_max = min(ch1_vals), max(ch1_vals)
    c1_avg = sum(ch1_vals) / len(ch1_vals)
    c1_swing = c1_max - c1_min

    report = list()
    report.append(f"Samples Parsed: {len(ch1_vals)}")
    report.append(f"CH1 Voltage: Min = {c1_min:.2f}V | Max = {c1_max:.2f}V | Avg = {c1_avg:.2f}V | Swing = {c1_swing:.2f}V")

    if len(ch2_vals) >= 10:
        c2_min, c2_max = min(ch2_vals), max(ch2_vals)
        c2_avg = sum(ch2_vals) / len(ch2_vals)
        c2_swing = c2_max - c2_min
        report.append(f"CH2 Voltage: Min = {c2_min:.2f}V | Max = {c2_max:.2f}V | Avg = {c2_avg:.2f}V | Swing = {c2_swing:.2f}V")

        # Dual-Channel High-Speed CAN Bus Evaluation
        if c1_max > 9.0 or c2_max > 9.0:
            diag = "FAULT: Short to Battery (+12V) detected on CAN bus (voltage exceeds 9V)."
        elif c1_max < 0.4 and c2_max < 0.4:
            diag = "FAULT: Both CAN-H and CAN-L shorted to Ground (0V flatline)."
        elif c2_max < 0.4 and c1_swing > 0.4:
            diag = "FAULT: CAN-L (CH2) shorted to Ground (0V) while CAN-H (CH1) is still trying to switch."
        elif 2.1 <= c1_min <= 2.8 and 3.1 <= c1_max <= 4.0 and 1.1 <= c2_min <= 1.9 and 2.1 <= c2_max <= 2.8:
            diag = "HEALTHY HIGH-SPEED CAN BUS: Recessive ~2.5V idle with clean ~3.5V (CAN-H) / ~1.5V (CAN-L) mirror swing."
        elif c1_swing < 0.25 and c2_swing < 0.25 and 2.2 <= c1_avg <= 2.8:
            diag = "IDLE / NO TRAFFIC CAN BUS: Sitting at 2.5V recessive bias, but no active data packets captured."
        else:
            diag = "ABNORMAL DUAL-CHANNEL WAVEFORM: Check for CAN-H/CAN-L shorted together, open wire, or missing 120-ohm termination."
    else:
        # Single-Channel Injector, Crank/Cam (CKP/CMP), or LIN / BMW BSD Evaluation
        if c1_max > 35.0 and c1_min < 1.5:
            diag = (
                f"HEALTHY SATURATED FUEL INJECTOR VOLTAGE WAVEFORM: Ground-side switch (~{c1_min:.2f}V ON) "
                f"with strong inductive turn-off spike ({c1_max:.1f}V) — confirms Terminal 87 power, DME MOSFET driver, and good injector coil."
            )
        elif -30.0 <= c1_min <= -0.8 and 0.8 <= c1_max <= 30.0:
            diag = (
                f"HEALTHY INDUCTIVE (VR) CRANK / CAM AC WAVEFORM: Clean zero-crossing AC sine wave "
                f"({c1_min:.2f}V to +{c1_max:.2f}V, {c1_swing:.2f}V peak-to-peak)."
            )
        elif -0.3 <= c1_min <= 0.4 and 4.4 <= c1_max <= 5.5:
            diag = (
                f"HEALTHY 5V HALL-EFFECT CRANK / CAM (CKP/CMP) SQUARE WAVE: Clean 0V-to-5V digital switching "
                f"({c1_min:.2f}V to {c1_max:.2f}V)."
            )
        elif c1_max < 0.5:
            diag = "FAULT (0V FLATLINE): Shorted to ground or missing power/pull-up feed (check Terminal 87 relay for injectors, or 5V/12V ref for CKP/CMP/BSD)."
        elif c1_swing < 0.5 and c1_max > 9.5:
            diag = "STUCK HIGH (~12V VBAT, NO SWITCHING): Good 12V feed present, but DME/Master is NOT pulsing ground (check CKP RPM signal, ISN/IMMO lock, or DME driver)."
        elif c1_max >= 9.5 and c1_min <= 2.0 and c1_swing >= 8.0:
            diag = "HEALTHY 12V SQUARE WAVE (LIN / BMW BSD / 12V HALL CKP-CMP): Clean pull-up near VBAT (~12V+) and crisp ground pull-down."
        elif 2.1 <= c1_min <= 2.8 and 3.1 <= c1_max <= 4.0:
            diag = "HEALTHY SINGLE-CHANNEL CAN-H: Clean 2.5V recessive to ~3.5V dominant swing."
        elif 1.1 <= c1_min <= 1.9 and 2.1 <= c1_max <= 2.8:
            diag = "HEALTHY SINGLE-CHANNEL CAN-L: Clean 2.5V recessive to ~1.5V dominant swing."
        else:
            diag = f"CUSTOM / DISTORTED SIGNAL: Min {c1_min:.2f}V to Max {c1_max:.2f}V — inspect edges for high resistance, weak inductive spike, or voltage drop."

    report.append(f"Automated Diagnosis: {diag}")
    return "\n".join(report)

def analyze_image_waveform(img_path: str) -> str:
    """
    Sends a scope screenshot (.png/.jpg) to local Ollama vision model (minicpm-v)
    alongside Checkmate's CAN/LIN/BSD waveform standards.
    """
    with open(img_path, "rb") as f:
        b64_img = base64.b64encode(f.read()).decode("utf-8")

    prompt = (
        "You are an automotive oscilloscope diagnostic expert. Inspect this oscilloscope waveform screenshot. "
        "Identify the voltage scale, min/max voltage levels, recessive vs dominant states, and edge quality. "
        "Determine whether it shows High-Speed CAN (2.5V idle, 3.5V/1.5V mirror), Hall/Inductive Crank/Cam (CKP/CMP), Fuel Injector voltage (12V feed, ground pulse, 60V inductive spike & pintle bump), or "
        "LIN/BMW BSD (12V idle, ~1V dominant pulses), or a short to ground/power, and give the exact next diagnostic step."
    )
    try:
        resp = requests.post(
            OLLAMA_URL,
            json={
                "model": VISION_MODEL,
                "prompt": prompt,
                "images": tuple([b64_img]),
                "options": {"num_thread": 4, "temperature": 0.2},
                "stream": False
            },
            timeout=180
        )
        if resp.status_code == 200 and "response" in resp.json():
            return resp.json().get("response", "").strip()
        return (
            f"[Vision Model Not Pulled Yet] To analyze scope screenshots visually, run once in terminal:\n"
            f"  ollama pull {VISION_MODEL}\n"
            f"(Note: Micsig .csv waveform exports work immediately with zero extra models!)"
        )
    except Exception as e:
        return f"[Vision Analysis Notice] {e}"

def upload_waveform(src_path: str):
    src_path = os.path.expanduser(src_path.strip().strip("'\""))
    if not os.path.exists(src_path):
        print(f"[Error] File not found: {src_path}\n")
        return

    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    orig_name = os.path.basename(src_path)
    saved_path = os.path.join(WAVE_DIR, f"{stamp}_{orig_name}")
    shutil.copy2(src_path, saved_path)

    ext = os.path.splitext(orig_name).pop().lower()
    print(f"\n=== CHECKMATE SCOPE WAVEFORM UPLOAD & DIAGNOSIS ===")
    print(f"  Archived File: {saved_path}")

    if ext == ".csv":
        analysis = analyze_csv_waveform(saved_path)
    elif ext in (".png", ".jpg", ".jpeg", ".bmp", ".webp"):
        analysis = analyze_image_waveform(saved_path)
    else:
        print("[Error] Supported formats: .csv (Micsig/Scope data) or .png/.jpg (Scope screenshots)\n")
        return

    print(f"\n{analysis}\n")

    save_kb = input("Save this waveform diagnosis to Checkmate's knowledge/ folder? (y/n): ").strip().lower()
    if save_kb in ("y", "yes"):
        vehicle = input("  Enter Vehicle / Bus Name (e.g., 2010 BMW X5 BSD Bus): ").strip() or orig_name
        slug = re.sub(r"[^a-zA-Z0-9]+", "_", vehicle)[:40].strip("_")
        md_path = os.path.join(KNOWLEDGE_DIR, f"{stamp}_wave_{slug}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# Oscilloscope Capture Analysis: {vehicle}\n")
            f.write(f"- **Date:** {datetime.datetime.now().strftime('%Y-%m-%d %I:%M %p')}\n")
            f.write(f"- **Archived Waveform:** waveforms/{os.path.basename(saved_path)}\n\n")
            f.write(f"## Diagnostic Findings\n```\n{analysis}\n```\n")
        print(f"[Saved to Knowledge Base] -> {md_path}\n")

if __name__ == "__main__":
    it = iter(sys.argv)
    next(it, None)
    cmd = next(it, "").lower()
    arg = next(it, "")
    if cmd == "upload" and arg:
        upload_waveform(arg)
    elif cmd and os.path.exists(os.path.expanduser(cmd)):
        upload_waveform(cmd)
    else:
        print("\n=== CHECKMATE SCOPE WAVEFORM ANALYZER ===")
        print("Usage:")
        print("  run scope_analyzer.py upload <path/to/micsig_capture.csv>")
        print("  run scope_analyzer.py upload <path/to/scope_screenshot.png>\n")
