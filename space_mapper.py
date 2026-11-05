import socket
import threading
import time
import random

# --- NETWORK BOUNDARIES (WINDOWS BASELINE) ---
MY_IP = "192.168.1.11"
TARGET_IP = "192.168.1.10"
PORT = 5005

def network_listener():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(('0.0.0.0', PORT))
        server.listen(2)
        while True:
            conn, addr = server.accept()
            message = conn.recv(1024).decode('utf-8')
            if message == "HEARTBEAT:HELLO":
                print(f"\n[Network Bridge] Linux Ocean Node checked in: 'Hey, I'm here!'")
            conn.close()
    except Exception: pass

def launch_heartbeat():
    while True:
        time.sleep(10)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(2.0)
        try:
            client.connect((TARGET_IP, PORT))
            client.sendall(b"HEARTBEAT:HELLO")
            client.close()
        except (socket.timeout, ConnectionRefusedError): pass

# Start background network threads
threading.Thread(target=network_listener, daemon=True).start()
threading.Thread(target=launch_heartbeat, daemon=True).start()

# --- STANDALONE OUTER SPACE TRAINING LOOP ---
print("\n==============================================================")
print("[+] WINDOWS NODE ACTIVE: Training Topic - OUTER SPACE SECTOR")
print("==============================================================")

sectors = ["Low Earth Orbit", "Lunar Trajectory", "Martian Vector", "Asteroid Belt", "Deep Cosmos"]

try:
    while True:
        distance_au = round(random.uniform(0.1, 5.0), 4)
        active_sector = random.choice(sectors)
        signal_delay = round(distance_au * 499, 1) # Earth-to-probe latency in seconds
        
        print(f" -> [Space Matrix] Target Vector: {active_sector:<18} | Distance: {distance_au:.4f} AU | Telemetry Delay: {signal_delay}s | Status: Scanning Coordinates...")
        time.sleep(1.5)
except KeyboardInterrupt:
    print("\nShutting down space array.")
