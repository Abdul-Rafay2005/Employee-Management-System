import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
import datetime
import calendar

# ---------- INIT DB ----------
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id TEXT UNIQUE,
        name TEXT,
        position TEXT,
        salary REAL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id TEXT,
        date TEXT,
        entry_time TEXT,
        exit_time TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )''')
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("admin", "admin"))
    conn.commit()
    conn.close()

def show_login():
    login_window = Tk()
    login_window.title("Login - Employee Management System")
    login_window.geometry("500x400")
    login_window.configure(bg="#e8f0fe")
    login_window.resizable(False, False)

    w, h = 500, 400
    screen_w = login_window.winfo_screenwidth()
    screen_h = login_window.winfo_screenheight()
    x = (screen_w - w) // 2
    y = (screen_h - h) // 2
    login_window.geometry(f"{w}x{h}+{x}+{y}")

    # Title
    Label(login_window, text="Employee Management Login", font=("Helvetica", 20, "bold"), bg="#e8f0fe", fg="#1a237e").pack(pady=30)

    # Container Frame
    frame = Frame(login_window, bg="white", bd=2, relief=RIDGE)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=360, height=200)

    user_var = StringVar()
    pass_var = StringVar()

    # Username
    Label(frame, text="Username", bg="white", font=("Arial", 12)).place(x=20, y=20)
    Entry(frame, textvariable=user_var, font=("Arial", 12), width=30, relief=SOLID, bd=1).place(x=20, y=45)

    # Password
    Label(frame, text="Password", bg="white", font=("Arial", 12)).place(x=20, y=80)
    Entry(frame, textvariable=pass_var, font=("Arial", 12), width=30, show="*", relief=SOLID, bd=1).place(x=20, y=105)

    # Attempt login function
    def attempt_login():
        username = user_var.get().strip()
        password = pass_var.get().strip()
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        if c.fetchone():
            login_window.destroy()
            run_app()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
        conn.close()

    # Login button
    Button(frame, text="Login", command=attempt_login,
           font=("Arial", 12), bg="#1a73e8", fg="white", width=20,
           relief=FLAT, cursor="hand2").place(x=70, y=150)

    login_window.mainloop()


# ---------- MAIN APPLICATION ----------
def run_app():
    root = Tk()
    root.title("Employee Management System")
    root.geometry("1200x800")
    root.configure(bg="#f2f2f2")
    root.resizable(False, False)

    Label(root, text="Employee Management System", font=("Helvetica", 22, "bold"), bg="#f2f2f2").pack(pady=10)

    # Form frame
    form_frame = Frame(root, bg="#f2f2f2")
    form_frame.pack(pady=10)

    emp_id_var = StringVar()
    name_var = StringVar()
    position_var = StringVar()
    salary_var = StringVar()

    Label(form_frame, text="Employee ID", bg="#f2f2f2").grid(row=0, column=0)
    Entry(form_frame, textvariable=emp_id_var).grid(row=0, column=1)
    Label(form_frame, text="Name", bg="#f2f2f2").grid(row=1, column=0)
    Entry(form_frame, textvariable=name_var).grid(row=1, column=1)
    Label(form_frame, text="Position", bg="#f2f2f2").grid(row=2, column=0)
    Entry(form_frame, textvariable=position_var).grid(row=2, column=1)
    Label(form_frame, text="Salary", bg="#f2f2f2").grid(row=3, column=0)
    Entry(form_frame, textvariable=salary_var).grid(row=3, column=1)

    def clear_form():
        emp_id_var.set("")
        name_var.set("")
        position_var.set("")
        salary_var.set("")

    def load_employees(search_text=""):
        for row in tree.get_children():
            tree.delete(row)
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        if search_text:
            c.execute("SELECT * FROM employees WHERE name LIKE ? OR emp_id LIKE ?", (f"%{search_text}%", f"%{search_text}%"))
        else:
            c.execute("SELECT * FROM employees")
        for row in c.fetchall():
            tree.insert("", END, values=row)
        conn.close()

    def save_employee():
        emp_id = emp_id_var.get().strip()
        name = name_var.get().strip()
        position = position_var.get().strip()
        salary = salary_var.get().strip()

        if not emp_id or not name:
            messagebox.showerror("Error", "Employee ID and Name required")
            return

        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute("INSERT INTO employees (emp_id, name, position, salary) VALUES (?, ?, ?, ?)",
                      (emp_id, name, position, salary))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Employee saved")
            clear_form()
            load_employees()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Employee ID already exists")

    def on_row_select(event):
        selected = tree.focus()
        if selected:
            values = tree.item(selected, 'values')
            emp_id_var.set(values[1])
            name_var.set(values[2])
            position_var.set(values[3])
            salary_var.set(values[4])

    def update_employee():
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select employee to update")
            return

        values = tree.item(selected, 'values')
        original_id = values[0]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("UPDATE employees SET emp_id=?, name=?, position=?, salary=? WHERE id=?",
                  (emp_id_var.get(), name_var.get(), position_var.get(), salary_var.get(), original_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Updated", "Employee updated")
        clear_form()
        load_employees()

    def delete_employee():
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Error", "Select employee to delete")
            return
        values = tree.item(selected, 'values')
        emp_id = values[1]
        confirm = messagebox.askyesno("Confirm", f"Delete employee {emp_id}?")
        if confirm:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute("DELETE FROM employees WHERE emp_id=?", (emp_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Deleted", "Employee deleted")
            clear_form()
            load_employees()

    Button(form_frame, text="Save", command=save_employee).grid(row=4, column=0)
    Button(form_frame, text="Update", command=update_employee).grid(row=4, column=1)
    Button(form_frame, text="Delete", command=delete_employee).grid(row=4, column=2)

    search_frame = Frame(root, bg="#f2f2f2")
    search_frame.pack()
    search_var = StringVar()
    Label(search_frame, text="Search", bg="#f2f2f2").pack(side=LEFT)
    Entry(search_frame, textvariable=search_var).pack(side=LEFT)
    Button(search_frame, text="Search", command=lambda: load_employees(search_var.get())).pack(side=LEFT)

    tree = ttk.Treeview(root, columns=("ID", "EmpID", "Name", "Position", "Salary"), show="headings")
    for col in ("ID", "EmpID", "Name", "Position", "Salary"):
        tree.heading(col, text=col)
    tree.bind("<<TreeviewSelect>>", on_row_select)
    tree.pack(pady=10, fill=X)
    load_employees()

    attendance_frame = Frame(root, bg="#f2f2f2")
    attendance_frame.pack(pady=10)
    attend_id_var = StringVar()
    Label(attendance_frame, text="Attendance - Emp ID", bg="#f2f2f2").grid(row=0, column=0)
    Entry(attendance_frame, textvariable=attend_id_var).grid(row=0, column=1)

    def mark_entry():
        emp_id = attend_id_var.get().strip()
        today = datetime.date.today().isoformat()
        now = datetime.datetime.now().strftime("%H:%M:%S")
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM attendance WHERE emp_id=? AND date=?", (emp_id, today))
        if c.fetchone():
            messagebox.showinfo("Info", "Entry already marked")
        else:
            c.execute("INSERT INTO attendance (emp_id, date, entry_time, exit_time) VALUES (?, ?, ?, '')",
                      (emp_id, today, now))
            conn.commit()
            messagebox.showinfo("Success", f"Entry marked at {now}")
        conn.close()

    def mark_exit():
        emp_id = attend_id_var.get().strip()
        today = datetime.date.today().isoformat()
        now = datetime.datetime.now().strftime("%H:%M:%S")
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM attendance WHERE emp_id=? AND date=?", (emp_id, today))
        row = c.fetchone()
        if row:
            if row[4]:
                messagebox.showinfo("Info", "Exit already marked")
            else:
                c.execute("UPDATE attendance SET exit_time=? WHERE emp_id=? AND date=?",
                          (now, emp_id, today))
                conn.commit()
                messagebox.showinfo("Success", f"Exit marked at {now}")
        else:
            messagebox.showerror("Error", "No entry found for today")
        conn.close()

    Button(attendance_frame, text="Mark Entry", command=mark_entry).grid(row=1, column=0)
    Button(attendance_frame, text="Mark Exit", command=mark_exit).grid(row=1, column=1)

    history_frame = Frame(root, bg="#f2f2f2")
    history_frame.pack(pady=10)
    hist_id_var = StringVar()
    Label(history_frame, text="Attendance History - Emp ID", bg="#f2f2f2").pack(side=LEFT)
    Entry(history_frame, textvariable=hist_id_var).pack(side=LEFT)

    def view_history():
        emp_id = hist_id_var.get().strip()
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT date, entry_time, exit_time FROM attendance WHERE emp_id=? ORDER BY date DESC", (emp_id,))
        rows = c.fetchall()
        conn.close()

        hist_window = Toplevel(root)
        hist_window.title("Attendance History")
        tree_hist = ttk.Treeview(hist_window, columns=("Date", "Entry", "Exit"), show="headings")
        for col in ("Date", "Entry", "Exit"):
            tree_hist.heading(col, text=col)
        tree_hist.pack(fill=BOTH, expand=True)

        for row in rows:
            tree_hist.insert("", END, values=row)

    Button(history_frame, text="View History", command=view_history).pack(side=LEFT)

    salary_frame = Frame(root, bg="#f2f2f2")
    salary_frame.pack(pady=10)
    salary_emp_id = StringVar()
    salary_month = StringVar()

    Label(salary_frame, text="Salary | Emp ID", bg="#f2f2f2").grid(row=0, column=0)
    Entry(salary_frame, textvariable=salary_emp_id).grid(row=0, column=1)
    Label(salary_frame, text="Month (YYYY-MM)", bg="#f2f2f2").grid(row=0, column=2)
    Entry(salary_frame, textvariable=salary_month).grid(row=0, column=3)

    def calculate_salary():
        emp_id = salary_emp_id.get().strip()
        month = salary_month.get().strip()

        try:
            year, mon = map(int, month.split('-'))
        except:
            messagebox.showerror("Error", "Invalid month format")
            return

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT salary FROM employees WHERE emp_id=?", (emp_id,))
        row = c.fetchone()
        if not row:
            messagebox.showerror("Error", "Employee not found")
            return

        monthly_salary = row[0]
        _, last_day = calendar.monthrange(year, mon)

        working_days = sum(1 for d in range(1, last_day + 1)
                           if datetime.date(year, mon, d).weekday() != 6)

        start_date = f"{month}-01"
        end_date = f"{month}-{last_day:02d}"

        c.execute("SELECT COUNT(*) FROM attendance WHERE emp_id=? AND date BETWEEN ? AND ?",
                  (emp_id, start_date, end_date))
        present_days = c.fetchone()[0]

        per_day_salary = monthly_salary / working_days
        final_salary = round(per_day_salary * present_days, 2)

        messagebox.showinfo("Salary Calculated",
                            f"Monthly Salary: {monthly_salary:,.0f} PKR\n"
                            f"Working Days: {working_days}\n"
                            f"Present Days: {present_days}\n"
                            f"Per Day: {per_day_salary:,.2f} PKR\n\n"
                            f"Final Salary: {final_salary:,.2f} PKR")
        conn.close()

    Button(salary_frame, text="Calculate Salary", command=calculate_salary).grid(row=0, column=4)
    root.mainloop()

# ---------- START ----------
init_db()
show_login()
