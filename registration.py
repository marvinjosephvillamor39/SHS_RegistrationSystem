import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from db_config import get_connection
from ui_utils import MAIN_COLOR, ACCENT_COLOR, TEXT_COLOR, style_hover_button, center_window

class SHSRegistrationSystem:
    def __init__(self, root):   #encapsulation
        self.root = root
        self.root.title("SHS Students Registration System")
        self.root.configure(bg=MAIN_COLOR)
        center_window(self.root, 400, 250)

        tk.Label(
            self.root,
            text="Welcome to SHS Registration System",
            font=("Arial", 12, "bold"),
            wraplength=300,
            bg=MAIN_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=20)

        for text, cmd in [
            ("Student Portal", self.open_student_registration),
            ("Administrator", self.open_admin_login),
            ("Registered Students", lambda: self.view_students(active_only=True))
        ]:
            btn = tk.Button(self.root, text=text, width=25, command=cmd)
            style_hover_button(btn)
            btn.pack(pady=10)

    #registration part
    def open_student_registration(self):
        reg_win = tk.Toplevel(self.root)
        reg_win.title("Student Registration Form")
        reg_win.configure(bg=MAIN_COLOR)
        center_window(reg_win, 500, 400)

        tk.Label(reg_win, text="Step 1: Fill Out Registration Form",
                 font=("Arial", 12, "bold"), bg=MAIN_COLOR, fg=TEXT_COLOR).pack(pady=10)

        entries = {}
        fields = ["First Name", "Last Name", "Grade Level", "Gender", "Age", "Guardian"]

        for f in fields:
            frame = tk.Frame(reg_win, bg=MAIN_COLOR)
            frame.pack(pady=5)
            tk.Label(frame, text=f + ":", width=15, anchor="e", bg=MAIN_COLOR, fg=TEXT_COLOR).pack(side="left")

            if f == "Grade Level":
                entry = ttk.Combobox(frame, values=["Grade 11", "Grade 12"], width=18)
            elif f == "Gender":
                entry = ttk.Combobox(frame, values=["Male", "Female"], width=18)
            else:
                entry = tk.Entry(frame, width=20)

            entry.pack(side="left")
            entries[f] = entry

        def next_step():
            data = {k: v.get() for k, v in entries.items()}
            if not all(data.values()):
                messagebox.showwarning("Warning", "Please fill in all fields before continuing!")
                return
            if not data["Age"].isdigit():
                messagebox.showwarning("Warning", "Please enter a valid number for Age!")
                return
            reg_win.destroy()
            self.open_strand_selection(data)

        next_btn = tk.Button(reg_win, text="Next", width=20, command=next_step)
        style_hover_button(next_btn)
        next_btn.pack(pady=20)

    # stranda selec
    def open_strand_selection(self, student_data):
        strand_win = tk.Toplevel(self.root)
        strand_win.title("Strand Selection")
        strand_win.configure(bg=MAIN_COLOR)
        center_window(strand_win, 400, 300)

        tk.Label(strand_win, text="Step 2: Choose Your Strand",
                 font=("Arial", 12, "bold"), bg=MAIN_COLOR, fg=TEXT_COLOR).pack(pady=20)

        strand_var = tk.StringVar()
        for s in ["STEM", "ABM", "HUMSS", "TVL ICT", "TVL EIM", "GAS"]:
            tk.Radiobutton(strand_win, text=s, variable=strand_var, value=s,
                           bg=MAIN_COLOR, fg=TEXT_COLOR).pack(anchor="w", padx=100)

        def next_step():
            if not strand_var.get():
                messagebox.showwarning("Warning", "Please select a strand!")
                return
            student_data["Strand"] = strand_var.get()
            strand_win.destroy()
            self.open_confirmation(student_data)

        next_btn = tk.Button(strand_win, text="Next", width=20, command=next_step)
        style_hover_button(next_btn)
        next_btn.pack(pady=20)

    # confirmation
    def open_confirmation(self, student_data):
        confirm_win = tk.Toplevel(self.root)
        confirm_win.title("Confirm Details")
        confirm_win.configure(bg=MAIN_COLOR)
        center_window(confirm_win, 400, 350)

        tk.Label(confirm_win, text="Step 3: Confirm Your Details",
                 font=("Arial", 12, "bold"), bg=MAIN_COLOR, fg=TEXT_COLOR).pack(pady=10)

        for k, v in student_data.items():
            tk.Label(confirm_win, text=f"{k}: {v}", bg=MAIN_COLOR, fg=TEXT_COLOR).pack(anchor="w", padx=50)

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
                messagebox.showinfo("Success", "Registration submitted for approval.")
                confirm_win.destroy()
            except Exception as e:
                messagebox.showerror("DB Error", str(e))

        reg_btn = tk.Button(confirm_win, text="Register", width=20, command=register)
        style_hover_button(reg_btn)
        reg_btn.pack(pady=20)

    # Makita mga registered students
    def view_students(self, active_only=True):
        view_win = tk.Toplevel(self.root)
        view_win.title("Registered Students")
        view_win.geometry("1100x450")
        view_win.configure(bg=MAIN_COLOR)

        columns = ("ID", "First Name", "Last Name", "Grade Level", "Gender",
                   "Age", "Guardian", "Strand", "Status")
        tree = ttk.Treeview(view_win, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        tree.pack(fill=tk.BOTH, expand=True)

        def refresh_tree():
            for i in tree.get_children():
                tree.delete(i)
            try:
                conn = get_connection()
                cur = conn.cursor()
                if active_only:
                    cur.execute("SELECT id, first_name, last_name, grade_level, gender, age, guardian, strand, status FROM students WHERE status IN ('Accepted', 'Dropped')")
                else:
                    cur.execute("SELECT id, first_name, last_name, grade_level, gender, age, guardian, strand, status FROM students")
                for row in cur.fetchall():
                    tree.insert("", "end", values=row)
                conn.close()
            except Exception as e:
                messagebox.showerror("DB Error", str(e))

        refresh_tree()

        btn_frame = tk.Frame(view_win, bg=MAIN_COLOR)
        btn_frame.pack(pady=10)

        if active_only:
  # mag update na part
            def update_student():
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("Warning", "Please select a student to update.")
                    return
                student = tree.item(selected)["values"]
                student_id = student[0]

                update_win = tk.Toplevel(view_win)
                update_win.title("Update Student Information")
                center_window(update_win, 400, 400)
                update_win.configure(bg=MAIN_COLOR)

                tk.Label(update_win, text="Update Student Information",
                         font=("Arial", 12, "bold"), bg=MAIN_COLOR, fg=TEXT_COLOR).pack(pady=10)

                fields = ["First Name", "Last Name", "Grade Level", "Gender", "Age", "Guardian", "Strand"]
                entries = {}

                for i, field in enumerate(fields):
                    frame = tk.Frame(update_win, bg=MAIN_COLOR)
                    frame.pack(pady=5)
                    tk.Label(frame, text=field + ":", width=12, anchor="e", bg=MAIN_COLOR, fg=TEXT_COLOR).pack(side="left")
                    entry = tk.Entry(frame, width=20)
                    entry.insert(0, student[i + 1])
                    entry.pack(side="left")
                    entries[field] = entry

                def save_update():
                    new_data = {k: v.get() for k, v in entries.items()}
                    try:
                        conn = get_connection()
                        cur = conn.cursor()
                        sql = """UPDATE students 
                                 SET first_name=%s, last_name=%s, grade_level=%s, gender=%s, age=%s, guardian=%s, strand=%s 
                                 WHERE id=%s"""
                        vals = (new_data["First Name"], new_data["Last Name"], new_data["Grade Level"],
                                new_data["Gender"], new_data["Age"], new_data["Guardian"], new_data["Strand"], student_id)
                        cur.execute(sql, vals)
                        conn.commit()
                        conn.close()
                        messagebox.showinfo("Success", "Student record updated successfully.")
                        update_win.destroy()
                        refresh_tree()
                    except Exception as e:
                        messagebox.showerror("DB Error", str(e))

                save_btn = tk.Button(update_win, text="Save Changes", width=20, command=save_update)
                style_hover_button(save_btn)
                save_btn.pack(pady=20)
#drop students with reason
            def drop_student():
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("Warning", "Please select a student.")
                    return
                student_id = tree.item(selected)["values"][0]
                reason = simpledialog.askstring("Drop Reason", "Enter reason for dropping this student:")
                if not reason:
                    messagebox.showwarning("Warning", "Drop reason is required!")
                    return
                if messagebox.askyesno("Confirm", f"Mark this student as Dropped?\nReason: {reason}"):
                    try:
                        conn = get_connection()
                        cur = conn.cursor()
                        cur.execute("UPDATE students SET status='Dropped', drop_reason=%s WHERE id=%s", (reason, student_id))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo("Updated", "Student marked as Dropped.")
                        refresh_tree()
                    except Exception as e:
                        messagebox.showerror("DB Error", str(e))
# mag delete ug students
            def delete_student():
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("Warning", "Select a student to delete.")
                    return
                student_id = tree.item(selected)["values"][0]
                if messagebox.askyesno("Confirm", "Are you sure you want to delete this student?"):
                    try:
                        conn = get_connection()
                        cur = conn.cursor()
                        cur.execute("DELETE FROM students WHERE id=%s", (student_id,))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo("Deleted", "Student record deleted.")
                        refresh_tree()
                    except Exception as e:
                        messagebox.showerror("DB Error", str(e))

            def register_another_student():
                view_win.destroy()
                self.open_student_registration()

            buttons = [
                ("Register Another Student", register_another_student),
                ("Update", update_student),
                ("Drop", drop_student),
                ("Delete", delete_student)
            ]

            for text, cmd in buttons:
                b = tk.Button(btn_frame, text=text, width=20, command=cmd)
                style_hover_button(b)
                b.pack(side=tk.LEFT, padx=10)

        else:
            # Admin view buttons: Accept / Reject
            def accept_student():
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("Warning", "Select a student to accept.")
                    return
                student_id = tree.item(selected)["values"][0]
                try:
                    conn = get_connection()
                    cur = conn.cursor()
                    cur.execute("UPDATE students SET status='Accepted' WHERE id=%s", (student_id,))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Accepted", "Student has been accepted successfully.")
                    refresh_tree()
                except Exception as e:
                    messagebox.showerror("DB Error", str(e))

            def reject_student():
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("Warning", "Select a student to reject.")
                    return
                student_id = tree.item(selected)["values"][0]
                if messagebox.askyesno("Confirm", "Are you sure you want to reject this student?"):
                    try:
                        conn = get_connection()
                        cur = conn.cursor()
                        cur.execute("UPDATE students SET status='Rejected' WHERE id=%s", (student_id,))
                        conn.commit()
                        conn.close()
                        messagebox.showinfo("Rejected", "Student has been rejected successfully.")
                        refresh_tree()
                    except Exception as e:
                        messagebox.showerror("DB Error", str(e))

            accept_btn = tk.Button(btn_frame, text="Accept", width=20, command=accept_student)
            reject_btn = tk.Button(btn_frame, text="Reject", width=20, command=reject_student)
            style_hover_button(accept_btn)
            style_hover_button(reject_btn)
            accept_btn.pack(side=tk.LEFT, padx=10)
            reject_btn.pack(side=tk.LEFT, padx=10)

    #ADMIN LOGIN
    def open_admin_login(self):
        admin_win = tk.Toplevel(self.root)
        admin_win.title("Administrator Login")
        admin_win.configure(bg=MAIN_COLOR)
        center_window(admin_win, 300, 200)

        tk.Label(admin_win, text="Administrator Login", font=("Arial", 12, "bold"),
                 bg=MAIN_COLOR, fg=TEXT_COLOR).pack(pady=10)

        tk.Label(admin_win, text="Username:", bg=MAIN_COLOR, fg=TEXT_COLOR).pack()
        username_entry = tk.Entry(admin_win, width=25)
        username_entry.pack()

        tk.Label(admin_win, text="Password:", bg=MAIN_COLOR, fg=TEXT_COLOR).pack()
        password_entry = tk.Entry(admin_win, show="*", width=25)
        password_entry.pack()

        def login():
            username = username_entry.get()
            password = password_entry.get()
            if username == "admin" and password == "12345":
                messagebox.showinfo("Login Successful", "Welcome, Admin!")
                admin_win.destroy()
                self.view_students(active_only=False)
            else:
                messagebox.showerror("Login Failed", "Invalid credentials.")

        login_btn = tk.Button(admin_win, text="Login", width=20, command=login)
        style_hover_button(login_btn)
        login_btn.pack(pady=10)
