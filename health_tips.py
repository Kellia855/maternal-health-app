class HealthTips:
    def __init__(self, connection):
        self.connection = connection

    def view_tips(self, week_number=None):
        cursor = self.connection.cursor(dictionary=True)

        if week_number:
            cursor.execute("SELECT * FROM health_tips WHERE week_number = %s", (week_number,))
        else:
            cursor.execute("SELECT * FROM health_tips")

        tips = cursor.fetchall()
        for tip in tips:
            print(f"\nWeek {tip['week_number']}: {tip['topic']} - {tip['tip']}")


