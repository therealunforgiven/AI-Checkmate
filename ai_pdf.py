import os
import sys
import glob
import requests
from weasyprint import HTML

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

SYSTEM_PROMPT = (
    "You are an offline technical assistant for Car and Computer Electric. "
    "Output ONLY valid semantic HTML (<h1>, <h2>, <p>, <ul>, <li>, <table>, "
    "<thead>, <tbody>, <tr>, <th>, <td>, <div class='callout'>) with zero markdown "
    "code fences, no explanations outside the HTML, and no external URLs."
)

def load_knowledge(knowledge_dir: str) -> str:
    notes = []
    for path in sorted(glob.glob(os.path.join(knowledge_dir, "*.txt")) + glob.glob(os.path.join(knowledge_dir, "*.md"))):
        with open(path, "r", encoding="utf-8") as f:
            notes.append(f"--- Reference: {os.path.basename(path)} ---\n{f.read()}")
    return "\n\n".join(notes)

def build_pdf(prompt: str, out_file: str, model: str = "dolphin-llama3:8b"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ref_context = load_knowledge(os.path.join(base_dir, "knowledge"))
    full_prompt = f"{ref_context}\n\nTask:\n{prompt}" if ref_context else prompt

    resp = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "system": SYSTEM_PROMPT,
            "prompt": full_prompt,
            "options": {"num_thread": 4, "temperature": 0.2},
            "stream": False
        }
    )
    raw_html = resp.json().get("response", "").strip()
    raw_html = raw_html.removeprefix("```html").removeprefix("```").removesuffix("```").strip()
    styled_html = f"<!DOCTYPE html><html><head><meta charset='utf-8'>{PRINT_CSS}</head><body>{raw_html}</body></html>"
    HTML(string=styled_html).write_pdf(out_file)
    print(f"Saved PDF: {out_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Usage: python3 ai_pdf.py "Your prompt here" output.pdf [model_name]')
        sys.exit(1)
    model_name = sys.argv[3] if len(sys.argv) > 3 else "dolphin-llama3:8b"
    build_pdf(sys.argv[1], sys.argv[2], model_name)
