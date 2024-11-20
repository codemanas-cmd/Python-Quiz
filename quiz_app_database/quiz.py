import os
from getpass import getpass
from datetime import datetime
import random
import sqlite3
from quiz_questions import MATH_CONFIG, SCIENCE_QUESTIONS, HISTORY_QUESTIONS

def init_database():
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS scores
                 (username TEXT,
                  quiz_type TEXT,
                  score REAL,
                  date TEXT)''')
    
    conn.commit()
    conn.close()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_user(username, password):
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute('INSERT INTO users VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

def check_user_exists(username):
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute('SELECT username FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()
    return result is not None

def verify_password(username, password):
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()
    return result[0] == password

def save_score(username, quiz_type, score):
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('INSERT INTO scores (username, quiz_type, score, date) VALUES (?, ?, ?, ?)',
             (username, quiz_type, score, date))
    conn.commit()
    conn.close()

def view_scores(username):
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute('''SELECT quiz_type, score, date FROM scores 
                 WHERE username = ? ORDER BY date DESC''', (username,))
    scores = c.fetchall()
    conn.close()
    
    if not scores:
        print("\nNo quiz attempts yet!")
        input("Press Enter to continue...")
        return
    
    print("\n=== Your Quiz History ===")
    for quiz_type, score, date in scores:
        print(f"\nQuiz Type: {quiz_type}")
        print(f"Score: {score}%")
        print(f"Date: {date}")
    input("\nPress Enter to continue...")

def take_quiz(username, quiz_type):
    if quiz_type == "Math":
        clear_screen()
        print(f"\n=== Math Quiz ===")
        score = 0
        total_questions = 5
        
        for i in range(total_questions):
            num1 = random.randint(*MATH_CONFIG['num1_range'])
            num2 = random.randint(*MATH_CONFIG['num2_range'])
            operator = random.choice(MATH_CONFIG['operators'])
            
            if operator == '+':
                correct_answer = num1 + num2
            elif operator == '-':
                correct_answer = num1 - num2
            else:  # operator == '*'
                correct_answer = num1 * num2
            
            while True:
                try:
                    print(f"\nQuestion {i + 1}:")
                    print(f"What is {num1} {operator} {num2}?")
                    user_answer = float(input("Your answer: "))
                    break
                except ValueError:
                    print("Please enter a valid number!")
            
            if abs(user_answer - correct_answer) < 0.01:
                print("Correct! ✓")
                score += 1
            else:
                print(f"Wrong! The correct answer was {correct_answer}")
            
            input("Press Enter for the next question...")
            clear_screen()
    
    else:
        questions = SCIENCE_QUESTIONS if quiz_type == "Science" else HISTORY_QUESTIONS
        clear_screen()
        print(f"\n=== {quiz_type} Quiz ===")
        score = 0
        total_questions = len(questions)
        
        for i, q in enumerate(questions, 1):
            print(f"\nQuestion {i}:")
            print(q['question'])
            for j, option in enumerate(q['options'], 1):
                print(f"{j}. {option}")
            
            while True:
                try:
                    answer = int(input("\nEnter your answer (1-4): "))
                    if 1 <= answer <= 4:
                        break
                    print("Please enter a number between 1 and 4!")
                except ValueError:
                    print("Please enter a valid number!")
            
            user_answer = q['options'][answer-1]
            if user_answer == q['correct_answer']:
                print("Correct! ✓")
                score += 1
            else:
                print(f"Wrong! The correct answer was: {q['correct_answer']}")
            
            input("Press Enter for the next question...")
            clear_screen()
    
    percentage = (score / total_questions) * 100
    print(f"\nQuiz completed!")
    print(f"You got {score} out of {total_questions} questions correct.")
    print(f"Your score: {percentage}%")
    
    save_score(username, quiz_type, percentage)
    input("Press Enter to continue...")

def quiz_menu(username):
    while True:
        clear_screen()
        print(f"\n=== Welcome {username} ===")
        print("1. Take Math Quiz")
        print("2. Take Science Quiz")
        print("3. Take History Quiz")
        print("4. View Previous Scores")
        print("5. Logout")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            take_quiz(username, "Math")
        elif choice == '2':
            take_quiz(username, "Science")
        elif choice == '3':
            take_quiz(username, "History")
        elif choice == '4':
            view_scores(username)
        elif choice == '5':
            print("\nLogging out...")
            print(f"Goodbye {username}! Come back soon!")
            input("Press Enter to continue...")
            return
        else:
            print("Invalid choice! Please try again.")
            input("Press Enter to continue...")

def signup():
    while True:
        clear_screen()
        print("\n=== Sign Up ===")
        username = input("Enter username (or 'q' to go back): ")
        if username.lower() == 'q':
            return None
        
        if check_user_exists(username):
            print("Username already exists! Please try another one.")
            input("Press Enter to continue...")
            continue
            
        password = getpass("Enter password: ")
        confirm_password = getpass("Confirm password: ")
        
        if password != confirm_password:
            print("Passwords don't match! Please try again.")
            input("Press Enter to continue...")
            continue
            
        save_user(username, password)
        print("Account created successfully!")
        input("Press Enter to continue...")
        return username

def login():
    while True:
        clear_screen()
        print("\n=== Login ===")
        username = input("Enter username (or 'q' to go back): ")
        if username.lower() == 'q':
            return None
            
        if not check_user_exists(username):
            print("Username not found!")
            input("Press Enter to continue...")
            continue
            
        password = getpass("Enter password: ")
        
        if not verify_password(username, password):
            print("Incorrect password!")
            input("Press Enter to continue...")
            continue
            
        print("Login successful!")
        input("Press Enter to continue...")
        return username

def main_menu():
    while True:
        clear_screen()
        print("\n=== Quiz App (Database Storage) ===")
        print("1. Login")
        print("2. Sign Up")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            username = login()
            if username:
                quiz_menu(username)
        elif choice == '2':
            username = signup()
            if username:
                quiz_menu(username)
        elif choice == '3':
            print("\nGoodbye!")
            exit()
        else:
            print("Invalid choice! Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    init_database()  # Initialize database tables
    while True:
        main_menu() 