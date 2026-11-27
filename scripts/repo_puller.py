import os
import json
import sys
import subprocess

BASE_DIR = os.path.expanduser("~/AI-Checkmate")
EXT_DIR = os.path.join(BASE_DIR, "external_repos")
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge")
os.makedirs(EXT_DIR, exist_ok=True)
os.makedirs(KNOWLEDGE_DIR, exist_ok=True)

def convert_notebooks_to_py(repo_dir: str) -> int:
    """Extracts code cells from .ipynb notebooks into clean .py scripts inside an extracted_py/ subfolder."""
    out_py_dir = os.path.join(repo_dir, "extracted_py")
    os.makedirs(out_py_dir, exist_ok=True)
    converted = 0
    for root_p, dirs, files in os.walk(repo_dir):
        if ".git" in root_p or "extracted_py" in root_p:
            continue
        for fn in sorted(files):
            if fn.endswith(".ipynb"):
                nb_path = os.path.join(root_p, fn)
                try:
                    with open(nb_path, "r", encoding="utf-8", errors="ignore") as f:
                        nb = json.load(f)
                    code_blocks = list()
                    for cell in nb.get("cells", ()):
                        if cell.get("cell_type") == "code":
                            src = "".join(cell.get("source", ()))
                            if src.strip():
                                code_blocks.append(src)
                    if code_blocks:
                        rel_tag = os.path.relpath(root_p, repo_dir).replace("/", "_")
                        py_name = f"{rel_tag}_{fn[:-6]}.py".lstrip("._")
                        with open(os.path.join(out_py_dir, py_name), "w", encoding="utf-8") as out:
                            out.write("\n\n# --- CELL ---\n".join(code_blocks) + "\n")
                        converted += 1
                except Exception:
                    pass
    return converted

def pull_github_repo(repo_input: str, import_mode: str = "all"):
    clean = repo_input.strip().rstrip("/")
    if clean.endswith(".git"):
        clean = clean[:-4]
    if not clean.startswith("http"):
        clean = f"https://github.com/{clean}"

    repo_name = clean.split("/").pop()
    target_dir = os.path.join(EXT_DIR, repo_name)

    print(f"\n=== GITHUB TRAINING REPO PULLER: {repo_name} ===")
    if os.path.exists(os.path.join(target_dir, ".git")):
        print(f"[Updating Existing Repo] Pulling latest changes in {target_dir} ...")
        subprocess.run(("git", "-C", target_dir, "pull"), check=False)
    else:
        print(f"[Shallow Cloning Repo] {clean} -> {target_dir} ...")
        res = subprocess.run(("git", "clone", "--depth", "1", clean, target_dir), capture_output=True, text=True)
        if res.returncode != 0:
            print(f"[Error] Clone failed: {res.stderr.strip()}\n")
            return

    py_count = 0
    doc_files = list()
    for root_p, dirs, files in os.walk(target_dir):
        if ".git" in root_p:
            continue
        for fn in sorted(files):
            full_p = os.path.join(root_p, fn)
            low = fn.lower()
            if low.endswith(".py"):
                py_count += 1
            elif low.endswith((".md", ".txt")) and os.path.getsize(full_p) < 350000:
                doc_files.append(full_p)

    nb_converted = convert_notebooks_to_py(target_dir)
    print(f"[Scan Complete] Found {py_count} native .py scripts & converted {nb_converted} Jupyter notebooks -> {target_dir}/extracted_py/")

    if import_mode in ("all", "docs") and doc_files:
        merged_md = os.path.join(KNOWLEDGE_DIR, f"repo_{repo_name}_notes.md")
        with open(merged_md, "w", encoding="utf-8") as out:
            out.write(f"# External GitHub Repository Knowledge: {repo_name} ({clean})\n\n")
            for d in doc_files[:15]:
                with open(d, "r", encoding="utf-8", errors="ignore") as df:
                    out.write(f"## {os.path.basename(d)}\n{df.read()[:5000]}\n\n")
        from scripts.knowledge_index import rebuild_index
        rebuild_index()
        print(f"[Indexed Docs] Saved & indexed top reference guides into -> {merged_md}")

    print(f"\n[All Training Files Ready] Folder: {target_dir}\n")

if __name__ == "__main__":
    it = iter(sys.argv)
    next(it, None)
    repo = next(it, "")
    mode = next(it, "all")
    if repo:
        pull_github_repo(repo, mode)
    else:
        print("Usage: run repo_puller.py <github_user/repo_name_or_url>")
