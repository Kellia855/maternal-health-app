import os
from datetime import datetime

def clear_screen():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix/Linux/MacOS
        os.system('clear')

class Reminder:
    def __init__(self, connection, current_user):
        self.connection = connection
        self.current_user = current_user

    def add_reminder(self):
        clear_screen()
        print("\n" + "="*50)
        print("** ADD REMINDER **")
        print("="*50)
        
        print("Reminder types:")
        print("1. Doctor Appointment")
        print("2. Medication")
        print("3. Exercise")
        print("4. Nutrition")
        print("5. Other")
        
        while True:
            try:
                type_choice = int(input("Select reminder type (1-5): ").strip())
                if 1 <= type_choice <= 5:
                    break
                print("! Please enter a number between 1 and 5.")
            except ValueError:
                print("! Please enter a valid number.")
        
        reminder_types = {
            1: "checkup",
            2: "medication",
            3: "exercise",
            4: "nutrition",
            5: "other"
        }
        
        reminder_type = reminder_types[type_choice]
        
        while True:
            date = input("Date (YYYY-MM-DD): ").strip()
            try:
                date_obj = datetime.strptime(date, "%Y-%m-%d")
                if date_obj >= datetime.now():
                    break
                print("! Please enter a future date.")
            except ValueError:
                print("! Please enter a valid date in YYYY-MM-DD format.")
        
        message = input("Message: ").strip()

        cursor = self.connection.cursor()
        sql = """
        INSERT INTO reminders (user_id, reminder_date, message, reminder_type) 
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (self.current_user['id'], date, message, reminder_type))
        self.connection.commit()
        print("\n* Reminder added successfully!")
        input("\nPress Enter to continue...")

    def view_reminders(self):
        clear_screen()
        print("\n" + "="*50)
        print("** YOUR REMINDERS **")
        print("="*50)
        
        print("Filter by:")
        print("1. All reminders")
        print("2. Doctor appointments")
        print("3. Medication reminders")
        print("4. Exercise reminders")
        print("5. Nutrition reminders")
        print("6. Other reminders")
        print("7. By date range")
        
        filter_choice = input("Select filter (1-7): ").strip()
        
        cursor = self.connection.cursor(dictionary=True)
        
        query = """
        SELECT id, reminder_date, message, reminder_type, is_completed 
        FROM reminders 
        WHERE user_id = %s 
        """
        
        params = [self.current_user['id']]
        
        if filter_choice == "2":
            query += "AND reminder_type = 'checkup' "
        elif filter_choice == "3":
            query += "AND reminder_type = 'medication' "
        elif filter_choice == "4":
            query += "AND reminder_type = 'exercise' "
        elif filter_choice == "5":
            query += "AND reminder_type = 'nutrition' "
        elif filter_choice == "6":
            query += "AND reminder_type = 'other' "
        elif filter_choice == "7":
            start_date = input("Start date (YYYY-MM-DD): ").strip()
            end_date = input("End date (YYYY-MM-DD): ").strip()
            query += "AND reminder_date BETWEEN %s AND %s "
            params.extend([start_date, end_date])
        
        query += "ORDER BY reminder_date"
        
        cursor.execute(query, params)
        reminders = cursor.fetchall()
        
        if not reminders:
            print("\nNo reminders found with the selected filter.")
            input("\nPress Enter to continue...")
            return
        
        clear_screen()
        print("\n" + "="*50)
        print("** YOUR REMINDERS **")
        print("="*50)
        print("\n" + "-"*70)
        print(f"{'ID':<5} {'Date':<12} {'Type':<12} {'Status':<10} Message")
        print("-"*70)
        
        for reminder in reminders:
            date_str = reminder['reminder_date'].strftime("%Y-%m-%d")
            status = "* Done" if reminder['is_completed'] else "o Pending"
            print(f"{reminder['id']:<5} {date_str:<12} {reminder['reminder_type']:<12} {status:<10} {reminder['message']}")
        
        print("\nWould you like to mark any reminder as completed? (y/n)")
        if input().lower() == 'y':
            self.mark_reminder_completed()
        else:
            input("\nPress Enter to continue...")

    def mark_reminder_completed(self):
        reminder_id = input("Enter reminder ID to mark as completed: ").strip()
        
        cursor = self.connection.cursor()
        cursor.execute("""
        UPDATE reminders SET is_completed = TRUE
        WHERE id = %s AND user_id = %s
        """, (reminder_id, self.current_user['id']))
        
        if cursor.rowcount > 0:
            self.connection.commit()
            print("* Reminder marked as completed!")
        else:
            print("! Reminder not found or already completed.")
        
        input("\nPress Enter to continue...")