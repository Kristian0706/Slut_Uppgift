import csv
import os
import random
import string
import hashlib

#  FILE PATH 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOGIN_FILE = os.path.join(BASE_DIR, "login.csv")
PASSWORD_FILE = os.path.join(BASE_DIR, "hashedpasswd.csv")

#  HASH FUNCTION 
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def pause():
    input("\nPress Enter to continue...")

#  LOAD USERS 
def load_users():
    users = {}

    if os.path.exists(LOGIN_FILE):
        with open(LOGIN_FILE, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)

            for row in reader:
                if len(row) == 2:
                    users[row[0].strip()] = row[1].strip()

    return users


def save_all_users(users):
    with open(LOGIN_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["username", "password"])

        for user, pwd in users.items():
            writer.writerow([user, pwd])


def save_user(username, password):
    file_exists = os.path.exists(LOGIN_FILE)

    with open(LOGIN_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["username", "password"])

        writer.writerow([username.strip(), password.strip()])


#  REGISTER 
def register():
    username = input("Choose username: ").strip()
    password = input("Choose password: ").strip()

    users = load_users()

    if username in users:
        print("Username already exists!")
        pause()
        return

    hashed = hash_password(password)
    save_user(username, hashed)

    print("Account created!")
    pause()


#  LOGIN 
def login():
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    users = load_users()

    if username not in users:
        print("Wrong login")
        pause()
        return None

    saved_password = users[username]
    hashed = hash_password(password)

    if saved_password == hashed:
        print("Login successful!")
        pause()
        return username

    elif saved_password == password:
        users[username] = hashed
        save_all_users(users)

        print("Login successful! (Upgraded to SHA-256)")
        pause()
        return username

    else:
        print("Wrong login")
        pause()
        return None


#  PASSWORD MANAGER 
def add_password(username):
    site = input("Website: ").strip()
    login_user = input("Login username: ").strip()
    password = input("Password: ").strip()

    hashed = hash_password(password)

    file_exists = os.path.exists(PASSWORD_FILE)

    with open(PASSWORD_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["username", "site", "login", "password"])

        writer.writerow([username, site, login_user, hashed])

    print("Password saved!")
    pause()


def view_passwords(username):
    if not os.path.exists(PASSWORD_FILE):
        print("No passwords saved.")
        pause()
        return

    data = []

    with open(PASSWORD_FILE, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)

        for row in reader:
            if len(row) == 4 and row[0] == username:
                data.append(row)

    if not data:
        print("No passwords for this user.")
        pause()
        return

    data.sort(key=lambda x: x[1])

    print("\n--- Your passwords ---")

    for row in data:
        user, site, login_user, password = row
        print(f"{site} | {login_user} | {password}")

    pause()


def generate_password():
    length = 12
    chars = string.ascii_letters + string.digits + "@#$%"

    password = "".join(random.choice(chars) for _ in range(length))
    print("Generated password:", password)
    pause()


#  USER MENU 
def user_menu(username):
    while True:
        print(f"\n--- Welcome {username} ---")
        print("1. Save password")
        print("2. Show passwords")
        print("3. Generate password")
        print("4. Sign out")

        choice = input("Choice: ")

        if choice == "1":
            add_password(username)

        elif choice == "2":
            view_passwords(username)

        elif choice == "3":
            generate_password()

        elif choice == "4":
            break


#  MAIN 
def main():
    while True:
        print("\n--- LOGIN SYSTEM ---")
        print("1. Sign in")
        print("2. Create account")
        print("3. Exit")

        choice = input("Choice: ")

        if choice == "1":
            user = login()
            if user:
                user_menu(user)

        elif choice == "2":
            register()

        elif choice == "3":
            break


if __name__ == "__main__":
    main()