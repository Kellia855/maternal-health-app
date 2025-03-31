class HospitalFinder:
    def __init__(self, connection):
        self.connection = connection

    def find_hospitals(self, district):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM hospitals WHERE district = %s", (district,))
        hospitals = cursor.fetchall()

        if not hospitals:
            print(f"\nNo hospitals found in {district}.")
        else:
            for hospital in hospitals:
                print(f"\n{hospital['name']} - {hospital['phone']} - {hospital['services']}")

