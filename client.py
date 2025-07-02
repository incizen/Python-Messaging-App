import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import tkinter.ttk as ttk

HOST = '127.0.0.1'
PORT = 1234

# Color palette
DARK_GREY = '#23272F'
MEDIUM_GREY = '#2C313C'
OCEAN_BLUE = '#4F8EF7'
WHITE = "#F7F7F7"
LIGHT_GREY = '#E5E5E5'
ACCENT = '#A3BFFA'
FONT = ("Segoe UI", 13)
BUTTON_FONT = ("Segoe UI", 12, 'bold')
SMALL_FONT = ("Segoe UI", 11)

# Style
style = ttk.Style()
style.theme_use('clam')
style.configure('TFrame', background=MEDIUM_GREY)
style.configure('TLabel', background=DARK_GREY, foreground=WHITE, font=FONT)
style.configure('Header.TLabel', background=OCEAN_BLUE, foreground=WHITE, font=("Segoe UI", 16, 'bold'))
style.configure('TButton', background=OCEAN_BLUE, foreground=WHITE, font=BUTTON_FONT, borderwidth=0, focusthickness=3, focuscolor=ACCENT)
style.map('TButton', background=[('active', ACCENT)])
style.configure('TEntry', fieldbackground=LIGHT_GREY, background=LIGHT_GREY, foreground=DARK_GREY, font=FONT, borderwidth=0)

# Socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Creating the main window as the very first Tkinter call
root = tk.Tk()
root.geometry("600x600")
root.title("Messenger Client")
root.resizable(False, False)
root.configure(bg=MEDIUM_GREY)

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

def connect():
    try:
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        add_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}", parent=root)

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty", parent=root)

    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

def send_message():
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, len(message))
    else:
        messagebox.showerror("Empty message", "Message cannot be empty", parent=root)

# Header bar
header_frame = ttk.Frame(root, height=50, style='TFrame')
header_frame.grid(row=0, column=0, sticky=tk.EW)
header_label = ttk.Label(header_frame, text="Messenger", style='Header.TLabel', anchor='center')
header_label.pack(fill=tk.BOTH, expand=True, pady=5)

root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=0)

# Top frame for the username
top_frame = ttk.Frame(root, style='TFrame', padding=10)
top_frame.grid(row=1, column=0, sticky=tk.EW)

username_label = ttk.Label(top_frame, text="Enter username:", style='TLabel')
username_label.pack(side=tk.LEFT, padx=(0, 10))

username_textbox = ttk.Entry(top_frame, font=FONT, width=20)
username_textbox.pack(side=tk.LEFT, padx=(0, 10))

username_button = ttk.Button(top_frame, text="Join", style='TButton', command=connect)
username_button.pack(side=tk.LEFT, padx=(0, 10))

# Chatbox
middle_frame = ttk.Frame(root, style='TFrame', padding=10)
middle_frame.grid(row=2, column=0, sticky=tk.NSEW)

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=WHITE, fg=DARK_GREY, width=67, height=22, bd=0, relief='flat', highlightthickness=1, highlightbackground=ACCENT)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5)

# Bottom bar for the message entry
bottom_frame = ttk.Frame(root, style='TFrame', padding=10)
bottom_frame.grid(row=3, column=0, sticky=tk.EW)

message_textbox = ttk.Entry(bottom_frame, font=FONT, width=38)
message_textbox.pack(side=tk.LEFT, padx=(0, 10), ipady=4)

message_button = ttk.Button(bottom_frame, text="Send", style='TButton', command=send_message)
message_button.pack(side=tk.LEFT)

# Enter key
def on_enter(event):
    send_message()
    return 'break'
message_textbox.bind('<Return>', on_enter)

def listen_for_messages_from_server(client):
    try:
        while True:
            message = client.recv(2048).decode('utf-8')
            if message:
                if '~' in message:
                    username, content = message.split('~', 1)
                    add_message(f"[{username}] {content}")
                else:
                    add_message(f"[SERVER] {message}")
            else:
                add_message("[SERVER] Disconnected from server.")
                break
    except Exception as e:
        add_message(f"[ERROR] Lost connection to server: {e}")
    finally:
        try:
            client.close()
        except:
            pass

# Main function
def main():

    root.mainloop()
    
if __name__ == '__main__':
    main()