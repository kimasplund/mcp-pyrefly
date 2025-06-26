def get_user_data(user_id: str) -> dict:
    return {"id": user_id, "name": "Test User"}

# FIXED: Converting int to str
result = get_user_data("123")  # Now passing string instead of int

# FIXED: Using consistent naming
data = get_user_data("456")  # Using snake_case consistently

print(f"Result: {result}")
print(f"Data: {data}")