import tkinter as tk
from tkinter import ttk

# MODERN COLOR SCHEME
PRIMARY_BG = "#F8F9FA"
SECONDARY_BG = "#FFFFFF"
ACCENT_COLOR = "#2C3E50"
ACCENT_HOVER = "#34495E"
SUCCESS_COLOR = "#27AE60"
DANGER_COLOR = "#E74C3C"
TEXT_PRIMARY = "#2C3E50"
TEXT_SECONDARY = "#7F8C8D"
BORDER_COLOR = "#E0E0E0"

# FONTS
FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_HEADING = ("Segoe UI", 14, "bold")
FONT_NORMAL = ("Segoe UI", 10)
FONT_BUTTON = ("Segoe UI", 10, "bold")


def center_window(win, w, h):
    """Center window on screen"""
    win.update_idletasks()
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    x = int((screen_w / 2) - (w / 2))
    y = int((screen_h / 2) - (h / 2))
    win.geometry(f"{w}x{h}+{x}+{y}")


def create_rounded_button(parent, text, command, color=ACCENT_COLOR, hover_color=ACCENT_HOVER, width=25):
    """Create a modern styled button"""
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=FONT_BUTTON,
        bg=color,
        fg="white",
        activebackground=hover_color,
        activeforeground="white",
        relief=tk.FLAT,
        cursor="hand2",
        width=width,
        height=2,
        borderwidth=0
    )

    def on_enter(e):
        e.widget['background'] = hover_color

    def on_leave(e):
        e.widget['background'] = color

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

    return btn


def create_entry_field(parent, label_text, is_password=False, width=30):
    """Create a labeled entry field with modern styling"""
    container = tk.Frame(parent, bg=SECONDARY_BG)
    container.pack(fill=tk.X, padx=30, pady=8)

    label = tk.Label(
        container,
        text=label_text,
        font=FONT_NORMAL,
        bg=SECONDARY_BG,
        fg=TEXT_PRIMARY,
        anchor="w"
    )
    label.pack(fill=tk.X, pady=(0, 5))

    entry_frame = tk.Frame(container, bg="white", highlightbackground=BORDER_COLOR, highlightthickness=1)
    entry_frame.pack(fill=tk.X)

    show_char = "*" if is_password else None
    entry = tk.Entry(
        entry_frame,
        font=FONT_NORMAL,
        relief=tk.FLAT,
        show=show_char,
        width=width,
        bg="white",
        fg=TEXT_PRIMARY
    )
    entry.pack(padx=10, pady=8, fill=tk.X)

    return entry


def create_combobox_field(parent, label_text, values, width=30):
    """Create a labeled combobox with modern styling"""
    container = tk.Frame(parent, bg=SECONDARY_BG)
    container.pack(fill=tk.X, padx=30, pady=8)

    label = tk.Label(
        container,
        text=label_text,
        font=FONT_NORMAL,
        bg=SECONDARY_BG,
        fg=TEXT_PRIMARY,
        anchor="w"
    )
    label.pack(fill=tk.X, pady=(0, 5))

    combo = ttk.Combobox(
        container,
        values=values,
        font=FONT_NORMAL,
        state="readonly",
        width=width
    )
    combo.pack(fill=tk.X)

    return combo


def create_header(parent, text):
    """Create a header label"""
    header = tk.Label(
        parent,
        text=text,
        font=FONT_TITLE,
        bg=SECONDARY_BG,
        fg=TEXT_PRIMARY
    )
    header.pack(pady=20)
    return header


def create_subheader(parent, text):
    """Create a subheader label"""
    subheader = tk.Label(
        parent,
        text=text,
        font=FONT_HEADING,
        bg=SECONDARY_BG,
        fg=TEXT_SECONDARY
    )
    subheader.pack(pady=10)
    return subheader


def style_treeview():
    """Configure treeview styling"""
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Treeview",
        background=SECONDARY_BG,
        foreground=TEXT_PRIMARY,
        fieldbackground=SECONDARY_BG,
        rowheight=30,
        font=FONT_NORMAL
    )

    style.configure(
        "Treeview.Heading",
        background=ACCENT_COLOR,
        foreground="white",
        font=FONT_BUTTON,
        relief=tk.FLAT
    )

    style.map('Treeview', background=[('selected', ACCENT_COLOR)])
    style.map('Treeview.Heading', background=[('active', ACCENT_HOVER)])
