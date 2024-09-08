import tkinter as tk
import tkinter.font as tkFont
import json
import random
import ttkthemes as th # type: ignore
from tkinter import ttk, messagebox, scrolledtext




button_width = 15

button_padding = 10

button_distance = 5

def open_signup_page():
    signup_window = tk.Toplevel(root)
    signup_window.title("Sign Up")
    signup_window.geometry("600x700")

    frame = ttk.Frame(signup_window)
    frame.pack(pady=10)

    global signup_username_entry
    global signup_password_entry

    username_label = ttk.Label(frame, text="Username:")
    username_label.grid(row=0, column=0, padx=5, pady=5)

    signup_username_entry = ttk.Entry(frame)
    signup_username_entry.grid(row=0, column=1, padx=5, pady=5)

    password_label = ttk.Label(frame, text="Password:")
    password_label.grid(row=1, column=0, padx=5, pady=5)

    signup_password_entry = ttk.Entry(frame, show="*")
    signup_password_entry.grid(row=1, column=1, padx=5, pady=5)

    signup_button = ttk.Button(frame, text="Sign Up", command=signup)
    signup_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

def open_login_page():
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("600x700")

    frame = ttk.Frame(login_window)
    frame.pack(pady=10)

    global login_username_entry
    global login_password_entry

    username_label = ttk.Label(frame, text="Username:")
    username_label.grid(row=0, column=0, padx=5, pady=5)

    login_username_entry = ttk.Entry(frame)
    login_username_entry.grid(row=0, column=1, padx=5, pady=5)

    password_label = ttk.Label(frame, text="Password:")
    password_label.grid(row=1, column=0, padx=5, pady=5)

    login_password_entry = ttk.Entry(frame, show="*")
    login_password_entry.grid(row=1, column=1, padx=5, pady=5)

    login_button = ttk.Button(frame, text="Login", command=lambda: login(login_username_entry.get(), login_password_entry.get()))
    login_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

def open_message_page(username, user_id):
    global sender_name_var, sender_id_var
    sender_name_var.set(username)
    sender_id_var.set(user_id)

      # إخفاء نافذة تسجيل الدخول إذا كانت مفتوحة

    root.withdraw()
    
    message_window = tk.Toplevel(root)
    message_window.title("Send Message")
    message_window.geometry("600x700")

    frame1 = ttk.Frame(message_window)
    frame1.pack(pady=10, fill="both")# تحديد fill لتعبئة العرض
    faram2 = ttk.Frame(message_window)
    faram2.pack(pady=10, fill="both")
    frame2 = ttk.Frame(message_window)
    frame2.pack(pady=10, fill="both")  # تحديد fill لتعبئة العرض
    frame3 = ttk.Frame(message_window)
    frame3.pack(pady=10, fill="both")  # تحديد fill لتعبئة العرض

    global phone_entry
    global message_entry

    field_width = 60  # عرض و طول الحقل
    button_width = 30  # عرض و طول الزر

    show_sender_name_button = ttk.Button(frame1, text="Show my Name", width=button_width, command=lambda: messagebox.showinfo("MY Name", f"MY Name: {username}"))
    show_sender_name_button.pack(side=tk.LEFT)

    show_sender_id_button = ttk.Button(frame1, text="Show my ID", width=button_width, command=lambda: messagebox.showinfo("My ID", f"MY ID: {user_id}"))
    show_sender_id_button.pack(side=tk.RIGHT)

    logout_button = ttk.Button(faram2, text="log out", width=button_width  ,command=lambda: close_message_page(message_window))
    logout_button.pack()

    phone_label = ttk.Label(frame2, text="Receiver ID:")
    phone_label.pack()

    phone_entry = ttk.Entry(frame2, width=field_width)
    phone_entry.pack()

    message_label = ttk.Label(frame2, text="Message:")
    message_label.pack()

    message_entry = ttk.Entry(frame2, width=field_width)
    message_entry.pack()

    send_button = ttk.Button(frame2, text="Send message", width=button_width, command=lambda: send_message(username, user_id, phone_entry.get(), message_entry.get()))
    send_button.pack()

    show_history_button = ttk.Button(frame3, text="My message", width=button_width, command=lambda: open_message_history(user_id, username))
    show_history_button.pack()


def close_message_page(message_window):
        # إعادة فتح النافذة الرئيسية
    root.deiconify()
        # إغلاق نافذة إرسال الرسالة
    message_window.destroy()

def open_message_history(user_id, username):
    message_history_window = tk.Toplevel(root)
    message_history_window.title("Message History")
    message_history_window.geometry("600x700")

    container = ttk.Frame(message_history_window)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    all_messages = get_all_user_messages(user_id)

    if not all_messages:
        messagebox.showinfo("No Messages", "No messages found.")
        return

    for message in all_messages:
        if message["sender_id"] == user_id:
            label_text = f"To: {message['receiver_name']} (ID: {message['receiver_id']})"
        else:
            label_text = f"From: {message['sender_name']} (ID: {message['sender_id']})"

        # إنشاء زر لكل رسالة
        message_button = ttk.Button(scrollable_frame, text=label_text, width=70,
                                    command=lambda msg=message: show_message(msg, user_id))
        message_button.pack(pady=5)

    # زر العودة للأسفل
    def scroll_to_bottom():
        canvas.yview_moveto(1.0)

    scroll_button = ttk.Button(message_history_window, text="Scroll to Bottom", command=scroll_to_bottom)
    scroll_button.pack(pady=5)

    root.mainloop()



def show_message(message, user_id):
    message_window = tk.Toplevel(root)
    message_window.title("Message")
    message_window.geometry("600x700")

    frame = ttk.Frame(message_window)
    frame.pack(fill="both", expand=True)

    # عرض نص "To" إذا كان المستخدم هو المرسل، و "From" إذا كان المستخدم هو المستلم
    if message["sender_id"] == user_id:
        label_text = f"To: {message['receiver_name']} (ID: {message['receiver_id']})"
    else:
        label_text = f"From: {message['sender_name']} (ID: {message['sender_id']})"

    # عرض اسم المرسل أو المستلم في الأعلى
    sender_label = ttk.Label(frame, text=label_text, font=("Helvetica", 14, "bold"))
    sender_label.pack(pady=10)

    # استخدام عنصر Text لعرض الرسالة مع شريط التمرير
    text_frame = ttk.Frame(frame)
    text_frame.pack(fill="both", expand=True)

    # تحديد نمط الخط الكبير
    large_font = tkFont.Font(family="Helvetica", size=16)

    message_text = tk.Text(text_frame, wrap="word", font=large_font)
    message_text.insert(tk.END, message["message"])
    message_text.config(state=tk.DISABLED)  # جعل النص غير قابل للتعديل
    message_text.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(text_frame, command=message_text.yview)
    scrollbar.pack(side="right", fill="y")

    message_text.config(yscrollcommand=scrollbar.set)

def signup():
    username = signup_username_entry.get()
    password = signup_password_entry.get()

    try:
        with open('users.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = {}

    if username in users:
        messagebox.showerror("Error", "Username already exists!")
    else:
        user_id = generate_unique_id(users)
        users[username] = {"password": password, "user_id": user_id}
        with open('users.json', 'w') as file:
            json.dump(users, file)
        messagebox.showinfo("Success", "Account created successfully!\nYour user ID: {}".format(user_id))
        open_message_page(username, user_id)

def login(username, password):
    try:
        with open('users.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Error", "No registered users yet.")
        return

    if username in users:
        if users[username]["password"] == password:
            user_id = users[username]["user_id"]
            messagebox.showinfo("Success", f"Login successful!\nYour user ID: {user_id}")
            open_message_page(username, user_id)
        else:
            messagebox.showerror("Error", "Incorrect username or password.")
    else:
        messagebox.showerror("Error", "User does not exist.")

def send_message(sender_name, sender_id, receiver_id, message):
    save_message(sender_id, receiver_id, message)
    messagebox.showinfo("Success", f"Message sent successfully from {sender_name}!")
    phone_entry.delete(0, 'end')
    message_entry.delete(0, 'end')

def get_username_from_id(user_id):
    try:
        with open('users.json', 'r') as file:
            users = json.load(file)
        for username, data in users.items():
            if data["user_id"] == user_id:
                return username
    except FileNotFoundError:
        pass
    return "Unknown"


def get_received_messages(user_id):
    try:
        with open(f'messages_{user_id}.json', 'r') as file:
            messages = json.load(file)
    except FileNotFoundError:
        messages = []
    return messages



def get_sent_messages(user_id):
    try:
        with open(f'messages_{user_id}.json', 'r') as file:
            messages = json.load(file)
    except FileNotFoundError:
        messages = []
    return [message for message in messages if message["sender_id"] == user_id]



def save_message(sender_id, receiver_id, message):
    sender_name = get_username_from_id(int(sender_id))
    receiver_name = get_username_from_id(int(receiver_id))

    message_data = {
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "sender_name": sender_name,
        "receiver_name": receiver_name,
        "message": message
    }

    # حفظ الرسالة للمستقبل
    try:
        with open(f'messages_{receiver_id}.json', 'r') as file:
            messages = json.load(file)
    except FileNotFoundError:
        messages = []

    messages.append(message_data)

    with open(f'messages_{receiver_id}.json', 'w') as file:
        json.dump(messages, file)

    # حفظ الرسالة للمرسل
    try:
        with open(f'messages_{sender_id}.json', 'r') as file:
            messages = json.load(file)
    except FileNotFoundError:
        messages = []

    messages.append(message_data)

    with open(f'messages_{sender_id}.json', 'w') as file:
        json.dump(messages, file)






def generate_unique_id(users):
    while True:
        user_id = random.randint(0, 100)
        if all(user_id != user["user_id"] for user in users.values()):
            return user_id

def get_all_user_messages(user_id):
    received_messages = get_received_messages(user_id)
    sent_messages = get_sent_messages(user_id)

    # دمج الرسائل المستلمة والمرسلة وتجنب التكرار
    all_messages = []
    unique_messages = set()

    for message in received_messages + sent_messages:
        message_tuple = (message["sender_id"], message["receiver_id"], message["message"])
        if message_tuple not in unique_messages:
            unique_messages.add(message_tuple)
            all_messages.append(message)

    # عكس ترتيب الرسائل لعرضها من الأحدث إلى الأقدم
    all_messages.reverse()

    return all_messages






root = th.ThemedTk(theme="radiance")
root.title("Login Page")
root.geometry("600x700")

mhd_label = ttk.Label(root, text="MHD-chat")
mhd_label.pack(pady=(10, 0))

frame = ttk.Frame(root)
frame.pack(pady=10)

signup_button = ttk.Button(frame, text="Sign Up",width=button_width, command=open_signup_page)
signup_button.grid(row=0, column=0, padx=5, pady=5)

login_button = ttk.Button(frame, text="Login", width=button_width, command=open_login_page)
login_button.grid(row=1, column=0, padx=5, pady=5)

sender_name_var = tk.StringVar()
sender_id_var = tk.StringVar()

root.mainloop()