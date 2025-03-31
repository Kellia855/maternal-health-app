import database

class Auth:
    def __init__(self, connection):
        self.connection = connection

    def register_user(self):
        name = input("Enter your name: ").strip()
        password = input("Enter your password: ").strip()

        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO users (name, password) VALUES (%s, %s)", (name, password))
        self.connection.commit()
        print("\n* Registration successful! You can now log in.")

    def login(self):
        name = input("Enter your name: ").strip()
        password = input("Enter your password: ").strip()

        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE name = %s AND password = %s", (name, password))
        user = cursor.fetchone()

        if user:
            print(f"\n* Welcome, {user['name']}!")
            return user
        else:
            print("\n! Invalid credentials. Try again.")
            return None

    def logout(self, user):
        if user:
            print(f"\n* Goodbye, {user['name']}! Have a wonderful day!")

