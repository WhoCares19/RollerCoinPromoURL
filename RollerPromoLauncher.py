import os
import sys
import tkinter as tk
import webbrowser

# Base URL for Rollercoin promo codes
BASE_URL = "https://rollercoin.com/sign-in?promocode="

def resource_path(relative_path):
    """
    Get absolute path to resource, works for development and PyInstaller bundled executables.
    """
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)

root = tk.Tk()
root.withdraw()

root.title("Rollercoin Promo Launcher")
root.resizable(True, False)  # Allow only horizontal resizing

# --- Theme Colors (Adjustable) ---
LIGHT_MODE_BG = "#F0F0F0"
LIGHT_MODE_FG = "black"
DARK_MODE_BG = "#303030"
DARK_MODE_FG = "white"

# Icon Colors (Adjustable - for Unicode icons)
MOON_ICON_COLOR = "blue"  # Color of the moon icon in light mode
SUN_ICON_COLOR = "#FFD700"  # Color of the sun icon in dark mode (light yellow)
# --- End Theme Colors ---


# Initial theme state
is_dark_mode = False # App starts in light mode by default

def apply_theme(dark_mode):
    global is_dark_mode
    is_dark_mode = dark_mode
    bg_color = DARK_MODE_BG if dark_mode else LIGHT_MODE_BG
    fg_color = DARK_MODE_FG if dark_mode else LIGHT_MODE_FG

    # Apply to root window
    root.config(bg=bg_color)

    # Apply to input frame
    input_frame.config(bg=bg_color)
    right_buttons_container.config(bg=bg_color) # Ensure container frame bg updates

    # Apply to entry
    entry.config(bg=bg_color, fg=fg_color if entry.get() != default_text else "#C8A2C8")
    if entry.get() == default_text:
        entry.config(fg="#C8A2C8") # Ensure placeholder color is consistent

    # Apply to buttons
    # "On Top" button color logic
    if dark_mode:
        toggle_btn.config(bg=bg_color, fg="white") # White in dark mode
    else:
        toggle_btn.config(bg=bg_color, fg="blue" if always_on_top else "red") # Original colors in light mode

    # "?" button color logic
    if dark_mode:
        question_btn.config(bg=bg_color, fg="white") # White in dark mode
    else:
        question_btn.config(bg=bg_color, fg="blue") # Blue in light mode

    theme_toggle_btn.config(bg=bg_color)

    # Update theme toggle button icon and color
    if dark_mode:
        theme_toggle_btn.config(text="☀️", fg=SUN_ICON_COLOR)
    else:
        theme_toggle_btn.config(text="🌙", fg=MOON_ICON_COLOR)

    # Apply to popup if it's open, passing the current dark_mode state
    global popup
    if popup and popup.winfo_exists():
        apply_theme_to_popup(dark_mode=is_dark_mode, popup_window=popup, labels_info=popup_labels_info)


def toggle_theme_command():
    apply_theme(not is_dark_mode)


# Adjusted min_width to accommodate the new theme toggle button
# Original min_width: 650. Adding ~50px for the new button and its padding.
min_width, fixed_height = 700, 60 # Increased width
root.minsize(min_width, fixed_height)

ico_path = resource_path("rcicon.ico")
if os.path.exists(ico_path):
    root.iconbitmap(ico_path)
# Removed logging.warning for missing icon


always_on_top = True
root.attributes('-topmost', always_on_top)

default_text = "Please Input the Code here"

def set_placeholder():
    entry.delete(0, tk.END)
    entry.insert(0, default_text)
    entry.config(fg="#C8A2C8")

def clear_placeholder(event=None):
    if entry.get() == default_text:
        entry.delete(0, tk.END)
    if entry.get().strip() == "": # This check should be separate for color
        entry.config(fg=DARK_MODE_FG if is_dark_mode else LIGHT_MODE_FG)


def open_url(event=None):
    code = entry.get().strip()
    if code and code != default_text:
        try:
            webbrowser.open(BASE_URL + code)
        except webbrowser.Error as e:
            error_message = f"Could not open web browser. Please ensure you have a default web browser set.\nError details: {e}"
            tk.messagebox.showerror("Browser Error", error_message)
            # Removed logging.error
        except Exception as e:
            error_message = f"An unexpected error occurred while trying to open the browser.\nError details: {e}"
            tk.messagebox.showerror("Unexpected Error", error_message)
            # Removed logging.error

def toggle_always_on_top():
    global always_on_top
    always_on_top = not always_on_top
    toggle_btn.config(text="On Top" if always_on_top else "Not On Top",
                      fg="blue" if always_on_top else "red")
    root.attributes('-topmost', always_on_top)

popup = None
popup_labels_info = [] # Global list to store (label_object, original_fg) tuples

def show_popup():
    global popup, popup_labels_info
    if popup and popup.winfo_exists():
        # If popup is already open, just ensure its theme is current
        apply_theme_to_popup(dark_mode=is_dark_mode, popup_window=popup, labels_info=popup_labels_info)
        return

    root.update_idletasks()
    root_x, root_y, root_w, root_h = root.winfo_x(), root.winfo_y(), root.winfo_width(), root.winfo_height()

    popup = tk.Toplevel(root)
    popup.withdraw()

    popup.title("How To Use")
    popup.attributes('-topmost', True)
    popup.transient(root)
    popup.resizable(False, False)
    popup.protocol("WM_DELETE_WINDOW", close_popup)
    popup.bind("<Escape>", close_popup)

    ico_path = resource_path("rcicon.ico")
    if os.path.exists(ico_path):
        popup.iconbitmap(ico_path)
    # Removed logging.warning for missing icon for popup


    messages = [
        ('This app puts the CODE after:', ("Arial", 12), "black", "center"),
        ('"https://rollercoin.com/sign-in?promocode="', ("Arial", 12, "italic"), "blue", "center"),
        ('After pressing Enter, full link is opened in your browser.', ("Arial", 12), "black", "center"),
        ('THIS APP DOES NOT AUTO CLAIM.', ("Arial", 12, "bold"), "red", "center"),
        ('You must be signed in and manually claim.', ("Arial", 12, "bold"), "red", "center"),
        ('Sometimes the promocode might take a few refreshes to show up for you.', ("Arial", 12), "black", "center"),
        ('This is not an app bug', ("Arial", 12, "italic"), "red", "center"),
        ('No responsibility is taken if the claim popup didn\'t show and you were unable to claim the prize.', ("Arial", 12, "bold"), "red", "center"),
        ('To be used for RollerCoin PromoCodes (not the whole links)', ("Arial", 8, "italic"), "black", "right"),
        ('Made by 00 with the help of ChatGPT + Copilot', ("Arial", 8, "italic"), "gray", "right"),
    ]

    container = tk.Frame(popup, padx=15, pady=5)
    container.pack(fill="both", expand=True)

    # Clear previous info and store (label_object, original_fg_color)
    popup_labels_info.clear()
    for text, font, fg, justify in messages[:-2]:
        lbl = tk.Label(container, text=text, font=font, fg=fg, justify=justify, anchor="center")
        lbl.pack(anchor="center", pady=0)
        popup_labels_info.append((lbl, fg)) # Store label and its original fg

    spacer = tk.Label(container, text="", height=1)
    spacer.pack()
    popup_labels_info.append((spacer, None)) # Spacer has no fg, store None

    for text, font, fg, justify in messages[-2:]:
        lbl = tk.Label(container, text=text, font=font, fg=fg, justify=justify, anchor="e")
        lbl.pack(anchor="e", fill="x")
        popup_labels_info.append((lbl, fg)) # Store label and its original fg

    def start_drag(event):
        popup._drag_start_x = event.x
        popup._drag_start_y = event.y

    def do_drag(event):
        x = popup.winfo_x() + event.x - popup._drag_start_x
        y = popup.winfo_y() + event.y - popup._drag_start_y
        popup.geometry(f"+{x}+{y}")

    popup.bind("<Button-1>", start_drag)
    popup.bind("<B1-Motion>", do_drag)

    popup.update_idletasks()
    width = container.winfo_reqwidth()
    height = container.winfo_reqheight()
    popup.geometry(f"{width}x{height}+{root_x + (root_w - width) // 2}+{root_y + (root_h - height) // 2}")

    def delayed_show():
        if popup and popup.winfo_exists():
            popup.deiconify()
            popup.focus_force()
    popup.after(10, delayed_show)

    # Apply current theme to popup contents immediately after creation
    apply_theme_to_popup(dark_mode=is_dark_mode, popup_window=popup, labels_info=popup_labels_info)


def apply_theme_to_popup(dark_mode, popup_window, labels_info):
    # Determine background color based on theme
    bg_color = DARK_MODE_BG if dark_mode else LIGHT_MODE_BG

    popup_window.config(bg=bg_color)

    # Ensure the main container frame and all its children get the correct background
    container_frame = None
    for child in popup_window.winfo_children():
        if isinstance(child, tk.Frame):
            container_frame = child
            break
    if container_frame:
        container_frame.config(bg=bg_color)
        # Recursively apply background to all widgets within the container
        for widget in container_frame.winfo_children():
            try:
                widget.config(bg=bg_color)
            except tk.TclError:
                pass # Widget might not have 'bg' option

    # Apply foregrounds using the stored original colors for the popup labels
    for lbl, original_fg in labels_info:
        if isinstance(lbl, tk.Label): # Ensure it's a label before trying to set fg
            if original_fg:
                lbl.config(fg=original_fg) # Always use original foreground color
            else: # For labels that don't have an original_fg specified (like the spacer, if it ever had text)
                # Fallback to the light mode FG as this is the default text color
                lbl.config(fg=LIGHT_MODE_FG)


def close_popup(event=None):
    global popup, popup_labels_info
    if popup and popup.winfo_exists():
        popup.destroy()
        popup = None
        popup_labels_info.clear() # Clear stored info when popup closes
        root.focus_force()

def exit_app(event=None):
    root.destroy()

root.bind("<Escape>", exit_app)

input_frame = tk.Frame(root)
input_frame.pack(padx=20, pady=8, fill="x")

toggle_btn = tk.Button(input_frame, text="On Top", font=("Arial", 12), fg="blue",
                       width=10, height=1, command=toggle_always_on_top)
toggle_btn.pack(side="left", padx=10)

entry = tk.Entry(input_frame, font=("Arial", 18), bd=4, fg="purple", justify="center")
entry.pack(side="left", expand=True, fill="x")

# --- New Right Buttons Container ---
right_buttons_container = tk.Frame(input_frame)
right_buttons_container.pack(side="right") # Pack this frame to the far right

question_btn = tk.Button(right_buttons_container, text="❓", font=("Arial", 12), fg="blue", width=3, command=show_popup)
question_btn.pack(side="left", padx=5) # Pack into new container, to its left (from container's perspective)

theme_toggle_btn = tk.Button(right_buttons_container, text="🌙", font=("Arial", 12), width=3, command=toggle_theme_command)
theme_toggle_btn.pack(side="left", padx=(5,0)) # Pack into new container, to its left (from container's perspective)
# --- End New Right Buttons Container ---


entry.bind("<FocusIn>", clear_placeholder)
entry.bind("<Return>", open_url)

def on_window_click(event):
    widget = event.widget
    if widget.winfo_toplevel() == root and widget != entry and (entry.get().strip() == "" or entry.get() == default_text):
        set_placeholder()
        root.focus()

root.bind_all("<Button-1>", on_window_click, add="+")

def on_focus_out(event):
    if entry.get().strip() == "":
        set_placeholder()

entry.bind("<FocusOut>", on_focus_out)

# Right-click context menu for entry
context_menu = tk.Menu(entry, tearoff=0)
context_menu.add_command(label="Cut", command=lambda: entry.event_generate("<<Cut>>"))
context_menu.add_command(label="Copy", command=lambda: entry.event_generate("<<Copy>>"))
context_menu.add_command(label="Paste", command=lambda: entry.event_generate("<<Paste>>"))
context_menu.add_command(label="Delete", command=lambda: entry.delete(0, tk.END))
context_menu.add_separator()
context_menu.add_command(label="Select All", command=lambda: entry.select_range(0, tk.END))

def show_context_menu(event):
    try:
        context_menu.tk_popup(event.x_root, event.y_root)
    finally:
        context_menu.grab_release()

entry.bind("<Button-3>", show_context_menu)


set_placeholder()

# Initial theme application (light mode by default)
apply_theme(dark_mode=False)

screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
x = (screen_width // 2) - (min_width // 2)
y = (screen_height // 2) - (fixed_height // 2)
root.geometry(f"{min_width}x{fixed_height}+{x}+{y}")

root.deiconify()
root.mainloop()
