from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Connect to Azure SQL via environment variable, falling back to local SQLite for testing
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'AZURE_SQL_CONNECTION_STRING', 
    'sqlite:///nclex_app.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Database Models ---
class User(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class Question(db.Model):
    __tablename__ = 'Questions'
    question_id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.Integer, default=1)
    prompt_text = db.Column(db.Text, nullable=False)
    options_json = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.String(10), nullable=False)
    rationale = db.Column(db.Text)

class UserProgress(db.Model):
    __tablename__ = 'UserProgress'
    progress_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    question_id = db.Column(db.Integer, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)


# --- Authentication Endpoints ---
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"status": "success", "message": "User registered successfully!"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and check_password_hash(user.password_hash, data['password']):
        return jsonify({"status": "success", "user_id": user.user_id, "username": user.username}), 200
    return jsonify({"status": "error", "message": "Invalid email or password"}), 401


# --- Practice Test & Cardiac Toggle Endpoint ---
@app.route('/api/practice/start', methods=['POST'])
def start_practice_test():
    """
    Starts a practice test session. 
    Accepts a 'cardiac_focus' boolean toggle to flood the quiz with cardiac/pharmacology items if true.
    """
    data = request.get_json()
    cardiac_focus = data.get('cardiac_focus', False)
    
    if cardiac_focus:
        # Filter strictly for cardiac and high-acuity pharmacology questions
        questions = Question.query.filter(Question.category.ilike('%cardiac%')).limit(10).all()
    else:
        # Pull general NCLEX cross-section mix
        questions = Question.query.limit(10).all()
        
    test_packet = []
    for q in questions:
        test_packet.append({
            "question_id": q.question_id,
            "category": q.category,
            "prompt_text": q.prompt_text,
            "options": q.options_json # In production, parse JSON string into list/dict
        })
        
    return jsonify({
        "status": "success",
        "cardiac_mode_active": cardiac_focus,
        "questions": test_packet
    }), 200


# --- Answer Submission & Evaluation Endpoint ---
@app.route('/api/practice/submit', methods=['POST'])
def submit_practice_test():
    data = request.get_json()
    user_id = data.get('user_id')
    responses = data.get('responses', []) # List of {"question_id": X, "selected_answer": "A"}
    
    correct_count = 0
    total_answered = len(responses)
    failed_categories = set()

    for item in responses:
        q_id = item.get('question_id')
        selected = item.get('selected_answer').strip().upper()
        
        question = Question.query.get(q_id)
        if not question:
            continue
            
        is_correct = (selected == question.correct_answer.strip().upper())
        if is_correct:
            correct_count += 1
        else:
            failed_categories.add(question.category)
            
        # Log progress to database
        progress = UserProgress(user_id=user_id, question_id=q_id, is_correct=is_correct)
        db.session.add(progress)
        
    db.session.commit()
    score_percentage = (correct_count / total_answered * 100) if total_answered > 0 else 0

    return jsonify({
        "status": "completed",
        "score_percentage": round(score_percentage, 1),
        "correct_count": correct_count,
        "total_answered": total_answered,
        "flagged_weak_areas": list(failed_categories),
        "message": "Practice test evaluated and saved to Azure SQL."
    }), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)