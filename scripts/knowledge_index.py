import os
import re
import glob
import sqlite3

BASE_DIR = os.path.expanduser("~/AI-Checkmate")
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge")
DB_PATH = os.path.join(BASE_DIR, "knowledge_index.db")

def rebuild_index():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS kb_fts")
    cur.execute("CREATE VIRTUAL TABLE kb_fts USING fts5(filename, section, content)")

    files = sorted(glob.glob(os.path.join(KNOWLEDGE_DIR, "*.txt")) + glob.glob(os.path.join(KNOWLEDGE_DIR, "*.md")))
    count = 0
    for path in files:
        fname = os.path.basename(path)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        # Split into clean ~800-char chunks so only exact matching sections go to the LLM
        paragraphs = tuple(p.strip() for p in text.split("\n\n") if p.strip())
        chunk = ""
        for p in paragraphs:
            if len(chunk) + len(p) > 900 and chunk:
                cur.execute("INSERT INTO kb_fts (filename, section, content) VALUES (?, ?, ?)", (fname, fname, chunk))
                count += 1
                chunk = p
            else:
                chunk = (chunk + "\n\n" + p).strip()
        if chunk:
            cur.execute("INSERT INTO kb_fts (filename, section, content) VALUES (?, ?, ?)", (fname, fname, chunk))
            count += 1

    conn.commit()
    conn.close()
    print(f"[Index Ready] Indexed {len(files)} files into {count} fast-search chunks ({DB_PATH})")

def query_index(query_str: str, max_chars: int = 3200) -> str:
    if not os.path.exists(DB_PATH):
        rebuild_index()
    words = tuple(w for w in re.findall(r"[a-zA-Z0-9_]+", query_str) if len(w) >= 2)
    if not words:
        return ""
    fts_query = " OR ".join(words)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        rows = cur.execute(
            "SELECT filename, content FROM kb_fts WHERE kb_fts MATCH ? ORDER BY bm25(kb_fts) LIMIT 5",
            (fts_query,)
        ).fetchall()
    except Exception:
        rows = ()
    conn.close()

    out = list()
    total = 0
    for fname, content in rows:
        entry = f"[{fname}]\n{content}\n"
        if total + len(entry) > max_chars:
            break
        out.append(entry)
        total += len(entry)
    return "\n".join(out)

if __name__ == "__main__":
    rebuild_index()
