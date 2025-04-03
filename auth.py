import os
from datetime import datetime, timedelta

def clear_screen():
    if os.name == 'nt': 
        os.system('cls')
    else: 
        os.system('clear')

class Auth:
    def __init__(self, connection):
        self.connection = connection

    def register_user(self):
        clear_screen()
        print("\n" + "="*50)
        print("** USER REGISTRATION **")
        print("="*50)
        
        name = input("Full name: ").strip()
        
        while True:
            username = input("Username: ").strip()
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                print("! This username is already taken. Please choose another one.")
            else:
                break
                
        password = input("Password: ").strip()
        
        while True:
            try:
                age = int(input("Age: ").strip())
                if 15 <= age <= 50:
                    break
                print("! Please enter a valid age between 15 and 50.")
            except ValueError:
                print("! Please enter a valid number for age.")
        
        while True:
            due_date = input("Due date (YYYY-MM-DD): ").strip()
            try:
                date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
                today = datetime.now().date()
                
                if date_obj > today and date_obj < today + timedelta(days=280):
                    break
                print("! Please enter a valid future due date within the next 9 months.")
            except ValueError:
                print("! Please enter a valid date in YYYY-MM-DD format.")

        try:
            cursor = self.connection.cursor()
            sql = """
            INSERT INTO users (name, username, password, age, due_date) 
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (name, username, password, age, due_date))
            self.connection.commit()
            
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            user_id = user[0]
            
            # Import this here to avoid circular import
            from main import create_default_checkup_reminders
            create_default_checkup_reminders(self.connection, user_id, date_obj)
            
            print("\n* Registration successful!")
            print("* Monthly checkup reminders have been automatically created for you.")
            input("\nPress Enter to continue...")
            return True
        except Exception as err:
            print(f"\n! Could not complete registration. Error: {err}")
            input("\nPress Enter to continue...")
            return False

    def login(self):
        clear_screen()
        print("\n" + "="*50)
        print("** USER LOGIN **")
        print("="*50)
        
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", 
                      (username, password))
        user = cursor.fetchone()

        if user:
            print(f"\n* Welcome back, {user['name']}!")
            
            # Check upcoming appointments
            self.check_upcoming_appointments(user)
            self.show_relevant_health_tips(user)
            
            input("\nPress Enter to continue...")
            return user
        else:
            print("\n! Invalid username or password. Please try again.")
            input("\nPress Enter to continue...")
            return None
    
    def check_upcoming_appointments(self, user):
        cursor = self.connection.cursor(dictionary=True)
        today = datetime.now().date().strftime("%Y-%m-%d")
        next_week = (datetime.now().date() + timedelta(days=7)).strftime("%Y-%m-%d")
        
        cursor.execute("""
        SELECT reminder_date, message FROM reminders 
        WHERE user_id = %s AND reminder_date BETWEEN %s AND %s AND reminder_type = 'checkup'
        ORDER BY reminder_date
        """, (user['id'], today, next_week))
        
        appointments = cursor.fetchall()
        
        if appointments:
            print("\n** UPCOMING APPOINTMENTS **")
            print("-" * 40)
            for appt in appointments:
                date_obj = appt['reminder_date']
                formatted_date = date_obj.strftime("%A, %B %d, %Y")
                print(f"* {formatted_date}: {appt['message']}")
    
    def show_relevant_health_tips(self, user):
        due_date = user['due_date']
        today = datetime.now().date()
        days_until_due = (due_date - today).days
        weeks_pregnant = max(1, int((280 - days_until_due) / 7))
        
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("""
        SELECT topic, tip FROM health_tips
        WHERE week_number <= %s
        ORDER BY week_number DESC
        LIMIT 1
        """, (weeks_pregnant,))
        
        tip = cursor.fetchone()
        
        if tip:
            print("\n** THIS WEEK'S HEALTH TIP **")
            print("-" * 40)
            print(f"You are in week {weeks_pregnant} of your pregnancy")
            print(f"Topic: {tip['topic']}")
            print(f"{tip['tip']}")
            
    def logout(self, user):
        if user:
            print(f"\n* Goodbye, {user['name']}! Have a wonderful day!")
            input("\nPress Enter to continue...")
        else:
            print("\nNo user is currently logged in.")
            input("\nPress Enter to continue...")