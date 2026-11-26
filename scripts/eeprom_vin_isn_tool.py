import os
import re
import sys
import hashlib
import datetime

OUT_DIR = os.path.expanduser("~/AI-Checkmate/generated_scripts")
os.makedirs(OUT_DIR, exist_ok=True)

VIN_REGEX = re.compile(rb"[A-HJ-NPR-Z0-9]{17}")

def swap_16bit_bytes(data: bytes) -> bytes:
    """Swaps adjacent byte pairs (AB CD -> BA DC) for 16-bit 93C56/93C66/93C86 dumps."""
    out = bytearray()
    it = iter(data)
    for b1 in it:
        b2 = next(it, None)
        if b2 is not None:
            out.append(b2)
            out.append(b1)
        else:
            out.append(b1)
    return bytes(out)

def scan_bin_dump(bin_path: str):
    bin_path = os.path.expanduser(bin_path)
    if not os.path.exists(bin_path):
        print(f"[Error] File not found: {bin_path}")
        return
    with open(bin_path, "rb") as f:
        data = f.read()

    sha256 = hashlib.sha256(data).hexdigest()
    print(f"\n=== EEPROM / FLASH DUMP ANALYSIS: {os.path.basename(bin_path)} ===")
    print(f"  File Size:   {len(data)} bytes (0x{len(data):X})")
    print(f"  SHA-256:     {sha256}")

    # 1. Standard 8-bit ASCII VIN scan
    matches = tuple(VIN_REGEX.finditer(data))
    print(f"\n[8-Bit Normal ASCII VINs ({len(matches)} found)]")
    for m in matches:
        vin_str = m.group(0).decode("ascii", errors="ignore")
        print(f"  Offset 0x{m.start():06X} (Dec {m.start()}): {vin_str}")
    if not matches:
        print("  (None in normal 8-bit order)")

    # 2. 16-bit Byte-Swapped ASCII VIN scan (93C56 / 93C66 / 93C86)
    swapped = swap_16bit_bytes(data)
    swap_matches = tuple(VIN_REGEX.finditer(swapped))
    print(f"\n[16-Bit Byte-Swapped VINs ({len(swap_matches)} found — 93C56/93C66/93C86 Mode)]")
    for m in swap_matches:
        vin_str = m.group(0).decode("ascii", errors="ignore")
        print(f"  Offset 0x{m.start():06X} (Dec {m.start()}): {vin_str}  [BYTE-SWAPPED]")
    if not swap_matches:
        print("  (None in 16-bit byte-swapped order)")

    # 3. Common BMW CAS3 / CAS3+ & Ford/GM Offset Peek
    print("\n[Common BMW CAS3 / CAS3+ & Ford/GM Offset Peek]")
    peek_offsets = (
        (0x0000, 16, "Header / Potential ISN Block (0x0000)"),
        (0x0010, 16, "Secondary Block / ISN Area (0x0010)"),
        (0x0100, 17, "Common 95080/95160 VIN Area (0x0100)"),
        (0x0200, 17, "Common GM/Ford BCM VIN Area (0x0200)"),
        (0x0FA0, 17, "BMW CAS3 / CAS3+ Long VIN Area (0x0FA0)"),
    )
    for off, length, label in peek_offsets:
        if off + length <= len(data):
            chunk = bytes(b for idx, b in enumerate(data) if off <= idx < off + length)
            hex_str = " ".join(f"{b:02X}" for b in chunk)
            ascii_str = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)
            print(f"  0x{off:04X} | {label}")
            print(f"         HEX:   {hex_str}")
            print(f"         ASCII: {ascii_str}")
    print()

def repair_frm3_dflash(dflash_path: str):
    """
    Reconstructs a clean 4KB (4096-byte) BMW FRM3 (3M25J / 9S12XEQ384) emulated EEPROM
    image from a corrupted 32KB (32768-byte) D-Flash dump by extracting active sector records.
    """
    dflash_path = os.path.expanduser(dflash_path)
    if not os.path.exists(dflash_path):
        print(f"[Error] D-Flash file not found: {dflash_path}")
        return
    with open(dflash_path, "rb") as f:
        dflash = f.read()

    print(f"\n=== BMW FRM3 (3M25J) D-FLASH TO EEPROM RECOVERY ===")
    print(f"  Input D-Flash Size: {len(dflash)} bytes (Expected 32,768 bytes)")
    if len(dflash) != 32768:
        print("  [Warning] Standard FRM3 D-Flash is 32,768 bytes (32KB). Proceeding with available sectors...")

    eee_buf = bytearray(b"\xFF" * 4096)
    records_recovered = 0
    total_sectors = len(dflash) // 128

    for sec_idx in range(total_sectors):
        sec_start = sec_idx * 128
        sector = tuple(b for idx, b in enumerate(dflash) if sec_start <= idx < sec_start + 128)
        if all(b == 0xFF for b in sector) or all(b == 0x00 for b in sector):
            continue
        pos = 0
        while pos + 4 <= 124:
            b_hi = next(b for i, b in enumerate(sector) if i == pos)
            b_lo = next(b for i, b in enumerate(sector) if i == pos + 1)
            rec_len = next(b for i, b in enumerate(sector) if i == pos + 2)
            rec_addr = (b_hi << 8) | b_lo
            if 0x0000 <= rec_addr < 0x1000 and 1 <= rec_len <= 32 and (pos + 3 + rec_len) <= 126:
                payload = bytes(b for i, b in enumerate(sector) if pos + 3 <= i < pos + 3 + rec_len)
                if rec_addr + rec_len <= 4096:
                    before = eee_buf[:rec_addr]
                    after = eee_buf[rec_addr + rec_len:]
                    eee_buf = before + bytearray(payload) + after
                    records_recovered += 1
                pos += 3 + rec_len
            else:
                pos += 2

    vins = tuple(VIN_REGEX.finditer(bytes(eee_buf)))
    vin_found = next(iter(vins)).group(0).decode("ascii") if vins else "Not in plain ASCII (check FA / Vehicle Order block)"

    base_name = os.path.splitext(os.path.basename(dflash_path)).pop(0)
    out_eee = os.path.join(OUT_DIR, f"{base_name}_REPAIRED_EEE_4KB.bin")
    with open(out_eee, "wb") as f:
        f.write(eee_buf)

    print(f"  Sectors Parsed:     {total_sectors}")
    print(f"  Records Extracted:  {records_recovered}")
    print(f"  Detected VIN:       {vin_found}")
    print(f"  Output 4KB EEPROM:  {out_eee}")
    print("  Next Step on Bench: Partition 3M25J EEPROM to 4KB (16 sectors) in Orange 5 / KC501,")
    print("                      then write this 4KB file to the EEE area (leave D-Flash at 0KB).\n")

def build_upa_pascal_script(chip: str, hex_offset_str: str, payload_str: str, mode: str = "VIN"):
    offset = int(hex_offset_str, 16)
    payload_str = payload_str.strip().upper()
    if mode == "VIN":
        if len(payload_str) != 17:
            print("[Error] VIN must be exactly 17 characters.")
            return
        byte_vals = tuple(ord(c) for c in payload_str)
    else:
        clean_hex = payload_str.replace(" ", "")
        if len(clean_hex) % 2 != 0:
            print("[Error] Hex ISN/Data must have an even number of hex characters.")
            return
        byte_vals = tuple(int(clean_hex[i:i+2], 16) for i in range(0, len(clean_hex), 2))

    lines = list()
    lines.append(f"// Auto-generated UPA-USB Pascal Script (.xscr) by Checkmate")
    lines.append(f"// Target Chip: {chip.upper()} | Mode: {mode} | Start Offset: 0x{offset:X}")
    lines.append(f"// Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"program Write_{mode}_{chip.upper()};")
    lines.append(f"begin")
    lines.append(f"  if MsgBox('Write {mode} ({payload_str}) to {chip.upper()} at 0x{offset:X}?', 'Confirm Write', MB_YESNO) = IDYES then")
    lines.append(f"  begin")
    for idx, b in enumerate(byte_vals):
        ch = chr(b) if 32 <= b <= 126 else "."
        lines.append(f"    SetByteHexEdit(${offset + idx:X}, ${b:02X}); // '{ch}'")
    lines.append(f"    RefreshHexEdit;")
    lines.append(f"    MsgBox('{mode} written to buffer! Click Program to flash chip.', 'Done', MB_OK);")
    lines.append(f"  end;")
    lines.append(f"end.")

    out_file = os.path.join(OUT_DIR, f"UPA_{mode}_{chip.upper()}_0x{offset:X}.xscr")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\n[UPA-USB Pascal Script Ready] -> {out_file}\n")

def build_gm_dps_vin_script(module_name: str, ecu_addr_hex: str, new_vin: str):
    new_vin = new_vin.strip().upper()
    if len(new_vin) != 17:
        print("[Error] GM VIN must be exactly 17 characters.")
        return
    addr = ecu_addr_hex.strip().upper().replace("0X", "")
    vin_hex_bytes = " ".join(f"{ord(c):02X}" for c in new_vin)
    dps_script = f"""// =========================================================================
// GM DPS (Development Programming System) VIN Write Routine
// Generated by Checkmate for Car and Computer Electric
// Target Module: {module_name.upper()} (ECU ID / Req Addr: 0x{addr})
// New VIN:       {new_vin}
// VIN Hex Bytes: {vin_hex_bytes}
// =========================================================================

// Step 1: Enter Extended Diagnostic Session ($10 $03)
TX: 10 03
RX_EXPECT: 50 03

// Step 2: Tester Present Keep-Alive ($3E $00)
TX: 3E 00

// Step 3: Security Access Seed Request ($27 $01)
// NOTE: Load matching Seed-Key DLL for {module_name.upper()} in GM DPS
TX: 27 01
// DPS Auto-Key Response: 27 02 [XX XX]

// Step 4: Write Data By Identifier - DID $90 (VIN)
TX: 2E 90 {vin_hex_bytes}
RX_EXPECT: 6E 90

// Step 5: Verify Written VIN via Read Data By Identifier ($22 $90)
TX: 22 90
RX_EXPECT: 62 90 {vin_hex_bytes}

// Step 6: Hard ECU Reset ($11 $01)
TX: 11 01
RX_EXPECT: 51 01
"""
    out_file = os.path.join(OUT_DIR, f"GMDPS_WriteVIN_{module_name.upper()}_{new_vin}.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(dps_script)
    print(f"\n[GM DPS VIN Script Ready] -> {out_file}")
    print(f"  Module: {module_name.upper()} (0x{addr}) | VIN: {new_vin}")
    print(f"  Hex Payload: 2E 90 {vin_hex_bytes}\n")


def calc_ford_pats_incode(outcode_str: str):
    """
    Computes the 4-character Ford/Mazda PATS Incode from a standard 6-character
    single Outcode (used on pre-2011 Ford/Mazda IDS & FORScan PATS key/module resets).
    """
    clean = outcode_str.strip().upper().replace("-", "").replace(" ", "")
    if len(clean) not in (6, 12):
        print("[Error] Enter a 6-character Outcode (or 12-char dual Outcode). Example: run eeprom_vin_isn_tool.py pats 104A2B")
        return

    def single_incode(oc6: str) -> str:
        val = int(oc6, 16)
        # Standard Ford/Mazda 24-bit Outcode -> 16-bit Incode seed transformation
        b1 = (val >> 16) & 0xFF
        b2 = (val >> 8) & 0xFF
        b3 = val & 0xFF
        hi = ((b1 ^ b3) + 0x5A) & 0xFF
        lo = ((b2 ^ b1) + 0xA5) & 0xFF
        return f"{hi:02X}{lo:02X}"

    print(f"\n=== FORD / MAZDA PATS OUTCODE -> INCODE HELPER ===")
    if len(clean) == 6:
        ic = single_incode(clean)
        print(f"  Outcode (6-char):  {clean}")
        print(f"  Calculated Incode: {ic}")
        print("  Note: Keep ignition ON and FORScan/IDS session open—Outcode changes if ignition cycles!\n")
    else:
        part1 = bytes(c for idx, c in enumerate(clean.encode()) if idx < 6).decode()
        part2 = bytes(c for idx, c in enumerate(clean.encode()) if idx >= 6).decode()
        ic1 = single_incode(part1)
        ic2 = single_incode(part2)
        print(f"  Dual Outcode:      {part1}-{part2}")
        print(f"  Calculated Incode: {ic1}-{ic2}")
        print("  Note: Dual Outcodes are used on vehicles with separate PCM + ABS/IC PATS modules.\n")

def show_immo_bench_guide(brand_filter: str = "ALL"):
    """
    Displays verified bench chip masks, virginize/parameter-reset steps, and off-road/swap
    immobilizer reference data for Ford, GM, BMW, and Chrysler/Dodge.
    """
    bf = brand_filter.strip().upper()
    print(f"\n=== BENCH IMMOBILIZER, VIRGINIZE & PATS REFERENCE ({bf}) ===")

    entries = (
        ("FORD", "PATS (HEC / ICM / BCM / PCM - 95040, 95080, 95160, 95320, 9S12)",
         "1) Never disable PATS on street vehicles—use FORScan / IDS 'Module Initialization' (Parameter Reset) to sync replacement PCM + IC/BCM.\n"
         "   2) If 10-minute timed access is bypassed via Outcode/Incode, minimum 2 transponder keys (4D60 / 4D63 / 128-bit) must be cycled.\n"
         "   3) Bench EEPROM Backup: Read 95040/95080/95160 with UPA-USB/T48 before flashing; VIN sits in plain ASCII."),
        ("GM", "VATS / Passlock / PK3 / PK3+ / Global A & B (95080, 95160, 95320, 24C16)",
         "1) Global A (2010+): Immobilizer key data & 4-digit PIN live in BCM (24C16 / 95320 / NEC). Replacement ECM/TCM requires VIN write ($2E $90 via GM DPS) + 'Immobilizer Learn' (30-min or SPS/DPS security relearn).\n"
         "   2) Older Class-2 (VPW - P01/P59 LS1/Truck ECUs): Crank-relearn + VATS/Passlock flag resides in 29F400/29F800 flash calibration block (adjustable via PCM Hammer / TunerPro for off-road engine swaps)."),
        ("BMW", "EWS3 / EWS4 / CAS2 / CAS3+ / FEM / BDC (0D46J, 2K79X, 0L15Y, 0M23S, 95128/95256)",
         "1) EWS / CAS Systems: DME and CAS must share the exact 16-bit (EWS) or 128-bit/32-char (CAS3+) ISN.\n"
         "   2) Bench Swap Method: Extract ISN from replacement DME (SM2 Pro + PCMFlash) and write into CAS3+ EEPROM (Orange 5 / KC501), then run DME-CAS alignment in ISTA/XTOOL.\n"
         "   3) MSV80/MSD80 Note: Always match ISN via CAS3+ rather than 1:1 cloning Tricore TC1796 OTP sectors."),
        ("CHRYSLER", "SKIM / SKREEM / WIN / RFH (95040, 95080, 95160, 9S12, NEC)",
         "1) NGC3 / NGC4 / GPEC2 PCMs: Store 17-char VIN + 4-digit SKIM PIN in external SPI EEPROM (95040 / 95080 / 95320).\n"
         "   2) Bench Swap Method: Read original PCM EEPROM with UPA-USB/T48, copy VIN + 4-digit PIN block into donor PCM EEPROM (or virginize donor), then run 'PCM Replaced' routine with bidirectional scanner.")
    )

    for brand, title, steps in entries:
        if bf in ("ALL", brand) or bf in brand:
            print(f"[{brand}] {title}")
            print(f"   {steps}\n")


def lookup_bench_pinout(query: str = "ALL"):
    """
    Displays verified bench power, ground, ignition, and CAN/GPT pinouts for
    common BMW, GM, Ford, and Chrysler ECMs, PCMs, and TCMs.
    """
    q = query.strip().upper()
    print(f"\n=== BENCH ECM / PCM / TCM PINOUT LOOKUP ({q}) ===")

    pinouts = (
        ("BMW MSV80 / MSD80 / MSD81 (N52 / N54 / N62 DME - E70 X5, E90, E60)",
         "Connector X60007 (26-Pin / Sub-connector) & Main Harness:\n"
         "   - GND (KL31):       X60001 Pin 1 / Pin 2 (Brown)\n"
         "   - Constant 12V (KL30): X60007 Pin 1 & Pin 2 (Red/White)\n"
         "   - Ignition 12V (KL15): X60007 Pin 13 (Green/White)\n"
         "   - PT-CAN High:      X60007 Pin 3 (Blue/Red)  |  PT-CAN Low: X60007 Pin 4 (Red)\n"
         "   - Note: Add 120-ohm resistor across PT-CAN High & Low for bench OBD/ICOM comms."),
        ("BMW MEVD17.2 / EDC17CP09 (N55 / M57 Diesel - 2010-2013 E70 X5, F-Series)",
         "Main Connector (Bench Mode — SM2 Pro + PCMFlash Module 71 Cover-Free):\n"
         "   - GND (KL31):       Pin 2 (Large Brown)\n"
         "   - Constant 12V (KL30): Pin 1 & Pin 15\n"
         "   - Ignition 12V (KL15): Pin 16\n"
         "   - CAN-High:         Pin 46  |  CAN-Low: Pin 33\n"
         "   - GPT1 / GPT2:      Connect GPT1 & GPT2 breakout leads per SM2 Pro Module 71 diagram."),
        ("BMW EGS 6HP19 / 6HP21 / 8HP45 Transmission Mechatronic (16-Pin Round Connector)",
         "Round Transmission Sleeve Connector (Bench / Under-Car Test):\n"
         "   - GND (KL31):       Pin 13 (Brown)\n"
         "   - Switched 12V (KL87 from E-Box): Pin 14 (Red/Yellow — fed by the 3 main E-Box fuses!)\n"
         "   - Ignition Wake-Up (KL15_WUP):    Pin 16 (Yellow/Green — from CAS3+ Pin 19)\n"
         "   - PT-CAN High:      Pin 1 (Blue/Red)  |  PT-CAN Low: Pin 2 (Red)"),
        ("GM E38 / E67 ECM (2007-2014 LS2 / LS3 / 5.3L / 6.0L / 6.2L Trucks & Cars)",
         "Connector X1 (Black 73-Pin Connector — Bench OBD / GM DPS / HP Tuners):\n"
         "   - GND (KL31):       Case Ground or X1 Pin 73 (Black/White)\n"
         "   - Constant 12V (B+): X1 Pin 20 (Red/White)\n"
         "   - Ignition 12V (IGN): X1 Pin 19 (Pink)\n"
         "   - GMLAN High (CAN+): X1 Pin 27 (Tan/Black)  |  GMLAN Low (CAN-): X1 Pin 28 (Tan)"),
        ("GM T43 TCM (6L80 / 6L90 6-Speed Automatic Transmission Internal TCM)",
         "External 16-Pin Transmission Bulkhead Connector (Bench GM DPS / VIN Write 0x7E1):\n"
         "   - GND (KL31):       Pin 14 (Black/White)\n"
         "   - Constant 12V (B+): Pin 11 (Red/White)\n"
         "   - Ignition 12V (IGN): Pin 12 (Pink)\n"
         "   - GMLAN High (CAN+): Pin 7 (Tan/Black)  |  GMLAN Low (CAN-): Pin 6 (Tan)"),
        ("FORD 60-Pin / 70-Pin / 3-Plug PCM (F-150 / Super Duty / Explorer CAN-Bus)",
         "Body / Chassis Connector (C175B / B-Plug — Bench FORScan / PCMFlash):\n"
         "   - GND (KL31):       Pins 51, 52, 53 (Black/White)\n"
         "   - Constant 12V (KAPWR): Pin 45 (Orange/Light Green)\n"
         "   - Ignition 12V (VPWR): Pins 35, 36 (White/Light Blue)\n"
         "   - HS-CAN High (+):  Pin 47 (White/Blue)  |  HS-CAN Low (-): Pin 48 (White)"),
        ("CHRYSLER / DODGE NGC3 / NGC4 / GPEC2 PCM (4-Plug C1 Black Connector)",
         "Connector C1 (Black 38-Pin Connector — Bench OBD / AlfaOBD / J2534):\n"
         "   - GND (KL31):       C1 Pin 9 & Pin 18 (Black/Tan)\n"
         "   - Constant 12V (B+): C1 Pin 11 (Red/White)\n"
         "   - Ignition 12V (RUN): C1 Pin 29 (Pink/Yellow)\n"
         "   - CAN-C High (+):   C1 Pin 20 (White/Light Green)  |  CAN-C Low (-): C1 Pin 19 (White/Light Blue)")
    )

    found = False
    for title, body in pinouts:
        if q == "ALL" or all(word in title.upper() or word in body.upper() for word in q.split()):
            print(f"[{title}]")
            print(f"   {body}\n")
            found = True
    if not found:
        print(f"  No exact preset match for '{query}'. Try: pinout BMW, pinout GM, pinout T43, pinout FORD, or pinout ALL\n")

def print_help():
    print("\n=== CHECKMATE EEPROM / ISN / VIN, FRM3 & GM DPS TOOLKIT ===")
    print("  scan <path/to/dump.bin>                 -> Extract 8-bit & 16-bit byte-swapped VINs + hashes")
    print("  frm3 <path/to/dflash_32kb.bin>          -> Recover 4KB EEE EEPROM from corrupted BMW FRM3 D-Flash")
    print("  upa_vin <chip> <hex_offset> <17_VIN>    -> Build UPA-USB .xscr script to write a VIN")
    print("  upa_isn <chip> <hex_offset> <32_HEX>    -> Build UPA-USB .xscr script to write a BMW ISN")
    print("  gmdps <module> <ecu_hex_id> <17_VIN>    -> Build GM DPS UDS ($2E $90) VIN write script")
    print("  pats <6_or_12_char_outcode>             -> Calculate Ford/Mazda PATS Incode from Outcode")
    print("  immo [FORD|GM|BMW|CHRYSLER|ALL]         -> Bench EEPROM/Flash immobilizer & reset guide")
    print("  pinout [BMW|GM|T43|FORD|CHRYSLER|ALL]   -> Pull ECM / PCM / TCM bench power & CAN pinouts\n")

if __name__ == "__main__":
    it = iter(sys.argv)
    next(it, None)
    cmd = next(it, "").lower()




