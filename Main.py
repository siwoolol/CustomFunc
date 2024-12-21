import tkinter as tk
from tkinter import ttk, messagebox
import keyboard
import os

custom_hotkeys = {}
hotkey_hooks = []

def add_hotkey():
    key_combination = key_entry.get().lower()
    action = action_entry.get()
    if not key_combination or not action:
        messagebox.showerror("Error", "Please enter both a key combination and an action.")
        return

    try:
        # Attempt to register the hotkey to check for validity
        keyboard.add_hotkey(key_combination, lambda: None)
        keyboard.remove_hotkey(key_combination)  # Remove immediately after check

        custom_hotkeys[key_combination] = action
        update_listbox()
        key_entry.delete(0, tk.END)
        action_entry.delete(0, tk.END)

        # Re-register all hotkeys
        register_hotkeys()

    except ValueError:
        messagebox.showerror("Error", "Invalid key combination.")

def remove_hotkey():
    try:
        selected_index = listbox.curselection()[0]
        key_combination = listbox.get(selected_index).split(":")[0].strip()
        del custom_hotkeys[key_combination]
        update_listbox()

        # Re-register all hotkeys
        register_hotkeys()

    except IndexError:
        messagebox.showerror("Error", "Please select a hotkey to remove.")

def update_listbox():
    listbox.delete(0, tk.END)
    for key_combination, action in custom_hotkeys.items():
        listbox.insert(tk.END, f"{key_combination}: {action}")

def save_hotkeys():
    with open("hotkeys.txt", "w") as f:
        for key_combination, action in custom_hotkeys.items():
            f.write(f"{key_combination}:{action}\n")

def load_hotkeys():
    """Loads hotkeys from a file."""
    try:
        with open("hotkeys.txt", "r") as f:
            for line in f:
                try:
                    key_combination, action = line.strip().split(":", 1)  # Split only at the first colon
                    custom_hotkeys[key_combination] = action
                except ValueError:
                    print(f"Skipping invalid line: {line.strip()}")  # Handle lines without colons
        update_listbox()

        # Register hotkeys after loading
        register_hotkeys()

    except FileNotFoundError:
        pass

def execute_action(key_combination):
    action = custom_hotkeys[key_combination]
    if action.startswith("open "):
        try:
            app_path = action.split("open ", 1)[1]
            os.startfile(app_path)
        except FileNotFoundError:
            messagebox.showerror("Error", f"Application not found: {app_path}")
    else:
        print(f"Executing action: {action}")


def register_hotkeys():
    """Registers all hotkeys from the custom_hotkeys dictionary."""
    global hotkey_hooks  # Access the global list

    # Remove existing hotkeys
    for hook in hotkey_hooks:
        keyboard.remove_hotkey(hook)
    hotkey_hooks = []  # Clear the list

    for key_combination, action in custom_hotkeys.items():
        hook = keyboard.add_hotkey(key_combination, lambda kc=key_combination: execute_action(kc))
        hotkey_hooks.append(hook)  # Store the hook object


# Create the main window
window = tk.Tk()
window.title("Hotkey Customizer")
window.configure(bg="#333333")  # Set dark gray background

# Configure style for rounded corners and larger elements
style = ttk.Style()
style.configure("TButton", padding=10, font=("TkDefaultFont", 12), borderwidth=0, relief="flat")
style.configure("TLabel", background="#333333", foreground="white", font=("TkDefaultFont", 12))
style.configure("TEntry", font=("TkDefaultFont", 12), padding=5)
style.configure("TListbox", font=("TkDefaultFont", 12), background="#444444", foreground="white")

# Key combination entry
key_label = ttk.Label(window, text="Key Combination:")
key_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
key_entry = ttk.Entry(window)
key_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

# Action entry
action_label = ttk.Label(window, text="Action (e.g., open path/to/app.exe):")
action_label.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
action_entry = ttk.Entry(window)
action_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

# Add button
add_button = ttk.Button(window, text="Add Hotkey", command=add_hotkey, style="TButton")
add_button.grid(row=2, column=0, columnspan=2, pady=10)

# Listbox to display hotkeys
listbox = tk.Listbox(window, width=50, height=10, bg="#444444", fg="white", font=("TkDefaultFont", 12))
listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Remove button
remove_button = ttk.Button(window, text="Remove Hotkey", command=remove_hotkey, style="TButton")
remove_button.grid(row=4, column=0, columnspan=2, pady=10)

# Save/Load buttons
save_button = ttk.Button(window, text="Save Hotkeys", command=save_hotkeys, style="TButton")
save_button.grid(row=5, column=0, pady=10)
load_button = ttk.Button(window, text="Load Hotkeys", command=load_hotkeys, style="TButton")
load_button.grid(row=5, column=1, pady=10)

# Configure grid weights for resizing
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.rowconfigure(3, weight=1)  # Allow listbox to expand vertically

# Load hotkeys on startup
load_hotkeys()

# Run the main event loop
window.mainloop()