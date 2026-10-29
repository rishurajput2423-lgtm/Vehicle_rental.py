import os

# ==========================================
# CLASSES & LOGIC
# ==========================================
class Vehicle:
    """Class to store individual vehicle details."""
    def __init__(self, v_id, v_type, model, rate, availability="Available"):
        self.id = v_id
        self.type = v_type
        self.model = model
        self.rate = float(rate)
        self.availability = availability

    def __str__(self):
        # Format explicitly matches the Expected Output in Test Case 1
        return f"ID: {self.id} | {self.type} | {self.model} | Rs. {int(self.rate)}/day | {self.availability}"

class RentalSystem:
    """Class to manage inventory, renting logic, and file handling."""
    def __init__(self, filename="vehicles.txt"):
        self.filename = filename
        self.vehicles = []        # List to store Vehicle objects
        self.rental_details = {}  # Dictionary mapping Vehicle ID to rental details
        self.load_data()

    def load_data(self):
        """Loads vehicle data from vehicles.txt on startup."""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    if len(parts) == 5:
                        v_id, v_type, model, rate, availability = parts
                        self.vehicles.append(Vehicle(v_id, v_type, model, rate, availability))

    def save_data(self):
        """Saves vehicle data and status back to vehicles.txt."""
        with open(self.filename, "w") as file:
            for v in self.vehicles:
                file.write(f"{v.id},{v.type},{v.model},{v.rate},{v.availability}\n")

    def generate_id(self):
        """Auto-generates IDs starting from V1."""
        if not self.vehicles:
            return "V1"
        last_id = self.vehicles[-1].id
        num = int(last_id[1:]) + 1
        return f"V{num}"

    def add_vehicle(self, v_type, model, rate):
        new_id = self.generate_id()
        new_vehicle = Vehicle(new_id, v_type, model, rate)
        self.vehicles.append(new_vehicle)
        self.save_data()
        print(f"Vehicle added. {new_vehicle}")

    def rent_vehicle(self, v_id, customer, days):
        if days < 1:
            print("Days must be 1 or more.")
            return

        # Find vehicle
        vehicle = next((v for v in self.vehicles if v.id == v_id), None)
        
        if not vehicle:
            print(f"Vehicle {v_id} does not exist.")
            return

        # Check availability
        if vehicle.availability != "Available":
            print(f"Vehicle {v_id} is not available.")
            return

        # Bill calculation with 10% discount for >= 7 days
        bill = vehicle.rate * days
        discount_msg = ""
        if days >= 7:
            bill -= (bill * 0.10)
            discount_msg = " 10% discount applied."
        
        # Update states
        vehicle.availability = "Rented"
        self.rental_details[v_id] = {"customer": customer, "days": days, "bill": bill}
        self.save_data()

        print(f"{v_id} rented to {customer} for {days} days.{discount_msg} Bill: Rs. {int(bill)}")

    def return_vehicle(self, v_id):
        vehicle = next((v for v in self.vehicles if v.id == v_id), None)
        
        if not vehicle:
            print(f"Vehicle {v_id} does not exist.")
            return
        
        if vehicle.availability == "Available":
            print(f"Vehicle {v_id} is already available.")
            return

        vehicle.availability = "Available"
        if v_id in self.rental_details:
            del self.rental_details[v_id]
        self.save_data()
        
        print(f"{v_id} returned. Status: Available")

    def view_available(self):
        available_vehicles = [v for v in self.vehicles if v.availability == "Available"]
        if not available_vehicles:
            print("No vehicles available.")
        else:
            for v in available_vehicles:
                print(v)

# ==========================================
# MAIN CONSOLE MENU
# ==========================================
def main():
    system = RentalSystem()
    
    while True:
        print("\n=== Vehicle Rental Management ===")
        print("1. Add Vehicle")
        print("2. Rent Vehicle")
        print("3. Return Vehicle")
        print("4. View Available Vehicles")
        print("5. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            v_type = input("Type (e.g., Car, Bike): ")
            model = input("Model: ")
            try:
                rate = float(input("Rate per day (Rs.): "))
                system.add_vehicle(v_type, model, rate)
            except ValueError:
                print("Invalid rate. Please enter a number.")
                
        elif choice == '2':
            v_id = input("Vehicle ID (e.g., V1): ")
            customer = input("Customer Name: ")
            try:
                days = int(input("Days: "))
                system.rent_vehicle(v_id, customer, days)
            except ValueError:
                print("Invalid days. Please enter a whole number.")
                
        elif choice == '3':
            v_id = input("Vehicle ID to return: ")
            system.return_vehicle(v_id)
            
        elif choice == '4':
            system.view_available()
            
        elif choice == '5':
            print("Exiting...")
            break
            
        else:
            print("Invalid choice! Please select 1-5.")

if __name__ == "__main__":
    main()