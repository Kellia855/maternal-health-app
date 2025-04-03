import os
from datetime import datetime

def clear_screen():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix/Linux/MacOS
        os.system('clear')

class Profile:
    def __init__(self, connection, current_user):
        self.connection = connection
        self.current_user = current_user

    def update_profile(self):
        clear_screen()
        print("\n" + "="*50)
        print("** UPDATE PROFILE **")
        print("="*50)
        
        print("What would you like to update?")
        print("1. Name")
        print("2. Password")
        print("3. Due date")
        print("4. Last checkup date")
        print("5. Go back")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            new_name = input("Enter new name: ").strip()
            cursor = self.connection.cursor()
            cursor.execute("UPDATE users SET name = %s WHERE id = %s", 
                          (new_name, self.current_user['id']))
            self.connection.commit()
            self.current_user['name'] = new_name
            print("\n* Name updated successfully!")
            
        elif choice == "2":
            new_password = input("Enter new password: ").strip()
            cursor = self.connection.cursor()
            cursor.execute("UPDATE users SET password = %s WHERE id = %s", 
                          (new_password, self.current_user['id']))
            self.connection.commit()
            self.current_user['password'] = new_password
            print("\n* Password updated successfully!")
            
        elif choice == "3":
            new_due_date = input("Enter new due date (YYYY-MM-DD): ").strip()
            try:
                date_obj = datetime.strptime(new_due_date, "%Y-%m-%d").date()
                cursor = self.connection.cursor()
                cursor.execute("UPDATE users SET due_date = %s WHERE id = %s", 
                            (new_due_date, self.current_user['id']))
                self.connection.commit()
                
                self.current_user['due_date'] = date_obj
                
                cursor.execute("""
                DELETE FROM reminders 
                WHERE user_id = %s AND reminder_type = 'checkup' AND reminder_date > CURDATE()
                """, (self.current_user['id'],))
                
                # Import create_default_checkup_reminders function
                from main import create_default_checkup_reminders
                create_default_checkup_reminders(self.connection, self.current_user['id'], date_obj)
                
                print("\n* Due date updated successfully!")
                print("* Your checkup schedule has been updated accordingly.")
            except ValueError:
                print("! Invalid date format. Please use YYYY-MM-DD.")
                
        elif choice == "4":
            new_checkup = input("Enter last checkup date (YYYY-MM-DD): ").strip()
            try:
                date_obj = datetime.strptime(new_checkup, "%Y-%m-%d").date()
                cursor = self.connection.cursor()
                cursor.execute("UPDATE users SET last_checkup = %s WHERE id = %s", 
                            (new_checkup, self.current_user['id']))
                self.connection.commit()
                self.current_user['last_checkup'] = date_obj
                print("\n* Last checkup date updated successfully!")
            except ValueError:
                print("! Invalid date format. Please use YYYY-MM-DD.")
            
        elif choice == "5":
            return
        
        else:
            print("\n! Invalid choice.")
        
        input("\nPress Enter to continue...")