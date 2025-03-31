class Reminder:
    def __init__(self, connection, current_user):
        self.connection = connection
        self.current_user = current_user

    def add_reminder(self):
        reminder_text = input("Enter reminder text: ").strip()
        reminder_date = input("Enter reminder date (YYYY-MM-DD): ").strip()

        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO reminders (user_id, reminder_text, reminder_date) VALUES (%s, %s, %s)",
                       (self.current_user['id'], reminder_text, reminder_date))
        self.connection.commit()
        print("\n* Reminder added successfully!")

