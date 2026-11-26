# Master Automotive Oscilloscope Waveform Guide (CAN, LIN & BMW BSD)
**Car and Computer Electric — Micsig Scope Reference**

## 1. High-Speed CAN Bus (500 kbps — PT-CAN, GMLAN, HS-CAN, CAN-C)
- **Healthy Mirror Image (Normal):**
  - **Recessive State (Idle):** Both `CAN-H` and `CAN-L` sit at **~2.5V** (`CAN-H` = 2.5V, `CAN-L` = 2.5V, Differential = 0V).
  - **Dominant State (Data Bit 0):** `CAN-H` jumps up to **~3.5V** (+1.0V swing) while `CAN-L` drops down to **~1.5V** (-1.0V swing). Differential = **~2.0V**.
  - **Termination Resistance (Battery Disconnected):** **60 Ohms** across `CAN-H` and `CAN-L` (two `120-Ohm` terminating resistors in parallel). **120 Ohms** = one terminating resistor or branch is open/unplugged.
- **Fault Signatures:**
  - **CAN-H Shorted to Ground (0V):** Both `CAN-H` and `CAN-L` flatline near **0V–0.2V** (no mirror switching).
  - **CAN-L Shorted to Ground (0V):** `CAN-L` stays pinned at **0V**; `CAN-H` still tries to pulse between **0V and ~1.0V–2.5V** distorted.
  - **CAN-H or CAN-L Shorted to Battery (+12V):** Affected line pins at **11V–12V+**, pulling the partner line up to **~10V–12V**; zero differential data.
  - **CAN-H and CAN-L Shorted Together:** Both lines mirror each other in the **same direction** (no opposite mirror split) sitting around **~2.5V**.
  - **Missing Termination Resistor (120 Ohms instead of 60 Ohms):** Square-wave corners look rounded, ringing/overshoot spikes appear on edges, and modules intermittently drop offline.

## 2. Single-Wire LIN Bus & BMW BSD (Bit-Serial Data Interface)
- **Healthy Waveform (Normal):**
  - **Recessive State (Idle):** Sits high near **Battery Voltage (`VBAT` = 12.0V–14.2V)** (or ~10.5V–12V on some 12V pull-up LIN branches).
  - **Dominant State (Data Bit 0):** Pulled cleanly down to **~0.8V–1.5V** (must drop below 20% of `VBAT` with crisp square vertical edges).
- **Fault Signatures (BMW BSD: Alternator, Electric Water Pump, Oil Sensor, IBS):**
  - **Flatline at 0V:** A slave node's internal driver (most commonly the **alternator voltage regulator** after a trunk jump-start, or the **electric water pump**) is shorted to ground and holding the entire single-wire bus down. Unplug one node at a time until the 12V square wave returns.
  - **Flatline at 12V (VBAT):** Master node (DME/BCM) is not transmitting wake-up frames, or the wire is open/broken between the DME and the probed sensor.
  - **Slow / Rounded Rising Edges (Shark-Fin Slope):** Excessive capacitance or water/green corrosion inside a connector pulling the pull-up resistor down.

## 3. Fault-Tolerant Low-Speed CAN (125 kbps — BMW K-CAN, Chrysler CAN-B)
- **Healthy Waveform:**
  - **Recessive State:** `CAN-H` rests near **0V–0.2V**; `CAN-L` rests near **4.8V–5.0V** (or ~11V on older 12V K-CAN1).
  - **Dominant State:** `CAN-H` switches up to **~3.6V–4.0V**; `CAN-L` switches down to **~1.0V–1.4V**.
  - **Key Trait:** Unlike High-Speed CAN, Low-Speed K-CAN/CAN-B can often limp along in single-wire mode if one wire opens or shorts, logging a "Single-Wire Operation" fault code.
