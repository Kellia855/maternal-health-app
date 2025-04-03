import os

def clear_screen():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix/Linux/MacOS
        os.system('clear')

class Menu:
    def __init__(self, app):
        self.app = app

    def main_menu(self):
        """
        Display the main menu options
        
        Returns:
            str: The user's choice
        """
        clear_screen()
        print("\n" + "*"*60)
        print("*" + " "*20 + "MATERNAL HEALTH SYSTEM" + " "*19 + "*")
        print("*" + " "*58 + "*")
        print("*  Supporting mothers through their pregnancy journey  *")
        print("*"*60)
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        
        return input("\nPlease select an option: ").strip()
    
    def user_menu(self, user_name):
        """
        Display the user menu options
        
        Args:
            user_name: The name of the current user
            
        Returns:
            str: The user's choice
        """
        clear_screen()
        print("\n" + "*"*60)
        print("*" + " "*20 + "MATERNAL HEALTH SYSTEM" + " "*19 + "*")
        print("*" + " "*58 + "*")
        print(f"*  Welcome, {user_name}" + " "*(47-len(user_name)) + "*")
        print("*"*60)
        
        print("\n1. Pregnancy Tracker")
        print("2. Add Reminder")
        print("3. View My Reminders")
        print("4. Health Tips")
        print("5. Find Nearby Hospitals")
        print("6. Update My Profile")
        print("7. Logout")
        
        return input("\nPlease select an option: ").strip()