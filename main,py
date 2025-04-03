from database import connect_db
from auth import Auth
from menu import Menu

class MaternalHealthApp:
    def __init__(self):
        self.connection = connect_db()
        self.current_user = None
        self.auth = Auth(self.connection)
        self.menu = Menu(self)

    def main(self):
        while True:
            choice = self.menu.main_menu()

            if choice == "1":
                self.auth.register_user()
            elif choice == "2":
                self.current_user = self.auth.login()
            elif choice == "3":
                break

if __name__ == "__main__":
    app = MaternalHealthApp()
    app.main()


