import os
from datetime import datetime

def clear_screen():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix/Linux/MacOS
        os.system('clear')

class PregnancyTracker:
    def __init__(self, connection, current_user):
        self.connection = connection
        self.current_user = current_user

    def track_pregnancy(self):
        clear_screen()
        print("\n" + "="*50)
        print("** PREGNANCY TRACKER **")
        print("="*50)
        
        due_date = self.current_user['due_date']
        today = datetime.now().date()
        days_until_due = (due_date - today).days
        
        if days_until_due < 0:
            print("\nCongratulations! Your due date has passed.")
            print(f"Your baby is {abs(days_until_due)} days old now!")
            input("\nPress Enter to continue...")
            return
            
        days_pregnant = 280 - days_until_due
        weeks_pregnant = days_pregnant // 7
        remaining_days = days_pregnant % 7
        
        if weeks_pregnant < 13:
            trimester = "First Trimester"
        elif weeks_pregnant < 27:
            trimester = "Second Trimester"
        else:
            trimester = "Third Trimester"
        
        progress = min(100, int(days_pregnant / 280 * 100))
        
        print(f"\nYou are {weeks_pregnant} weeks and {remaining_days} days pregnant")
        print(f"Current trimester: {trimester}")
        print(f"Progress: {progress}% complete")
        print(f"Days until due date: {days_until_due}")
        
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("""
        SELECT week_number, topic FROM health_tips
        WHERE week_number > %s
        ORDER BY week_number
        LIMIT 3
        """, (weeks_pregnant,))
        
        milestones = cursor.fetchall()
        
        if milestones:
            print("\nUpcoming milestones:")
            for milestone in milestones:
                weeks_away = milestone['week_number'] - weeks_pregnant
                print(f"* Week {milestone['week_number']} ({weeks_away} weeks away): {milestone['topic']}")
        
        input("\nPress Enter to continue...")