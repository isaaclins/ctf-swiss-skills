import os
import secrets

def calculate_hash(password: str) -> str:
    hash_digest = ['c'] * 32
    i = 0
    for c in password:
        hash_index = i * 13 % 32
        value = int(hash_digest[hash_index], 16)
        current_hash_value = hex(ord(c) ^ value)[-1]
        hash_digest[hash_index] = current_hash_value
        i += 1
    return ''.join(hash_digest)
        
USER_DATABASE = {
    # Admin password needs to be *really* strong
    # Jerry, stop whining and use a password manager or learn to type faster
    "admin": calculate_hash(secrets.token_hex(1028)),
}
          

def show_help():
    print("Available commands:")
    print("  help     - Show this help message")
    print("  login    - Login to the system")
    print("  register - Register a new user")
    print("  breach   - Display breach")
    print("  exit     - Exit the program")

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if username not in USER_DATABASE:
        print("Username not found.")
        return None
    if USER_DATABASE[username] == calculate_hash(password):
        print(f"Welcome back, {username}!")
        return username
    else:
        print("Incorrect password.")
        return None

def register():
    username = input("Choose a username: ")
    password = input("Choose a password: ")
    if username in USER_DATABASE:
        print("Username already exists. Please choose a different one.")
        return
    USER_DATABASE[username] = calculate_hash(password)
    print(f"User {username} registered successfully!")

def breach():
    print(
        'On the last security conference, we learned about "assume breach": Always assume that '
        'someone has already stolen your database. We are now going a step further: "ensure breach". '
        'We openly publish our database!'
        )
    print(USER_DATABASE)

def flag(username: str):
    if username == "admin":
        print(os.getenv("FLAG"))
    else:
        print("No flag for you!")

def main():
    current_user = None
    print("Welcome to ACME Inc!")
    print("Type 'help' for a list of commands.")
    while True:
        command = input("Enter a command: ").strip().lower()
        if command == "help":
            show_help()
        elif command == "login":
            current_user = login()
        elif command == "register":
            register()
        elif command == "breach":
            breach()
        elif command == "flag":
            flag(username=current_user)
        elif command == "exit":
            print("Exiting the program. Goodbye!")
            break
        elif command == "logout":
            if current_user is not None:
                print(f"User {current_user} logged out.")
                current_user = None
            else:
                print("No user is currently logged in.")
        else:
            print("Unknown command. Type 'help' for a list of commands.")

if __name__ == "__main__":
    main()