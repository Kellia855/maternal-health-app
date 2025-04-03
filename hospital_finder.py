import os

def clear_screen():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix/Linux/MacOS
        os.system('clear')

class HospitalFinder:
    def __init__(self, connection):
        self.connection = connection

    def find_hospitals(self):
        """Find hospitals by province"""
        clear_screen()
        print("\n" + "="*50)
        print("** NEARBY HOSPITALS **")
        print("="*50)
        
        # Get available provinces
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT DISTINCT province FROM hospitals ORDER BY province")
        provinces = cursor.fetchall()
        
        if not provinces:
            print("\nNo hospital data available in the system.")
            input("\nPress Enter to continue...")
            return
            
        print("\nAvailable provinces:")
        for i, p in enumerate(provinces, 1):
            print(f"{i}. {p['province']}")
            
        province = input("\nEnter your province: ").strip().capitalize()
        
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("""
        SELECT name, province, phone, services FROM hospitals 
        WHERE province = %s
        """, (province,))
        
        hospitals = cursor.fetchall()
        
        if not hospitals:
            print(f"\nNo hospitals found in {province} province.")
            input("\nPress Enter to continue...")
            return
        
        clear_screen()
        print("\n" + "="*50)
        print(f"** HOSPITALS IN {province.upper()} PROVINCE **")
        print("="*50)
            
        for i, hospital in enumerate(hospitals, 1):
            print("\n" + "-"*60)
            print(f"{i}. {hospital['name']}")
            print(f"   Phone: {hospital['phone']}")
            print(f"   Services: {hospital['services']}")
        
        input("\nPress Enter to continue...")