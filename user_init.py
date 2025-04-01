import json
import re
from typing import cast


class User:
    def __init__(self, username, phone_number):
        """
        Initialize the User object with username and phone number.
        """
        if not self.validate_phone_number(phone_number):
            raise ValueError("Invalid phone number format. Expected format: +493041736523")

        self.username = username
        self.phone_number = phone_number
        self.receipt_ids = []  # List to store recipe IDs

    @staticmethod
    def validate_phone_number(phone_number):
        """
        Validates the phone number format: starts with '+' followed by digits, no spaces.
        """
        return bool(re.fullmatch(r'\+\d+', phone_number))

    def add_recipe_id(self, recipe_id):
        """
        Adds a new recipe ID to the list.
        """
        self.receipt_ids.append(recipe_id)

    def to_dict(self):
        """
        Converts the User object to a dictionary.
        """
        return {
            "username": self.username,
            "phone_number": self.phone_number,
            "receipt_ids": self.receipt_ids
        }

    def to_json(self, filename: str):
        """
        Saves the User data to a JSON file.
        """
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(self.to_dict(), cast('SupportsWrite[str]', file), indent=4)


# --- Testing the functionality ---
if __name__ == "__main__":
    # User input
    input_username = input("Enter username: ")

    while True:
        input_phone_number = input("Enter phone number (+493041736523 format): ")
        if User.validate_phone_number(input_phone_number):
            break
        print("Invalid phone number format. Please try again.")

    user = User(input_username, input_phone_number)

    # Print username and phone number
    print("Username:", user.username)
    print("Phone number:", user.phone_number)

    # Adding recipe IDs
    while True:
        add_id = input("Add recipe ID (or press Enter to finish): ")
        if not add_id:
            break
        user.add_recipe_id(add_id)

    # Save to JSON
    user.to_json("user_data.json")
    print("User data saved to user_data.json")

    # Displaying the user data
    print(json.dumps(user.to_dict(), indent=4))
