import mysql.connector


# Connect to the MySQL database
def connect_to_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="arinv3110",  # Replace with your MySQL password
            database="quiz_app"
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        exit()


# Register a new user
def register_user():
    db = connect_to_db()
    cursor = db.cursor()
    username = input("Enter a username: ")
    password = input("Enter a password: ")

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        print("User registered successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        db.close()


# Login user
def login_user():
    db = connect_to_db()
    cursor = db.cursor()
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    result = cursor.fetchone()

    db.close()
    if result:
        print("Login successful!")
        return username
    else:
        print("Invalid credentials.")
        return None


# Start the quiz
def start_quiz(username):
    db = connect_to_db()
    cursor = db.cursor()

    topic = input("Choose a topic (Math, Science, History): ").capitalize()
    cursor.execute("SELECT question, answer FROM questions WHERE topic = %s", (topic,))
    questions = cursor.fetchall()

    if not questions:
        print("No questions available for this topic.")
        return

    score = 0
    for question, answer in questions[:5]:  # Ask up to 5 questions
        print(f"\n{question}")
        user_answer = input("Your answer: ")
        if user_answer.strip().lower() == answer.strip().lower():
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer was: {answer}")

    print(f"\nYour score: {score}/{len(questions[:5])}")

    # Save the score
    cursor.execute("INSERT INTO scores (username, score) VALUES (%s, %s)", (username, score))
    db.commit()
    db.close()


# Main program
def main():
    print("Welcome to the Quiz Application!")
    while True:
        choice = input("Do you want to (1) Register or (2) Login? Enter 1 or 2: ")
        if choice == '1':
            register_user()
        elif choice == '2':
            username = login_user()
            if username:
                break

    while True:
        start_quiz(username)
        retry = input("Do you want to (1) Retry or (2) Exit? Enter 1 or 2: ")
        if retry == '2':
            print("Thank you for playing!")
            break


main()


