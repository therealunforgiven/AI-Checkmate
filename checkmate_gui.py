import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PY_EXEC = os.path.join(BASE_DIR, "venv", "bin", "python3")
if not os.path.exists(PY_EXEC):
    PY_EXEC = sys.executable

sys.path.insert(0, BASE_DIR)
import checkmate

class CheckmateGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Car and Computer Electric - Checkmate Workstation")
        self.root.geometry("1220x820")
        self.root.configure(bg="#141b24")
        self.root.tk.call("tk", "scaling", 1.35)
        self.console_font_size = 13

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#141b24", borderwidth=0)
        style.configure("TNotebook.Tab", background="#1e293b", foreground="#e2e8f0", padding=(10, 6), font=("Liberation Sans", 12, "bold"))
        style.map("TNotebook.Tab", background=(("selected", "#2563eb"),), foreground=(("selected", "#ffffff"),))
        style.configure("TFrame", background="#1e293b")
        style.configure("TLabel", background="#1e293b", foreground="#f8fafc", font=("Liberation Sans", 13))
        style.configure("Header.TLabel", background="#141b24", foreground="#38bdf8", font=("Liberation Sans", 18, "bold"))

        top_bar = tk.Frame(root, bg="#141b24", pady=8, padx=12)
        top_bar.pack(fill="x")
        ttk.Label(top_bar, text="CHECKMATE AI & BENCH WORKSTATION", style="Header.TLabel").pack(side="left")

        tk.Button(top_bar, text="Font +", bg="#334155", fg="white", font=("Liberation Sans", 11, "bold"),
                  relief="flat", padx=8, pady=4, command=lambda: self.change_font(2)).pack(side="right", padx=3)
        tk.Button(top_bar, text="Font -", bg="#334155", fg="white", font=("Liberation Sans", 11, "bold"),
                  relief="flat", padx=8, pady=4, command=lambda: self.change_font(-2)).pack(side="right", padx=3)
        tk.Button(top_bar, text="Sync to GitHub", bg="#16a34a", fg="white", font=("Liberation Sans", 12, "bold"),
                  relief="flat", padx=10, pady=4, command=self.action_git_sync).pack(side="right", padx=4)
        tk.Button(top_bar, text="Open PDFs", bg="#0284c7", fg="white", font=("Liberation Sans", 12, "bold"),
                  relief="flat", padx=10, pady=4, command=lambda: self.open_folder("generated_pdfs")).pack(side="right", padx=4)
        tk.Button(top_bar, text="Open Scripts", bg="#475569", fg="white", font=("Liberation Sans", 12, "bold"),
                  relief="flat", padx=10, pady=4, command=lambda: self.open_folder("generated_scripts")).pack(side="right", padx=4)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=False, padx=10, pady=4)

        self.build_tab_chat()
        self.build_tab_eeprom()
        self.build_tab_scope()
        self.build_tab_docs()
        self.build_tab_money()
        self.build_tab_cluster()
        self.build_tab_advanced()

        console_frame = tk.Frame(root, bg="#141b24", padx=10, pady=6)
        console_frame.pack(fill="both", expand=True)

        hdr = tk.Frame(console_frame, bg="#141b24")
        hdr.pack(fill="x")
        tk.Label(hdr, text="LIVE WORKSTATION CONSOLE", bg="#141b24", fg="#94a3b8", font=("Liberation Sans", 12, "bold")).pack(side="left")
        tk.Button(hdr, text="Clear", bg="#334155", fg="#e2e8f0", font=("Liberation Sans", 11), relief="flat", padx=8,
                  command=lambda: self.console.delete("1.0", "end")).pack(side="right")

        self.console = scrolledtext.ScrolledText(console_frame, height=15, bg="#0b0f14", fg="#22c55e",
                                                 insertbackground="white", font=("Liberation Mono", 13), wrap="word")
        self.console.pack(fill="both", expand=True, pady=(4, 0))
        self.log("Checkmate 7-Tab Workstation Online.\n")

    def change_font(self, delta):
        self.console_font_size = max(10, min(24, self.console_font_size + delta))
        self.console.configure(font=("Liberation Mono", self.console_font_size))

    def log(self, text):
        self.root.after(0, lambda: (self.console.insert("end", text), self.console.see("end")))

    def open_folder(self, sub):
        p = os.path.join(BASE_DIR, sub)
        os.makedirs(p, exist_ok=True)
        subprocess.Popen(("xdg-open", p))

    def run_bg(self, fn, *args):
        threading.Thread(target=fn, args=args, daemon=True).start()

    def run_script(self, script_name, args_tuple, stdin_txt="n\n"):
        sp = os.path.join(BASE_DIR, "scripts", script_name)
        self.log(f"\n>>> {script_name} {' '.join(args_tuple)}\n")
        try:
            proc = subprocess.run((PY_EXEC, sp) + args_tuple, cwd=BASE_DIR, input=stdin_txt, capture_output=True, text=True, timeout=300)
            if proc.stdout: self.log(proc.stdout + "\n")
            if proc.stderr: self.log("[ERR] " + proc.stderr + "\n")
        except Exception as e:
            self.log(f"[Error] {e}\n")

    def prompt_box(self, lbl, ent, hint):
        lbl.configure(text=hint, fg="#facc15")
        ent.configure(highlightthickness=2, highlightbackground="#facc15", highlightcolor="#facc15")
        ent.focus_set()
        self.log(f"\n[Ready] {hint}\n")

    def build_tab_chat(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="1. AI Chat")
        self.chat_hint = tk.Label(tab, text="TYPE HERE -> Ask AI, Search a Topic, or Paste a URL:", bg="#1e293b", fg="#38bdf8", font=("Liberation Sans", 11, "bold"), anchor="w")
        self.chat_hint.pack(fill="x", pady=(0, 3))
        self.chat_entry = tk.Entry(tab, font=("Liberation Sans", 13), bg="#0f172a", fg="white", insertbackground="white")
        self.chat_entry.pack(fill="x", pady=4)
        self.chat_entry.bind("<Return>", lambda e: self.action_chat())
        r = tk.Frame(tab, bg="#1e293b"); r.pack(fill="x", pady=4)
        tk.Button(r, text="Ask AI", bg="#2563eb", fg="white", padx=12, command=self.action_chat).pack(side="left", padx=4)
        tk.Button(r, text="Search & Learn Topic", bg="#0d9488", fg="white", padx=12, command=self.action_search).pack(side="left", padx=4)
        tk.Button(r, text="Scrape URL", bg="#6366f1", fg="white", padx=12, command=self.action_url).pack(side="left", padx=4)

    def action_chat(self):
        q = self.chat_entry.get().strip()
        if not q:
            self.prompt_box(self.chat_hint, self.chat_entry, "TYPE QUESTION ABOVE -> Ex: How to test BMW E70 CAS3+ KL15 wake-up?")
            return
        self.chat_entry.delete(0, "end")
        self.log(f"\nYou > {q}\n[Thinking ...]\n")
        def w():
            kb = checkmate.load_knowledge()
            ans = checkmate.ask_ollama(f"Reference:\n{kb}\n\nQuestion:\n{q}" if kb else q)
            self.log(f"Checkmate > {ans}\n")
        self.run_bg(w)

    def action_search(self):
        t = self.chat_entry.get().strip()
        if not t:
            self.prompt_box(self.chat_hint, self.chat_entry, "TYPE TOPIC ABOVE -> Ex: BMW E70 X5 CAS3+ 0L15Y BDM pinout")
            return
        self.log(f"\n[Searching] {t} ...\n")
        self.run_bg(lambda: (checkmate.search_and_learn(t), self.log("[Saved to knowledge/]\n")))

    def action_url(self):
        u = self.chat_entry.get().strip()
        if not u.startswith("http"):
            self.prompt_box(self.chat_hint, self.chat_entry, "PASTE FULL URL ABOVE -> Ex: https://wikipedia.org")
            return
        self.log(f"\n[Scraping] {u} ...\n")
        self.run_bg(lambda: (checkmate.learn_from_url(u), self.log("[Saved to knowledge/]\n")))

    def build_tab_eeprom(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="2. EEPROM/VIN")
        f1 = tk.Frame(tab, bg="#1e293b"); f1.pack(fill="x", pady=4)
        self.bin_var = tk.StringVar()
        tk.Entry(f1, textvariable=self.bin_var, width=42, bg="#0f172a", fg="white").pack(side="left", padx=4)
        tk.Button(f1, text="Browse .bin", bg="#475569", fg="white", command=lambda: self.bin_var.set(filedialog.askopenfilename() or self.bin_var.get())).pack(side="left", padx=3)
        tk.Button(f1, text="Auto-Backup", bg="#16a34a", fg="white", command=lambda: self.run_bg(self.run_script, "eeprom_vin_isn_tool.py", ("backup", self.bin_var.get()))).pack(side="left", padx=3)
        tk.Button(f1, text="Scan VIN", bg="#2563eb", fg="white", command=lambda: self.run_bg(self.run_script, "eeprom_vin_isn_tool.py", ("scan", self.bin_var.get()))).pack(side="left", padx=3)
        tk.Button(f1, text="Repair FRM3", bg="#d97706", fg="white", command=lambda: self.run_bg(self.run_script, "eeprom_vin_isn_tool.py", ("frm3", self.bin_var.get()))).pack(side="left", padx=3)

        f2 = tk.Frame(tab, bg="#1e293b"); f2.pack(fill="x", pady=6)
        self.mod_var = tk.StringVar(value="BCM")
        self.id_var = tk.StringVar(value="241")
        self.vin_var = tk.StringVar(value="1G1YY26U865104821")
        tk.Entry(f2, textvariable=self.mod_var, width=10, bg="#0f172a", fg="white").pack(side="left", padx=3)
        tk.Entry(f2, textvariable=self.id_var, width=10, bg="#0f172a", fg="white").pack(side="left", padx=3)
        tk.Entry(f2, textvariable=self.vin_var, width=22, bg="#0f172a", fg="white").pack(side="left", padx=3)
        tk.Button(f2, text="GM DPS", bg="#0284c7", fg="white", command=lambda: self.run_bg(self.run_script, "eeprom_vin_isn_tool.py", ("gmdps", self.mod_var.get(), self.id_var.get(), self.vin_var.get()))).pack(side="left", padx=3)
        tk.Button(f2, text="MicroPod", bg="#7c3aed", fg="white", command=lambda: self.run_bg(self.run_script, "eeprom_vin_isn_tool.py", ("micropod", self.mod_var.get(), self.vin_var.get(), self.id_var.get()))).pack(side="left", padx=3)
        tk.Button(f2, text="UPA VIN", bg="#0d9488", fg="white", command=lambda: self.run_bg(self.run_script, "eeprom_vin_isn_tool.py", ("upa_vin", self.mod_var.get(), self.id_var.get(), self.vin_var.get()))).pack(side="left", padx=3)
        tk.Button(f2, text="Pinouts", bg="#334155", fg="white", command=lambda: self.run_bg(self.run_script, "eeprom_vin_isn_tool.py", ("pinout", "ALL"))).pack(side="left", padx=3)

    def build_tab_scope(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="3. Scope")
        f = tk.Frame(tab, bg="#1e293b"); f.pack(fill="x", pady=8)
        self.wave_var = tk.StringVar()
        tk.Entry(f, textvariable=self.wave_var, width=52, bg="#0f172a", fg="white").pack(side="left", padx=4)
        tk.Button(f, text="Browse CSV/PNG", bg="#475569", fg="white", command=lambda: self.wave_var.set(filedialog.askopenfilename() or self.wave_var.get())).pack(side="left", padx=4)
        tk.Button(f, text="Analyze Waveform", bg="#2563eb", fg="white", command=lambda: self.run_bg(self.run_script, "scope_analyzer.py", ("upload", self.wave_var.get()))).pack(side="left", padx=4)

    def build_tab_docs(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="4. PDFs & TSBs")
        self.doc_entry = tk.Entry(tab, font=("Liberation Sans", 13), bg="#0f172a", fg="white", insertbackground="white")
        self.doc_entry.pack(fill="x", pady=4)
        r = tk.Frame(tab, bg="#1e293b"); r.pack(fill="x", pady=4)
        tk.Button(r, text="Pull NHTSA TSBs", bg="#0284c7", fg="white", command=lambda: self.run_bg(lambda: (checkmate.fetch_nhtsa_tsbs(self.doc_entry.get()), self.log("[TSB PDF Ready]\n")))).pack(side="left", padx=4)
        tk.Button(r, text="Build Contract PDF", bg="#16a34a", fg="white", command=lambda: self.run_bg(lambda: (checkmate.build_contract(self.doc_entry.get()), self.log("[Contract PDF Ready]\n")))).pack(side="left", padx=4)
        tk.Button(r, text="Draw SVG Diagram", bg="#7c3aed", fg="white", command=lambda: self.run_bg(lambda: (checkmate.draw_diagram_pdf(self.doc_entry.get()), self.log("[Diagram PDF Ready]\n")))).pack(side="left", padx=4)

    def build_tab_money(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="5. Money & CSV")
        self.tx_entry = tk.Entry(tab, font=("Liberation Sans", 13), bg="#0f172a", fg="white", insertbackground="white")
        self.tx_entry.pack(fill="x", pady=4)
        r = tk.Frame(tab, bg="#1e293b"); r.pack(fill="x", pady=4)
        tk.Button(r, text="+ Money In", bg="#16a34a", fg="white", command=lambda: self.run_bg(lambda: (checkmate.log_transaction("Money In", self.tx_entry.get()), self.log("[Income Logged]\n")))).pack(side="left", padx=4)
        tk.Button(r, text="- Expense", bg="#dc2626", fg="white", command=lambda: self.run_bg(lambda: (checkmate.log_transaction("Money Out", self.tx_entry.get()), self.log("[Expense Logged]\n")))).pack(side="left", padx=4)
        tk.Button(r, text="CSV + PDF Report", bg="#2563eb", fg="white", command=lambda: self.run_bg(lambda: (checkmate.generate_transaction_report(), self.log("[Report Ready]\n")))).pack(side="left", padx=4)

    def build_tab_cluster(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="6. 2-Laptop Cluster")
        f = tk.Frame(tab, bg="#1e293b"); f.pack(fill="x", pady=6)
        self.ip_var = tk.StringVar(value="192.168.1.52")
        tk.Entry(f, textvariable=self.ip_var, width=18, bg="#0f172a", fg="white").pack(side="left", padx=4)
        tk.Button(f, text="Add IP", bg="#0284c7", fg="white", command=lambda: self.run_bg(self.run_script, "cluster_dispatch.py", ("add", self.ip_var.get()))).pack(side="left", padx=4)
        tk.Button(f, text="Status", bg="#16a34a", fg="white", command=lambda: self.run_bg(self.run_script, "cluster_dispatch.py", ("status",))).pack(side="left", padx=4)

    def build_tab_advanced(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="7. Advanced & Terminal")
        r = tk.Frame(tab, bg="#1e293b"); r.pack(fill="x", pady=4)
        tk.Button(r, text="Open Ubuntu Terminal", bg="#0f172a", fg="#38bdf8", font=("Liberation Sans", 12, "bold"), padx=10, command=self.open_term).pack(side="left", padx=4)
        tk.Button(r, text="Git Pull", bg="#0284c7", fg="white", padx=10, command=lambda: self.run_sh("git pull origin main")).pack(side="left", padx=4)
        tk.Button(r, text="Ollama List", bg="#0d9488", fg="white", padx=10, command=lambda: self.run_sh("ollama list")).pack(side="left", padx=4)
        self.sh_entry = tk.Entry(r, width=36, bg="#0f172a", fg="#22c55e", insertbackground="white")
        self.sh_entry.pack(side="left", padx=4)
        tk.Button(r, text="Run", bg="#16a34a", fg="white", command=lambda: self.run_sh(self.sh_entry.get())).pack(side="left", padx=2)

    def open_term(self):
        c = f"cd '{BASE_DIR}' && source venv/bin/activate && exec bash"
        subprocess.Popen(("gnome-terminal", "--working-directory", BASE_DIR, "--", "bash", "-c", c))

    def run_sh(self, cmd):
        if not cmd.strip(): return
        self.log(f"\n$ {cmd}\n")
        def w():
            p = subprocess.run(("bash", "-c", f"cd '{BASE_DIR}' && source venv/bin/activate && {cmd}"), capture_output=True, text=True)
            if p.stdout: self.log(p.stdout + "\n")
            if p.stderr: self.log(p.stderr + "\n")
        self.run_bg(w)

    def action_git_sync(self):
        self.log("\n[Syncing to GitHub ...]\n")
        self.run_bg(lambda: (checkmate.git_push(), self.log("[GitHub Sync Done]\n")))

if __name__ == "__main__":
    root = tk.Tk()
    app = CheckmateGUI(root)
    root.mainloop()
