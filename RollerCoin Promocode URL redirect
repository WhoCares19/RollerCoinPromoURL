import os
import sys
import tkinter as tk
import webbrowser
from PIL import Image, ImageTk

# Base URL for Rollercoin promo codes
BASE_URL = "https://rollercoin.com/sign-in?promocode="

# Utility Functions (Resource Handling)
def resource_path(relative_path):
    """Correctly reference bundled resources (icons) for an .exe."""
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)

# GUI Setup
root = tk.Tk()
root.title("Rollercoin Promo Launcher")
root.resizable(True, False)  # Prevent resizing

# Always on Top Configuration
always_on_top = True
root.attributes('-topmost', always_on_top)

# Entry Box Functions
default_text = "Please Input the Code here"

def clear_placeholder(event):
    """Remove placeholder completely when clicking inside the input box."""
    if entry.get() == default_text:
        entry.delete(0, tk.END)
        entry.config(fg="black")
        entry.icursor(0)

def restore_placeholder(event):
    """Restore placeholder when focus is lost and input is empty, ensuring cursor disappears."""
    if not entry.get().strip():
        entry.insert(0, default_text)
        entry.config(fg="gray")
        entry.master.focus_set()

# Main Functionality
def open_url(event=None):
    """Open the promo code URL when the user presses Enter."""
    if entry.get().strip() and entry.get() != default_text:
        webbrowser.open(BASE_URL + entry.get().strip())

def toggle_always_on_top():
    """Toggle 'Always on Top' window behavior."""
    global always_on_top
    always_on_top = not always_on_top
    root.attributes('-topmost', always_on_top)
    toggle_btn.config(
        text="This window is always on top" if always_on_top else "This window is not on top",
        fg="green" if always_on_top else "black",
        relief="raised"
    )

# Popup Functions
popup = None

def show_popup():
    """Display or close the instruction popup."""
    global popup
    if popup and popup.winfo_exists():
        popup.destroy()
        popup = None
        return

    root.update_idletasks()
    root_x, root_y, root_w, root_h = root.winfo_x(), root.winfo_y(), root.winfo_width(), root.winfo_height()

    # Create the popup
    popup = tk.Toplevel(root)
    popup.title("How To Use")
    popup.attributes('-topmost', True)
    popup.resizable(False, False)
    popup.bind("<Escape>", close_popup)  
    popup.focus_force()  

    # Add explanatory labels
    messages = [
        ('This app puts the CODE after:', ("Arial", 12), "black"),
        ('"https://rollercoin.com/sign-in?promocode="', ("Arial", 12, "italic"), "blue"),
        ('After pressing Enter, full link is opened in your browser.', ("Arial", 12), "black"),
        ('THIS APP DOES NOT AUTO CLAIM.\nYou must be signed in and manually claim.', ("Arial", 12, "bold"), "red"),
        ('Sometimes the promocode might take a few refreshes to show up for you.', ("Arial", 12), "black"),
        ('This is not an app bug', ("Arial", 12, "italic"), "red"), 
        ('No responsibility is taken if the claim popup didn\'t show and you were unable to claim the prize.', ("Arial", 12, "bold"), "red"),
        ('To be used for RollerCoin PromoCodes (not the whole links)', ("Arial", 8, "italic"), "black"),
        ('Made by 00 with the help of ChatGPT + Copilot', ("Arial", 8, "italic"), "gray"),
    ]

    for msg, font, color in messages:
        label = tk.Label(popup, text=msg, font=font, fg=color)

        # Apply right alignment ONLY to these specific messages
        if msg.startswith("To be used for RollerCoin PromoCodes") or msg.startswith("Made by 00"):
            label.config(anchor="e")  # Align text to the right

        label.pack(pady=0, fill="x")

    # Center the popup
    popup.update_idletasks()
    width = max(widget.winfo_reqwidth() for widget in popup.winfo_children()) + 80
    height = sum(widget.winfo_reqheight() for widget in popup.winfo_children()) + 10
    popup.geometry(f"{width}x{height}+{root_x + (root_w - width)//2}+{root_y + (root_h - height)//2}")

def close_popup(event=None):
    """Close the popup window (but not the main application)."""
    global popup
    if popup and popup.winfo_exists():
        popup.destroy()
        popup = None

# Exit Application
def exit_app(event=None):
    """Exit the application only when the main window is active."""
    if not popup or not popup.winfo_exists():
        root.destroy()

root.bind("<Escape>", exit_app)  

# Load and apply the window icon
image_path = resource_path("rollercoinICON.png")
icon = ImageTk.PhotoImage(Image.open(image_path)) if os.path.exists(image_path) else None
if icon:
    root.iconphoto(False, icon)

ico_path = resource_path("rollercoinICON.ico")
if os.path.exists(ico_path):
    root.iconbitmap(ico_path)

# Entry Field for Promo Codes
input_frame = tk.Frame(root)
input_frame.pack(padx=20, pady=8, fill="x")

entry = tk.Entry(input_frame, font=("Arial", 18), bd=2, fg="gray", justify="center")
entry.insert(0, default_text)
entry.bind("<FocusIn>", clear_placeholder)
entry.bind("<FocusOut>", restore_placeholder)
entry.bind("<Return>", open_url)
entry.pack(side="left", expand=True, fill="x")

# Help Button (Popup)
question_btn = tk.Button(input_frame, text="❓", font=("Arial", 12), fg="blue", width=3, command=show_popup)
question_btn.pack(side="right")

# Toggle "Always on Top" Button
toggle_btn = tk.Button(root, text="This window is always on top", fg="green",
                       font=("Arial", 18), command=toggle_always_on_top)
toggle_btn.pack(pady=4, fill="x")

# Ensure placeholder restores when clicking anywhere inside the window & cursor disappears
root.bind("<Button-1>", lambda event: restore_placeholder(event) if event.widget != entry else None)

# Window Sizing & Positioning
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
width = max(widget.winfo_reqwidth() for widget in root.winfo_children()) + 150
height = sum(widget.winfo_reqheight() for widget in root.winfo_children()) + 60  # Increased by 20 pixels

# Calculate center position
x, y = (screen_width // 2) - (width // 2), (screen_height // 2) - (height // 2)

# Set window size and position
root.geometry(f"{width}x{height}+{x}+{y}")
root.minsize(width, height)

root.mainloop()
