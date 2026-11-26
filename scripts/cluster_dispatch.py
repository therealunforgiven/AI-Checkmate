import os
import re
import sys
import datetime
import concurrent.futures
import requests

KNOWLEDGE_DIR = os.path.expanduser("~/AI-Checkmate/knowledge")
NODES_FILE = os.path.expanduser("~/AI-Checkmate/cluster_nodes.txt")
os.makedirs(KNOWLEDGE_DIR, exist_ok=True)

MODEL = "dolphin-llama3:8b"

def init_nodes_file():
    if not os.path.exists(NODES_FILE):
        with open(NODES_FILE, "w", encoding="utf-8") as f:
            f.write("# List one Ollama worker URL per line (Dynabook #1 local + Dynabook #2 Ethernet IP)\n")
            f.write("http://localhost:11434\n")
            f.write("# http://192.168.1.52:11434\n")

def load_active_nodes() -> tuple:
    init_nodes_file()
    nodes = list()
    with open(NODES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            clean = line.strip()
            if clean and not clean.startswith("#"):
                nodes.append(clean.rstrip("/"))
    return tuple(nodes)

def check_cluster_status():
    nodes = load_active_nodes()
    print("\n=== CHECKMATE ETHERNET CLUSTER STATUS ===")
    online = list()
    for url in nodes:
        try:
            r = requests.get(f"{url}/api/tags", timeout=3)
            if r.status_code == 200:
                models = tuple(m.get("name", "") for m in r.json().get("models", ()))
                print(f"  [ONLINE]  {url}  | Models: {', '.join(models) or 'None'}")
                online.append(url)
            else:
                print(f"  [ERROR]   {url}  | HTTP {r.status_code}")
        except Exception:
            print(f"  [OFFLINE] {url}  | Unreachable (check Ethernet cable or worker_setup.sh)")
    print(f"\nActive Worker Nodes: {len(online)} / {len(nodes)}")
    print(f"Edit node IPs anytime in: {NODES_FILE}\n")
    return tuple(online)

def add_worker_node(ip_or_url: str):
    init_nodes_file()
    clean = ip_or_url.strip().rstrip("/")
    if not clean.startswith("http"):
        clean = f"http://{clean}:11434"
    existing = load_active_nodes()
    if clean in existing:
        print(f"[Info] Node already registered: {clean}\n")
        return
    with open(NODES_FILE, "a", encoding="utf-8") as f:
        f.write(f"{clean}\n")
    print(f"[Added Worker Node] {clean} -> {NODES_FILE}\n")

def run_single_task(node_url: str, task_prompt: str) -> tuple:
    resp = requests.post(
        f"{node_url}/api/generate",
        json={
            "model": MODEL,
            "system": "You are Checkmate, a technical AI assistant for Car and Computer Electric. Provide thorough, structured Markdown technical notes.",
            "prompt": task_prompt,
            "options": {"num_thread": 4, "temperature": 0.2},
            "stream": False
        },
        timeout=600
    )
    answer = resp.json().get("response", "").strip()
    return (node_url, task_prompt, answer)

def dispatch_batch(tasks_file: str):
    tasks_file = os.path.expanduser(tasks_file)
    if not os.path.exists(tasks_file):
        print(f"[Error] Tasks file not found: {tasks_file}\n")
        return

    online_nodes = check_cluster_status()
    if not online_nodes:
        print("[Abort] No online Ollama nodes available.\n")
        return

    tasks = list()
    with open(tasks_file, "r", encoding="utf-8") as f:
        for line in f:
            clean = line.strip()
            if clean and not clean.startswith("#"):
                tasks.append(clean)

    if not tasks:
        print("[Info] No tasks found in file.\n")
        return

    print(f"[Dispatching] Splitting {len(tasks)} tasks across {len(online_nodes)} Dynabook node(s) in parallel ...\n")
    num_nodes = len(online_nodes)

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_nodes) as pool:
        futures = list()
        for idx, task in enumerate(tasks):
            assigned_node = next(u for i, u in enumerate(online_nodes) if i == (idx % num_nodes))
            print(f"  -> Task {idx + 1} assigned to {assigned_node}: {task[:60]}...")
            futures.append(pool.submit(run_single_task, assigned_node, task))

        for fut in concurrent.futures.as_completed(futures):
            node_url, task_text, result_md = fut.result()
            slug = re.sub(r"[^a-zA-Z0-9]+", "_", task_text)[:40].strip("_")
            stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            out_path = os.path.join(KNOWLEDGE_DIR, f"{stamp}_cluster_{slug}.md")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(f"# Cluster Research Note\n- **Node:** {node_url}\n- **Prompt:** {task_text}\n\n{result_md}\n")
            print(f"  [Saved] ({node_url}) -> {os.path.basename(out_path)}")

    print("\n[Cluster Batch Complete] All outputs saved to ~/AI-Checkmate/knowledge/ (type 'sync' in Checkmate to push to GitHub).\n")

def print_help():
    print("\n=== CHECKMATE TWO-DYNABOOK ETHERNET CLUSTER DISPATCHER ===")
    print("  run cluster_dispatch.py status               -> Ping all Dynabook nodes on Ethernet LAN")
    print("  run cluster_dispatch.py add <192.168.1.52>   -> Register second Dynabook's Ethernet IP")
    print("  run cluster_dispatch.py batch <tasks.txt>    -> Split tasks across all online Dynabooks\n")

if __name__ == "__main__":
    it = iter(sys.argv)
    next(it, None)
    cmd = next(it, "").lower()
    arg = next(it, "")
    if cmd == "status":
        check_cluster_status()
    elif cmd == "add" and arg:
        add_worker_node(arg)
    elif cmd == "batch" and arg:
        dispatch_batch(arg)
    else:
        print_help()
