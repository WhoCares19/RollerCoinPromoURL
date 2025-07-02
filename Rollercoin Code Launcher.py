import tkinter as tk
from tkinter import messagebox, PhotoImage, font
import os
import webbrowser
import sys
import functools


# --- Configuration Variables ---
# Main Window Defaults
DEFAULT_MAIN_TITLE = "Rollercoin Promo Launcher"
DEFAULT_MIN_WIDTH = 750
DEFAULT_MIN_HEIGHT = 100
DEFAULT_HEIGHT_RESIZABLE = False
DEFAULT_WIDTH_RESIZABLE = False
ICON_SIZE_WIDTH = 16
ICON_SIZE_HEIGHT = 16

# Input Box Defaults
DEFAULT_BASE_URL = "https://rollercoin.com/sign-in?promocode="
DEFAULT_MAIN_INPUT_PLACEHOLDER = "Please input The Code Here"
# MODIFIED: Removed DEFAULT_MAIN_INPUT_PLACEHOLDER_FG as it's now theme-dependent.
# DEFAULT_MAIN_INPUT_PLACEHOLDER_FG = "#DBA2C2" # A bit more purple-ish pink
DEFAULT_ON_TOP_BUTTON_GAP = 5
DEFAULT_ON_TOP_BUTTON_EXTRA_WIDTH = 0
DEFAULT_ON_TOP_TEXT_SIZE = 12

# MODIFIED: Define DEFAULT_MAIN_INPUT_FONT_SIZE, as it was used but not defined in the provided code
DEFAULT_MAIN_INPUT_FONT_FONT = "Fixedsys" # Change to a monospace font for 8-bit style
DEFAULT_MAIN_INPUT_FONT_SIZE = 18

# Popup Window Defaults
DEFAULT_POPUP_TITLE = "How to use"
DEFAULT_POPUP_MIN_WIDTH = 1050
DEFAULT_POPUP_MIN_HEIGHT = 350 # Keeping this strictly at 350 as requested
DEFAULT_POPUP_WIDTH_RESIZABLE = False
DEFAULT_POPUP_HEIGHT_RESIZABLE = False
DEFAULT_POPUP_IMAGE_VERTICAL_OFFSET = 100 # Vertical offset for RIGHT image in popup (no longer directly used by .place(), but kept for reference)
DEFAULT_POPUP_LEFT_IMAGE_VERTICAL_OFFSET = 100 # NEW: Vertical offset for LEFT image in popup (no longer directly used by .place(), but kept for reference)

# NEW: Second Popup Window Defaults are now internal to PopupHowTo
# SECOND_POPUP_TITLE = "Chamster Images" # No longer a separate title
# SECOND_POPUP_WIDTH = 700 # No longer a separate width
# SECOND_POPUP_HEIGHT = 500 # No longer a separate height

# Popup text defaults (for labels without explicit settings)
POPUP_DEFAULT_TEXT_FONT_FAMILY = "Arial"
POPUP_DEFAULT_TEXT_FONT_SIZE = 10
# NEW: Font for 8-bit style text in popup
POPUP_EIGHT_BIT_FONT_FAMILY = "Fixedsys" # Or try "Terminal", "Courier New" if Fixedsys isn't available or doesn't look right.

# NEW: Chamster Button Defaults for Popup
RIGHT_CHAMSTER_BUTTON_WIDTH_DEFAULT = 200 # Matches image width
RIGHT_CHAMSTER_BUTTON_HEIGHT_DEFAULT = 200 # Matches image height
RIGHT_CHAMSTER_BUTTON_PADX_DEFAULT = (10, 0)
RIGHT_CHAMSTER_BUTTON_PADY_DEFAULT = (0, 105)

# NEW: Left Chamster Button Defaults for Popup (on the image page)
LEFT_CHAMSTER_BUTTON_WIDTH_DEFAULT = 200 # Matches image width
LEFT_CHAMSTER_BUTTON_HEIGHT_DEFAULT = 200 # Matches image height
LEFT_CHAMSTER_BUTTON_PADX_DEFAULT = (10, 0) # Padding on the left for the button
LEFT_CHAMSTER_BUTTON_PADY_DEFAULT = (0, 100) # Padding at the bottom for the button

# REMOVED: Day/Night Mode Icon Row Padding variables


# --- Theme Colors ---
# Main Window Colors
LIGHT_THEME_MAIN_CONTENT_BG = "#f0f0f0"
DARK_THEME_MAIN_CONTENT_BG = "#333333"
LIGHT_THEME_MAIN_TITLEBAR_BG = "#e0e0e0"
DARK_THEME_MAIN_TITLEBAR_BG = "#444444"

# Popup Window Colors
LIGHT_THEME_POPUP_CONTENT_BG = "#f8f8f8"
DARK_THEME_POPUP_CONTENT_BG = "#2a2a2a"
LIGHT_THEME_POPUP_TITLEBAR_BG = "#d0d0d0"
DARK_THEME_POPUP_TITLEBAR_BG = "#3a3a3a"

# General Foreground (text) Colors
LIGHT_THEME_FG = "#333333"
DARK_THEME_FG = "#f0f0f0"

# Button Hover Colors
BUTTON_HOVER_COLOR = "#cccccc"
DARK_BUTTON_HOVER_COLOR = "#555555"

# Entry Widget Colors (for main window and general use)
ENTRY_BG_LIGHT = "#ffffff"
ENTRY_FG_LIGHT = "#333333"
ENTRY_BG_DARK = "#444444"
ENTRY_FG_DARK = "#f0f0f0" # Default foreground for main entry in dark mode

# NEW: Main Input Placeholder Foreground Colors
MAIN_INPUT_PLACEHOLDER_FG_LIGHT = "#DBA2C8" # A softer gray for light mode placeholder
MAIN_INPUT_PLACEHOLDER_FG_DARK = "#DBA2C8" # Original color for dark mode placeholder, which user likes

# Popup Entry Widget Colors (NEW - Specific for Popup Input Box)
# Colors for when the popup input box is ENABLED (typing)
POPUP_ENABLED_ENTRY_FG_LIGHT = "#333333" # Text color when typing in light mode
POPUP_ENABLED_ENTRY_FG_DARK = "white"   # Text color when typing in dark mode

# Colors for when the popup input box is DISABLED (non-typing/placeholder)
POPUP_DISABLED_ENTRY_FG_LIGHT = "#0096FF" # Color of the base URL text in light mode (non-editing)
POPUP_DISABLED_ENTRY_FG_DARK = "#0096FF" # Color of the base URL text in dark mode (non-editing - Light Blue as example)


# Border Colors
BORDER_COLOR_LIGHT = "#aaaaaa"
BORDER_COLOR_DARK = "#666666"

# --- Theme Transition Settings ---
THEME_TRANSITION_DURATION_MS = 400 # MODIFIED: Increased for smoother transitions
THEME_TRANSITION_STEPS = 30 # MODIFIED: Increased for smoother transitions
THEME_ICON_DISPLAY_WIDTH = 32
THEME_ICON_DISPLAY_HEIGHT = 32
ICON_SLIDE_DURATION_MS = 250
ICON_SLIDE_STEPS = 10
POPUP_FADE_DURATION_MS = 250 # MODIFIED: Increased for smoother popup fade-in
POPUP_FADE_STEPS = 15 # MODIFIED: Increased for smoother popup fade-in
MAIN_FADE_DURATION_MS = 200 # Duration for main window fade-in
MAIN_FADE_STEPS = 15 # Number of steps for main window fade-in


# Global dictionary to store active color transition animation IDs
_active_color_transitions = {}
# Removed global active_windows list as it's no longer needed for ESC key handling

# --- Helper function to handle resource paths for portability ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- Define asset paths using the resource_path helper ---
# All image assets are now assumed to be in the "Pixel Icons" directory
PIXEL_ICONS_DIR = resource_path("Pixel Icons")
POPUP_PIXEL_ICONS_DIR = resource_path("Pixel Icons")
# Updated MAIN_ICON_PATH to point inside the "Pixel Icons" folder
MAIN_ICON_PATH = resource_path(os.path.join("Pixel Icons", "rcicon.png"))
# New icons for "On Top" button
ON_TOP_LOCKED_ICON_PATH = resource_path(os.path.join("Pixel Icons", "RClocked.png"))
ON_TOP_UNLOCKED_ICON_PATH = resource_path(os.path.join("Pixel Icons", "RCUnlock.png"))
# NEW: Icons for Chat Lock button - now only using dark theme versions
CHAT_LOCK_ON_DARK_ICON_PATH = resource_path(os.path.join("Pixel Icons", "RCDarkUnlock.png"))
CHAT_LOCK_OFF_DARK_ICON_PATH = resource_path(os.path.join("Pixel Icons", "RCDarkLock.png"))
# NEW: Popup Window Icon
POPUP_WINDOW_ICON_PATH = resource_path(os.path.join("Pixel Icons", "RCPopupWindow.png"))
# NEW: Clicked Chamster Icon for first popup page
RCHAMSTER_LEFT_CLICKED_ICON_PATH = resource_path(os.path.join("Pixel Icons", "RChamsterLookingLeftClicked.png"))
# NEW: Clicked Chamster Icon for the second popup page
RCHAMSTER_RIGHT_CLICKED_ICON_PATH = resource_path(os.path.join("Pixel Icons", "RChamsterLookingRightClicked.png"))


# --- Helper Functions (Independent of Classes or simple global state) ---
def get_main_window_bg_color(theme_name):
    """Returns the main window content background color for the given theme."""
    return DARK_THEME_MAIN_CONTENT_BG if theme_name == 'dark' else LIGHT_THEME_MAIN_CONTENT_BG

def get_main_title_bar_color(theme_name):
    """Returns the main window title bar background color for the given theme."""
    return DARK_THEME_MAIN_TITLEBAR_BG if theme_name == 'dark' else LIGHT_THEME_MAIN_TITLEBAR_BG

def get_popup_window_bg_color(theme_name):
    """Returns the popup window content background color for the given theme."""
    return DARK_THEME_POPUP_CONTENT_BG if theme_name == 'dark' else LIGHT_THEME_POPUP_CONTENT_BG

def get_popup_title_bar_color(theme_name):
    """Returns the popup window title bar background color for the given theme."""
    return DARK_THEME_POPUP_TITLEBAR_BG if theme_name == 'dark' else LIGHT_THEME_POPUP_TITLEBAR_BG

def get_fg_color(theme_name):
    """Returns the general foreground color based on the theme."""
    return DARK_THEME_FG if theme_name == 'dark' else LIGHT_THEME_FG

def hex_to_rgb(hex_color):
    """Converts a hex color string (#RRGGBB) to an RGB tuple (R, G, B)."""
    # FIX: Corrected typo from hex_lstrip to hex_color.lstrip
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb_color):
    """Converts an RGB tuple (R, G, B) to a hex color string (#RRGGBB)."""
    return '#%02x%02x%02x' % tuple(max(0, min(255, int(c))) for c in rgb_color)

def smooth_color_transition(widget, prop_name, start_hex, end_hex, duration_ms, steps):
    """Smoothly transitions a color property of a widget."""
    if not widget.winfo_exists(): return

    transition_key = (str(widget), prop_name)
    if transition_key in _active_color_transitions:
        try:
            widget.after_cancel(_active_color_transitions[transition_key])
        except ValueError: pass
        finally:
            del _active_color_transitions[transition_key]

    try:
        start_rgb = hex_to_rgb(start_hex)
        end_rgb = hex_to_rgb(end_hex)
    except ValueError:
        if widget.winfo_exists() and prop_name in widget.config():
            widget.config(**{prop_name: end_hex})
        return

    if duration_ms == 0 or steps == 0:
        if widget.winfo_exists() and prop_name in widget.config():
            widget.config(**{prop_name: end_hex})
        return

    step_time = duration_ms // steps
    r_step, g_step, b_step = [(end_rgb[i] - start_rgb[i]) / steps for i in range(3)]

    def animate(current_step):
        if not widget.winfo_exists():
            if transition_key in _active_color_transitions: del _active_color_transitions[transition_key]
            return

        if current_step <= steps:
            r, g, b = [int(start_rgb[i] + [r_step, g_step, b_step][i] * current_step) for i in range(3)]
            current_hex = rgb_to_hex((r, g, b))
            try:
                if prop_name in widget.config():
                    widget.config(**{prop_name: current_hex})
            except tk.TclError:
                if transition_key in _active_color_transitions: del _active_color_transitions[transition_key]
                return
            _active_color_transitions[transition_key] = widget.after(step_time, animate, current_step + 1)
        else:
            if widget.winfo_exists() and prop_name in widget.config():
                widget.config(**{prop_name: end_hex})
            if transition_key in _active_color_transitions: del _active_color_transitions[transition_key]

    _active_color_transitions[transition_key] = widget.after(0, animate, 0)

# MODIFIED: DraggableWindowMixin now allows explicit bind/unbind
class DraggableWindowMixin:
    """
    Mixin to add draggable functionality to a Tkinter widget.
    This version allows explicit binding/unbinding of drag events.
    """
    def __init__(self, master_or_self_widget, root_window):
        self.master_or_self = master_or_self_widget
        self.root_window = root_window
        self._drag_offset_x = 0
        self._drag_offset_y = 0
        self._is_dragging = False # To track active drag operation

        # Store references to the bound functions to allow unbinding
        self._start_drag_id = None
        self._drag_window_id = None
        self._stop_drag_id = None

    def bind_drag_events(self):
        # Only bind if not already bound (checking any of the IDs is sufficient)
        if self._start_drag_id is None:
            self._start_drag_id = self.master_or_self.bind("<ButtonPress-1>", self._start_drag_wrapper)
            self._drag_window_id = self.master_or_self.bind("<B1-Motion>", self._drag_window_wrapper)
            self._stop_drag_id = self.master_or_self.bind("<ButtonRelease-1>", self._stop_drag_wrapper)

    def unbind_drag_events(self):
        # Only unbind if currently bound
        if self._start_drag_id is not None:
            self.master_or_self.unbind("<ButtonPress-1>", self._start_drag_id)
            self.master_or_self.unbind("<B1-Motion>", self._drag_window_id)
            self.master_or_self.unbind("<ButtonRelease-1>", self._stop_drag_id)
            self._start_drag_id = None
            self._drag_window_id = None
            self._stop_drag_id = None
            self._is_dragging = False # Reset drag state if unbinding mid-drag

    def _start_drag_wrapper(self, event):
        self._is_dragging = True
        # Calculate offset relative to the root window's top-left corner
        # event.x_root, event.y_root are screen coordinates of the mouse click
        # self.root_window.winfo_x(), self.root_window.winfo_y() are screen coordinates of the root window's top-left
        self._drag_offset_x = event.x_root - self.root_window.winfo_x()
        self._drag_offset_y = event.y_root - self.root_window.winfo_y()

    def _drag_window_wrapper(self, event):
        if not self._is_dragging: return # Only drag if a drag operation has started

        if getattr(self.root_window, 'is_maximized', False):
            self.root_window.toggle_maximize()
            self.root_window.update_idletasks()
            # MODIFIED: Recalculate offset based on the new window position to prevent jump
            self._drag_offset_x = event.x_root - self.root_window.winfo_x()
            self._drag_offset_y = event.y_root - self.root_window.winfo_y()

        x = self.root_window.winfo_pointerx() - self._drag_offset_x
        y = self.root_window.winfo_pointery() - self._drag_offset_y
        self.root_window.geometry(f"+{x}+{y}")

    def _stop_drag_wrapper(self, event):
        self._is_dragging = False


class CustomTitleBar(tk.Frame):
    """Custom title bar for Tkinter windows."""
    def __init__(self, parent, title_text, icon_path, minimize_cmd=None, maximize_cmd=None, close_cmd=None, main_window=True):
        super().__init__(parent, relief="flat", height=30)
        self.parent = parent
        self.main_window = main_window
        self.pack_propagate(False)

        try:
            original_icon_image = PhotoImage(file=icon_path)
            x_factor = max(1, original_icon_image.width() // ICON_SIZE_WIDTH)
            y_factor = max(1, original_icon_image.height() // ICON_SIZE_HEIGHT)
            self.icon_image = original_icon_image.subsample(x_factor, y_factor)
            self.icon_label = tk.Label(self, image=self.icon_image)
            self.icon_label.pack(side="left", padx=5, pady=2)
            # MODIFIED: Store DraggableWindowMixin instance and bind later
            self.icon_draggable_mixin = DraggableWindowMixin(self.icon_label, self.parent) 
        except Exception:
            self.icon_image = None

        self.title_label = tk.Label(self, text=title_text, font=("Arial", 10))
        self.title_label.pack(side="left", padx=5)
        # MODIFIED: Store DraggableWindowMixin instance and bind later
        self.title_label_draggable_mixin = DraggableWindowMixin(self.title_label, self.parent) 

        self.control_buttons_frame = tk.Frame(self)
        self.control_buttons_frame.pack(side="right")

        # --- MODIFIED: Directly bind hover events for close_button ---
        self.close_button = tk.Button(self.control_buttons_frame, text="✕", command=close_cmd, font=("Arial", 10), bd=0, relief="flat", padx=8, pady=0)
        self.close_button.pack(side="right", fill="y")
        self.close_button.bind("<Enter>", functools.partial(self._on_enter_hover, self.close_button, True))
        self.close_button.bind("<Leave>", functools.partial(self._on_leave_hover, self.close_button, True))

        if main_window and maximize_cmd:
            # --- MODIFIED: Directly bind hover events for maximize_button ---
            self.maximize_button = tk.Button(self.control_buttons_frame, text="⬜", command=maximize_cmd, font=("Arial", 10), bd=0, relief="flat", padx=8, pady=0)
            self.maximize_button.pack(side="right", fill="y")
            self.maximize_button.bind("<Enter>", functools.partial(self._on_enter_hover, self.maximize_button, False))
            self.maximize_button.bind("<Leave>", functools.partial(self._on_leave_hover, self.maximize_button, False))

        if main_window and minimize_cmd:
            # --- MODIFIED: Directly bind hover events for minimize_button ---
            self.minimize_button = tk.Button(self.control_buttons_frame, text="—", command=minimize_cmd, font=("Arial", 10), bd=0, relief="flat", padx=8, pady=0)
            self.minimize_button.pack(side="right", fill="y")
            self.minimize_button.bind("<Enter>", functools.partial(self._on_enter_hover, self.minimize_button, False))
            self.minimize_button.bind("<Leave>", functools.partial(self._on_leave_hover, self.minimize_button, False))

        # MODIFIED: Store DraggableWindowMixin instance and bind later
        self.frame_draggable_mixin = DraggableWindowMixin(self, self.parent) 

        # If it's the main window's title bar, bind drag events immediately
        if self.main_window:
            self.bind_all_drag_events()

    def bind_all_drag_events(self):
        """Binds drag events to all draggable elements within the title bar."""
        if self.icon_image:
            self.icon_draggable_mixin.bind_drag_events()
        self.title_label_draggable_mixin.bind_drag_events()
        self.frame_draggable_mixin.bind_drag_events()

    def unbind_all_drag_events(self):
        """Unbinds drag events from all draggable elements within the title bar."""
        if self.icon_image:
            self.icon_draggable_mixin.unbind_drag_events()
        self.title_label_draggable_mixin.unbind_drag_events()
        self.frame_draggable_mixin.unbind_drag_events()

    def _on_enter_hover(self, widget, is_close_button, event):
        hover_color = "#f00" if is_close_button else (DARK_BUTTON_HOVER_COLOR if current_theme == 'dark' else BUTTON_HOVER_COLOR)
        fg_color = "white" if is_close_button else get_fg_color(current_theme)
        widget.config(bg=hover_color, fg=fg_color)

    def _on_leave_hover(self, widget, is_close_button, event):
        bg_color = get_main_title_bar_color(current_theme) if self.main_window else get_popup_title_bar_color(current_theme)
        
        # Determine foreground color for close button based on theme
        if is_close_button and current_theme == 'light':
            fg_color = "#333333"  # Set to LIGHT_THEME_FG for visibility
        else:
            fg_color = get_fg_color(current_theme) # Default theme foreground

        widget.config(bg=bg_color, fg=fg_color)

    def update_theme(self, theme_name):
        """Smoothly transitions the colors of the title bar elements."""
        target_bg_color = get_main_title_bar_color(theme_name) if self.main_window else get_popup_title_bar_color(theme_name)
        target_fg_color = get_fg_color(theme_name)

        # Transition the title bar's own background
        smooth_color_transition(self, 'bg', self.cget('bg'), target_bg_color, THEME_TRANSITION_DURATION_MS, THEME_TRANSITION_STEPS)

        # Transition title label's background and foreground
        smooth_color_transition(self.title_label, 'bg', self.title_label.cget('bg'), target_bg_color, THEME_TRANSITION_DURATION_MS, THEME_TRANSITION_STEPS)
        smooth_color_transition(self.title_label, 'fg', self.title_label.cget('fg'), target_fg_color, THEME_TRANSITION_DURATION_MS, THEME_TRANSITION_STEPS)

        # Transition icon label's background
        if self.icon_image:
            smooth_color_transition(self.icon_label, 'bg', self.icon_label.cget('bg'), target_bg_color, THEME_TRANSITION_DURATION_MS, THEME_TRANSITION_STEPS)

        # Transition control buttons frame background
        smooth_color_transition(self.control_buttons_frame, 'bg', self.control_buttons_frame.cget('bg'), target_bg_color, THEME_TRANSITION_DURATION_MS, THEME_TRANSITION_STEPS)

        # Transition control buttons background and foreground
        for btn in [self.close_button, getattr(self, 'maximize_button', None), getattr(self, 'minimize_button', None)]:
            if btn and btn.winfo_exists():
                # Re-bind hover events after transition to ensure they react to new colors
                is_close = (btn['text'] == '✕')
                btn.bind("<Enter>", functools.partial(self._on_enter_hover, btn, is_close))
                btn.bind("<Leave>", functools.partial(self._on_leave_hover, btn, is_close))
                
                # Determine target foreground for the button
                if is_close and theme_name == 'light': # If it's a close button in light theme
                    btn_target_fg = "#333333" # Set to LIGHT_THEME_FG for visibility
                elif is_close: # If it's a close button in dark theme
                    btn_target_fg = "white" # White for visibility in dark theme title bar
                else: # For other buttons
                    btn_target_fg = target_fg_color
                
                smooth_color_transition(btn, 'bg', btn.cget('bg'), target_bg_color, THEME_TRANSITION_DURATION_MS, THEME_TRANSITION_STEPS)
                smooth_color_transition(btn, 'fg', btn.cget('fg'), btn_target_fg, THEME_TRANSITION_DURATION_MS, THEME_TRANSITION_STEPS)

# Helper function to get widget target colors based on theme and type
def get_widget_target_colors(widget, theme_name, is_main_window_content=False, is_popup_window_content=False, top_level_instance=None, is_internal_popup_content=False):
    """
    Determines the target background and foreground colors for a given widget based on the theme.
    `is_internal_popup_content` is used for both pages within the single PopupHowTo window.
    """
    bg_color = None
    fg_color = None

    if is_main_window_content:
        bg_color = get_main_window_bg_color(theme_name)
        fg_color = get_fg_color(theme_name)
        if widget == top_level_instance.main_input_entry:
            # MODIFIED: These colors are now static and do not change with the popup open state
            bg_color = ENTRY_BG_DARK if theme_name == 'dark' else ENTRY_BG_LIGHT
            if top_level_instance.is_main_input_placeholder_active.get():
                fg_color = MAIN_INPUT_PLACEHOLDER_FG_DARK if theme_name == 'dark' else MAIN_INPUT_PLACEHOLDER_FG_LIGHT
            else:
                fg_color = ENTRY_FG_DARK if theme_name == 'dark' else ENTRY_FG_LIGHT
        elif widget == top_level_instance.how_to_use_button: # Specific color for how_to_use_button
            # The how_to_use_button now uses an image, so fg color is not directly visible for the button text itself.
            # However, if text were visible, this would apply. For consistency, keeping it.
            fg_color = "#00008B" if theme_name == 'light' else get_fg_color(theme_name) 
        elif widget in [top_level_instance.toggle_on_top_button, top_level_instance.toggle_chat_lock_button]:
            # Special handling for "On Top" and "Chat Lock" button text color
            # When using images, fg color of the button itself might not be visible/relevant for the image
            fg_color = get_fg_color(theme_name) 
        elif widget == top_level_instance.theme_canvas:
            # Updated to use THEME_ICON_DISPLAY_WIDTH + 10 for the theme button
            button_width = THEME_ICON_DISPLAY_WIDTH + 10
            button_height = THEME_ICON_DISPLAY_HEIGHT + 10
            fg_color = get_fg_color(theme_name) # Not directly applicable to canvas, but good for consistency
        elif widget == top_level_instance.grid_container_frame:
            # grid_container_frame's fg is implicitly inherited or not used for its own text, but can be set for consistency
            fg_color = get_fg_color(theme_name)

    elif is_popup_window_content or is_internal_popup_content: # Applies to all content within PopupHowTo
        bg_color = get_popup_window_bg_color(theme_name)
        fg_color = get_fg_color(theme_name)

        if hasattr(widget, '_item_data'):
            item_data = widget._item_data
            if "fg" in item_data: # If specific fg color is defined
                fg_color = item_data["fg"]
            elif "light_fg" in item_data and "dark_fg" in item_data: # If theme-specific fg colors are defined
                fg_color = item_data["dark_fg"] if theme_name == 'dark' else item_data["light_fg"]

        if is_popup_entry_widget(widget):
            # This logic should reflect on_popup_input_focus_out logic for disabled state
            if widget.cget('state') == 'normal' or (top_level_instance and top_level_instance.popup_input_editable):
                fg_color = POPUP_ENABLED_ENTRY_FG_DARK if theme_name == 'dark' else POPUP_ENABLED_ENTRY_FG_LIGHT
            else:
                fg_color = POPUP_DISABLED_ENTRY_FG_DARK if theme_name == 'dark' else POPUP_DISABLED_ENTRY_FG_LIGHT
            bg_color = get_popup_window_bg_color(theme_name) # Entry background always matches popup content background

    return bg_color, fg_color

def is_popup_entry_widget(widget):
    return hasattr(widget, '_is_popup_entry') and widget._is_popup_entry


# Removed PopupImages class - its functionality is merged into PopupHowTo

class PopupHowTo(tk.Toplevel):
    """Popup window providing 'How to use' information with internal sliding pages."""
    def __init__(self, parent, icon_path):
        super().__init__(parent)
        self.parent = parent
        self.icon_path = icon_path

        self.popup_title = DEFAULT_POPUP_TITLE
        self.popup_width = DEFAULT_POPUP_MIN_WIDTH
        self.popup_height = DEFAULT_POPUP_MIN_HEIGHT
        
        self.base_url = self.parent.base_url

        self.withdraw()
        self.overrideredirect(True)
        self.title(self.popup_title)
        self.set_icon()
        self.minsize(self.popup_width, self.popup_height)
        self.resizable(DEFAULT_POPUP_WIDTH_RESIZABLE, DEFAULT_POPUP_HEIGHT_RESIZABLE)
        self.attributes("-topmost", True)
        self.attributes('-alpha', 0.0) # Start fully transparent
        
        self.transient(parent) # Locks the popup to the parent window
        self.grab_set() # Makes the popup modal, disabling interaction with other windows
        self.update_idletasks() # Force update after grab_set

        # Calculate x and y coordinates for centering
        self.update_idletasks() # Ensure window dimensions are updated
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_pos = (screen_width // 2) - (self.popup_width // 2)
        y_pos = (screen_height // 2) - (self.popup_height // 2)
        self.geometry(f"{self.popup_width}x{self.popup_height}+{x_pos}+{y_pos}")

        # Initialize drag offsets for this window
        self._drag_offset_x = 0
        self._drag_offset_y = 0
        self._is_popup_dragging_active = False
        
        # Bind drag events directly to the Toplevel window
        self.bind("<ButtonPress-1>", self._start_drag_popup)
        self.bind("<B1-Motion>", self._drag_popup_window)
        self.bind("<ButtonRelease-1>", self._stop_drag_popup) # Ensure release also stops drag

        self.title_bar = CustomTitleBar(self, self.popup_title, self.icon_path, close_cmd=self.close_window, main_window=False)
        self.title_bar.pack(side="top", fill="x")

        # Main content frame that will hold the sliding page frames
        self.content_frame = tk.Frame(self, padx=10, pady=10)
        self.content_frame.pack(side="top", fill="both", expand=True)

        self.left_chamster_photo = self.load_popup_icon("RChamsterLookingRight.png", 150, 150)
        self.right_chamster_photo = self.load_popup_icon("RChamsterLookingLeft.png", 150, 150)
        # NEW: Load the clicked state for the right chamster
        self.right_chamster_clicked_photo = self.load_popup_icon("RChamsterLookingLeftClicked.png", 150, 150)
        # NEW: Load the clicked state for the left chamster on the image page
        self.left_chamster_clicked_photo = self.load_popup_icon("RChamsterLookingRightClicked.png", 150, 150)


        # Create the page frames within content_frame
        self.main_page_frame = tk.Frame(self.content_frame)
        self.image_page_frame = tk.Frame(self.content_frame)

        # Position them using place()
        self.main_page_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.image_page_frame.place(x=self.popup_width, y=0, relwidth=1, relheight=1) # Initially off-screen to the right

        self._create_main_page_content(self.main_page_frame)
        self._create_image_page_content(self.image_page_frame)

        self.popup_input_editable = False 
        self.bind("<Escape>", lambda event: self.close_window()) # Bind ESC for all popup pages
        self.deiconify()
        self.update_idletasks()
        self._set_initial_theme_colors(current_theme)
        self._fade_in()
        self.parent.main_window_buttons_state('disabled') # Disable main window buttons
        self.parent.main_window_content_draggable_mixin.unbind_drag_events()
        self.parent.title_bar.unbind_all_drag_events()
        
        self.current_page = "main" # Keep track of the current page

    def _slide_page(self, target_main_x, target_image_x, direction, callback=None):
        """Animates the sliding of pages."""
        # Ensure we capture the current width dynamically
        page_width = self.winfo_width() - 20 # Account for content_frame padding

        current_main_x = self.main_page_frame.winfo_x()
        current_image_x = self.image_page_frame.winfo_x()

        # Calculate steps for smooth animation
        total_distance = abs(target_main_x - current_main_x)
        if total_distance == 0:
            if callback: callback()
            return

        step_x = (target_main_x - current_main_x) / THEME_TRANSITION_STEPS
        
        step_time = POPUP_FADE_DURATION_MS // THEME_TRANSITION_STEPS

        def animate(step_count):
            if not self.winfo_exists(): return

            if step_count < THEME_TRANSITION_STEPS:
                new_main_x = current_main_x + (step_x * step_count)
                new_image_x = current_image_x + (step_x * step_count)

                self.main_page_frame.place(x=new_main_x, y=0, relwidth=1, relheight=1)
                self.image_page_frame.place(x=new_image_x, y=0, relwidth=1, relheight=1)
                self.after(step_time, animate, step_count + 1)
            else:
                # Ensure final position is exact
                self.main_page_frame.place(x=target_main_x, y=0, relwidth=1, relheight=1)
                self.image_page_frame.place(x=target_image_x, y=0, relwidth=1, relheight=1)
                if callback: callback()

        animate(0)


    def show_main_page(self, event=None):
        """Slides to show the main 'How to use' page."""
        self.current_page = "main"
        self._slide_page(0, self.popup_width, "right", self._enable_main_page_interaction)
        self.title_bar.title_label.config(text=DEFAULT_POPUP_TITLE)


    def show_image_page(self, event=None):
        """Slides to show the 'Chamster Images' page."""
        self.current_page = "images"
        self._slide_page(-self.popup_width, 0, "left", self._disable_main_page_interaction)
        self.title_bar.title_label.config(text=DEFAULT_POPUP_TITLE) # Set to DEFAULT_POPUP_TITLE


    def _enable_main_page_interaction(self):
        """Enables interactive elements on the main popup page."""
        self.popup_input_editable = False # Ensure it starts disabled for placeholder behavior
        self.popup_input_entry.config(state='disabled')
        self.floppy_icon_button.config(text="\U0001f5ab", state='normal')
        self.set_popup_entry_colors_based_on_state() # Apply correct colors
        self.popup_input_entry.update_idletasks()

    def _disable_main_page_interaction(self):
        """Disables interactive elements on the main popup page."""
        self.popup_input_entry.config(state='disabled')
        self.floppy_icon_button.config(state='disabled')


    def apply_smooth_theme_transition(self, old_theme, new_theme):
        if getattr(self, '_popup_transition_in_progress', False):
            return
        self._popup_transition_in_progress = True

        target_content_bg = get_popup_window_bg_color(new_theme)

        smooth_color_transition(self.content_frame, 'bg', self.content_frame.cget('bg'), target_content_bg, THEME_TRANSITION_DURATION_MS, THEME_TRANSITION_STEPS)
        self.title_bar.update_theme(new_theme)

        # Recursively transition content for both pages
        def _recursively_transition_widgets(parent_widget, old_theme_for_start, new_theme_for_target):
            if not parent_widget.winfo_exists():
                return
            
            # Use is_internal_popup_content=True to ensure correct color fetching for sub-widgets
            current_theme_bg, current_theme_fg = get_widget_target_colors(parent_widget, old_theme_for_start, is_internal_popup_content=True)
            target_bg, target_fg = get_widget_target_colors(parent_widget, new_theme_for_target, is_internal_popup_content=True)

            if current_theme_bg != target_bg and target_bg is not None:
                smooth_color_transition(parent_widget, 'bg', current_theme_bg, target_bg, THEME_TRANSITION_DURATION_MS, THEME_TRANSITION_STEPS)
            
            if 'fg' in parent_widget.config():
                if current_theme_fg != target_fg and target_fg is not None:
                    smooth_color_transition(parent_widget, 'fg', current_theme_fg, target_fg, THEME_TRANSITION_DURATION_MS, THEME_TRANSITION_STEPS)

            # Special handling for Entry widgets to update disabled colors directly
            if isinstance(parent_widget, tk.Entry) and hasattr(parent_widget, '_is_popup_entry') and parent_widget._is_popup_entry:
                if new_theme == 'dark':
                    parent_widget.config(disabledbackground=get_popup_window_bg_color('dark'), disabledforeground=POPUP_DISABLED_ENTRY_FG_DARK)
                else:
                    parent_widget.config(disabledbackground=get_popup_window_bg_color('light'), disabledforeground=POPUP_DISABLED_ENTRY_FG_LIGHT)
            
            for child in parent_widget.winfo_children():
                _recursively_transition_widgets(child, old_theme_for_start, new_theme_for_target)
        
        _recursively_transition_widgets(self.main_page_frame, old_theme, new_theme)
        _recursively_transition_widgets(self.image_page_frame, old_theme, new_theme)


        def finalize_popup_theme():
            if hasattr(self, 'popup_input_entry'):
                self.on_popup_input_focus_out(None) 
            setattr(self, '_popup_transition_in_progress', False)

        self.after(THEME_TRANSITION_DURATION_MS + 50, finalize_popup_theme)


    def _start_drag_popup(self, event):
        if 0 <= event.x <= self.winfo_width() and 0 <= event.y <= self.winfo_height():
            self._drag_offset_x = event.x_root - self.winfo_x()
            self._drag_offset_y = event.y_root - self.winfo_y()
            self._is_popup_dragging_active = True
        else:
            self._is_popup_dragging_active = False
            self._drag_offset_x = 0
            self._drag_offset_y = 0
            
    def _drag_popup_window(self, event):
        if not hasattr(self, '_is_popup_dragging_active') or not self._is_popup_dragging_active:
            return

        x = event.x_root - self._drag_offset_x
        y = event.y_root - self._drag_offset_y
        self.geometry(f"+{x}+{y}")

    def _stop_drag_popup(self, event):
        self._is_popup_dragging_active = False


    def _fade_in(self):
        current_alpha = self.attributes('-alpha')
        target_alpha = 1.0
        alpha_step = (target_alpha - current_alpha) / POPUP_FADE_STEPS
        
        if current_alpha < target_alpha:
            new_alpha = current_alpha + alpha_step
            if new_alpha > target_alpha:
                new_alpha = target_alpha
            self.attributes('-alpha', new_alpha)
            self.after(POPUP_FADE_DURATION_MS // POPUP_FADE_STEPS, self._fade_in)
        else:
            self.attributes('-alpha', target_alpha)

    def _set_initial_theme_colors(self, theme_name):
        # Set background for the content frame
        self.content_frame.config(bg=get_popup_window_bg_color(theme_name))
        self.title_bar.update_theme(theme_name)

        # Apply colors recursively to both page frames
        def _apply_initial_recursive(widget):
            if not widget.winfo_exists(): return
            target_bg, target_fg = get_widget_target_colors(widget, theme_name, is_internal_popup_content=True)
            try:
                if 'bg' in widget.config(): widget.config(bg=target_bg)
                if 'fg' in widget.config() and target_fg is not None:
                    widget.config(fg=target_fg)
                if isinstance(widget, tk.Entry) and hasattr(widget, '_is_popup_entry') and widget._is_popup_entry:
                    if theme_name == 'dark':
                        widget.config(disabledbackground=get_popup_window_bg_color('dark'), disabledforeground=POPUP_DISABLED_ENTRY_FG_DARK)
                    else:
                        widget.config(disabledbackground=get_popup_window_bg_color('light'), disabledforeground=POPUP_DISABLED_ENTRY_FG_LIGHT)
            except tk.TclError: pass
            for child in widget.winfo_children():
                _apply_initial_recursive(child)

        _apply_initial_recursive(self.main_page_frame)
        _apply_initial_recursive(self.image_page_frame)

        # Special handling for initial floppy button color setting (was separated)
        self.floppy_icon_button.config(bg=get_popup_window_bg_color(current_theme), fg=get_fg_color(current_theme))

        # Update the right chamster button's background to ensure it matches the popup background
        # and doesn't have any default button styling for its background.
        if hasattr(self, 'right_chamster_button') and self.right_chamster_button.winfo_exists():
            self.right_chamster_button.config(bg=get_popup_window_bg_color(theme_name))
        
        # Update the left chamster button's background on image page
        if hasattr(self, 'left_chamster_button_image_page') and self.left_chamster_button_image_page.winfo_exists():
            self.left_chamster_button_image_page.config(bg=get_popup_window_bg_color(theme_name))


    def set_icon(self):
        try:
            self.icon_photo = PhotoImage(file=self.icon_path)
            self.wm_iconphoto(True, self.icon_photo)
        except Exception as ex:
            pass

    def load_popup_icon(self, icon_filename, target_width, target_height):
        icon_path_full = os.path.join(POPUP_PIXEL_ICONS_DIR, icon_filename)
        if not os.path.exists(icon_path_full):
            return None
        try:
            original_image = PhotoImage(file=icon_path_full)
            x_factor = max(1, original_image.width() // target_width)
            y_factor = max(1, original_image.height() // target_height)
            return original_image.subsample(x_factor, y_factor)
        except Exception as ex:
            return None

    def close_window(self):
        # MODIFIED: Removed conditional page slide, now always closes directly
        self._perform_close_operations()

    def _perform_close_operations(self):
        """Actual close operations after any necessary page transitions."""
        self.grab_release()
        self.parent.main_window_buttons_state('normal')
        self.parent.after(100, self.parent.main_window_content_draggable_mixin.bind_drag_events)
        self.parent.after(100, self.parent.title_bar.bind_all_drag_events)
        if hasattr(self.parent, 'popup_window') and self.parent.popup_window is self:
            self.parent.popup_window = None
        
        self.parent.keep_focus_active = self.parent.chat_lock_state.get()

        self.parent.lift()
        self.parent.focus_set()
        self.parent.main_input_entry.focus_set()
        self.parent.focus_set()

        self.destroy()

    def _create_main_page_content(self, parent_frame):
        """Creates all widgets for the main 'How to use' page within the given frame."""
        parent_frame.grid_columnconfigure(0, weight=0) # Left image
        parent_frame.grid_columnconfigure(1, weight=1) # Center content
        parent_frame.grid_columnconfigure(2, weight=0) # Right image
        parent_frame.grid_rowconfigure(0, weight=1)
        parent_frame.grid_rowconfigure(1, weight=0)
        parent_frame.grid_rowconfigure(2, weight=0)

        popup_content_bg = get_popup_window_bg_color(current_theme)
        parent_frame.config(bg=popup_content_bg) # Set background for the main page frame itself

        if self.left_chamster_photo:
            # This is the left chamster on the MAIN page. It's still a label.
            self.left_image_label = tk.Label(parent_frame, image=self.left_chamster_photo, bg=popup_content_bg)
            self.left_image_label.grid(row=0, column=0, rowspan=3, sticky="sw", padx=(0, 1), pady=(0, 10)) 
        
        self.center_content_frame = tk.Frame(parent_frame, bg=popup_content_bg)
        self.center_content_frame.grid(row=0, column=1, sticky="nsew")

        title_label_data = {"text": "This app puts the CODE after:", "font_size": 12, "font_style": "normal", "padx": 20, "light_fg": LIGHT_THEME_FG, "dark_fg": DARK_THEME_FG}
        title_label = tk.Label(self.center_content_frame, text=title_label_data["text"], font=(POPUP_EIGHT_BIT_FONT_FAMILY, title_label_data["font_size"], title_label_data["font_style"]), justify='center', bg=popup_content_bg)
        title_label._item_data = title_label_data
        title_label.config(fg=get_widget_target_colors(title_label, current_theme, is_internal_popup_content=True)[1])
        title_label.pack(pady=(0, 5), fill="x", padx=title_label_data["padx"])
        
        input_frame = tk.Frame(self.center_content_frame, bd=0, relief="flat", highlightthickness=0, bg=popup_content_bg)
        input_frame.pack(pady=5, expand=True, anchor="center")

        initial_popup_fg_color = POPUP_DISABLED_ENTRY_FG_DARK if current_theme == 'dark' else POPUP_DISABLED_ENTRY_FG_LIGHT
        
        self.popup_input_entry = tk.Entry(input_frame, width=40, bd=2, relief="flat", font=(POPUP_EIGHT_BIT_FONT_FAMILY, 10), justify='center',
                                          bg=get_popup_window_bg_color(current_theme),
                                          fg=initial_popup_fg_color,
                                          disabledbackground=get_popup_window_bg_color(current_theme),
                                          disabledforeground=initial_popup_fg_color
                                         )
        self.popup_input_entry.insert(0, self.base_url)
        self.popup_input_entry._is_popup_entry = True 
        self.popup_input_entry.config(state='disabled') 
        self.popup_input_entry.pack(side="left", padx=5, pady=2)
        self.popup_input_entry.bind("<Return>", self.save_popup_url)
        self.popup_input_entry.bind("<FocusIn>", self.on_popup_input_focus_in)
        self.popup_input_entry.bind("<FocusOut>", self.on_popup_input_focus_out)

        self.floppy_icon_button = tk.Button(input_frame, text="\U0001f5ab", command=self.toggle_popup_input_edit, font=("Arial", 12), bd=2, relief="raised", padx=5, pady=2)
        self.floppy_icon_button.pack(side="left", padx=(5, 2), pady=2)
        self.floppy_icon_button.config(bg=get_popup_window_bg_color(current_theme))
        self.floppy_icon_button.bind("<Enter>", functools.partial(self._on_enter_hover_popup_button, self.floppy_icon_button))
        self.floppy_icon_button.bind("<Leave>", functools.partial(self._on_leave_hover_popup_button, self.floppy_icon_button))

        link_info_label_data = {"text": "After pressing Enter, full link is opened in your browser", "font_size": 12, "font_style": "normal", "light_fg": LIGHT_THEME_FG, "dark_fg": "white"}
        link_info_label = tk.Label(self.center_content_frame, text=link_info_label_data["text"], font=(POPUP_EIGHT_BIT_FONT_FAMILY, link_info_label_data["font_size"], link_info_label_data["font_style"]), justify='center', bg=popup_content_bg)
        link_info_label._item_data = link_info_label_data
        link_info_label.config(fg=get_widget_target_colors(link_info_label, current_theme, is_internal_popup_content=True)[1])
        link_info_label.pack(pady=5, fill="x")

        info_lines_data = [
            {"text": "THIS APP DOES NOT AUTO CLAIM", "fg": "red", "font_size": 12, "font_style": "bold"},
            {"text": "You must be signed in and manually claim", "fg": "red", "font_size": 14, "font_style": "bold"},
            {"text": "Sometimes the promocode might take a few refreshes to show up for you", "font_size": 12, "light_fg": LIGHT_THEME_FG, "dark_fg": "white"},
            {"text": "This is not an app Issue/Bug", "fg": "red", "font_size": 12, "font_style": "italic"},
            {"text": "No responsibility is taken if the claim popup did not show up for you", "fg": "red", "font_style": "italic", "font_size": 12},
        ]
        info_lines_frame = tk.Frame(self.center_content_frame, bg=popup_content_bg)
        info_lines_frame.pack(fill="both", expand=True, pady=5) 
        for item in info_lines_data:
            label = tk.Label(info_lines_frame, text=item["text"], font=(POPUP_EIGHT_BIT_FONT_FAMILY, item.get("font_size", 10), item.get("font_style", "normal")), justify='center', bg=popup_content_bg)
            label._item_data = item
            label.pack(fill="both", expand=True)
            label.lift()
        
        # MODIFIED: Replaced tk.Label with tk.Button for the right chamster image
        if self.right_chamster_photo:
            self.right_chamster_button = tk.Button(
                parent_frame,
                image=self.right_chamster_photo,
                bg=popup_content_bg,
                command=self._on_click_right_chamster, # Make the button clickable
                bd=0, # No border
                relief="flat", # No relief
                highlightthickness=0, # No highlight border
                compound="center", # Center the image within the button
                # Set default width/height of the button to match the image size
                width=RIGHT_CHAMSTER_BUTTON_WIDTH_DEFAULT,
                height=RIGHT_CHAMSTER_BUTTON_HEIGHT_DEFAULT
            )
            # Use the new configurable padding and position
            self.right_chamster_button.grid(
                row=0, column=2, rowspan=3, sticky="se",
                padx=RIGHT_CHAMSTER_BUTTON_PADX_DEFAULT,
                pady=RIGHT_CHAMSTER_BUTTON_PADY_DEFAULT
            )
            # Bind hover events to change the image, but NOT the background.
            self.right_chamster_button.bind("<Enter>", self._on_enter_right_chamster)
            self.right_chamster_button.bind("<Leave>", self._on_leave_right_chamster)
            self.right_chamster_button.config(cursor="") # Ensure no hand cursor

        footer_label1_data = {"text": "To be used for Rollercoin Promocodes", "font_size": 8, "font_style": "italic"}
        self.footer_label1 = tk.Label(parent_frame, text=footer_label1_data["text"], font=(POPUP_EIGHT_BIT_FONT_FAMILY, footer_label1_data["font_size"], footer_label1_data["font_style"]), justify="center", bg=popup_content_bg)
        self.footer_label1._item_data = footer_label1_data
        self.footer_label1.config(fg=get_widget_target_colors(self.footer_label1, current_theme, is_internal_popup_content=True)[1])
        self.footer_label1.grid(row=1, column=0, columnspan=3, rowspan=3,  sticky="ew", padx=(700, 0), pady=(0,25))
        
        footer_label2_data = {"text": "made by 00", "fg": "gray", "font_size": 7, "font_style": "italic"}
        self.footer_label2 = tk.Label(parent_frame, text=footer_label2_data["text"], font=(POPUP_EIGHT_BIT_FONT_FAMILY, footer_label2_data["font_size"], footer_label2_data["font_style"]), justify="center", bg=popup_content_bg)
        self.footer_label2._item_data = footer_label2_data
        self.footer_label2.config(fg=get_widget_target_colors(self.footer_label2, current_theme, is_internal_popup_content=True)[1])
        self.footer_label2.grid(row=2, column=0, rowspan=3, columnspan=3, sticky="ew", padx=(750, 0), pady=(0,5))

    def _create_image_page_content(self, parent_frame):
        """Creates all widgets for the 'How to use (Information)' page within the given frame."""
        popup_content_bg = get_popup_window_bg_color(current_theme)
        parent_frame.config(bg=popup_content_bg)

        # MODIFIED: Changed left_chamster_back_label from Label to Button
        if self.left_chamster_photo:
            self.left_chamster_button_image_page = tk.Button(
                parent_frame,
                image=self.left_chamster_photo,
                bg=popup_content_bg,
                command=self.show_main_page, # Still goes back to main page on click
                bd=0,
                relief="flat",
                highlightthickness=0,
                compound="center",
                width=LEFT_CHAMSTER_BUTTON_WIDTH_DEFAULT,
                height=LEFT_CHAMSTER_BUTTON_HEIGHT_DEFAULT
            )
            # Using pack to stick to bottom-left with configurable padding
            self.left_chamster_button_image_page.pack(
                side="left", anchor="sw",
                padx=LEFT_CHAMSTER_BUTTON_PADX_DEFAULT,
                pady=LEFT_CHAMSTER_BUTTON_PADY_DEFAULT
            )
            # NEW: Bind hover events for the left chamster button on the image page
            self.left_chamster_button_image_page.bind("<Enter>", self._on_enter_left_chamster)
            self.left_chamster_button_image_page.bind("<Leave>", self._on_leave_left_chamster)
            self.left_chamster_button_image_page.config(cursor="") # Remove hand cursor, button handles it


        if self.right_chamster_photo:
            self.right_chamster_deco_label = tk.Label(parent_frame, image=self.right_chamster_photo, bg=popup_content_bg)
            # Using pack to stick to bottom-right
            self.right_chamster_deco_label.pack(side="right", anchor="se", padx=10, pady=10)
            self.right_chamster_deco_label.config(cursor="") # Remove hand cursor

        # Main frame to hold all central content
        main_content_frame = tk.Frame(parent_frame, bg=popup_content_bg)
        # Pack to fill the remaining space horizontally and vertically, centering itself
        main_content_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Configure columns for centering content inside main_content_frame
        main_content_frame.grid_columnconfigure(0, weight=1) # Left spacer
        main_content_frame.grid_columnconfigure(1, weight=0) # Content column (will hold content_wrapper_frame)
        main_content_frame.grid_columnconfigure(2, weight=1) # Right spacer
        main_content_frame.grid_rowconfigure(0, weight=1) # Top spacer for vertical centering
        main_content_frame.grid_rowconfigure(1, weight=0) # Content row
        main_content_frame.grid_rowconfigure(2, weight=1) # Bottom spacer for vertical centering

        # Frame to hold the actual icon-text rows
        content_wrapper_frame = tk.Frame(main_content_frame, bg=popup_content_bg)
        # Place in the center of main_content_frame's grid
        content_wrapper_frame.grid(row=1, column=1) 

        # Helper to create an icon-text row
        def create_icon_text_row(parent_widget, icon_image, text_content, icon_padx=(0, 5), text_padx=(5, 10)): # Modified default padx here
            row_frame = tk.Frame(parent_widget, bg=parent_widget.cget("bg"))
            row_frame.pack(pady=5)

            # Ensure column 0 and 3 are always present and act as flexible spacers
            row_frame.grid_columnconfigure(0, weight=1) # Left spacer
            row_frame.grid_columnconfigure(1, weight=0) # Icon column
            row_frame.grid_columnconfigure(2, weight=0) # Text column
            row_frame.grid_columnconfigure(3, weight=1) # Right spacer
            row_frame.grid_rowconfigure(0, weight=1)

            if icon_image:
                icon_label = tk.Label(row_frame, image=icon_image, bg=row_frame.cget("bg"))
                # Sticking the icon to the east of its column (column 1)
                icon_label.grid(row=0, column=1, padx=icon_padx, sticky="e") 
            
            text_label = tk.Label(row_frame, text=text_content, 
                                 font=(POPUP_EIGHT_BIT_FONT_FAMILY, POPUP_DEFAULT_TEXT_FONT_SIZE), 
                                 bg=row_frame.cget("bg"), wraplength=450, 
                                 justify=tk.LEFT)
            # Sticking the text to the west of its column (column 2)
            text_label.grid(row=0, column=2, padx=text_padx, sticky="w") 

            text_label.config(fg=get_fg_color(current_theme))

        # Add icon-text rows, now passing specific padx values
        create_icon_text_row(content_wrapper_frame, self.parent.on_top_icon_locked,
                             "Toggling this icon puts the whole app constantly on top or disables it", icon_padx=(0, 5), text_padx=(5, 10)) # Adjusted padx for consistency
        
        create_icon_text_row(content_wrapper_frame, self.parent.chat_lock_icon_off_photo,
                             "Toggling this icon forces the input box to constantly be active and be able to type in it", icon_padx=(0, 5), text_padx=(5, 10)) # Adjusted padx for consistency
        
        # MODIFIED: Use rc_popup_window_icon for the popup explanation
        create_icon_text_row(content_wrapper_frame, self.parent.rc_popup_window_icon, 
                             "This icon opens the popup window, where you can change the url of the promocode", icon_padx=(0, 5), text_padx=(5, 10)) # Adjusted padx for consistency
        
        # To align this with the above, ensure its icon_padx and text_padx are consistent with the new default or explicitly set.
        # The default for create_icon_text_row is now (0,5) for icon_padx and (5,10) for text_padx, which should ensure alignment.
        create_icon_text_row(content_wrapper_frame, self.parent.sun_photo_image,
                             "This icon cycles between light/dark mode and changes the theme of the app accordingly. By Default, the app is in dark mode",
                             icon_padx=(0, 5), text_padx=(5, 10)) # Explicitly set to match for guaranteed alignment


        # .ini file text - centered below the icon-text rows
        ini_file_text_label = tk.Label(content_wrapper_frame, 
                                       text=".ini file is created in your OS documents folder. If you wish,\n you can change base url an other settings from there too", 
                                       font=(POPUP_EIGHT_BIT_FONT_FAMILY, POPUP_DEFAULT_TEXT_FONT_SIZE), 
                                       bg=popup_content_bg, wraplength=600, justify=tk.CENTER)
        ini_file_text_label.pack(pady=10, fill="x", expand=True)
        ini_file_text_label.config(fg=get_fg_color(current_theme))


    def _on_enter_hover_popup_image(self, widget, event):
        # This function is used by the left chamster image on the image page.
        # It still allows background highlighting for that specific widget.
        hover_color = DARK_BUTTON_HOVER_COLOR if current_theme == 'dark' else BUTTON_HOVER_COLOR
        widget.config(bg=hover_color)

    def _on_leave_hover_popup_image(self, widget, event):
        # This function is used by the left chamster image on the image page.
        # It still allows background highlighting for that specific widget.
        widget.config(bg=get_popup_window_bg_color(current_theme))

    # NEW: Specific hover handlers for the right chamster on the main popup page (image change only)
    def _on_enter_right_chamster(self, event):
        """Changes the right chamster image to its 'clicked' state on hover."""
        if self.right_chamster_clicked_photo:
            self.right_chamster_button.config(image=self.right_chamster_clicked_photo)

    def _on_leave_right_chamster(self, event):
        """Changes the right chamster image back to its normal state when hover ends."""
        if self.right_chamster_photo:
            self.right_chamster_button.config(image=self.right_chamster_photo)

    def _on_click_right_chamster(self): # MODIFIED: Removed 'event' parameter
        # Ensure the clicked image is shown instantly (if not already from hover)
        if self.right_chamster_clicked_photo:
            self.right_chamster_button.config(image=self.right_chamster_clicked_photo)
        self.show_image_page()

    # NEW: Specific hover handlers for the left chamster on the image page (image change only)
    def _on_enter_left_chamster(self, event):
        """Changes the left chamster image to its 'clicked' state on hover on the image page."""
        if self.left_chamster_clicked_photo:
            self.left_chamster_button_image_page.config(image=self.left_chamster_clicked_photo)

    def _on_leave_left_chamster(self, event):
        """Changes the left chamster image back to its normal state when hover ends on the image page."""
        if self.left_chamster_photo:
            self.left_chamster_button_image_page.config(image=self.left_chamster_photo)


    def _on_enter_hover_popup_button(self, widget, event):
        hover_color = DARK_BUTTON_HOVER_COLOR if current_theme == 'dark' else BUTTON_HOVER_COLOR
        widget.config(bg=hover_color)

    def _on_leave_hover_popup_button(self, widget, event):
        widget.config(bg=get_popup_window_bg_color(current_theme))

    def save_popup_url(self, event=None):
        new_base_url = self.popup_input_entry.get().strip()

        if new_base_url != self.base_url:
            self.base_url = new_base_url
            self.parent.base_url = self.base_url

        self.popup_input_entry.config(state='disabled')
        self.popup_input_editable = False
        self.floppy_icon_button.config(text="\U0001f5ab")
        self.set_popup_entry_colors_based_on_state()
        self.popup_input_entry.update_idletasks()

    def set_popup_entry_colors_based_on_state(self):
        if not hasattr(self, 'popup_input_entry') or not self.popup_input_entry.winfo_exists():
            return

        current_theme_bg = get_popup_window_bg_color(current_theme)
        if self.popup_input_editable:
            fg_color = POPUP_ENABLED_ENTRY_FG_DARK if current_theme == 'dark' else POPUP_ENABLED_ENTRY_FG_LIGHT
            self.popup_input_entry.config(fg=fg_color, bg=current_theme_bg)
            self.popup_input_entry.config(disabledforeground=fg_color, disabledbackground=current_theme_bg) 
        else:
            fg_color = POPUP_DISABLED_ENTRY_FG_DARK if current_theme == 'dark' else POPUP_DISABLED_ENTRY_FG_LIGHT
            self.popup_input_entry.config(fg=fg_color, bg=current_theme_bg,
                                          disabledforeground=fg_color, disabledbackground=current_theme_bg)

    def toggle_popup_input_edit(self):
        if not self.popup_input_editable:
            self.popup_input_editable = True
            self.popup_input_entry.config(state='normal')
            self.popup_input_entry.update_idletasks()
            self.set_popup_entry_colors_based_on_state()
            
            self.popup_input_entry.focus_set()
            self.popup_input_entry.selection_range(0, tk.END)

            self.floppy_icon_button.config(text="✓")
            self.popup_input_entry.update_idletasks() 
        else:
            self.save_popup_url()


    def on_popup_input_focus_in(self, event):
        target_fg = POPUP_ENABLED_ENTRY_FG_DARK if current_theme == 'dark' else POPUP_ENABLED_ENTRY_FG_LIGHT
        self.popup_input_entry.config(fg=target_fg)


    def on_popup_input_focus_out(self, event):
        if not hasattr(self, 'popup_input_entry') or not self.popup_input_entry.winfo_exists():
            return

        if not self.popup_input_entry.get().strip():
            self.popup_input_entry.delete(0, tk.END)
            self.main_input_entry.config(fg=MAIN_INPUT_PLACEHOLDER_FG_DARK if current_theme == 'dark' else MAIN_INPUT_PLACEHOLDER_FG_LIGHT)
            self.popup_input_entry.insert(0, self.base_url)

        if not self.popup_input_editable:
            self.popup_input_entry.config(state='disabled')
            self.set_popup_entry_colors_based_on_state()


# Placed before get_widget_target_colors
class MainWindow(tk.Toplevel):
    """Main application window for Rollercoin Promo Launcher."""
    def __init__(self, parent, icon_path): # Removed config_data from init
        super().__init__(parent)
        self.parent = parent
        self.icon_path = icon_path

        self.main_title = DEFAULT_MAIN_TITLE
        self.min_width = DEFAULT_MIN_WIDTH
        self.min_height = DEFAULT_MIN_HEIGHT
        
        # MODIFIED: Initialize base_url with DEFAULT_BASE_URL
        self.base_url = DEFAULT_BASE_URL 
        
        # Initialize popup_window to None
        self.popup_window = None 

        global current_theme
        current_theme = 'dark' # Default to dark theme for demonstration based on user's query

        self.withdraw()
        self.overrideredirect(True)
        self.title(self.main_title)
        self.set_icon()
        self.minsize(self.min_width, self.min_height)
        self.resizable(DEFAULT_WIDTH_RESIZABLE, DEFAULT_HEIGHT_RESIZABLE)
        
        self.attributes("-topmost", True)
        self.attributes('-alpha', 0.0) # Start fully transparent for fade-in
        self.on_top_state = tk.BooleanVar(value=True)
        self.is_main_input_placeholder_active = tk.BooleanVar(value=True)
        
        # NEW: Chat Lock state variable, defaulted to True (locked)
        self.chat_lock_state = tk.BooleanVar(value=False) # Default to True (keep focus active)
        self.keep_focus_active = self.chat_lock_state.get() # Initialize based on chat_lock_state
        self._keep_foreground_loop()  # Start the focus loop

        # Initialize just_submitted_main_input to False
        self.just_submitted_main_input = False 

        # --- FIX: Simplified state management for maximize ---
        self.is_maximized = False
        self._previous_geometry = None

        self.update_idletasks()
        x_pos = (self.winfo_screenwidth() // 2) - (self.min_width // 2)
        y_pos = (self.winfo_screenheight() // 2) - (self.min_height // 2)
        self.geometry(f"{self.min_width}x{self.min_height}+{x_pos}+{y_pos}")
        self._previous_geometry = self.geometry()

        self.title_bar = CustomTitleBar(self, self.main_title, self.icon_path, self.minimize_window, self.toggle_maximize, self.close_window, main_window=True)
        self.title_bar.pack(side="top", fill="x")

        self.content_frame = tk.Frame(self, padx=10, pady=10)
        self.content_frame.pack(side="top", fill="both", expand=True)
        # MODIFIED: Store DraggableWindowMixin instance and bind later
        self.main_window_content_draggable_mixin = DraggableWindowMixin(self.content_frame, self) 
        self.main_window_content_draggable_mixin.bind_drag_events() # Bind initially for main window

        self.grid_container_frame = tk.Frame(self.content_frame)
        self.grid_container_frame.pack(fill="both", expand=True)
        # MODIFIED: Adjust column weights for the new button order
        # Column 0: On Top Button (weight 0)
        # Column 1: Chat Lock Button (weight 0)
        # Column 2: Main Input (weight 1, expands)
        # Column 3: How to Use Button (weight 0)
        # Column 4: Theme Canvas (weight 0)
        self.grid_container_frame.columnconfigure(0, weight=0) # On Top button
        self.grid_container_frame.columnconfigure(1, weight=0) # Chat Lock button
        self.grid_container_frame.columnconfigure(2, weight=1) # Main input column
        self.grid_container_frame.columnconfigure(3, weight=0) # How to Use button column
        self.grid_container_frame.columnconfigure(4, weight=0) # Theme button column

        self.grid_container_frame.rowconfigure(0, weight=1)

        # Load the new icons for the "On Top" button
        self.on_top_icon_locked = self.load_pixel_icon("RClocked.png", THEME_ICON_DISPLAY_WIDTH, THEME_ICON_DISPLAY_HEIGHT)
        self.on_top_icon_unlocked = self.load_pixel_icon("RCUnlock.png", THEME_ICON_DISPLAY_WIDTH, THEME_ICON_DISPLAY_HEIGHT)
        
        # Load all chat lock icons (only dark theme versions now) and store them as PhotoImage objects
        self.chat_lock_icon_on_photo = self.load_pixel_icon("RCDarkUnlock.png", THEME_ICON_DISPLAY_WIDTH, THEME_ICON_DISPLAY_HEIGHT)
        self.chat_lock_icon_off_photo = self.load_pixel_icon("RCDarkLock.png", THEME_ICON_DISPLAY_WIDTH, THEME_ICON_DISPLAY_HEIGHT)

        # Load icon for the main app (used in popup for explanation)
        self.app_icon_for_popup = self.load_pixel_icon("rcicon.png", ICON_SIZE_WIDTH * 2, ICON_SIZE_HEIGHT * 2) # Slightly larger for clarity in popup

        # NEW: Load popup window toggle icon
        self.rc_popup_window_icon = self.load_pixel_icon("RCPopupWindow.png", ICON_SIZE_WIDTH * 2, ICON_SIZE_HEIGHT * 2) # Adjust size if needed


        # MODIFIED: Placed On Top button in column 0
        self.toggle_on_top_button = tk.Button(
            self.grid_container_frame,
            command=self.toggle_on_top,
            bd=2,
            relief="raised",
            width=THEME_ICON_DISPLAY_WIDTH + 10, # Give some extra width for padding
            height=THEME_ICON_DISPLAY_HEIGHT + 10, # Give some extra height for padding
            compound="center" # To center the image if needed, though only image will be used
        )
        self.toggle_on_top_button.grid(row=0, column=0, padx=(10, DEFAULT_ON_TOP_BUTTON_GAP), pady=5, sticky="nw")
        self.update_on_top_button_icon() # Call the new update function
        self.bind_content_button_hover(self.toggle_on_top_button) # Ensure hover is bound

        # NEW: Chat Lock Toggle Button - now in column 1
        self.toggle_chat_lock_button = tk.Button(
            self.grid_container_frame,
            command=self.toggle_chat_lock,
            bd=2,
            relief="raised",
            width=THEME_ICON_DISPLAY_WIDTH + 10,
            height=THEME_ICON_DISPLAY_HEIGHT + 10,
            compound="center"
        )
        self.toggle_chat_lock_button.grid(row=0, column=1, padx=(0, DEFAULT_ON_TOP_BUTTON_GAP), pady=5, sticky="nw")
        self.update_chat_lock_button_icon() # Set initial icon for chat lock button
        # BINDING MOVED TO _set_initial_theme_colors
        # self.bind_content_button_hover(self.toggle_chat_lock_button) # Bind hover events


        self.main_input_entry = tk.Entry(
            self.grid_container_frame,
            width=40,
            bd=2,
            relief="sunken",
            borderwidth=5,
            # MODIFIED: Apply 8-bit font to the main input entry
            font=(DEFAULT_MAIN_INPUT_FONT_FONT, DEFAULT_MAIN_INPUT_FONT_SIZE),
            justify='center',
            bg=ENTRY_BG_LIGHT,
            # Set initial disabled background and foreground to match the enabled state
            disabledbackground=ENTRY_BG_LIGHT,
            disabledforeground=MAIN_INPUT_PLACEHOLDER_FG_LIGHT # Match initial placeholder fg
        )
        # Set initial text and foreground color for the placeholder
        self.main_input_entry.insert(0, DEFAULT_MAIN_INPUT_PLACEHOLDER)
        # MODIFIED: Set placeholder foreground dynamically based on theme
        self.main_input_entry.config(fg=MAIN_INPUT_PLACEHOLDER_FG_DARK if current_theme == 'dark' else MAIN_INPUT_PLACEHOLDER_FG_LIGHT) 
        # MODIFIED: Moved to column 2
        self.main_input_entry.grid(row=0, column=2, padx=5, pady=5, sticky="new")
        self.main_input_entry.bind("<FocusIn>", self.on_main_input_focus_in)
        self.main_input_entry.bind("<FocusOut>", self.on_main_input_focus_out)
        self.main_input_entry.bind("<Return>", self.open_main_url)
        # NEW: Bind <Button-1> to ensure explicit focus and editability on click
        self.main_input_entry.bind("<Button-1>", self.on_main_input_click) 
        
        # MODIFIED: Use new icon for how_to_use_button
        self.how_to_use_button = tk.Button(self.grid_container_frame, image=self.rc_popup_window_icon, command=self.open_how_to_use_popup, 
                                           bd=2, relief="raised", compound="center", 
                                           width=THEME_ICON_DISPLAY_WIDTH + 10, # Match icon button size
                                           height=THEME_ICON_DISPLAY_HEIGHT + 10) # Match icon button size
        # MODIFIED: Adjusted column for how_to_use_button to 3
        self.how_to_use_button.grid(row=0, column=3, padx=(5, 5), pady=5, sticky="ne")
        # Set initial background color for the how_to_use_button
        self.how_to_use_button.config(bg=get_main_window_bg_color(current_theme))
        self.bind_content_button_hover(self.how_to_use_button)

        # CHANGED: theme_canvas width and height to match the popup button
        self.theme_canvas = tk.Canvas(
            self.grid_container_frame,
            width=THEME_ICON_DISPLAY_WIDTH + 10,
            height=THEME_ICON_DISPLAY_HEIGHT + 10,
            bd=2, relief="raised", highlightthickness=0
        )
        # MODIFIED: Adjusted column for theme_canvas to 4
        self.theme_canvas.grid(row=0, column=4, padx=(5, 10), pady=5, sticky="ne")
        self.theme_canvas.update_idletasks()

        self.sun_photo_image = self.load_pixel_icon("RCPixelSun.png", THEME_ICON_DISPLAY_WIDTH, THEME_ICON_DISPLAY_HEIGHT)
        self.moon_photo_image = self.load_pixel_icon("RCPixelMoon.png", THEME_ICON_DISPLAY_WIDTH, THEME_ICON_DISPLAY_HEIGHT)
        
        # CHANGED: Icon coordinates to be centered within the new canvas dimensions
        center_x = (THEME_ICON_DISPLAY_WIDTH + 10) / 2
        center_y = (THEME_ICON_DISPLAY_HEIGHT + 10) / 2
        self.sun_icon_item = self.theme_canvas.create_image(center_x, center_y, image=self.sun_photo_image, state='hidden', anchor=tk.CENTER)
        self.moon_icon_item = self.theme_canvas.create_image(center_x, center_y, image=self.moon_photo_image, state='hidden', anchor=tk.CENTER)
        
        self.theme_canvas.bind("<Button-1>", self.toggle_theme)
        self.bind_content_button_hover(self.theme_canvas)
        
        # Bind Escape to main window's specific handler
        self.bind("<Escape>", self._on_main_window_escape)
        self.bind("<Button-1>", self.on_window_click)

        self.deiconify()
        self.after(50, self._initial_icon_display)
        self._set_initial_theme_colors(current_theme)
        self._fade_in() # Start fade-in animation for main window

    def _keep_foreground_loop(self):
        # The loop should only be active if chat_lock_state is true AND no popup is open.
        if self.keep_focus_active and (self.popup_window is None or not self.popup_window.winfo_exists()):
            try:
                self.lift()
                self.focus_force()
                self.main_input_entry.focus_set()
            except:
                pass
        self.after(1000, self._keep_foreground_loop)


    def main_window_buttons_state(self, state):
        """Enables or disables main window interactive elements."""
        for widget in [self.toggle_on_top_button, self.toggle_chat_lock_button, self.main_input_entry, self.how_to_use_button, self.theme_canvas]:
            if isinstance(widget, (tk.Button, tk.Entry)):
                widget.config(state=state)
                # Specific handling for main_input_entry's disabled colors
                if widget == self.main_input_entry:
                    if state == 'disabled':
                        # Set disabled colors based on the current theme
                        disabled_bg = ENTRY_BG_DARK if current_theme == 'dark' else ENTRY_BG_LIGHT
                        disabled_fg = MAIN_INPUT_PLACEHOLDER_FG_DARK if current_theme == 'dark' else MAIN_INPUT_PLACEHOLDER_FG_LIGHT
                        widget.config(disabledbackground=disabled_bg, disabledforeground=disabled_fg)
                    else: # state == 'normal'
                        # When re-enabling, ensure active colors are applied
                        current_fg = MAIN_INPUT_PLACEHOLDER_FG_DARK if self.is_main_input_placeholder_active.get() else (ENTRY_FG_DARK if current_theme == 'dark' else ENTRY_FG_LIGHT)
                        current_bg = ENTRY_BG_DARK if current_theme == 'dark' else ENTRY_BG_LIGHT
                        widget.config(bg=current_bg, fg=current_fg)


            elif isinstance(widget, tk.Canvas): # For theme_canvas, change bind state
                if state == 'disabled':
                    widget.unbind("<Button-1>")
                    widget.unbind("<Enter>")
                    widget.unbind("<Leave>")
                else:
                    widget.bind("<Button-1>", self.toggle_theme)
                    self.bind_content_button_hover(widget)


    def _fade_in(self):
        """Gradually increases the window's alpha from 0 to 1 for a fade-in effect."""
        current_alpha = self.attributes('-alpha')
        target_alpha = 1.0
        alpha_step = (target_alpha - current_alpha) / MAIN_FADE_STEPS
        
        if current_alpha < target_alpha:
            new_alpha = current_alpha + alpha_step
            if new_alpha > target_alpha:
                new_alpha = target_alpha
            self.attributes('-alpha', new_alpha)
            self.after(MAIN_FADE_DURATION_MS // MAIN_FADE_STEPS, self._fade_in)
        else:
            self.attributes('-alpha', target_alpha)

    def _initial_icon_display(self):
        if not self.theme_canvas.winfo_exists(): return
        # Calculate center coordinates based on the new fixed size
        center_x = (THEME_ICON_DISPLAY_WIDTH + 10) / 2
        center_y = (THEME_ICON_DISPLAY_HEIGHT + 10) / 2

        if current_theme == 'light':
            if self.moon_photo_image:
                self.theme_canvas.itemconfig(self.moon_icon_item, state='normal')
                self.theme_canvas.coords(self.moon_icon_item, center_x, center_y)
            self.theme_canvas.itemconfig(self.sun_icon_item, state='hidden')
        else:
            if self.sun_photo_image:
                self.theme_canvas.itemconfig(self.sun_icon_item, state='normal')
                self.theme_canvas.coords(self.sun_icon_item, center_x, center_y)
            self.theme_canvas.itemconfig(self.moon_icon_item, state='hidden')
        self.theme_canvas.update_idletasks()

    def load_pixel_icon(self, icon_filename, target_width, target_height):
        icon_path_full = os.path.join(PIXEL_ICONS_DIR, icon_filename)
        if not os.path.exists(icon_path_full):
            return None
        try:
            original_image = PhotoImage(file=icon_path_full)
            x_factor = max(1, original_image.width() // target_width)
            y_factor = max(1, original_image.height() // target_height)
            return original_image.subsample(x_factor, y_factor)
        except Exception as ex:
            pass

    def slide_icon_animation(self, current_icon_item, next_icon_item, duration_ms, steps, new_theme_name):
        if not self.theme_canvas.winfo_exists(): return

        transition_key = (str(self.theme_canvas), '_icon_animation')
        if transition_key in _active_color_transitions:
            try:
                self.theme_canvas.after_cancel(_active_color_transitions[transition_key])
            except ValueError:
                pass
            del _active_color_transitions[transition_key]
        
        # Calculate new center coordinates
        center_x = (THEME_ICON_DISPLAY_WIDTH + 10) / 2
        center_y = (THEME_ICON_DISPLAY_HEIGHT + 10) / 2

        move_y_per_step = (THEME_ICON_DISPLAY_HEIGHT + 10) / steps # Use button height for total slide distance
        delay_per_step = duration_ms // steps
        
        self.theme_canvas.itemconfigure(next_icon_item, state='hidden')
        next_image = self.moon_photo_image if new_theme_name == 'light' else self.sun_photo_image
        if not next_image: return
        self.theme_canvas.itemconfig(next_icon_item, image=next_image)
        # Place the incoming icon just below the canvas, ready to slide up
        self.theme_canvas.coords(next_icon_item, center_x, center_y + (THEME_ICON_DISPLAY_HEIGHT + 10)) 
        self.theme_canvas.itemconfigure(next_icon_item, state='normal')
        
        def animate_step(step_count):
            if not self.theme_canvas.winfo_exists():
                if transition_key in _active_color_transitions: del _active_color_transitions[transition_key]
                return
            if step_count < steps:
                self.theme_canvas.move(current_icon_item, 0, -move_y_per_step)
                self.theme_canvas.move(next_icon_item, 0, -move_y_per_step)
                _active_color_transitions[transition_key] = self.theme_canvas.after(delay_per_step, animate_step, step_count + 1)
            else:
                # Ensure final positions are exact
                self.theme_canvas.coords(current_icon_item, center_x, center_y - (THEME_ICON_DISPLAY_HEIGHT + 10)) # Off-screen above
                self.theme_canvas.itemconfig(current_icon_item, state='hidden')
                self.theme_canvas.coords(next_icon_item, center_x, center_y) # Centered
                if transition_key in _active_color_transitions: del _active_color_transitions[transition_key]
        
        _active_color_transitions[transition_key] = self.theme_canvas.after(0, animate_step, 0)
        
    def _set_initial_theme_colors(self, theme_name):
        self.content_frame.config(bg=get_main_window_bg_color(theme_name))
        self.title_bar.update_theme(theme_name)
        self.theme_canvas.config(bg=get_main_window_bg_color(theme_name))
        
        self.grid_container_frame.config(bg=get_main_window_bg_color(theme_name))

        self.update_on_top_button_icon()
        self.update_chat_lock_button_icon()
        
        chat_lock_target_bg, chat_lock_target_fg = get_widget_target_colors(self.toggle_chat_lock_button, theme_name, is_main_window_content=True, top_level_instance=self)
        self.toggle_chat_lock_button.config(bg=chat_lock_target_bg, fg=chat_lock_target_fg)
        self.bind_content_button_hover(self.toggle_chat_lock_button)

        # Update how_to_use_button's background based on theme
        how_to_use_target_bg, _ = get_widget_target_colors(self.how_to_use_button, theme_name, is_main_window_content=True, top_level_instance=self)
        self.how_to_use_button.config(bg=how_to_use_target_bg)
        self.bind_content_button_hover(self.how_to_use_button)

        target_bg, target_fg = get_widget_target_colors(self.toggle_on_top_button, current_theme, is_main_window_content=True, top_level_instance=self)
        smooth_color_transition(self.toggle_on_top_button, 'bg', self.toggle_on_top_button.cget('bg'), target_bg, THEME_TRANSITION_DURATION_MS, THEME_TRANSITION_STEPS)
        smooth_color_transition(self.toggle_on_top_button, 'fg', self.toggle_on_top_button.cget('fg'), target_fg, THEME_TRANSITION_DURATION_MS, THEME_TRANSITION_STEPS)
        self.bind_content_button_hover(self.toggle_on_top_button)

        main_input_bg = ENTRY_BG_DARK if theme_name == 'dark' else ENTRY_BG_LIGHT
        self.main_input_entry.config(bg=main_input_bg)
        self.main_input_entry.config(disabledbackground=main_input_bg)

        if self.is_main_input_placeholder_active.get():
            main_input_fg = MAIN_INPUT_PLACEHOLDER_FG_DARK if theme_name == 'dark' else MAIN_INPUT_PLACEHOLDER_FG_LIGHT
        else:
            main_input_fg = ENTRY_FG_DARK if theme_name == 'dark' else ENTRY_FG_LIGHT
        
        self.main_input_entry.config(fg=main_input_fg)
        self.main_input_entry.config(disabledforeground=main_input_fg)

    def on_window_click(self, event):
        if self.focus_get() == self.main_input_entry and event.widget != self.main_input_entry:
            self.focus_set()
        if event.widget == self.main_input_entry:
            self.ensure_main_input_editable()

    def bind_content_button_hover(self, widget):
        widget.bind("<Enter>", functools.partial(self._on_enter_hover, widget, False))
        widget.bind("<Leave>", functools.partial(self._on_leave_hover, widget, False))

    def _on_enter_hover(self, widget, is_close_button, event):
        hover_color = DARK_BUTTON_HOVER_COLOR if current_theme == 'dark' else BUTTON_HOVER_COLOR
        if widget == self.theme_canvas:
            self.theme_canvas.config(bg=hover_color)
        else:
            widget.config(bg=hover_color)

    def _on_leave_hover(self, widget, is_close_button, event):
        target_bg, _ = get_widget_target_colors(widget, current_theme, is_main_window_content=True, top_level_instance=self)
        widget.config(bg=target_bg)

    def set_icon(self):
        try:
            self.icon_photo = PhotoImage(file=self.icon_path)
            self.wm_iconphoto(True, self.icon_photo)
        except Exception as ex:
            pass

    def minimize_window(self):
        self.state('withdrawn')

    def toggle_maximize(self):
        if self.is_maximized:
            # Restore the window to its previous geometry
            if hasattr(self, '_previous_geometry') and self._previous_geometry:
                try: self.geometry(self._previous_geometry)
                except tk.TclError: self.geometry(f"{self.min_width}x{self.min_height}")
            self.title_bar.maximize_button.config(text="⬜") # Set to maximize icon
            self.is_maximized = False
        else:
            # Maximize the window
            self._previous_geometry = self.geometry()
            screen_width = self.winfo_screenwidth()
            # MODIFIED: Use self.min_height for the height when maximized
            self.geometry(f"{screen_width}x{self.min_height}+0+0") # Maximize to full screen width, keep fixed height
            self.title_bar.maximize_button.config(text="🗗") # Set to restore down icon
            self.is_maximized = True

    def close_window(self):
        if self.popup_window is not None and self.popup_window.winfo_exists():
            self.popup_window.close_window()
        self.parent.destroy()

    def toggle_on_top(self):
        new_on_top_state = not self.on_top_state.get()
        self.on_top_state.set(new_on_top_state)
        self.attributes("-topmost", new_on_top_state)
        self.update_on_top_button_icon()
        
        target_bg, target_fg = get_widget_target_colors(self.toggle_on_top_button, current_theme, is_main_window_content=True, top_level_instance=self)
        smooth_color_transition(self.toggle_on_top_button, 'bg', self.toggle_on_top_button.cget('bg'), target_bg, THEME_TRANSITION_DURATION_MS, THEME_TRANSITION_STEPS)
        smooth_color_transition(self.toggle_on_top_button, 'fg', self.toggle_on_top_button.cget('fg'), target_fg, THEME_TRANSITION_DURATION_MS, THEME_TRANSITION_STEPS)
        self.bind_content_button_hover(self.toggle_on_top_button)

    def toggle_chat_lock(self):
        new_chat_lock_state = not self.chat_lock_state.get()
        self.chat_lock_state.set(new_chat_lock_state)
        self.keep_focus_active = self.chat_lock_state.get()
        self.update_chat_lock_button_icon()

        target_bg, target_fg = get_widget_target_colors(self.toggle_chat_lock_button, current_theme, is_main_window_content=True, top_level_instance=self)
        smooth_color_transition(self.toggle_chat_lock_button, 'bg', target_bg, target_bg, THEME_TRANSITION_DURATION_MS, THEME_TRANSITION_STEPS)
        if 'fg' in self.toggle_chat_lock_button.config() and self.toggle_chat_lock_button.cget('fg') != target_fg and target_fg is not None:
             smooth_color_transition(self.toggle_chat_lock_button, 'fg', target_fg, target_fg, THEME_TRANSITION_DURATION_MS, THEME_TRANSITION_STEPS)
        self.bind_content_button_hover(self.toggle_chat_lock_button)


    def function_that_causes_the_glitch(self):
        # This is a dummy function. Do not change it.
        pass

    def update_on_top_button_icon(self):
        """Updates the image of the 'On Top' button based on its state."""
        if self.on_top_state.get():
            if self.on_top_icon_locked:
                self.toggle_on_top_button.config(image=self.on_top_icon_locked)
        else:
            if self.on_top_icon_unlocked:
                self.toggle_on_top_button.config(image=self.on_top_icon_unlocked)
        self.toggle_on_top_button.update_idletasks()

    def update_chat_lock_button_icon(self):
        """Updates the image of the 'Chat Lock' button based on its state."""
        if self.chat_lock_state.get():
            if self.chat_lock_icon_on_photo:
                self.toggle_chat_lock_button.config(image=self.chat_lock_icon_on_photo)
        else:
            if self.chat_lock_icon_off_photo:
                self.toggle_chat_lock_button.config(image=self.chat_lock_icon_off_photo)
        self.toggle_chat_lock_button.update_idletasks()


    def on_main_input_focus_in(self, event):
        if self.main_input_entry.get() == DEFAULT_MAIN_INPUT_PLACEHOLDER:
            self.main_input_entry.delete(0, tk.END)
            self.main_input_entry.config(fg=ENTRY_FG_DARK if current_theme == 'dark' else ENTRY_FG_LIGHT)
            self.is_main_input_placeholder_active.set(False)

    def on_main_input_focus_out(self, event):
        if self.just_submitted_main_input:
            self.just_submitted_main_input = False
            return

        if not self.main_input_entry.get().strip():
            self.main_input_entry.insert(0, DEFAULT_MAIN_INPUT_PLACEHOLDER)
            self.main_input_entry.config(fg=MAIN_INPUT_PLACEHOLDER_FG_DARK if current_theme == 'dark' else MAIN_INPUT_PLACEHOLDER_FG_LIGHT)
            self.is_main_input_placeholder_active.set(True)
        else:
            self.main_input_entry.config(fg=ENTRY_FG_DARK if current_theme == 'dark' else ENTRY_FG_LIGHT)
            self.is_main_input_placeholder_active.set(False)


    def on_main_input_click(self, event):
        """Ensures the main input box is editable and focused when clicked."""
        self.ensure_main_input_editable()

    def ensure_main_input_editable(self):
        """Ensures the main input box is in a normal state and focused."""
        if self.main_input_entry.cget('state') == 'disabled':
            self.main_input_entry.config(state='normal')
        self.main_input_entry.focus_set()
        self.main_input_entry.icursor(tk.END)
        self.main_input_entry.selection_clear()

    def open_main_url(self, event=None):
        code = self.main_input_entry.get()
        if code == DEFAULT_MAIN_INPUT_PLACEHOLDER:
            code = ""
        
        full_url = self.base_url + code

        try:
            webbrowser.open_new(full_url)
        except webbrowser.Error as e:
            messagebox.showerror("Browser Error", f"Could not open browser: {e}\nPlease ensure you have a default web browser configured.")
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")

        self.just_submitted_main_input = True
        self.main_input_entry.delete(0, tk.END)
        self.main_input_entry.config(fg=ENTRY_FG_DARK if current_theme == 'dark' else ENTRY_FG_LIGHT)
        self.is_main_input_placeholder_active.set(False)

        self.lift()
        self.focus_force()
        self.main_input_entry.focus_set()


    def open_how_to_use_popup(self):
        if self.popup_window is not None and self.popup_window.winfo_exists():
            self.popup_window.close_window()
        else:
            self.popup_window = PopupHowTo(self, self.icon_path)
            self.keep_focus_active = False 
            self.after(50, lambda: self.popup_window.focus_force())


    def _on_main_window_escape(self, event=None):
        """Handles Escape key press for the main window."""
        if self.popup_window is not None and self.popup_window.winfo_exists():
            self.popup_window.close_window()
        else:
            self.close_window()

    def toggle_theme(self, event=None):
        global current_theme
        old_theme = current_theme
        current_theme = 'dark' if old_theme == 'light' else 'light'
        
        current_icon = self.moon_icon_item if old_theme == 'light' else self.sun_icon_item
        next_icon = self.sun_icon_item if old_theme == 'light' else self.moon_icon_item
        self.slide_icon_animation(current_icon, next_icon, ICON_SLIDE_DURATION_MS, ICON_SLIDE_STEPS, current_theme)
        
        self.apply_smooth_theme_transition(old_theme, current_theme)

    def apply_smooth_theme_transition(self, old_theme, new_theme):
        current_content_bg = self.content_frame.cget('bg')
        target_content_bg = get_main_window_bg_color(new_theme)
        smooth_color_transition(self.content_frame, 'bg', current_content_bg, target_content_bg, THEME_TRANSITION_DURATION_MS, THEME_TRANSITION_STEPS)
        self.title_bar.update_theme(new_theme)
        
        for widget in [self.toggle_on_top_button, self.toggle_chat_lock_button, self.how_to_use_button, self.main_input_entry, self.theme_canvas, self.grid_container_frame]:
             start_bg, start_fg = get_widget_target_colors(widget, old_theme, is_main_window_content=True, top_level_instance=self)
             target_bg, target_fg = get_widget_target_colors(widget, new_theme, is_main_window_content=True, top_level_instance=self)
             
             smooth_color_transition(widget, 'bg', start_bg, target_bg, THEME_TRANSITION_DURATION_MS, THEME_TRANSITION_STEPS)
             
             if target_fg is not None and start_fg is not None: 
                 if 'fg' in widget.config() and start_fg != target_fg: 
                     smooth_color_transition(widget, 'fg', start_fg, target_fg, THEME_TRANSITION_DURATION_MS, THEME_TRANSITION_STEPS)

        if self.popup_window is not None and self.popup_window.winfo_exists():
            self.popup_window.apply_smooth_theme_transition(old_theme, new_theme)
        
        self.after(THEME_TRANSITION_DURATION_MS + 50, self._post_recursive_theme_update, new_theme)

    def _post_recursive_theme_update(self, theme_name):
        if self.popup_window is not None and self.popup_window.winfo_exists():
            self.popup_window.on_popup_input_focus_out(None)
        self.update_chat_lock_button_icon()


# --- Application Setup ---
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.main_window = MainWindow(self, MAIN_ICON_PATH)
        self.protocol("WM_DELETE_WINDOW", self.main_window.close_window) 

if __name__ == "__main__":
    app = App()
    app.mainloop()
