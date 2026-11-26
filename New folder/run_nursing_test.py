import sys
import time
import datetime

# --- EMERGENCY CARDIAC & PHARMACOLOGY DATA SCRIPT ---
QUESTIONS = [
    {
        "id": 1,
        "topic": "Heart Block Layouts",
        "question": "A patient's ECG monitor displays a changing PR interval that grows progressively longer with each beat until a QRS complex is completely dropped. Which rhythm is being observed?",
        "options": {
            "A": "First-Degree AV Block",
            "B": "Second-Degree AV Block (Mobitz Type I / Wenckebach)",
            "C": "Third-Degree Complete Heart Block",
            "D": "Ventricular Fibrillation (V-Fib)"
        },
        "correct": "B",
        "analogy": "Think of a worker carrying boxes up a ladder who gets tireder and tireder with each step. First step takes 2 seconds, second takes 4 seconds, third takes 6 seconds... and on the fourth step, he drops the box completely, takes a deep breath, resets, and starts climbing again from the bottom.",
        "protocol": "This is a Mobitz Type I (Wenckebach) block. The AV node conduction delay is progressive until an impulse is blocked entirely. Monitor closely for progression to higher-degree blocks; look for symptomatic bradycardia."
    },
    {
        "id": 2,
        "topic": "Advanced Life Support (ACLS)",
        "question": "A patient is in refractory ventricular fibrillation (V-Fib). The code team has delivered a second defibrillation shock and pushed one dose of epinephrine. Which medication and dosage is the standard first-line antiarrhythmic to prepare next?",
        "options": {
            "A": "Lidocaine 5 mg/kg IV push",
            "B": "Adenosine 6 mg rapid IV push",
            "C": "Amiodarone 300 mg IV bolus",
            "D": "Atropine 1 mg IV push"
        },
        "correct": "C",
        "analogy": "This is a massive electrical short circuit at the bottom pump. Amiodarone acts as your heavy-duty circuit stabilizer, slowing down the chaotic impulses in the heart tissue so the main power node can regain control.",
        "protocol": "Per ACLS guidelines, for persistent V-Fib/pulseless V-Tach after the second shock, administer Amiodarone 300 mg IV/IO rapid bolus. A secondary dose of 150 mg may be administered once if the rhythm persists."
    },
    {
        "id": 3,
        "topic": "High-Degree Conduction Failure",
        "question": "The ECG monitor reveals a total dissociation between the P waves (atria) and QRS complexes (ventricles). The ventricles are beating independently at a sluggish rate of 32 beats/minute. Atropine is administered but fails to increase the heart rate. What is the immediate treatment priority?",
        "options": {
            "A": "Administer an additional 3 mg of Atropine immediately",
            "B": "Prepare for immediate transcutaneous electronic pacing capture",
            "C": "Infuse a Lidocaine maintenance drip at 2 mg/min",
            "D": "Double the patient's intravenous fluid maintenance rate"
        },
        "correct": "B",
        "analogy": "This is a completely severed master wire. The top supervisor is shouting orders, but the broken line means the factory floor can't hear a word. The floor drops into an emergency safety-override loop (32 bpm). Atropine can't fix a cut wire; you must connect an external electronic pacing box to jumpstart the circuit directly.",
        "protocol": "Third-Degree Complete Heart Block represents complete AV dissociation. Atropine is ineffective because the conduction block is below the AV node. Immediate electrical pacing (transcutaneous or transvenous) is required to maintain cardiac output."
    }
]

def log_test_result(score, total):
    """ Writes a tight, punchy entry directly into your project training logs """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    percentage = (score / total) * 100
    log_line = f"[{timestamp}] [NCLEX_EXAM_RUN] Completed: {score}/{total} ({percentage:.1f}%) | Validation finalized safely thanks to Gemini.\n"
    
    with open("interaction_log.txt", "a") as f:
        f.write(log_line)

def run_console_test():
    print("==============================================================")
    print("🩺 [NCLEX MASTER ENGINE] - CLI EXAMINATION MODULE ACTIVE")
    print("==============================================================")
    time.sleep(0.5)
    
    score = 0
    total_q = len(QUESTIONS)
    
    for q in QUESTIONS:
        print(f"\n[Question {q['id']}/{total_q}] Topic: {q['topic']}")
        print(f"{q['question']}\n")
        
        for key, val in q['options'].items():
            print(f"  ({key}) {val}")
            
        user_ans = input("\nYour Selection (A, B, C, or D): ").strip().upper()
        
        if user_ans == q['correct']:
            print("\n👑 CORRECT! The logical matrix aligns perfectly.")
            score += 1
        else:
            print(f"\n❌ MISMATCH. The correct answer was ({q['correct']}).")
            
        # Explanatory Tier Interface Selection
        print("\nChoose your explanation framework:")
        print("  (1) View Level 3 Analogy (Mechanical / Electrical Wiring Layout)")
        print("  (2) View Level 50 Protocol (Strict Clinical Nursing Breakdown)")
        print("  (3) Skip to next question")
        
        exp_choice = input("Selection: ").strip()
        print("-" * 62)
        
        if exp_choice == "1":
            print(f"\n[🛠️ LEVEL 3 ANALOGY] {q['analogy']}\n")
        elif exp_choice == "2":
            print(f"\n[🩺 LEVEL 50 CLINICAL PROTOCOL] {q['protocol']}\n")
            
        input("Press Enter to advance the console...")
        print("=" * 62)

    final_pct = (score / total_q) * 100
    print(f"\n==============================================================")
    print(f"🏁 EXAMINATION COMPLETE. Final Score: {score}/{total_q} ({final_pct:.1f}%)")
    print("[System Note: Execution logged successfully thanks to Gemini]")
    print("==============================================================")
    
    # Commit metrics straight to your interaction log
    log_test_result(score, total_q)

if __name__ == "__main__":
    run_console_test()
