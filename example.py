#!/usr/bin/env python3
"""Example demonstrating common LLM coding errors that MCP Pyrefly catches."""

# Example 1: Type error
def process_user_id(user_id: str) -> dict:
    """Process a user ID and return user data."""
    return {"id": user_id, "name": f"User {user_id}"}

# LLM often makes this mistake - passing wrong type
# result = process_user_id(12345)  # ERROR: Expected str, got int

# Example 2: Naming inconsistency
def get_user_data(user_id: str) -> dict:
    """Get user data from database."""
    # Imagine this is a database call
    return {"id": user_id, "name": "John Doe"}

# Later in the code, LLM uses different naming convention
# This is a common LLM error - inconsistent naming
# user_info = getUserData("123")  # Should be get_user_data

# Example 3: Another common pattern - mixing naming styles
class UserManager:
    def fetch_user(self, id: str) -> dict:
        return get_user_data(id)
    
    # LLM might later add this method with inconsistent naming
    # def fetchUserById(self, id: str) -> dict:  # Should be fetch_user_by_id
    #     return self.fetch_user(id)

# Example 4: Parameter order confusion
def create_user(name: str, email: str, age: int) -> dict:
    return {"name": name, "email": email, "age": age}

# LLM might mix up parameter order
# new_user = create_user("john@example.com", "John Doe", 25)  # Wrong order!

# Example 5: Return type mismatch
def calculate_total(items: list[float]) -> int:
    # Bug: Returning float but declared return type is int
    return sum(items) * 1.1  # This will be a float!

if __name__ == "__main__":
    # Correct usage examples
    user = process_user_id("123")
    print(f"User: {user}")
    
    data = get_user_data("456")
    print(f"Data: {data}")
    
    manager = UserManager()
    fetched = manager.fetch_user("789")
    print(f"Fetched: {fetched}")
    
    # This would be caught by Pyrefly
    # total = calculate_total([10.0, 20.0, 30.0])  # Return type error