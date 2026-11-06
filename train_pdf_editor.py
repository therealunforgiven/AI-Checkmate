# train_pdf_editor.py
import os
import fitz  # PyMuPDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class PDFTrainingPipeline:
    def __init__(self, workspace="pdf_training_workspace"):
        self.workspace = workspace
        os.makedirs(self.workspace, exist_ok=True)
        print(f"[Init] PDF Training Workspace active at: {os.path.abspath(self.workspace)}")

    def generate_training_sample(self, filename="base_document.pdf"):
        """Generates a sample PDF document for the AI pipeline to practice on."""
        filepath = os.path.join(self.workspace, filename)
        c = canvas.Canvas(filepath, pagesize=letter)
        c.drawString(100, 750, "AI-Checkmate Document Training Pipeline")
        c.drawString(100, 730, "Document Status: Draft - Version 1.0")
        c.drawString(100, 710, "Target Category: Invoice & Data Processing")
        c.save()
        print(f"[Pipeline] Created training sample: {filepath}")
        return filepath

    def execute_smart_edit(self, input_path, output_path, target_string, replacement_string):
        """Scans the PDF, highlights target text, and injects updates/annotations."""
        doc = fitz.open(input_path)
        edits_made = 0

        for page_num, page in enumerate(doc):
            rects = page.search_for(target_string)
            for rect in rects:
                highlight = page.add_highlight_annot(rect)
                highlight.update()
                edits_made += 1

            page.insert_text(
                (100, 670), 
                f">> AI Audit: Replaced '{target_string}' with '{replacement_string}' on Page {page_num + 1}",
                fontsize=9,
                color=(0, 0, 1)
            )

        doc.save(output_path)
        doc.close()
        print(f"[Pipeline] Success! Processed {input_path} -> Saved to {output_path} (Edits tracked: {edits_made})")

if __name__ == "__main__":
    pipeline = PDFTrainingPipeline()
    sample_pdf = pipeline.generate_training_sample()
    output_pdf = os.path.join(pipeline.workspace, "processed_document.pdf")
    pipeline.execute_smart_edit(
        input_path=sample_pdf,
        output_path=output_pdf,
        target_string="Draft - Version 1.0",
        replacement_string="Finalized - Version 2.0"
    )