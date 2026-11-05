import json
from app import app, db, Question

def seed_database():
    print("[🌱 SEEDER] Initializing question bank import...")

    # Sample dataset representing questions from different categories/certifications
    sample_questions = [
        {
            "category": "Cardiac Pharmacology",
            "difficulty": 2,
            "prompt_text": "A patient in ventricular fibrillation is unresponsive. Following initial CPR and defibrillation, which initial IV bolus dose of Amiodarone is indicated per ACLS protocols?",
            "options_json": json.dumps(["A) 150 mg", "B) 300 mg", "C) 1.0 mg/kg", "D) 3 mg"]),
            "correct_answer": "B",
            "rationale": "The initial recommended adult IV/IO bolus dose of Amiodarone for cardiac arrest (VF/pulseless VT) is 300 mg, followed by a possible second dose of 150 mg."
        },
        {
            "category": "Cardiac Pharmacology",
            "difficulty": 3,
            "prompt_text": "An adult patient presents with stable narrow-complex supraventricular tachycardia (SVT). Adenosine is ordered. What is the correct initial rapid IV push dosage?",
            "options_json": json.dumps(["A) 3 mg", "B) 6 mg", "C) 12 mg", "D) 20 mg"]),
            "correct_answer": "B",
            "rationale": "The initial rapid IV push dose of Adenosine for SVT is 6 mg, followed immediately by a normal saline flush. A second dose of 12 mg can be given if needed."
        },
        {
            "category": "Medical-Surgical",
            "difficulty": 1,
            "prompt_text": "Which nursing intervention is top priority when caring for a client newly diagnosed with acute asthma exacerbation experiencing intercostal retractions?",
            "options_json": json.dumps(["A) Administer an over-the-counter cough suppressant", "B) Immediately prepare for emergent airway stabilization", "C) Instruct the patient to perform deep breathing exercises", "D) Document baseline vital signs only"]),
            "correct_answer": "B",
            "rationale": "Silent chest and severe retractions indicate impending respiratory failure and airway collapse, making airway management the absolute highest priority."
        },
        {
            "category": "Pharmacology",
            "difficulty": 2,
            "prompt_text": "A client is experiencing symptomatic bradycardia with a heart rate of 34 bpm. According to ACLS guidelines, what is the initial medication of choice and dosage?",
            "options_json": json.dumps(["A) Atropine 1 mg IV push", "B) Epinephrine 1 mg IV push", "C) Lidocaine 1.5 mg/kg", "D) Dopamine infusion"]),
            "correct_answer": "A",
            "rationale": "Atropine 1 mg IV push is the first-line drug for symptomatic bradycardia, repeatable every 3 to 5 minutes to a maximum dose of 3 mg."
        }
    ]

    with app.app_context():
        # Optional: Clear out old test questions if resetting
        # Question.query.delete()

        added_count = 0
        for q_data in sample_questions:
            # Check if question already exists to avoid duplicates
            existing = Question.query.filter_by(prompt_text=q_data["prompt_text"]).first()
            if not existing:
                new_q = Question(
                    category=q_data["category"],
                    difficulty=q_data["difficulty"],
                    prompt_text=q_data["prompt_text"],
                    options_json=q_data["options_json"],
                    correct_answer=q_data["correct_answer"],
                    rationale=q_data["rationale"]
                )
                db.session.add(new_q)
                added_count += 1

        db.session.commit()
        print(f"[✅ SUCCESS] Successfully seeded {added_count} new questions into the database!")

if __name__ == "__main__":
    seed_database()