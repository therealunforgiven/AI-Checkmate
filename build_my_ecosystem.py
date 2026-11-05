import os

def create_automated_workspace():
    # 1. Define project directory paths
    project_dir = r"C:\Users\11\Desktop\tetris_ai_training"
    app_file = os.path.join(project_dir, "nursing_app_frontend.py")
    sql_file = os.path.join(project_dir, "azure_database_setup.sql")
    
    print("==============================================================")
    print("[🚀 AUTO-BUILD] Initializing Workspace Generator Script...")
    print("==============================================================")

    # 2. Automated Python Code for her Medical Dark-Mode Frontend App
    app_code = """import tkinter as tk
from tkinter import ttk

# Initialize modern medical dark mode workspace
root = tk.Tk()
root.title("🩺 NCLEX COACH - Medical Training Console v1.0")
root.geometry("650x550")
root.configure(bg="#121212") # Matte Black/Charcoal background

# Style configurations for Crisp Teal and Deep Blue borders
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#121212", foreground="#00F0FF", font=("Courier", 11))
style.configure("TButton", background="#1A1A1A", foreground="#00FFCC", font=("Courier", 10))

# Question Display Frame
lbl_question = ttk.Label(root, text="[ACTIVE EXAM MODULE: CARDIAC MATRIX]\\n\\nA patient is displaying intercostal retractions and a silent chest\\nduring an acute asthma flare... Which action is first?", justify="left")
lbl_question.pack(pady=20, padx=20, fill="x")

# Interactive Selection Panel
var_choice = tk.StringVar(value="None")
r1 = tk.Radiobutton(root, text="[A] Administer an over-the-counter cough suppressant", variable=var_choice, value="A", bg="#121212", fg="#FFFFFF", font=("Courier", 10), selectcolor="#121212")
r2 = tk.Radiobutton(root, text="[B] Immediately prepare for emergent airway stabilization", variable=var_choice, value="B", bg="#121212", fg="#00FFCC", font=("Courier", 10), selectcolor="#121212")
r3 = tk.Radiobutton(root, text="[C] Instruct the patient to perform deep breathing exercises", variable=var_choice, value="C", bg="#121212", fg="#FFFFFF", font=("Courier", 10), selectcolor="#121212")
r1.pack(anchor="w", padx=40, pady=5)
r2.pack(anchor="w", padx=40, pady=5)
r3.pack(anchor="w", padx=40, pady=5)

# Feedback Box Entry Frame
lbl_feedback = ttk.Label(root, text="\\n💬 CLIENT FEEDBACK & STUDENT REVIEWS:")
lbl_feedback.pack(pady=10)
txt_feedback = tk.Text(root, height=4, width=60, bg="#1A1A1A", fg="#FFFFFF", insertbackground="#00FFCC", font=("Courier", 10))
txt_feedback.pack(pady=5)

def submit_to_kenny():
    print("[System Output] Streaming review packet to Kenny's Azure server log...")

btn_submit = ttk.Button(root, text="[🚀 SUBMIT FEEDBACK TO KENNY]", command=submit_to_kenny)
btn_submit.pack(pady=15)

root.mainloop()
"""

    # 3. Automated Azure SQL Schema Layout script
    sql_code = """-- NCLEX & CARDIAC DUAL-MODE SCHEMA LAYOUT
CREATE TABLE NCLEX_Cardiac_Engine (
    Question_ID INT PRIMARY KEY IDENTITY(1,1),
    Module_Type VARCHAR(50), -- 'NCLEX_General' or 'Cardiac_Focus'
    Question_Text TEXT NOT NULL,
    Correct_Answer CHAR(1),
    Level_3_Analogy TEXT,    -- The electrical/mechanical analogy (Wiring layout)
    Level_50_Clinical TEXT   -- The strict clinical nursing protocol breakdown
);
"""

    # 4. Write files instantly to your folder path
    with open(app_file, "w", encoding="utf-8") as f:
        f.write(app_code)
    print(f"[+] Successfully generated app frontend: {app_file}")
        
    with open(sql_file, "w", encoding="utf-8") as f:
        f.write(sql_code)
    print(f"[+] Successfully generated database schema: {sql_file}")

    print("==============================================================")
    print("[👑 COMPLETE] Ecosytem configuration automated successfully!")
    print("==============================================================")

if __name__ == "__main__":
    create_automated_workspace()
