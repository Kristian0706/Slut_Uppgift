import csv
import os
import random
import string
import hashlib
import customtkinter as ctk
from tkinter import messagebox

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

    file_exists = os.path.exists(PASSWORD_FILE)

    with open(PASSWORD_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["username", "site", "login", "password"])

        writer.writerow([username, site, login_user, password])

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

    data.sort(key=lambda row: row[1])

    print("\nSecurity warning!")
    print("Make sure nobody is looking at your screen before viewing your passwords.")
    confirm = input("Do you want to continue? (y/n): ").lower()

    if confirm != "y":
        print("Password display cancelled.")
        pause()
        return

    print("\n--- Your passwords ---")

    for row in data:
        user, site, login_user, password = row
        print(f"{site} | {login_user} | {password}")

    pause()


def delete_password(username):
    if not os.path.exists(PASSWORD_FILE):
        print("No passwords to delete.")
        pause()
        return

    data = []

    with open(PASSWORD_FILE, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader, None)

        for row in reader:
            if len(row) == 4:
                data.append(row)

    user_data = [row for row in data if row[0] == username]

    if not user_data:
        print("No passwords found.")
        pause()
        return

    print("\n--- Select password to delete ---")

    for i, row in enumerate(user_data):
        _, site, login_user, _ = row
        print(f"{i + 1}. {site} | {login_user}")

    try:
        choice = int(input("Select number: ")) - 1
        to_delete = user_data[choice]
    except:
        print("Invalid choice.")
        pause()
        return

    data.remove(to_delete)

    with open(PASSWORD_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)

    print("Password deleted!")
    pause()


def generate_password(username):
    length = 12
    chars = string.ascii_letters + string.digits + "@#$%"

    password = "".join(random.choice(chars) for _ in range(length))
    print("Generated password:", password)

    save = input("Do you want to save this password? (y/n): ").lower()

    if save == "y":
        site = input("Website: ").strip()
        login_user = input("Login username: ").strip()

        file_exists = os.path.exists(PASSWORD_FILE)

        with open(PASSWORD_FILE, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(["username", "site", "login", "password"])

            writer.writerow([username, site, login_user, password])

        print("Password saved!")

    pause()


#  USER MENU 
def user_menu(username):
    while True:
        print(f"\n--- Welcome {username} ---")
        print("1. Save password")
        print("2. Show passwords")
        print("3. Generate password")
        print("4. Delete password")
        print("5. Sign out")

        choice = input("Choice: ")

        if choice == "1":
            add_password(username)

        elif choice == "2":
            view_passwords(username)

        elif choice == "3":
            generate_password(username)

        elif choice == "4":
            delete_password(username)

        elif choice == "5":
            break


# GUI
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class PasswordManagerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Password Manager")
        self.geometry("1150x720")
        self.minsize(950, 620)

        self.current_user = None
        self.selected_password = None
        self.visible_passwords = set()

        self.bg = "#070A13"
        self.card = "#101827"
        self.card2 = "#151F33"
        self.accent = "#7C3AED"
        self.accent2 = "#06B6D4"
        self.green = "#22C55E"
        self.red = "#EF4444"
        self.text = "#F8FAFC"
        self.muted = "#94A3B8"

        self.configure(fg_color=self.bg)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.container = ctk.CTkFrame(self, fg_color=self.bg)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.show_login_screen()

    def clear_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_screen()

        frame = ctk.CTkFrame(self.container, fg_color=self.bg)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        left = ctk.CTkFrame(frame, fg_color=self.bg, corner_radius=0)
        left.grid(row=0, column=0, sticky="nsew", padx=(45, 20), pady=35)

        ctk.CTkLabel(left, text="PASSWD", font=("Segoe UI", 42, "bold"), text_color=self.text).pack(anchor="w", pady=(55, 0))
        ctk.CTkLabel(left, text="MANAGER", font=("Segoe UI", 42, "bold"), text_color=self.accent2).pack(anchor="w", pady=(0, 20))

        ctk.CTkLabel(
            left,
            text="Secure, clean and simple password storage for your accounts.",
            font=("Segoe UI", 18),
            text_color=self.muted,
            wraplength=420,
            justify="left"
        ).pack(anchor="w")

        badge = ctk.CTkFrame(left, fg_color="#111C2E", corner_radius=20)
        badge.pack(anchor="w", pady=30)

        ctk.CTkLabel(
            badge,
            text="SHA-256 login protection",
            font=("Segoe UI", 15, "bold"),
            text_color=self.green,
            padx=22,
            pady=12
        ).pack()

        right = ctk.CTkFrame(frame, fg_color=self.card, corner_radius=28)
        right.grid(row=0, column=1, sticky="nsew", padx=(20, 45), pady=45)
        right.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(right, text="Welcome back", font=("Segoe UI", 32, "bold"), text_color=self.text).pack(pady=(40, 5))
        ctk.CTkLabel(right, text="Sign in to continue", font=("Segoe UI", 15), text_color=self.muted).pack(pady=(0, 28))

        self.login_username = ctk.CTkEntry(
            right,
            placeholder_text="Username",
            height=48,
            corner_radius=14,
            fg_color=self.card2,
            border_color="#243044",
            text_color=self.text,
            font=("Segoe UI", 15)
        )
        self.login_username.pack(fill="x", padx=55, pady=8)

        self.login_password = ctk.CTkEntry(
            right,
            placeholder_text="Password",
            show="*",
            height=48,
            corner_radius=14,
            fg_color=self.card2,
            border_color="#243044",
            text_color=self.text,
            font=("Segoe UI", 15)
        )
        self.login_password.pack(fill="x", padx=55, pady=8)

        ctk.CTkButton(
            right,
            text="Sign in",
            height=48,
            corner_radius=14,
            fg_color=self.accent,
            hover_color="#6D28D9",
            font=("Segoe UI", 16, "bold"),
            command=self.gui_login
        ).pack(fill="x", padx=55, pady=(22, 10))

        ctk.CTkButton(
            right,
            text="Create account",
            height=48,
            corner_radius=14,
            fg_color="#0F766E",
            hover_color="#115E59",
            font=("Segoe UI", 16, "bold"),
            command=self.show_register_screen
        ).pack(fill="x", padx=55, pady=10)

        ctk.CTkButton(
            right,
            text="Exit",
            height=48,
            corner_radius=14,
            fg_color="#1E293B",
            hover_color="#334155",
            font=("Segoe UI", 16, "bold"),
            command=self.destroy
        ).pack(fill="x", padx=55, pady=(10, 25))

    def show_register_screen(self):
        self.clear_screen()

        frame = ctk.CTkFrame(self.container, fg_color=self.bg)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        card = ctk.CTkFrame(frame, fg_color=self.card, corner_radius=28)
        card.grid(row=0, column=0, padx=120, pady=55, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(card, text="Create account", font=("Segoe UI", 34, "bold"), text_color=self.text).pack(pady=(55, 8))
        ctk.CTkLabel(card, text="Start protecting your saved passwords", font=("Segoe UI", 15), text_color=self.muted).pack(pady=(0, 30))

        self.register_username = ctk.CTkEntry(
            card,
            placeholder_text="Choose username",
            height=50,
            corner_radius=14,
            fg_color=self.card2,
            border_color="#243044",
            text_color=self.text,
            font=("Segoe UI", 15)
        )
        self.register_username.pack(fill="x", padx=180, pady=8)

        self.register_password = ctk.CTkEntry(
            card,
            placeholder_text="Choose password",
            show="*",
            height=50,
            corner_radius=14,
            fg_color=self.card2,
            border_color="#243044",
            text_color=self.text,
            font=("Segoe UI", 15)
        )
        self.register_password.pack(fill="x", padx=180, pady=8)

        ctk.CTkButton(
            card,
            text="Create account",
            height=50,
            corner_radius=14,
            fg_color=self.accent,
            hover_color="#6D28D9",
            font=("Segoe UI", 16, "bold"),
            command=self.gui_register
        ).pack(fill="x", padx=180, pady=(22, 10))

        ctk.CTkButton(
            card,
            text="Back to login",
            height=50,
            corner_radius=14,
            fg_color="#1E293B",
            hover_color="#334155",
            font=("Segoe UI", 16, "bold"),
            command=self.show_login_screen
        ).pack(fill="x", padx=180, pady=10)

    def show_dashboard(self):
        self.clear_screen()
        self.selected_password = None

        frame = ctk.CTkFrame(self.container, fg_color=self.bg)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        sidebar = ctk.CTkFrame(frame, fg_color="#0B1220", corner_radius=0, width=250)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        ctk.CTkLabel(sidebar, text="PASSWD", font=("Segoe UI", 28, "bold"), text_color=self.text).pack(anchor="w", padx=25, pady=(35, 0))
        ctk.CTkLabel(sidebar, text="MANAGER", font=("Segoe UI", 28, "bold"), text_color=self.accent2).pack(anchor="w", padx=25, pady=(0, 30))

        ctk.CTkLabel(
            sidebar,
            text=f"Signed in as\n{self.current_user}",
            font=("Segoe UI", 15, "bold"),
            text_color=self.muted,
            justify="left"
        ).pack(anchor="w", padx=25, pady=(0, 30))

        ctk.CTkButton(sidebar, text="Save password", height=44, corner_radius=12, fg_color=self.accent, hover_color="#6D28D9", font=("Segoe UI", 14, "bold"), command=self.focus_save_form).pack(fill="x", padx=20, pady=8)
        ctk.CTkButton(sidebar, text="Generate password", height=44, corner_radius=12, fg_color="#0369A1", hover_color="#075985", font=("Segoe UI", 14, "bold"), command=self.gui_generate_password).pack(fill="x", padx=20, pady=8)
        ctk.CTkButton(sidebar, text="Delete selected", height=44, corner_radius=12, fg_color="#991B1B", hover_color="#7F1D1D", font=("Segoe UI", 14, "bold"), command=self.gui_delete_password).pack(fill="x", padx=20, pady=8)
        ctk.CTkButton(sidebar, text="Sign out", height=44, corner_radius=12, fg_color="#1E293B", hover_color="#334155", font=("Segoe UI", 14, "bold"), command=self.sign_out).pack(side="bottom", fill="x", padx=20, pady=25)

        content = ctk.CTkFrame(frame, fg_color=self.bg, corner_radius=0)
        content.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(1, weight=1)

        top = ctk.CTkFrame(content, fg_color=self.card, corner_radius=24)
        top.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 25))
        top.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(top, text="Dashboard", font=("Segoe UI", 32, "bold"), text_color=self.text).grid(row=0, column=0, sticky="w", padx=25, pady=(22, 0))
        ctk.CTkLabel(top, text="Manage your saved logins in one clean place.", font=("Segoe UI", 15), text_color=self.muted).grid(row=1, column=0, sticky="w", padx=25, pady=(0, 22))

        left = ctk.CTkFrame(content, fg_color=self.card, corner_radius=24)
        left.grid(row=1, column=0, sticky="nsew", padx=(0, 12))
        left.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(left, text="Save new password", font=("Segoe UI", 22, "bold"), text_color=self.text).pack(anchor="w", padx=25, pady=(25, 15))

        self.site_entry = ctk.CTkEntry(left, placeholder_text="Website", height=46, corner_radius=13, fg_color=self.card2, border_color="#243044", font=("Segoe UI", 14), text_color=self.text)
        self.site_entry.pack(fill="x", padx=25, pady=8)

        self.login_entry = ctk.CTkEntry(left, placeholder_text="Login username", height=46, corner_radius=13, fg_color=self.card2, border_color="#243044", font=("Segoe UI", 14), text_color=self.text)
        self.login_entry.pack(fill="x", padx=25, pady=8)

        self.password_entry = ctk.CTkEntry(left, placeholder_text="Password", height=46, corner_radius=13, fg_color=self.card2, border_color="#243044", font=("Segoe UI", 14), text_color=self.text)
        self.password_entry.pack(fill="x", padx=25, pady=8)

        ctk.CTkButton(left, text="Save password", height=46, corner_radius=13, fg_color=self.green, hover_color="#16A34A", font=("Segoe UI", 15, "bold"), command=self.gui_add_password).pack(fill="x", padx=25, pady=(22, 8))
        ctk.CTkButton(left, text="Generate into password field", height=46, corner_radius=13, fg_color=self.accent, hover_color="#6D28D9", font=("Segoe UI", 15, "bold"), command=self.generate_to_field).pack(fill="x", padx=25, pady=8)

        self.generated_label = ctk.CTkLabel(left, text="", font=("Segoe UI", 14, "bold"), text_color=self.accent2)
        self.generated_label.pack(anchor="w", padx=25, pady=(10, 0))

        right = ctk.CTkFrame(content, fg_color=self.card, corner_radius=24)
        right.grid(row=1, column=1, sticky="nsew", padx=(12, 0))
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(right, text="Saved passwords", font=("Segoe UI", 22, "bold"), text_color=self.text).grid(row=0, column=0, sticky="w", padx=25, pady=(25, 10))

        self.warning_label = ctk.CTkLabel(right, text="Click a blurred password to reveal it.", font=("Segoe UI", 13), text_color=self.muted)
        self.warning_label.grid(row=1, column=0, sticky="w", padx=25, pady=(0, 10))

        self.password_list = ctk.CTkScrollableFrame(right, fg_color="#0B1220", corner_radius=18)
        self.password_list.grid(row=2, column=0, sticky="nsew", padx=25, pady=(5, 25))
        self.password_list.grid_columnconfigure(0, weight=1)

        self.load_password_cards()

    def gui_register(self):
        username = self.register_username.get().strip()
        password = self.register_password.get().strip()

        if username == "" or password == "":
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return

        users = load_users()

        if username in users:
            messagebox.showerror("Error", "Username already exists!")
            return

        hashed = hash_password(password)
        save_user(username, hashed)

        messagebox.showinfo("Success", "Account created!")
        self.show_login_screen()

    def gui_login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()

        users = load_users()

        if username not in users:
            messagebox.showerror("Error", "Wrong login")
            return

        saved_password = users[username]
        hashed = hash_password(password)

        if saved_password == hashed:
            self.current_user = username
            self.visible_passwords = set()
            self.show_dashboard()

        elif saved_password == password:
            users[username] = hashed
            save_all_users(users)
            self.current_user = username
            self.visible_passwords = set()
            self.show_dashboard()

        else:
            messagebox.showerror("Error", "Wrong login")

    def gui_add_password(self):
        site = self.site_entry.get().strip()
        login_user = self.login_entry.get().strip()
        password = self.password_entry.get().strip()

        if site == "" or login_user == "" or password == "":
            messagebox.showerror("Error", "Fill in all fields.")
            return

        file_exists = os.path.exists(PASSWORD_FILE)

        with open(PASSWORD_FILE, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(["username", "site", "login", "password"])

            writer.writerow([self.current_user, site, login_user, password])

        self.site_entry.delete(0, "end")
        self.login_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.generated_label.configure(text="")

        messagebox.showinfo("Success", "Password saved!")
        self.load_password_cards()

    def get_user_passwords(self):
        data = []

        if not os.path.exists(PASSWORD_FILE):
            return data

        with open(PASSWORD_FILE, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)

            for row in reader:
                if len(row) == 4 and row[0] == self.current_user:
                    data.append(row)

        data.sort(key=lambda row: row[1])
        return data

    def load_password_cards(self):
        for widget in self.password_list.winfo_children():
            widget.destroy()

        data = self.get_user_passwords()

        if not data:
            empty = ctk.CTkLabel(self.password_list, text="No passwords saved yet.", font=("Segoe UI", 15), text_color=self.muted)
            empty.grid(row=0, column=0, padx=20, pady=25)
            return

        for i, row in enumerate(data):
            user, site, login_user, password = row
            key = f"{site}|{login_user}|{password}"
            is_visible = key in self.visible_passwords

            card = ctk.CTkFrame(self.password_list, fg_color=self.card2, corner_radius=16)
            card.grid(row=i, column=0, sticky="ew", padx=12, pady=8)
            card.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(card, text=site, font=("Segoe UI", 17, "bold"), text_color=self.text).grid(row=0, column=0, sticky="w", padx=18, pady=(14, 0))
            ctk.CTkLabel(card, text=f"Login: {login_user}", font=("Segoe UI", 13), text_color=self.muted).grid(row=1, column=0, sticky="w", padx=18, pady=(2, 0))

            shown_password = password if is_visible else "••••••••••••"
            password_label = ctk.CTkLabel(card, text=f"Password: {shown_password}", font=("Segoe UI", 13, "bold"), text_color=self.accent2, cursor="hand2")
            password_label.grid(row=2, column=0, sticky="w", padx=18, pady=(2, 14))
            password_label.bind("<Button-1>", lambda event, r=row: self.toggle_password_visibility(r))

            ctk.CTkButton(card, text="Select", width=90, height=34, corner_radius=10, fg_color=self.accent, hover_color="#6D28D9", command=lambda r=row: self.select_password(r)).grid(row=0, column=1, rowspan=3, padx=15, pady=15)

    def toggle_password_visibility(self, row):
        user, site, login_user, password = row
        key = f"{site}|{login_user}|{password}"

        if key in self.visible_passwords:
            self.visible_passwords.remove(key)
            self.warning_label.configure(text="Password hidden again.")
            self.load_password_cards()
            return

        confirm = messagebox.askyesno("Security warning", "Make sure nobody is looking at your screen before viewing your password.\n\nDo you want to continue?")

        if confirm:
            self.visible_passwords.add(key)
            self.warning_label.configure(text="Password is visible. Click it again to hide it.")
            self.load_password_cards()

    def select_password(self, row):
        self.selected_password = row
        messagebox.showinfo("Selected", f"Selected password:\n{row[1]} | {row[2]}")

    def gui_delete_password(self):
        if self.selected_password is None:
            messagebox.showerror("Error", "Select a password first.")
            return

        confirm = messagebox.askyesno("Delete password", f"Do you want to delete:\n{self.selected_password[1]} | {self.selected_password[2]}?")
        if not confirm:
            return

        if not os.path.exists(PASSWORD_FILE):
            messagebox.showerror("Error", "No passwords to delete.")
            return

        data = []

        with open(PASSWORD_FILE, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader, None)

            for row in reader:
                if len(row) == 4:
                    data.append(row)

        if self.selected_password in data:
            data.remove(self.selected_password)

        selected_key = f"{self.selected_password[1]}|{self.selected_password[2]}|{self.selected_password[3]}"

        if selected_key in self.visible_passwords:
            self.visible_passwords.remove(selected_key)

        with open(PASSWORD_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(header if header else ["username", "site", "login", "password"])
            writer.writerows(data)

        self.selected_password = None
        messagebox.showinfo("Success", "Password deleted!")
        self.load_password_cards()

    def gui_generate_password(self):
        length = 12
        chars = string.ascii_letters + string.digits + "@#$%"
        password = "".join(random.choice(chars) for _ in range(length))

        self.generated_label.configure(text=f"Generated: {password}")
        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, password)

        save = messagebox.askyesno("Generated password", f"Generated password:\n{password}\n\nDo you want to save this password now?")

        if save:
            self.focus_save_form()

    def generate_to_field(self):
        length = 12
        chars = string.ascii_letters + string.digits + "@#$%"
        password = "".join(random.choice(chars) for _ in range(length))

        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, password)
        self.generated_label.configure(text=f"Generated: {password}")

    def focus_save_form(self):
        self.site_entry.focus()

    def sign_out(self):
        self.current_user = None
        self.selected_password = None
        self.visible_passwords = set()
        self.show_login_screen()


#  MAIN 
def main():
    app = PasswordManagerGUI()
    app.mainloop()


if __name__ == "__main__":
    main()