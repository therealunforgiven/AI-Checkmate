# train_pdf_editor.py
import os
import pymupdf  # Modern PyMuPDF import
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class AdvancedPDFPipeline:
    def __init__(self, workspace="pdf_training_workspace"):
        self.workspace = workspace
        os.makedirs(self.workspace, exist_ok=True)
        print(f"[Init] Advanced PDF Workspace active at: {os.path.abspath(self.workspace)}")

    def generate_batch_samples(self):
        """Generates multiple sample PDFs for batch training processing."""
        samples = ["invoice_01.pdf", "invoice_02.pdf"]
        created_files = []
        
        for filename in samples:
            filepath = os.path.join(self.workspace, filename)
            c = canvas.Canvas(filepath, pagesize=letter)
            c.drawString(100, 750, f"AI-Checkmate Document: {filename}")
            c.drawString(100, 730, "Status: Pending Review - Draft Mode")
            c.drawString(100, 710, "Action Required: Verification & Approval")
            c.save()
            created_files.append(filepath)
            
        print(f"[Pipeline] Generated batch training samples: {created_files}")
        return created_files

    def batch_process_documents(self, target_string, replacement_string):
        """Scans all PDFs in the workspace and updates them automatically."""
        processed_count = 0
        
        for filename in os.listdir(self.workspace):
            if filename.endswith(".pdf") and "processed" not in filename:
                input_path = os.path.join(self.workspace, filename)
                output_path = os.path.join(self.workspace, f"processed_{filename}")
                
                doc = pymupdf.open(input_path)
                edits_made = 0

                for page_num, page in enumerate(doc):
                    rects = page.search_for(target_string)
                    for rect in rects:
                        highlight = page.add_highlight_annot(rect)
                        highlight.update()
                        edits_made += 1

                    page.insert_text(
                        (100, 670), 
                        f">> AI Automated Update: '{target_string}' -> '{replacement_string}'",
                        fontsize=9,
                        color=(0, 0.5, 0) # Green audit stamp
                    )

                doc.save(output_path)
                doc.close()
                print(f"[Batch Engine] Processed: {filename} -> Saved as processed_{filename} (Edits: {edits_made})")
                processed_count += 1
                
        print(f"[Pipeline] Batch execution complete. Total documents handled: {processed_count}")

if __name__ == "__main__":
    pipeline = AdvancedPDFPipeline()
    pipeline.generate_batch_samples()
    pipeline.batch_process_documents(
        target_string="Pending Review - Draft Mode",
        replacement_string="Approved & Verified - Production Mode"
    )