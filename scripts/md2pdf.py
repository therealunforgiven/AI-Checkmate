import os
import sys
import markdown
from weasyprint import HTML

PRINT_CSS = """
<style>
  @page { size: letter; margin: 0.45in; }
  body { font-family: "Liberation Sans", Arial, sans-serif; font-size: 9.5pt; line-height: 1.35; color: #111; }
  h1 { font-size: 15pt; border-bottom: 2px solid #1e3a5f; padding-bottom: 4px; margin: 0 0 8px 0; }
  h2 { font-size: 11.5pt; color: #1e3a5f; margin: 12px 0 5px 0; }
  table { width: 100%; border-collapse: collapse; margin: 6px 0 10px 0; font-size: 8.5pt; }
  th { background-color: #1e3a5f; color: #fff; text-align: left; padding: 5px 6px; border: 1px solid #1e3a5f; }
  td { padding: 4px 6px; border: 1px solid #ccc; vertical-align: top; }
</style>
"""

it = iter(sys.argv)
next(it, None)
md_file = os.path.expanduser(next(it, ""))
if not md_file or not os.path.exists(md_file):
    print("Usage: run md2pdf.py <path/to/file.md>")
    sys.exit(1)

with open(md_file, "r", encoding="utf-8") as f:
    html_body = markdown.markdown(f.read(), extensions=("tables", "fenced_code"))

base = os.path.splitext(os.path.basename(md_file)).pop(0)
out_pdf = os.path.expanduser(f"~/AI-Checkmate/generated_pdfs/{base}.pdf")
HTML(string=f"<!DOCTYPE html><html><head><meta charset='utf-8'>{PRINT_CSS}</head><body>{html_body}</body></html>").write_pdf(out_pdf)
print(f"[Instant PDF Ready] -> {out_pdf}")
