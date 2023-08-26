# Define the UserInput class
class UserInput:

    # The __init__ method initializes the object
    def __init__(self):
        pass  # No initialization needed for this class

    # Method to capture user input from the command line
    def get_user_input(self):
        # Capture user input and remove any leading/trailing whitespace
        user_input = input("User: ").strip()
        # Check if the input is empty and recursively ask for input until valid
        if not user_input:
            print("Input cannot be empty. Please try again.")
            return self.get_user_input()
        return user_input
