import csv 
import os
import random
import string

LOGIN_FILE = "login.csv"
PASSWORD_FILE = "hashedpasswd.csv"

#LOAD USERS

def load_users():  
    users = {}
    
    if os.path.exists(LOGIN_FILE):
        with open(LOGIN_FILE "r") as file:
            reader = csv.reader(file)
            next(reader, None) 
            
            for row in reader: 
                if len(row) == 2:
                    users[row[0]] = row[1]
    return users


def save_user(username, password): 
    file_exists = os.path.exists(LOGIN_FILE)
    
    with open(LOGIN_FILE, "a", newline="") as file: 
        writer = csv.writer(file)
        
        if not file_exists:
            writer.weiterow(["username", "password"])
        
        writer.writerow([username, password]) 

def get_user_file(username):
    return f"{username}_passwords.csv"


# LOGIN / REGISTER 

def register(): 
    username = input("Choose username: ")
    password = input("Choose password: ")
    
    users = load_users()
    
    if username in users:
        print("Username already exists!")
        return
    
    save_user(username, password)
    print("account created!")

def login():
    username = input("Username: ")
    password = input("Password: ")
    
    users = load_users()
    
    if username in users and users[username] == password:
        print("Login successful!")
        return username 
    else:
        print("wrong login")
        return None 
    
# PASSWORD MANAGER

def add_password(username):
    site = input("website:")    
    login_user = input("Username:")
    password = input("Password")
    
    file_exists = os.path.exists(PASS_FILE)
    
    with open(PASS_FILE. "a", newline="") as file:
        writer = csv.writer(file)
        
        if not file_exists:
            writer.writerow(["username", "site", "login", "password"])
            
        print("Password saved!")
    
    
    def view_passwords(username):
        if not os.path.exists(PASS_FILE):
            print("No passwords saved.")
            return
        
        data = []
        
        with open(PASS_FILE, "r") as file:
            reader = csv.reader(file)
            next(reader, None)
            
            for row in reader:
                if row[0] == username
                data.append(row)
        if not data:
            print("No passwords for this user.")
            return
        
#SORTERA EFTER SITE

data.sort(key=lambda x: x[1])

print("\n--- Your passwords ---")

for row in data: 
    user, site, login_user, password = row 
    print(" | ".join([site, login_user, password]))
    
    
def generate_password():
    length = 12
    char = string.ascii_letters + string.digits + "@#$%"
    
    password = "".join(random.choice(chars)for _ in range(length))
    print("Generated password:", password)
    
    
#menu
        