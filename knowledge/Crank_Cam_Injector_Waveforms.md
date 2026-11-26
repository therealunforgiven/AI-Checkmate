# Master Crankshaft (CKP), Camshaft (CMP) & Fuel Injector Waveform Guide
**Car and Computer Electric — Micsig Scope Reference**

## 1. Crankshaft (CKP) & Camshaft (CMP) Sensor Waveforms
### A. Hall-Effect / Magnetoresistive (3-Wire Digital — Most BMW, Modern GM, Ford, Chrysler)
- **Healthy Waveform:**
  - Crisp **0V to 5V** (or **0V to 12V** pull-up) digital square wave with vertical rising and falling edges.
  - **Missing-Tooth Sync Gap (e.g., 60-2 or 36-1 trigger wheel):** Regular evenly spaced square pulses interrupted by a single wider pulse gap once per crank revolution.
  - **Cam/Crank Correlation:** The Cam (`CMP`) rising/falling edge must align consistently with the exact same tooth count after the Crank (`CKP`) missing-tooth gap on every revolution.
- **Fault Signatures:**
  - **Stuck at 5V / 12V (No Pulses):** Open ground wire, sensor air-gap too wide, broken reluctor wheel, or dead Hall sensor.
  - **Stuck at 0V:** Signal wire shorted to ground, or missing 5V/12V pull-up reference voltage from the DME/PCM.
  - **Shifted Cam Edge Relative to Crank Sync Gap:** Stretched timing chain, jumped timing tooth, or stuck VANOS / VVT cam phaser.

### B. Inductive / Variable Reluctance (2-Wire AC Analog — Older Crank/Cam & Wheel Speed Sensors)
- **Healthy Waveform:**
  - Analog **AC sine wave** crossing **0V** symmetrically (+V peak above 0V, -V peak below 0V).
  - Amplitude grows with engine RPM: **~1.5V–4.0V peak-to-peak** at cranking speed (~200 RPM), rising to **10V–40V+ peak-to-peak** at higher RPM.
  - **Sync Gap:** Amplitude spikes slightly larger right at the missing-tooth gap (`60-2` / `36-1`).
- **Fault Signatures:**
  - **Weak Amplitude (<0.5V peak-to-peak during cranking):** Excessive sensor air gap, metal shavings on magnet tip, or weak internal coil (DME will not see RPM or fire injectors/coils).
  - **Flatline at 0V:** Open sensor coil or shorted twisted-pair harness.

---

## 2. Fuel Injector Voltage & Current-Ramp Waveforms
### A. Standard 12V Saturated Port Fuel Injector (PFI — e.g., BMW N52 MSV80, GM LS, Ford, Chrysler)
- **Healthy Voltage Waveform (Probed at DME Ground-Control Pin):**
  1. **Idle (Injector Off):** Sits flat at **Battery Voltage (`VBAT` = 12.0V–14.2V)** fed through `Terminal 87` (DME Main Relay).
  2. **Turn-On (Injection Pulse):** DME switches ground ON → voltage drops cleanly to **~0.2V–0.8V** for **1.5ms–3.5ms** (warm idle) or **8ms–15ms** (cold crank).
  3. **Turn-Off Inductive Kick & Pintle Bump:** When the DME releases ground, the magnetic field collapses and creates a sharp **inductive voltage spike of ~55V–80V** (clamped by the DME's internal Zener/MOSFET), followed by a small **pintle-closing hump** on the falling tail as the injector needle physically snaps shut.
- **Fault Signatures:**
  - **0V Before Turn-On:** Missing `Terminal 87` (`KL87`) relay power feed (check those 3 main E-Box fuses on BMW!) or open injector coil.
  - **Voltage Only Drops to ~3V–5V During Pulse:** High-resistance ground driver MOSFET inside DME (`MSV80` `30BA`/`30BB` fault) or poor DME ground.
  - **Missing Inductive Spike (<20V) or Missing Pintle Bump:** Shorted injector windings or mechanically stuck/clogged injector pintle.

### B. High-Pressure Direct Injection (GDI / Piezo & Solenoid — BMW N54/N55/N63 MSD80/MEVD17, GM SIDI, Ford EcoBoost)
- **Healthy Waveform (Requires Differential / High-Voltage Attenuator Probe):**
  - Uses a **65V–150V+ high-voltage boost phase** to crack the injector open against high rail pressure, followed by a **Peak-and-Hold** current modulation (~10A–15A peak, dropping to ~3A–5A hold).
  - **Safety Warning:** Never probe GDI/Piezo injector wires directly with a standard 1x scope lead—always use a **10x or 20x attenuator** and keep hands off while cranking/running.
