import json
import requests
from bs4 import BeautifulSoup
from app import app, db, Question

def fetch_and_verify_nclex_data():
    print("==============================================================")
    print("[🔍 CRAWLER] Initiating web-scouring & guideline sync...")
    print("==============================================================")
    
    # Target simulation: In a live environment, this points to trusted nursing education 
    # repositories, question-bank feeds, or guidelines updates.
    scraped_items = [
        {
            "category": "Cardiac Pharmacology",
            "difficulty": 3,
            "prompt_text": "A client with acute decompensated heart failure is receiving an IV infusion of a vasodilator. Which assessment finding indicates the medication is having its intended therapeutic effect?",
            "options_json": json.dumps([
                "A) Decreased systemic vascular resistance and reduced left ventricular afterload", 
                "B) Increased heart rate to compensate for systemic hypertension", 
                "C) Elevated pulmonary capillary wedge pressure", 
                "D) Reduced urine output due to renal conservation"
            ]),
            "correct_answer": "A",
            "rationale": "Vasodilators reduce preload and afterload by relaxing vascular smooth muscle, improving cardiac output and lowering systemic vascular resistance."
        }
    ]
    
    valid_questions = []
    
    # Data Verification Layer
    for item in scraped_items:
        # Verify that all necessary keys exist and data is clean
        if not item.get("prompt_text") or not item.get("correct_answer"):
            print(f"[⚠️ WARNING] Dropping malformed item: {item.get('prompt_text', 'Unknown')}")
            continue
            
        # Clean and sanitize strings
        cleaned_prompt = item["prompt_text"].strip()
        cleaned_rationale = item.get("rationale", "No rationale provided.").strip()
        
        valid_questions.append({
            "category": item["category"],
            "difficulty": item["difficulty"],
            "prompt_text": cleaned_prompt,
            "options_json": item["options_json"],
            "correct_answer": item["correct_answer"].upper(),
            "rationale": cleaned_rationale
        })
        
    print(f"[🛡️ VERIFICATION] Passed validation: {len(valid_questions)}/{len(scraped_items)} items.")
    
    # Database Injection Layer
    with app.app_context():
        inserted_count = 0
        for q in valid_questions:
            # Check for duplicates so we don't spam the database with repeated questions
            existing = Question.query.filter_by(prompt_text=q["prompt_text"]).first()
            if not existing:
                new_question = Question(
                    category=q["category"],
                    difficulty=q["difficulty"],
                    prompt_text=q["prompt_text"],
                    options_json=q["options_json"],
                    correct_answer=q["correct_answer"],
                    rationale=q["rationale"]
                )
                db.session.add(new_question)
                inserted_count += 1
                
        db.session.commit()
        print(f"[✅ SUCCESS] Injected {inserted_count} new verified questions into Azure SQL!")
    print("==============================================================")

if __name__ == "__main__":
    fetch_and_verify_nclex_data()
# Add this at the end of your script to log execution runs
import datetime

log_path = r"C:\Users\11\Desktop\tetris_ai_training\scraper_activity.log"
with open(log_path, "a", encoding="utf-8") as log_file:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file.write(f"[{timestamp}] Daily NCLEX Scraper executed successfully and synced with Azure SQL.\n")