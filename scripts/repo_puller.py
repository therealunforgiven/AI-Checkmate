import os
import re
import sys
import shutil
import subprocess

BASE_DIR = os.path.expanduser("~/AI-Checkmate")
EXT_DIR = os.path.join(BASE_DIR, "external_repos")
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge")
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
os.makedirs(EXT_DIR, exist_ok=True)

def pull_github_repo(repo_input: str, import_mode: str = "all"):
    """
    Clones or updates any public GitHub repo (accepts 'user/repo' or full 'https://github.com'),
    lists all .py training scripts and model weights (.zip/.pt/.pth/.onnx/.gguf), and optionally
    imports docs into knowledge/ + rebuilds the SQLite FTS5 search index.
    """
    clean = repo_input.strip().rstrip("/")
    if clean.endswith(".git"):
        clean = clean[:-4]
    if not clean.startswith("http"):
        clean = f"https://github.com{clean}"

    repo_name = clean.split("/").pop()
    target_dir = os.path.join(EXT_DIR, repo_name)

    print(f"\n=== GITHUB TRAINING REPO PULLER: {repo_name} ===")
    if os.path.exists(os.path.join(target_dir, ".git")):
        print(f"[Updating Existing Repo] Pulling latest changes in {target_dir} ...")
        subprocess.run(("git", "-C", target_dir, "pull"), check=False)
    else:
        print(f"[Cloning Repo] {clean} -> {target_dir} ...")
        res = subprocess.run(("git", "clone", "--depth", "1", clean, target_dir), capture_output=True, text=True)
        if res.returncode != 0:
            print(f"[Error] Clone failed: {res.stderr.strip()}\n")
            return

    py_files = list()
    model_files = list()
    doc_files = list()

    for root_p, dirs, files in os.walk(target_dir):
        if ".git" in root_p:
            continue
        for fn in sorted(files):
            full_p = os.path.join(root_p, fn)
            low = fn.lower()
            if low.endswith(".py"):
                py_files.append(full_p)
            elif low.endswith((".zip", ".pt", ".pth", ".onnx", ".safetensors", ".gguf", ".bin", ".h5")):
                model_files.append(full_p)
            elif low.endswith((".md", ".txt")) and os.path.getsize(full_p) < 250000:
                doc_files.append(full_p)

    print(f"\n[Found in {repo_name}]")
    print(f"  Python Scripts ({len(py_files)}):")
    for p in py_files[:15]:
        print(f"    - {os.path.relpath(p, target_dir)}")

    print(f"  Model / Dataset Weights ({len(model_files)}):")
    for m in model_files[:15]:
        sz_mb = os.path.getsize(m) / (1024 * 1024)
        print(f"    - {os.path.relpath(m, target_dir)} ({sz_mb:.2f} MB)")

    if import_mode in ("all", "docs") and doc_files:
        merged_md = os.path.join(KNOWLEDGE_DIR, f"repo_{repo_name}_notes.md")
        with open(merged_md, "w", encoding="utf-8") as out:
            out.write(f"# External GitHub Repository Notes: {repo_name} ({clean})\n\n")
            for d in doc_files[:10]:
                with open(d, "r", encoding="utf-8", errors="ignore") as df:
                    out.write(f"## {os.path.basename(d)}\n{df.read()[:4000]}\n\n")
        from scripts.knowledge_index import rebuild_index
        rebuild_index()
        print(f"\n[Indexed Docs] Saved & indexed documentation into -> {merged_md}")

    print(f"\n[Ready to Run] All files saved in: {target_dir}")
    print(f"Tip: Copy any script you want into ~/AI-Checkmate/scripts/ or run directly with:\n  ~/AI-Checkmate/venv/bin/python3 {target_dir}/<script.py>\n")

if __name__ == "__main__":
    it = iter(sys.argv)
    next(it, None)
    repo = next(it, "")
    mode = next(it, "all")
    if repo:
        pull_github_repo(repo, mode)
    else:
        print("Usage: run repo_puller.py <github_user/repo_name_or_url>")
