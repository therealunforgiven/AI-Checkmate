import os
import re
import glob
import datetime
import subprocess
import requests
from bs4 import BeautifulSoup
from weasyprint import HTML
from ddgs import DDGS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge")
PDF_DIR = os.path.join(BASE_DIR, "generated_pdfs")
os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

MODEL = "dolphin-llama3:8b"
OLLAMA_URL = "http://localhost:11434/api/generate"

PRINT_CSS = """
<style>
  @page { size: letter; margin: 0.45in; }
  body { font-family: "Liberation Sans", Arial, sans-serif; font-size: 9.5pt; line-height: 1.35; color: #111; }
  h1 { font-size: 15pt; border-bottom: 2px solid #1e3a5f; padding-bottom: 4px; margin: 0 0 8px 0; break-after: avoid; }
  h2 { font-size: 11.5pt; color: #1e3a5f; margin: 12px 0 5px 0; break-after: avoid; }
  table { width: 100%; border-collapse: collapse; margin: 6px 0 10px 0; font-size: 8.5pt; }
  thead { display: table-header-group; }
  th { background-color: #1e3a5f; color: #fff; text-align: left; padding: 5px 6px; border: 1px solid #1e3a5f; }
  td { padding: 4px 6px; border: 1px solid #ccc; vertical-align: top; }
  tr { break-inside: avoid; }
  .callout { background-color: #f4f6f9; border-left: 3px solid #1e3a5f; padding: 6px 8px; margin: 8px 0; break-inside: avoid; }
</style>
"""

def run_git(args):
    return subprocess.run(["git"] + args, cwd=BASE_DIR, capture_output=True, text=True)

def git_pull():
    print("[GitHub] Pulling latest updates ...")
    res = run_git(["pull", "--rebase", "origin", "main"])
    if res.returncode == 0:
        print(f"[GitHub] {res.stdout.strip() or 'Up to date.'}")
    else:
        print(f"[GitHub Pull Notice] {res.stderr.strip()}")

def git_push(msg: str = None):
    if not msg:
        msg = f"Checkmate knowledge & script update {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
    print("[GitHub] Staging and pushing updates ...")
    run_git(["add", "."])
    commit_res = run_git(["commit", "-m", msg])
    if "nothing to commit" in (commit_res.stdout + commit_res.stderr).lower():
        print("[GitHub] Nothing new to commit.\n")
        return
    push_res = run_git(["push", "origin", "main"])
    if push_res.returncode == 0:
        print("[GitHub] Successfully pushed to GitHub!\n")
    else:
        print(f"[GitHub Push Error] {push_res.stderr.strip()}\n")

def ask_ollama(prompt: str, system: str = "You are Checkmate, a technical AI assistant for Car and Computer Electric.") -> str:
    resp = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "system": system,
            "prompt": prompt,
            "options": {"num_thread": 4, "temperature": 0.2},
            "stream": False
        },
        timeout=300
    )
    return resp.json().get("response", "").strip()

def load_knowledge(query: str = "", max_chars: int = 14000) -> str:
    if isinstance(query, int):
        max_chars = query
        query = ""
    files = sorted(glob.glob(os.path.join(KNOWLEDGE_DIR, "*.txt")) + glob.glob(os.path.join(KNOWLEDGE_DIR, "*.md")))
    keywords = tuple(w.lower() for w in re.findall(r"[a-zA-Z0-9_]+", str(query)) if len(w) >= 2)
    scored = list()
    for path in files:
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read()
        low_all = (os.path.basename(path) + " " + txt).lower()
        score = sum(low_all.count(k) * 5 for k in keywords)
        scored.append((score, os.path.basename(path), txt))
    scored.sort(key=lambda item: next(iter(item)), reverse=True)
    chunks, total = list(), 0
    for score, fname, txt in scored:
        entry = f"=== KNOWLEDGE: {fname} ===\n{txt}\n"
        if total + len(entry) > int(max_chars):
            continue
        chunks.append(entry)
        total += len(entry)
    return "\n".join(chunks)

def scrape_text(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()
    return re.sub(r"\n{3,}", "\n\n", soup.get_text(separator="\n")).strip()

def learn_from_url(url: str):
    print(f"[Scraping] {url} ...")
    raw_text = scrape_text(url)[:15000]
    print("[Digesting] Extracting clean technical notes ...")
    summary = ask_ollama(
        f"Extract and organize all useful technical facts, pinouts, procedures, chip numbers, or rules from this text into clean Markdown notes:\n\n{raw_text}",
        system="You are a technical archivist. Condense scraped web text into accurate, structured reference notes."
    )
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", url.split("://")[-1])[:45].strip("_")
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    out_path = os.path.join(KNOWLEDGE_DIR, f"{stamp}_{slug}.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"Source URL: {url}\n\n{summary}\n")
    print(f"[Learned!] Saved to: {out_path}\n")

def search_and_learn(topic: str, max_results: int = 3):
    print(f"[DuckDuckGo] Searching: {topic} ...")
    results = list(DDGS().text(topic, max_results=max_results))
    if not results:
        print("[DuckDuckGo] No results found.\n")
        return
    combined = []
    for idx, res in enumerate(results, 1):
        url = res.get("href", "")
        title = res.get("title", "")
        snippet = res.get("body", "")
        print(f"  ({idx}) {title} -> {url}")
        page_text = snippet
        try:
            scraped = scrape_text(url)
            if len(scraped) > 300:
                page_text = scraped[:5000]
        except Exception:
            pass
        combined.append(f"Source {idx}: {title} ({url})\n{page_text}\n")

    print("[Digesting] Synthesizing search results into permanent knowledge ...")
    summary = ask_ollama(
        f"Topic: {topic}\n\nSynthesize all accurate technical facts, pinouts, part numbers, and procedures from these sources into clean Markdown notes:\n\n" + "\n---\n".join(combined),
        system="You are a technical archivist. Organize search findings into accurate, structured reference notes."
    )
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", topic)[:45].strip("_")
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    out_path = os.path.join(KNOWLEDGE_DIR, f"{stamp}_ddg_{slug}.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"Search Topic: {topic}\n\n{summary}\n")
    print(f"[Learned!] Saved to: {out_path}\n")


DESKTOP_DIR = os.path.expanduser("~/Desktop")
os.makedirs(DESKTOP_DIR, exist_ok=True)

def make_desktop_pdf(topic: str):
    kb = load_knowledge(topic)
    prompt = f"{kb}\n\nCreate a comprehensive, print-ready technical report for:\n{topic}" if kb else topic
    system = (
        "Output ONLY valid semantic HTML (<h1>, <h2>, <p>, <ul>, <li>, <table>, "
        "<thead>, <tbody>, <tr>, <th>, <td>, <div class='summary-box'>) with zero markdown fences."
    )
    print(f"[Desktop PDF] Building full report for: {topic} ...")
    raw_html = ask_ollama(prompt, system=system).removeprefix("```html").removeprefix("```").removesuffix("```").strip()
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", topic)[:40].strip("_") or "Report"
    out_pdf = os.path.join(DESKTOP_DIR, f"Checkmate_{slug}.pdf")
    render_pdf(raw_html, out_pdf)
    return out_pdf

def make_pdf_interactive(topic: str):
    kb = load_knowledge()
    prompt = f"{kb}\n\nCreate a detailed, print-ready document for:\n{topic}" if kb else topic
    system = (
        "Output ONLY valid semantic HTML (<h1>, <h2>, <p>, <ul>, <li>, <table>, "
        "<thead>, <tbody>, <tr>, <th>, <td>, <div class='callout'>) with zero markdown "
        "code fences, no explanations outside the HTML, and no external URLs."
    )
    print("[Generating PDF] Thinking ...")
    raw_html = ask_ollama(prompt, system=system)
    raw_html = raw_html.removeprefix("```html").removeprefix("```").removesuffix("```").strip()
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", topic)[:40].strip("_") or "document"
    out_pdf = os.path.join(PDF_DIR, f"{slug}.pdf")
    styled_html = f"<!DOCTYPE html><html><head><meta charset='utf-8'>{PRINT_CSS}</head><body>{raw_html}</body></html>"
    HTML(string=styled_html).write_pdf(out_pdf)
    print(f"[PDF Ready] {out_pdf}\n")


SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
os.makedirs(SCRIPTS_DIR, exist_ok=True)

def list_custom_scripts():
    py_files = sorted(f for f in os.listdir(SCRIPTS_DIR) if f.endswith(".py"))
    print("\n=== CUSTOM SCRIPTS IN ~/AI-Checkmate/scripts/ ===")
    for f in py_files:
        print(f"  - {f}")
    if not py_files:
        print("  (No .py scripts found yet)")
    print("Run any script with: run <script_name.py> [args]\n")

def run_custom_script(cmd_str: str):
    parts = cmd_str.split()
    if not parts:
        list_custom_scripts()
        return
    name = parts if parts.endswith(".py") else parts + ".py"
    path = os.path.join(SCRIPTS_DIR, os.path.basename(name))
    if not os.path.exists(path):
        print(f"[Error] Not found: {path}\n")
        return
    py_exec = os.path.join(BASE_DIR, "venv", "bin", "python3")
    if not os.path.exists(py_exec):
        py_exec = "python3"
    print(f"[Executing] {name} ...\n")
    subprocess.run([py_exec, path] + parts[1:], cwd=BASE_DIR)
    print()

def main():
    git_pull()
    print("\n=== CHECKMATE LOCAL AI (Search + Scrape + PDF + GitHub Sync) ===")
    print("Commands:")
    print("  search <topic>        -> Search DuckDuckGo, scrape top pages & save to knowledge/")
    print("  learn <https://url>   -> Scrape an exact URL & save notes to knowledge/")
    print("  pdf <what you want>   -> Generate a printable PDF using your knowledge/")
    print("  sync                  -> Commit & push all new scripts/knowledge to GitHub")
    print("  exit                  -> Sync & quit\n")
    while True:
        try:
            user_in = input("You > ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user_in:
            continue
        if user_in.lower() in ("exit", "quit"):
            git_push()
            break
        elif user_in.lower() == "sync":
            git_push()
        elif user_in.lower().startswith("search "):
            try:
                search_and_learn(user_in[7:].strip())
            except Exception as e:
                print(f"[Search Error] {e}\n")
        elif user_in.lower().startswith("learn "):
            try:
                learn_from_url(user_in[6:].strip())
            except Exception as e:
                print(f"[Scrape Error] {e}\n")
        elif user_in.lower().startswith("pdf "):
            make_pdf_interactive(user_in[4:].strip())
        else:
            kb = load_knowledge()
            prompt = f"Reference Knowledge:\n{kb}\n\nUser Question:\n{user_in}" if kb else user_in
            print("\nCheckmate > " + ask_ollama(prompt) + "\n")

if __name__ == "__main__":
    main()
