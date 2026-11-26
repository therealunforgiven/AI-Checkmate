import os
import sys
import time
import subprocess

BASE_DIR = os.path.expanduser("~/AI-Checkmate")
sys.path.insert(0, BASE_DIR)
import checkmate
from scripts.knowledge_index import rebuild_index

TOPICS_FILE = os.path.join(BASE_DIR, "night_topics.txt")

def run_overnight_study():
    if not os.path.exists(TOPICS_FILE):
        print("[Error] night_topics.txt not found.")
        return

    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        topics = tuple(line.strip() for line in f if line.strip() and not line.startswith("#"))

    print(f"=== OVERNIGHT KNOWLEDGE BUILDER STARTING ({len(topics)} TOPICS) ===")
    for idx, topic in enumerate(topics, 1):
        print(f"\n[{idx}/{len(topics)}] Researching & Indexing: {topic}")
        try:
            checkmate.search_and_learn(topic)
        except Exception as e:
            print(f"  [Warning] Skipped due to error: {e}")
        time.sleep(3)

    print("\n[Rebuilding Fast SQLite FTS5 Search Index] ...")
    rebuild_index()

    print("[Pushing Overnight Research to GitHub] ...")
    subprocess.run(("git", "add", "knowledge/"), cwd=BASE_DIR)
    subprocess.run(("git", "commit", "-m", "Add overnight researched automotive diagnostic guides"), cwd=BASE_DIR)
    subprocess.run(("git", "push", "origin", "main"), cwd=BASE_DIR)
    print("\n=== OVERNIGHT RUN COMPLETE! ALL GUIDES INDEXED & SYNCED ===")

if __name__ == "__main__":
    run_overnight_study()
