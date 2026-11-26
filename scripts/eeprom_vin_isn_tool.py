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

def print_help():
    print("\n=== CHECKMATE EEPROM / ISN / VIN, FRM3 & GM DPS TOOLKIT ===")
    print("  scan <path/to/dump.bin>                 -> Extract 8-bit & 16-bit byte-swapped VINs + hashes")
    print("  frm3 <path/to/dflash_32kb.bin>          -> Recover 4KB EEE EEPROM from corrupted BMW FRM3 D-Flash")
    print("  upa_vin <chip> <hex_offset> <17_VIN>    -> Build UPA-USB .xscr script to write a VIN")
    print("  upa_isn <chip> <hex_offset> <32_HEX>    -> Build UPA-USB .xscr script to write a BMW ISN")
    print("  gmdps <module> <ecu_hex_id> <17_VIN>    -> Build GM DPS UDS ($2E $90) VIN write script\n")

if __name__ == "__main__":
    it = iter(sys.argv)
    next(it, None)
    cmd = next(it, "").lower()




```bash
python3 - << 'EOF'
from scripts.eeprom_vin_isn_tool import swap_16bit_bytes

# 1. Create synthetic 16-bit byte-swapped 93C66 dump
swapped_vin = swap_16bit_bytes(b"JF2SH6CC9AH712345")
dump_93c66 = (b"\xFF" * 64) + swapped_vin + (b"\xFF" * (512 - 64 - 17))
with open("/tmp/test_93c66.bin", "wb") as f:
    f.write(dump_93c66)

# 2. Create synthetic 32KB FRM3 D-Flash dump containing a VIN record at EEE offset 0x0100
dflash = bytearray(b"\xFF" * 32768)
rec = b"\x01\x00\x11WBAFE43589L123456"
dflash = bytearray(rec) + dflash[len(rec):]
with open("/tmp/test_frm3_dflash.bin", "wb") as f:
    f.write(dflash)
