-- 1. Users Table (Handles student accounts and logins)
CREATE TABLE Users (
    user_id INT PRIMARY KEY IDENTITY(1,1),
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT GETDATE()
);

-- 2. Question Bank Table (Stores NCLEX and high-acuity cardiac questions)
CREATE TABLE Questions (
    question_id INT PRIMARY KEY IDENTITY(1,1),
    category VARCHAR(100) NOT NULL, -- e.g., 'Cardiac Pharmacology', 'Med-Surg', 'Safety'
    difficulty INT DEFAULT 1,       -- 1 (Easy) to 3 (Hard)
    prompt_text TEXT NOT NULL,
    options_json TEXT NOT NULL,     -- JSON string containing A, B, C, D choices
    correct_answer CHAR(1) NOT NULL, -- 'A', 'B', 'C', or 'D'
    rationale TEXT                  -- Clinical explanation for the answer
);

-- 3. Practice Test Sessions (Tracks individual test attempts)
CREATE TABLE TestSessions (
    session_id INT PRIMARY KEY IDENTITY(1,1),
    user_id INT FOREIGN KEY REFERENCES Users(user_id),
    mode VARCHAR(50) DEFAULT 'Standard_NCLEX', -- 'Standard_NCLEX' or 'Cardiac_Focus'
    score FLOAT,
    completed_at DATETIME DEFAULT GETDATE()
);

-- 4. User Progress & Analytics (Logs individual question responses for weakness detection)
CREATE TABLE UserProgress (
    progress_id INT PRIMARY KEY IDENTITY(1,1),
    user_id INT FOREIGN KEY REFERENCES Users(user_id),
    question_id INT FOREIGN KEY REFERENCES Questions(question_id),
    selected_answer CHAR(1) NOT NULL,
    is_correct BIT NOT NULL,
    attempted_at DATETIME DEFAULT GETDATE()
);