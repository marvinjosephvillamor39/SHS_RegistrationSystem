import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from db_config import get_connection
from ui_utils import *


class SHSRegistrationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("SHS Registration System")
        self.root.configure(bg=PRIMARY_BG)
        center_window(self.root, 600, 500)
        self.root.resizable(False, False)

        # Apply treeview styling
        style_treeview()

        # Header
        header_frame = tk.Frame(self.root, bg=ACCENT_COLOR, height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="🎓 SHS Registration System",
            font=("Segoe UI", 24, "bold"),
            bg=ACCENT_COLOR,
            fg="white"
        ).pack(expand=True)

        # Main content
        content_frame = tk.Frame(self.root, bg=PRIMARY_BG)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=40)

        tk.Label(
            content_frame,
            text="Welcome! Please select an option below:",
            font=FONT_NORMAL,
            bg=PRIMARY_BG,
            fg=TEXT_SECONDARY
        ).pack(pady=(0, 30))

        # Buttons
        buttons = [
            ("👨‍🎓 Student Registration", self.open_student_registration, ACCENT_COLOR),
            ("🔐 Administrator Portal", self.open_admin_login, ACCENT_COLOR),
            ("📋 View Registered Students", lambda: self.view_students(active_only=True), SUCCESS_COLOR)
        ]

        for text, cmd, color in buttons:
            btn = create_rounded_button(content_frame, text, cmd, color=color, hover_color=ACCENT_HOVER)
            btn.pack(pady=10)

    def open_student_registration(self):
        """Step 1: Student Registration Form"""
        reg_win = tk.Toplevel(self.root)
        reg_win.title("Student Registration")
        reg_win.configure(bg=SECONDARY_BG)
        reg_win.grab_set()  # Make modal
        center_window(reg_win, 550, 700)
        reg_win.resizable(False, False)

        # Header
        create_header(reg_win, "Student Registration Form")
        create_subheader(reg_win, "Step 1 of 3: Personal Information")

        # Form container
        form_frame = tk.Frame(reg_win, bg=SECONDARY_BG)
        form_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Fields
        entries = {}
        entries["First Name"] = create_entry_field(form_frame, "First Name *")
        entries["Last Name"] = create_entry_field(form_frame, "Last Name *")
        entries["Grade Level"] = create_combobox_field(form_frame, "Grade Level *", ["Grade 11", "Grade 12"])
        entries["Gender"] = create_combobox_field(form_frame, "Gender *", ["Male", "Female"])
        entries["Age"] = create_entry_field(form_frame, "Age *")
        entries["Guardian"] = create_entry_field(form_frame, "Guardian/Parent Name *")

        def next_step():
            data = {}
            for k, v in entries.items():
                value = v.get().strip()
                data[k] = value

            # Validation
            if not all(data.values()):
                messagebox.showwarning("Incomplete Form", "Please fill in all required fields!", parent=reg_win)
                return

            age_str = data["Age"]
            if not age_str.isdigit():
                messagebox.showwarning("Invalid Age", "Please enter a valid number for Age!", parent=reg_win)
                return

            age = int(age_str)
            if age < 1 or age > 100:
                messagebox.showwarning("Invalid Age", "Please enter a valid age (1-100)!", parent=reg_win)
                return

            reg_win.destroy()
            self.open_strand_selection(data)

        def cancel():
            reg_win.destroy()

        # Buttons
        btn_frame = tk.Frame(reg_win, bg=SECONDARY_BG)
        btn_frame.pack(pady=30)

        tk.Button(btn_frame, text="Cancel", command=cancel, font=FONT_BUTTON,
                  bg=TEXT_SECONDARY, fg="white", width=12, height=2, cursor="hand2", relief=tk.FLAT).pack(side=tk.LEFT,
                                                                                                          padx=10)

        create_rounded_button(btn_frame, "Next →", next_step, width=12).pack(side=tk.LEFT, padx=10)

    def open_strand_selection(self, student_data):
        """Step 2: Strand Selection"""
        strand_win = tk.Toplevel(self.root)
        strand_win.title("Strand Selection")
        strand_win.configure(bg=SECONDARY_BG)
        strand_win.grab_set()
        center_window(strand_win, 500, 550)
        strand_win.resizable(False, False)

        create_header(strand_win, "Choose Your Strand")
        create_subheader(strand_win, "Step 2 of 3: Academic Track")

        # Strand selection
        strand_frame = tk.Frame(strand_win, bg=SECONDARY_BG)
        strand_frame.pack(pady=20, padx=50, fill=tk.BOTH, expand=True)

        strand_var = tk.StringVar()

        strands = [
            ("STEM", "Science, Technology, Engineering, Mathematics"),
            ("ABM", "Accountancy, Business, Management"),
            ("HUMSS", "Humanities and Social Sciences"),
            ("TVL ICT", "Information & Communication Technology"),
            ("TVL EIM", "Electrical Installation & Maintenance"),
            ("GAS", "General Academic Strand")
        ]

        for strand, desc in strands:
            frame = tk.Frame(strand_frame, bg="white", highlightbackground=BORDER_COLOR,
                             highlightthickness=1, cursor="hand2")
            frame.pack(fill=tk.X, pady=8, ipady=10)

            rb = tk.Radiobutton(
                frame,
                text=strand,
                variable=strand_var,
                value=strand,
                font=FONT_HEADING,
                bg="white",
                fg=TEXT_PRIMARY,
                activebackground="white",
                selectcolor=ACCENT_COLOR,
                cursor="hand2"
            )
            rb.pack(anchor="w", padx=20)

            tk.Label(
                frame,
                text=desc,
                font=("Segoe UI", 9),
                bg="white",
                fg=TEXT_SECONDARY
            ).pack(anchor="w", padx=40)

        # Buttons
        btn_frame = tk.Frame(strand_win, bg=SECONDARY_BG)
        btn_frame.pack(pady=30)

        def back():
            strand_win.destroy()
            self.open_student_registration()

        def next_step():
            if not strand_var.get():
                messagebox.showwarning("No Selection", "Please select a strand!", parent=strand_win)
                return

            student_data["Strand"] = strand_var.get()
            strand_win.destroy()
            self.open_confirmation(student_data)

        tk.Button(btn_frame, text="← Back", command=back, font=FONT_BUTTON,
                  bg=TEXT_SECONDARY, fg="white", width=12, height=2, cursor="hand2").pack(side=tk.LEFT, padx=10)

        create_rounded_button(btn_frame, "Next →", next_step, width=12).pack(side=tk.LEFT, padx=10)

    def open_confirmation(self, student_data):
        """Step 3: Confirmation"""
        confirm_win = tk.Toplevel(self.root)
        confirm_win.title("Confirm Registration")
        confirm_win.configure(bg=SECONDARY_BG)
        confirm_win.grab_set()
        center_window(confirm_win, 550, 600)
        confirm_win.resizable(False, False)

        create_header(confirm_win, "Confirm Your Details")
        create_subheader(confirm_win, "Step 3 of 3: Review & Submit")

        # Info display
        info_frame = tk.Frame(confirm_win, bg="white", highlightbackground=BORDER_COLOR,
                              highlightthickness=1)
        info_frame.pack(pady=20, padx=50, fill=tk.BOTH, expand=True)

        tk.Label(
            info_frame,
            text="Please review your information carefully:",
            font=FONT_NORMAL,
            bg="white",
            fg=TEXT_SECONDARY
        ).pack(pady=15)

        for k, v in student_data.items():
            row = tk.Frame(info_frame, bg="white")
            row.pack(fill=tk.X, padx=30, pady=5)

            tk.Label(
                row,
                text=f"{k}:",
                font=FONT_BUTTON,
                bg="white",
                fg=TEXT_PRIMARY,
                width=15,
                anchor="w"
            ).pack(side=tk.LEFT)

            tk.Label(
                row,
                text=v,
                font=FONT_NORMAL,
                bg="white",
                fg=TEXT_PRIMARY,
                anchor="w"
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(
            info_frame,
            text="\n⚠ Your registration will be pending admin approval",
            font=("Segoe UI", 9, "italic"),
            bg="white",
            fg=TEXT_SECONDARY
        ).pack(pady=15)

        # Buttons
        btn_frame = tk.Frame(confirm_win, bg=SECONDARY_BG)
        btn_frame.pack(pady=30)

        def back():
            confirm_win.destroy()
            self.open_strand_selection(student_data)

        def register():
            try:
                conn = get_connection()
                cur = conn.cursor()
                sql = """INSERT INTO students
                         (first_name, last_name, grade_level, gender, age, guardian, strand, status)
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                vals = (
                    student_data["First Name"],
                    student_data["Last Name"],
                    student_data["Grade Level"],
                    student_data["Gender"],
                    int(student_data["Age"]),
                    student_data["Guardian"],
                    student_data["Strand"],
                    "Pending"
                )
                cur.execute(sql, vals)
                conn.commit()
                cur.close()
                conn.close()

                messagebox.showinfo(
                    "Registration Successful!",
                    "Your registration has been submitted successfully!\n\n"
                    "Please wait for admin approval.",
                    parent=confirm_win
                )
                confirm_win.destroy()

            except Exception as e:
                messagebox.showerror("Database Error", f"An error occurred:\n{str(e)}", parent=confirm_win)

        tk.Button(btn_frame, text="← Back", command=back, font=FONT_BUTTON,
                  bg=TEXT_SECONDARY, fg="white", width=12, height=2, cursor="hand2").pack(side=tk.LEFT, padx=10)

        create_rounded_button(btn_frame, "✓ Submit", register, color=SUCCESS_COLOR, width=12).pack(side=tk.LEFT,
                                                                                                   padx=10)

    def view_students(self, active_only=True):
        """View all students with actions"""
        view_win = tk.Toplevel(self.root)
        title = "Registered Students" if active_only else "Admin - All Students"
        view_win.title(title)
        view_win.configure(bg=PRIMARY_BG)
        view_win.geometry("1200x600")

        # Header
        header_frame = tk.Frame(view_win, bg=ACCENT_COLOR, height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text=title,
            font=("Segoe UI", 20, "bold"),
            bg=ACCENT_COLOR,
            fg="white"
        ).pack(expand=True)

        # Table frame
        table_frame = tk.Frame(view_win, bg=PRIMARY_BG)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Treeview with scrollbar
        tree_scroll = ttk.Scrollbar(table_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ("ID", "First Name", "Last Name", "Grade", "Gender",
                   "Age", "Guardian", "Strand", "Status")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                            yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=tree.yview)

        # Column configuration
        widths = {"ID": 50, "First Name": 120, "Last Name": 120, "Grade": 80,
                  "Gender": 80, "Age": 50, "Guardian": 150, "Strand": 100, "Status": 100}

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=widths.get(col, 100),
                        anchor="center" if col in ["ID", "Age", "Grade", "Gender", "Status"] else "w")

        tree.pack(fill=tk.BOTH, expand=True)

        def refresh_tree():
            for i in tree.get_children():
                tree.delete(i)
            try:
                conn = get_connection()
                cur = conn.cursor()
                if active_only:
                    cur.execute("""SELECT id, first_name, last_name, grade_level, gender, age, 
                                guardian, strand, status FROM students 
                                WHERE status IN ('Accepted', 'Dropped')""")
                else:
                    cur.execute("""SELECT id, first_name, last_name, grade_level, gender, age, 
                                guardian, strand, status FROM students""")

                for row in cur.fetchall():
                    tree.insert("", "end", values=row, tags=(row[8],))

                # Color coding
                tree.tag_configure("Accepted", background="#d4edda")
                tree.tag_configure("Pending", background="#fff3cd")
                tree.tag_configure("Dropped", background="#f8d7da")
                tree.tag_configure("Rejected", background="#f8d7da")

                conn.close()
            except Exception as e:
                messagebox.showerror("Database Error", f"Error loading data:\n{str(e)}", parent=view_win)

        refresh_tree()

        # Action buttons
        btn_frame = tk.Frame(view_win, bg=PRIMARY_BG)
        btn_frame.pack(pady=20)

        if active_only:
            # Student portal buttons
            def update_student():
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("No Selection", "Please select a student to update.", parent=view_win)
                    return

                student = tree.item(selected)["values"]
                student_id = student[0]

                update_win = tk.Toplevel(view_win)
                update_win.title("Update Student")
                update_win.configure(bg=SECONDARY_BG)
                update_win.grab_set()
                center_window(update_win, 550, 650)

                create_header(update_win, "Update Student Information")

                form_frame = tk.Frame(update_win, bg=SECONDARY_BG)
                form_frame.pack(fill=tk.BOTH, expand=True, pady=10)

                entries = {}
                fields = ["First Name", "Last Name", "Grade Level", "Gender", "Age", "Guardian", "Strand"]

                for i, field in enumerate(fields):
                    if field in ["Grade Level", "Gender"]:
                        values = ["Grade 11", "Grade 12"] if field == "Grade Level" else ["Male", "Female"]
                        combo = create_combobox_field(form_frame, field, values)
                        combo.set(student[i + 1])
                        entries[field] = combo
                    else:
                        entry = create_entry_field(form_frame, field)
                        entry.insert(0, student[i + 1])
                        entries[field] = entry

                def save_update():
                    new_data = {k: v.get() for k, v in entries.items()}
                    if not all(new_data.values()):
                        messagebox.showwarning("Incomplete", "All fields are required!", parent=update_win)
                        return

                    try:
                        conn = get_connection()
                        cur = conn.cursor()
                        sql = """UPDATE students 
                                 SET first_name=%s, last_name=%s, grade_level=%s, gender=%s, 
                                     age=%s, guardian=%s, strand=%s 
                                 WHERE id=%s"""
                        vals = (new_data["First Name"], new_data["Last Name"],
                                new_data["Grade Level"], new_data["Gender"],
                                new_data["Age"], new_data["Guardian"],
                                new_data["Strand"], student_id)
                        cur.execute(sql, vals)
                        conn.commit()
                        conn.close()

                        messagebox.showinfo("Success", "Student updated successfully!", parent=update_win)
                        update_win.destroy()
                        refresh_tree()
                    except Exception as e:
                        messagebox.showerror("Error", f"Update failed:\n{str(e)}", parent=update_win)

                btn_container = tk.Frame(update_win, bg=SECONDARY_BG)
                btn_container.pack(pady=20)
                create_rounded_button(btn_container, "💾 Save Changes", save_update, color=SUCCESS_COLOR).pack()

            def drop_student():
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("No Selection", "Please select a student.", parent=view_win)
                    return

                student_id = tree.item(selected)["values"][0]
                reason = simpledialog.askstring("Drop Reason",
                                                "Enter reason for dropping this student:",
                                                parent=view_win)
                if not reason:
                    messagebox.showwarning("Required", "Drop reason is required!", parent=view_win)
                    return

                if messagebox.askyesno("Confirm Drop",
                                       f"Mark this student as Dropped?\n\nReason: {reason}",
                                       parent=view_win):
                    try:
                        conn = get_connection()
                        cur = conn.cursor()
                        cur.execute("UPDATE students SET status='Dropped', drop_reason=%s WHERE id=%s",
                                    (reason, student_id))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo("Success", "Student marked as Dropped.", parent=view_win)
                        refresh_tree()
                    except Exception as e:
                        messagebox.showerror("Error", str(e), parent=view_win)

            def delete_student():
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("No Selection", "Select a student to delete.", parent=view_win)
                    return

                if messagebox.askyesno("Confirm Delete",
                                       "Are you sure you want to permanently delete this student?",
                                       parent=view_win):
                    try:
                        student_id = tree.item(selected)["values"][0]
                        conn = get_connection()
                        cur = conn.cursor()
                        cur.execute("DELETE FROM students WHERE id=%s", (student_id,))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo("Deleted", "Student record deleted.", parent=view_win)
                        refresh_tree()
                    except Exception as e:
                        messagebox.showerror("Error", str(e), parent=view_win)

            def register_another():
                view_win.destroy()
                self.open_student_registration()

            buttons = [
                ("➕ Register New Student", register_another, SUCCESS_COLOR),
                ("✏ Update", update_student, ACCENT_COLOR),
                ("⚠ Drop", drop_student, "#F39C12"),
                ("🗑 Delete", delete_student, DANGER_COLOR)
            ]

            for text, cmd, color in buttons:
                create_rounded_button(btn_frame, text, cmd, color=color, width=20).pack(side=tk.LEFT, padx=8)

        else:
            # Admin buttons
            def accept_student():
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("No Selection", "Select a student to accept.", parent=view_win)
                    return

                student_id = tree.item(selected)["values"][0]
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("UPDATE students SET status='Accepted' WHERE id=%s", (student_id,))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Accepted", "Student accepted successfully!", parent=view_win)
                    refresh_tree()
                except Exception as e:
                    messagebox.showerror("Error", str(e), parent=view_win)

            def reject_student():
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("No Selection", "Select a student to reject.", parent=view_win)
                    return

                if messagebox.askyesno("Confirm Reject",
                                       "Are you sure you want to reject this student?",
                                       parent=view_win):
                    try:
                        student_id = tree.item(selected)["values"][0]
                        conn = get_connection()
                        cur = conn.cursor()
                        cur.execute("UPDATE students SET status='Rejected' WHERE id=%s", (student_id,))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo("Rejected", "Student rejected.", parent=view_win)
                        refresh_tree()
                    except Exception as e:
                        messagebox.showerror("Error", str(e), parent=view_win)

            buttons = [
                ("✓ Accept", accept_student, SUCCESS_COLOR),
                ("✗ Reject", reject_student, DANGER_COLOR)
            ]

            for text, cmd, color in buttons:
                create_rounded_button(btn_frame, text, cmd, color=color, width=20).pack(side=tk.LEFT, padx=8)

    def open_admin_login(self):
        """Admin login window"""
        admin_win = tk.Toplevel(self.root)
        admin_win.title("Administrator Login")
        admin_win.configure(bg=SECONDARY_BG)
        admin_win.grab_set()
        center_window(admin_win, 450, 400)
        admin_win.resizable(False, False)

        # Icon/Header
        header_frame = tk.Frame(admin_win, bg=ACCENT_COLOR, height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="🔐",
            font=("Segoe UI", 40),
            bg=ACCENT_COLOR
        ).pack(expand=True)

        create_header(admin_win, "Administrator Login")

        form_frame = tk.Frame(admin_win, bg=SECONDARY_BG)
        form_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        username_entry = create_entry_field(form_frame, "Username")
        password_entry = create_entry_field(form_frame, "Password", is_password=True)

        # Buttons
        btn_frame = tk.Frame(admin_win, bg=SECONDARY_BG)
        btn_frame.pack(pady=30)

        def login():
            username = username_entry.get()
            password = password_entry.get()

            if not username or not password:
                messagebox.showwarning("Incomplete", "Please enter both username and password!", parent=admin_win)
                return

            if username == "admin" and password == "12345":
                messagebox.showinfo("Login Successful", "Welcome, Administrator!", parent=admin_win)
                admin_win.destroy()
                self.view_students(active_only=False)
            else:
                messagebox.showerror("Login Failed", "Invalid username or password!", parent=admin_win)
                password_entry.delete(0, tk.END)

        def cancel():
            admin_win.destroy()

        tk.Button(btn_frame, text="Cancel", command=cancel, font=FONT_BUTTON,
                  bg=TEXT_SECONDARY, fg="white", width=12, height=2, cursor="hand2").pack(side=tk.LEFT, padx=10)

        create_rounded_button(btn_frame, "🔓 Login", login, width=12).pack(side=tk.LEFT, padx=10)

        admin_win.bind('<Return>', lambda e: login())
