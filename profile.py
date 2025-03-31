import database
from datetime import datetime

class Profile:
    def __init__(self, connection, current_user):
        self.connection = connection
        self.current_user = current_user

    def update_profile(self):
        print("\n1. Name\n2. Password\n3. Due date\n4. Last checkup date\n5. Go back")
        choice = input("Enter your choice: ").strip()

        cursor = self.connection.cursor()

        if choice == "1":
            new_name = input("Enter new name: ").strip()
            cursor.execute("UPDATE users SET name = %s WHERE id = %s", (new_name, self.current_user['id']))
            self.connection.commit()
            self.current_user['name'] = new_name
            print("\n* Name updated successfully!")

        elif choice == "2":
            new_password = input("Enter new password: ").strip()
            cursor.execute("UPDATE users SET password = %s WHERE id = %s", (new_password, self.current_user['id']))
            self.connection.commit()
            print("\n* Password updated successfully!")

        elif choice == "3":
            new_due_date = input("Enter new due date (YYYY-MM-DD): ").strip()
            try:
                date_obj = datetime.strptime(new_due_date, "%Y-%m-%d").date()
                cursor.execute("UPDATE users SET due_date = %s WHERE id = %s", (new_due_date, self.current_user['id']))
                self.connection.commit()
                print("\n* Due date updated successfully!")
            except ValueError:
                print("! Invalid date format. Please use YYYY-MM-DD.")

        elif choice == "4":
            new_checkup = input("Enter last checkup date (YYYY-MM-DD): ").strip()
            try:
                date_obj = datetime.strptime(new_checkup, "%Y-%m-%d").date()
                cursor.execute("UPDATE users SET last_checkup = %s WHERE id = %s", (new_checkup, self.current_user['id']))
                self.connection.commit()
                print("\n* Last checkup date updated successfully!")
            except ValueError:
                print("! Invalid date format. Please use YYYY-MM-DD.")

