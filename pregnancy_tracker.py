from datetime import datetime

class PregnancyTracker:
    def __init__(self, connection, current_user):
        self.connection = connection
        self.current_user = current_user

    def track_pregnancy(self):
        due_date = self.current_user['due_date']
        today = datetime.now().date()
        days_until_due = (due_date - today).days
        days_pregnant = 280 - days_until_due
        weeks_pregnant = days_pregnant // 7

        print(f"\nYou are {weeks_pregnant} weeks pregnant. Days until due date: {days_until_due}.")


