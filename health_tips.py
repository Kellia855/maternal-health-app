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
        print("4. Trimester")
        
        choice = input("Select an option (1-4): ").strip()
        
        cursor = self.connection.cursor(dictionary=True)
        
        if choice == "1" and current_user:
            # Calculate current pregnancy week
            due_date = current_user['due_date']
            today = datetime.now().date()
            days_until_due = (due_date - today).days
            weeks_pregnant = max(1, int((280 - days_until_due) / 7))
            
            # Get current week tip and nearby weeks
            cursor.execute("""
            SELECT week_number, topic, tip FROM health_tips
            WHERE week_number <= %s
            ORDER BY week_number DESC
            LIMIT 3
            """, (weeks_pregnant,))
            
            tips = cursor.fetchall()
            
            print(f"\nYou are currently in week {weeks_pregnant} of your pregnancy")
            
            # If no tips found for current week, try to find closest week
            if not tips:
                cursor.execute("""
                SELECT week_number, topic, tip FROM health_tips
                ORDER BY ABS(week_number - %s)
                LIMIT 1
                """, (weeks_pregnant,))
                tips = cursor.fetchall()
            
        elif choice == "3":
            try:
                week = int(input("Enter pregnancy week (1-40): ").strip())
                if week < 1 or week > 40:
                    print("! Please enter a week between 1 and 40.")
                    input("\nPress Enter to continue...")
                    return
                
                # Get exact week and nearby weeks
                cursor.execute("""
                SELECT week_number, topic, tip FROM health_tips
                WHERE week_number = %s OR ABS(week_number - %s) <= 2
                ORDER BY week_number
                """, (week, week))
                
                tips = cursor.fetchall()
                
                # If no exact match, try to find closest week
                if not tips:
                    cursor.execute("""
                    SELECT week_number, topic, tip FROM health_tips
                    ORDER BY ABS(week_number - %s)
                    LIMIT 3
                    """, (week,))
                    tips = cursor.fetchall()
                    print(f"\nNo tip for exactly week {week}, showing closest available tips:")
                
            except ValueError:
                print("! Please enter a valid week number.")
                input("\nPress Enter to continue...")
                return
        
        elif choice == "4":
            print("\nSelect trimester:")
            print("1. First Trimester (Weeks 1-12)")
            print("2. Second Trimester (Weeks 13-27)")
            print("3. Third Trimester (Weeks 28-40)")
            
            trimester = input("Enter your choice (1-3): ").strip()
            
            if trimester == "1":
                cursor.execute("""
                SELECT week_number, topic, tip FROM health_tips
                WHERE week_number BETWEEN 1 AND 12
                ORDER BY week_number
                """)
            elif trimester == "2":
                cursor.execute("""
                SELECT week_number, topic, tip FROM health_tips
                WHERE week_number BETWEEN 13 AND 27
                ORDER BY week_number
                """)
            elif trimester == "3":
                cursor.execute("""
                SELECT week_number, topic, tip FROM health_tips
                WHERE week_number BETWEEN 28 AND 40
                ORDER BY week_number
                """)
            else:
                print("! Invalid selection.")
                input("\nPress Enter to continue...")
                return
                
            tips = cursor.fetchall()
        
        else:  # Option 2 or any other input: show all tips
            cursor.execute("""
            SELECT week_number, topic, tip FROM health_tips
            ORDER BY week_number
            """)
            
            tips = cursor.fetchall()
            
        if not tips:
            print("\nNo health tips available for the selected option.")
            input("\nPress Enter to continue...")
            return
        
        # Display the tips
        clear_screen()
        print("\n" + "="*50)
        print("** MATERNAL HEALTH TIPS **")
        print("="*50)
        
        for tip in tips:
            print("\n" + "-"*60)
            print(f"WEEK {tip['week_number']}: {tip['topic']}")
            print("-"*60)
            print(f"{tip['tip']}")
        
        # Offer to save tip to personal notes if viewing a specific week
        if choice == "3" and current_user and len(tips) == 1:
            print("\nWould you like to save this tip to your personal notes? (y/n)")
            save_choice = input().lower()
            if save_choice == 'y':
                try:
                    note_cursor = self.connection.cursor()
                    note_cursor.execute("""
                    INSERT INTO user_notes (user_id, note_content, created_date) 
                    VALUES (%s, %s, CURDATE())
                    """, (current_user['id'], f"Week {tips[0]['week_number']} Tip: {tips[0]['tip']}"))
                    self.connection.commit()
                    print("* Tip saved to your notes!")
                except Exception as e:
                    print("* Note: This feature requires the user_notes table to be added to your database.")
                    print(f"* Error: {e}")
        
        input("\nPress Enter to continue...")