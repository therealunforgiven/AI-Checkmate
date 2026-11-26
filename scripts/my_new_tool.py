


import sys
import requests

# Starter template for your custom Checkmate scripts
# Usage from Checkmate: run hello_template.py "Your question here"

PROMPT = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Give me 3 quick tips for testing a 12V automotive relay."

resp = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "dolphin-llama3:8b",
        "prompt": PROMPT,
        "options": {"num_thread": 4, "temperature": 0.2},
        "stream": False
    },
    timeout=120
)
print("\n[hello_template.py Output]\n" + resp.json().get("response", "").strip() + "\n")
