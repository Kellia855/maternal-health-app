from auth import Auth
from menu import Menu
from pregnancy_tracker import PregnancyTracker
from health_tips import HealthTips
from reminders import Reminder
from hospital_finder import HospitalFinder
from profile import Profile
import mysql.connector
from datetime import datetime, timedelta
import os

def clear_screen():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix/Linux/MacOS
        os.system('clear')

def connect_db():
    """Establishes a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        print("* Database connection successful!")
        return connection
    except mysql.connector.Error as err:
        print("\n! Database connection error. Please check your credentials.")
        print(f"Error: {err}")
        return None

def setup_database(connection):
    """Sets up the database with all necessary tables and sample data."""
    if connection is None:
        print("\n! Database connection failed. Cannot set up the application.")
        return False
        
    cursor = connection.cursor()
    
    # Create database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS maternal_health_db")
    connection.commit()
    print("* Database created!")
    
    # Use the database
    cursor.execute("USE maternal_health_db")

    # Drop existing tables to ensure clean setup
    cursor.execute("DROP TABLE IF EXISTS reminders")
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS health_tips")
    cursor.execute("DROP TABLE IF EXISTS hospitals")
    
    # Create tables
    sql_statements = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            age INT NOT NULL,
            due_date DATE NOT NULL,
            last_checkup DATE NULL
        )""",
        """
        CREATE TABLE IF NOT EXISTS reminders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            reminder_date DATE NOT NULL,
            message TEXT NOT NULL,
            reminder_type VARCHAR(50) NOT NULL,
            is_completed BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )""",
        """
        CREATE TABLE IF NOT EXISTS health_tips (
            id INT AUTO_INCREMENT PRIMARY KEY,
            week_number INT NOT NULL,
            topic VARCHAR(255) NOT NULL,
            tip TEXT NOT NULL
        )""",
        """
        CREATE TABLE IF NOT EXISTS hospitals (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            province VARCHAR(255) NOT NULL,
            phone VARCHAR(20),
            services TEXT
        )"""
    ]

    for sql in sql_statements:
        cursor.execute(sql)
    
    connection.commit()
    print("* Database tables created!")
    
    # Add sample data
    add_sample_health_tips(connection)
    add_sample_hospitals(connection)
    
    return True

def add_sample_health_tips(connection):
    """Adds sample health tips to the database."""
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM health_tips")
    count = cursor.fetchone()[0]
    
    if count == 0:
        tips = [
            (4, "Early Pregnancy", "Start taking prenatal vitamins with folic acid to help prevent birth defects."),
            (8, "Morning Sickness", "Eat small, frequent meals and stay hydrated to help manage nausea."),
            (12, "First Trimester Checkup", "Schedule your first ultrasound to confirm your due date."),
            (16, "Nutrition", "Increase your intake of calcium-rich foods for your baby's bone development."),
            (20, "Anatomy Scan", "Your mid-pregnancy ultrasound will check your baby's development."),
            (24, "Gestational Diabetes", "Your doctor will offer screening for gestational diabetes around now."),
            (28, "Third Trimester", "Begin monitoring baby's kicks and movements daily."),
            (32, "Preparing for Birth", "Consider taking a childbirth preparation class."),
            (36, "Final Weeks", "Pack your hospital bag and finalize your birth plan."),
            (40, "Due Date", "Watch for signs of labor and stay in contact with your healthcare provider.")
        ]
        
        sql = "INSERT INTO health_tips (week_number, topic, tip) VALUES (%s, %s, %s)"
        cursor.executemany(sql, tips)
        connection.commit()
        print("* Sample health tips added!")

def add_sample_hospitals(connection):
    """Adds sample hospitals to the database."""
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM hospitals")
    count = cursor.fetchone()[0]
    
    if count == 0:
        hospitals = [
            ("Central Maternity Hospital", "Central", "+123-456-7890", "24/7 Labor & Delivery, NICU, Prenatal Care"),
            ("Northern Women's Clinic", "North", "+123-456-7891", "Obstetrics, Gynecology, Prenatal Classes"),
            ("Eastern General Hospital", "East", "+123-456-7892", "Labor & Delivery, Family Planning, Ultrasound"),
            ("Southern Maternal Care Center", "South", "+123-456-7893", "High-Risk Pregnancy Care, NICU, Lactation Support"),
            ("Western Health Center", "West", "+123-456-7894", "Midwifery Services, Natural Birth Options, Prenatal Yoga")
        ]
        
        sql = "INSERT INTO hospitals (name, province, phone, services) VALUES (%s, %s, %s, %s)"
        cursor.executemany(sql, hospitals)
        connection.commit()
        print("* Sample hospitals added!")

def create_default_checkup_reminders(connection, user_id, due_date):
    """Create default checkup reminders for a new user."""
    cursor = connection.cursor()
    
    conception_date = due_date - timedelta(days=280)
    
    checkup_dates = []
    
    for month in range(1, 4):
        checkup_date = conception_date + timedelta(days=30 * month)
        checkup_dates.append((checkup_date, f"{month} month checkup"))
    
    for month in range(4, 7):
        checkup_date = conception_date + timedelta(days=30 * month)
        checkup_dates.append((checkup_date, f"{month} month checkup"))
    
    weeks = 28
    while weeks <= 40:
        checkup_date = conception_date + timedelta(days=7 * weeks)
        if weeks < 36:
            checkup_dates.append((checkup_date, f"Week {weeks} checkup"))
            weeks += 2
        else:
            checkup_dates.append((checkup_date, f"Week {weeks} checkup"))
            weeks += 1
    
    for date, description in checkup_dates:
        if date > datetime.now().date():
            sql = """
            INSERT INTO reminders (user_id, reminder_date, message, reminder_type)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (user_id, date.strftime("%Y-%m-%d"), 
                                f"Schedule your {description} with your doctor", "checkup"))
    
    connection.commit()

class MaternalHealthApp:
    def __init__(self):
        # Connect to database and set it up
        self.connection = connect_db()
        if self.connection:
            setup_database(self.connection)
        
        # Initialize state
        self.current_user = None
        
        # Initialize components
        self.auth = Auth(self.connection)
        self.menu = Menu(self)
        
    def main(self):
        """Main application entry point."""
        if self.connection is None:
            print("\n! Could not connect to the database. Please check your configuration.")
            return
            
        clear_screen()
        print("\n" + "="*60)
        print("  WELCOME TO THE MATERNAL HEALTH SUPPORT SYSTEM  ".center(60, "="))
        print("="*60)
        print("\nThis system helps expectant mothers track their pregnancy journey,")
        print("receive health tips, set reminders, and locate nearby hospitals.")
        
        input("\nPress Enter to continue...")
        
        # Start main application loop
        while True:
            choice = self.menu.main_menu()
            if choice == "1":
                self.auth.register_user()
            elif choice == "2":
                user = self.auth.login()
                if user:
                    self.current_user = user
                    self.user_menu()
            elif choice == "3":
                clear_screen()
                print("\n* Thank you for using the Maternal Health System. Goodbye!")
                break
            else:
                print("\n! Invalid option. Please try again.")
                input("\nPress Enter to continue...")
    
    def user_menu(self):
        """Handle the user menu after login."""
        while self.current_user:
            choice = self.menu.user_menu(self.current_user['name'])
            
            if choice == "1":
                tracker = PregnancyTracker(self.connection, self.current_user)
                tracker.track_pregnancy()
            elif choice == "2":
                reminder = Reminder(self.connection, self.current_user)
                reminder.add_reminder()
            elif choice == "3":
                reminder = Reminder(self.connection, self.current_user)
                reminder.view_reminders()
            elif choice == "4":
                tips = HealthTips(self.connection)
                tips.view_tips(self.current_user)
            elif choice == "5":
                hospital_finder = HospitalFinder(self.connection)
                hospital_finder.find_hospitals()
            elif choice == "6":
                profile = Profile(self.connection, self.current_user)
                profile.update_profile()
            elif choice == "7":
                self.auth.logout(self.current_user)
                self.current_user = None
                break
            else:
                print("\n! Invalid option. Please try again.")
                input("\nPress Enter to continue...")


if __name__ == "__main__":
    app = MaternalHealthApp()
    app.main()