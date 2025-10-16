import tkinter as tk

# COLORS
MAIN_COLOR = "#E3F2FD"
ACCENT_COLOR = "#1565C0"
HOVER_COLOR = "#64B5F6"
TEXT_COLOR = "black"

# WINDOW CENTER
def center_window(win, w, h):
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    x = int((screen_w / 2) - (w / 2))
    y = int((screen_h / 2) - (h / 2))
    win.geometry(f"{w}x{h}+{x}+{y}")

# BUTTON STYLING
def style_button(btn):
    btn.config(
        bg=ACCENT_COLOR,
        fg="white",
        activebackground=HOVER_COLOR,
        activeforeground="black"
    )

def on_enter(e):
    e.widget['background'] = HOVER_COLOR

def on_leave(e):
    e.widget['background'] = ACCENT_COLOR

def style_hover_button(btn):
    style_button(btn)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
