# Hotel Management System (python)
CLI-based Hotel Management System using Python with room booking and file handling
# Design Choices

- Used JSON instead of database for simplicity and ease of implementation  
- Implemented modular design using classes  
- Focused on clarity and maintainability over complexity  

# How It Works

- Rooms are stored in a JSON file with availability status  
- Bookings are recorded with customer details and room allocation  
- On booking, room availability is updated  
- On checkout, room is marked available again

# Complexity

- Search Booking: O(n) (linear search)  
- Room Lookup: O(n)  
