import os
import re
import sys
import hashlib

STARTER_DIR = os.path.expanduser("~/AI-Checkmate/starter_files")
os.makedirs(STARTER_DIR, exist_ok=True)

WIN_KEY_REGEX = re.compile(rb"[BCDFGHJKMPQRTVWXY2346789]{5}-[BCDFGHJKMPQRTVWXY2346789]{5}-[BCDFGHJKMPQRTVWXY2346789]{5}-[BCDFGHJKMPQRTVWXY2346789]{5}-[BCDFGHJKMPQRTVWXY2346789]{5}")

def generate_starter_templates():
    """Creates verified blank 0xFF starter binary templates for common automotive & laptop chips."""
    specs = (
        ("BLANK_95080_1KB.bin", 1024),
        ("BLANK_95160_2KB.bin", 2048),
        ("BLANK_95320_4KB.bin", 4096),
        ("BLANK_24C16_2KB.bin", 2048),
        ("BLANK_93C66_512B.bin", 512),
        ("BLANK_BMW_FRM3_EEE_4KB.bin", 4096),
        ("BLANK_25Q64_8MB_BIOS.bin", 8388608),
        ("BLANK_25Q128_16MB_BIOS.bin", 16777216),
    )
    print("\n=== GENERATING CLEAN STARTER .BIN TEMPLATES ===")
    for fname, size in specs:
        fpath = os.path.join(STARTER_DIR, fname)
        if not os.path.exists(fpath):
            with open(fpath, "wb") as f:
                f.write(b"\xFF" * size)
        print(f"  [Ready] {fname} ({size:,} bytes)")
    print(f"Saved inside: {STARTER_DIR}\n")

def analyze_laptop_bios(bin_path: str):
    """Scans a laptop SPI BIOS dump (25Q64 / 25Q128 / 25Q256) for Flash Descriptor, Intel ME, Windows MSDM Key & Serial."""
    bin_path = os.path.expanduser(bin_path.strip().strip("'\""))
    if not os.path.exists(bin_path):
        print(f"[Error] BIOS dump not found: {bin_path}\n")
        return

    with open(bin_path, "rb") as f:
        data = f.read()

    sha = hashlib.sha256(data).hexdigest()
    print(f"\n=== LAPTOP SPI BIOS / EC DUMP ANALYSIS: {os.path.basename(bin_path)} ===")
    print(f"  Chip Size:   {len(data):,} bytes ({len(data)//1024:,} KB / {len(data)//1048576} MB)")
    print(f"  SHA-256:     {sha}")

    # 1. Check Intel Flash Descriptor Signature (5A A5 F0 0F at 0x10)
    has_fd = (len(data) >= 20 and data[16:20] == b"\x5A\xA5\xF0\x0F")
    print(f"  Intel FD:    {'FOUND (Valid 5A A5 F0 0F Descriptor at 0x10)' if has_fd else 'Not at 0x10 (EC/KBC dump or AMD/Non-IFD BIOS)'}")

    # 2. Check Intel ME Region Signature ($FPT)
    fpt_pos = data.find(b"$FPT")
    print(f"  Intel ME:    {'FOUND ($FPT Partition Table at 0x' + f'{fpt_pos:06X})' if fpt_pos != -1 else 'No $FPT header detected'}")

    # 3. Extract Embedded Windows 10/11 OEM Product Key (MSDM ACPI Table)
    keys = tuple(WIN_KEY_REGEX.finditer(data))
    print(f"  Windows Key: {len(keys)} embedded MSDM OEM key(s) found")
    for k in keys:
        print(f"    -> Offset 0x{k.start():06X}: {k.group(0).decode('ascii')}")

    # 4. Check for DMI / Service Tag / Serial strings (Toshiba/Dynabook, Dell, HP, Lenovo)
    for tag in (b"Dynabook", b"TOSHIBA", b"TECRA", b"Latitude", b"ThinkPad", b"ProBook", b"EliteBook"):
        pos = data.find(tag)
        if pos != -1:
            snippet = "".join(chr(b) if 32 <= b <= 126 else "." for b in data[pos:pos+48])
            print(f"  DMI String:  0x{pos:06X} -> {snippet}")
    print()

def show_laptop_chip_guide():
    print("\n=== LAPTOP SPI BIOS & EC FLASHING BENCH GUIDE (3.3V / 1.8V) ===")
    print("  1. Common Laptop BIOS Chips (SOIC-8 Wide 200mil / WSON-8):")
    print("     - 25Q32 (4MB) | 25Q64 (8MB) | 25Q128 (16MB) | 25Q256 (32MB)")
    print("     - WARNING: '25Q64FW' / '25Q128FW' / '25LQ64' ('W' or 'L' = 1.8V Low-Voltage!).")
    print("       Always use a 1.8V SPI Adapter on CH341A/T48 for 'FW'/'LQ' chips or you will fry the chip!")
    print("  2. Dynabook / Toshiba Tecra A40-J Recovery Workflow:")
    print("     - Unplug AC adapter AND disconnect internal main battery + CMOS coin cell before clipping.")
    print("     - Read original 25Q128/25Q256 twice, verify identical SHA-256 hashes, and extract Windows Key/DMI first.")
    print("     - Copy your original DMI block (Serial/Model/Windows Key) into the clean donor BIOS before flashing.\n")

if __name__ == "__main__":
    it = iter(sys.argv)
    next(it, None)
    cmd = next(it, "").lower()
    arg = next(it, "")
    if cmd == "init":
        generate_starter_templates()
    elif cmd == "scan" and arg:
        analyze_laptop_bios(arg)
    else:
        show_laptop_chip_guide()
