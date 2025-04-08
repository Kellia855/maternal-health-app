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
        
        try:
            # Ensure the correct database is selected
            cursor = self.connection.cursor()
            cursor.execute("USE maternal_health_management_system")
            
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
            
            # Prompt for province selection
            while True:
                try:
                    province_choice = input("\nEnter the number of your province: ").strip()
                    province_index = int(province_choice) - 1
                    
                    if 0 <= province_index < len(provinces):
                        selected_province = provinces[province_index]['province']
                        break
                    else:
                        print("\n! Invalid province number. Please try again.")
                except ValueError:
                    print("\n! Please enter a valid number.")
            
            # Find hospitals in the selected province
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
            SELECT name, province, phone, services FROM hospitals 
            WHERE province = %s
            """, (selected_province,))
            
            hospitals = cursor.fetchall()
            
            if not hospitals:
                print(f"\nNo hospitals found in {selected_province} province.")
                input("\nPress Enter to continue...")
                return
            
            clear_screen()
            print("\n" + "="*50)
            print(f"** HOSPITALS IN {selected_province.upper()} PROVINCE **")
            print("="*50)
                
            for i, hospital in enumerate(hospitals, 1):
                print("\n" + "-"*60)
                print(f"{i}. {hospital['name']}")
                print(f"   Province: {hospital['province']}")
                print(f"   Phone: {hospital['phone']}")
                print(f"   Services: {hospital['services']}")
            
            input("\nPress Enter to continue...")
        
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            input("\nPress Enter to continue...")