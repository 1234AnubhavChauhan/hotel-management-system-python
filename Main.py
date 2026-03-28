import json
import os
from datetime import datetime

class Room:
    def __init__(self, room_number, room_type, price):
        self.room_number = room_number
        self.room_type = room_type
        self.price = price
        self.is_available = True

    def to_dict(self):
        return self.__dict__


class Booking:
    def __init__(self, name, room_number, days, check_in):
        self.name = name
        self.room_number = room_number
        self.days = days
        self.check_in = check_in
        self.check_out = self.calculate_checkout()

    def calculate_checkout(self):
        check_in_date = datetime.strptime(self.check_in, "%Y-%m-%d")
        return (check_in_date).strftime("%Y-%m-%d")

    def to_dict(self):
        return self.__dict__


class HotelManagement:
    def __init__(self):
        self.room_file = "rooms.json"
        self.booking_file = "bookings.json"
        self.rooms = self.load_data(self.room_file)
        self.bookings = self.load_data(self.booking_file)

        if not self.rooms:
            self.initialize_rooms()

    def load_data(self, filename):
        if os.path.exists(filename):
            with open(filename, "r") as f:
                return json.load(f)
        return []

    def save_data(self, filename, data):
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def initialize_rooms(self):
        print("Initializing rooms...")
        for i in range(1, 11):
            room_type = "Single" if i <= 5 else "Double"
            price = 1000 if room_type == "Single" else 2000
            room = Room(i, room_type, price)
            self.rooms.append(room.to_dict())
        self.save_data(self.room_file, self.rooms)

    def show_rooms(self):
        print("\n--- Room Status ---")
        for r in self.rooms:
            status = "Available" if r["is_available"] else "Booked"
            print(f"Room {r['room_number']} ({r['room_type']}) - ₹{r['price']} - {status}")
        print()

    def find_room(self, room_number):
        for r in self.rooms:
            if r["room_number"] == room_number:
                return r
        return None

    def book_room(self):
        name = input("Enter customer name: ")
        self.show_rooms()
        room_number = int(input("Enter room number: "))
        days = int(input("Enter number of days: "))
        check_in = input("Enter check-in date (YYYY-MM-DD): ")

        room = self.find_room(room_number)

        if room and room["is_available"]:
            booking = Booking(name, room_number, days, check_in)
            self.bookings.append(booking.to_dict())

            room["is_available"] = False

            self.save_data(self.booking_file, self.bookings)
            self.save_data(self.room_file, self.rooms)

            total = room["price"] * days
            print(f"✅ Booking successful! Total cost: ₹{total}\n")
        else:
            print("❌ Room not available!\n")

    def view_bookings(self):
        if not self.bookings:
            print("No bookings found.\n")
            return

        print("\n--- Bookings ---")
        for b in self.bookings:
            print(f"{b['name']} | Room {b['room_number']} | {b['days']} days | Check-in: {b['check_in']}")
        print()

    def search_booking(self):
        name = input("Enter name to search: ")
        found = False

        for b in self.bookings:
            if b["name"].lower() == name.lower():
                print(f"Found: Room {b['room_number']}, Days: {b['days']}")
                found = True

        if not found:
            print("❌ No booking found.\n")

    def checkout(self):
        name = input("Enter customer name for checkout: ")
        new_bookings = []
        found = False

        for b in self.bookings:
            if b["name"].lower() == name.lower():
                room = self.find_room(b["room_number"])
                if room:
                    room["is_available"] = True
                found = True
                print("✅ Checkout successful!\n")
            else:
                new_bookings.append(b)

        if not found:
            print("❌ Booking not found.\n")

        self.bookings = new_bookings
        self.save_data(self.booking_file, self.bookings)
        self.save_data(self.room_file, self.rooms)


def main():
    system = HotelManagement()

    while True:
        print("====== HOTEL MANAGEMENT SYSTEM ======")
        print("1. Show Rooms")
        print("2. Book Room")
        print("3. View Bookings")
        print("4. Search Booking")
        print("5. Checkout")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            system.show_rooms()
        elif choice == "2":
            system.book_room()
        elif choice == "3":
            system.view_bookings()
        elif choice == "4":
            system.search_booking()
        elif choice == "5":
            system.checkout()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice!\n")


if __name__ == "__main__":
    main()
