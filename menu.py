class Menu:
    def __init__(self, app):
        self.app = app

    def main_menu(self):
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Select an option: ").strip()
        return choice

