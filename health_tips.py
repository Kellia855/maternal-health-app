import os
from datetime import datetime

def clear_screen():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix/Linux/MacOS
        os.system('clear')

class HealthTips:
    def __init__(self, connection):
        self.connection = connection

    def view_tips(self, current_user=None):
        clear_screen()
        print("\n" + "="*50)
        print("** MATERNAL HEALTH TIPS **")
        print("="*50)
        
        print("View tips by:")
        print("1. Current pregnancy stage")
        print("2. All pregnancy stages")
        print("3. Specific week")
        
        choice = input("Select an option (1-3): ").strip()
        
        cursor = self.connection.cursor(dictionary=True)
        
        if choice == "1" and current_user:
            due_date = current_user['due_date']
            today = datetime.now().date()
            days_until_due = (due_date - today).days
            weeks_pregnant = max(1, int((280 - days_until_due) / 7))
            
            cursor.execute("""
            SELECT week_number, topic, tip FROM health_tips
            WHERE week_number <= %s
            ORDER BY week_number DESC
            LIMIT 3
            """, (weeks_pregnant,))
            
            tips = cursor.fetchall()
            
            print(f"\nYou are currently in week {weeks_pregnant} of your pregnancy")
            
        elif choice == "3":
            try:
                week = int(input("Enter pregnancy week (1-40): ").strip())
                if week < 1 or week > 40:
                    print("! Please enter a week between 1 and 40.")
                    input("\nPress Enter to continue...")
                    return
                    
                cursor.execute("""
                SELECT week_number, topic, tip FROM health_tips
                WHERE week_number = %s OR ABS(week_number - %s) <= 2
                ORDER BY week_number
                """, (week, week))
                
                tips = cursor.fetchall()
                
            except ValueError:
                print("! Please enter a valid week number.")
                input("\nPress Enter to continue...")
                return
        else:
            cursor.execute("""
            SELECT week_number, topic, tip FROM health_tips
            ORDER BY week_number
            """)
            
            tips = cursor.fetchall()
            
        if not tips:
            print("\nNo health tips available for the selected option.")
            input("\nPress Enter to continue...")
            return
        
        clear_screen()
        print("\n" + "="*50)
        print("** MATERNAL HEALTH TIPS **")
        print("="*50)
            
        for tip in tips:
            print("\n" + "-"*60)
            print(f"WEEK {tip['week_number']}: {tip['topic']}")
            print("-"*60)
            print(f"{tip['tip']}")
        
        input("\nPress Enter to continue...")