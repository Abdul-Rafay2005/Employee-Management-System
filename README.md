

 🧑‍💼 Employee Management System (with Attendance & Authentication)

A simple **Employee Management System** built with **Python**, **Tkinter** for the GUI, and **SQLite** for data storage. This system includes login authentication, employee CRUD operations, and attendance tracking (extendable).

---

📋 Features

✅ User Login with Authentication
✅ Add, Update, and Delete Employee Records
✅ Search Employees by Name or ID
✅ Responsive Treeview for Viewing Records
✅ SQLite Integration (No external DB needed)
✅ Styled GUI with Tkinter

---

💻 Technologies Used

| Component | Tech                                       |
| --------- | ------------------------------------------ |
| Language  | Python 3.x                                 |
| GUI       | Tkinter                                    |
| Database  | SQLite3                                    |
| Styling   | Tkinter `ttk`, custom layout               |
| Structure | Modular functions (login, init, app logic) |

---

 🚀 Getting Started

1. Clone the Repository

```bash
git clone https://github.com/your-username/employee-management-system.git
cd employee-management-system
```

2. Run the Application

Ensure Python 3.x is installed, then:

```bash
python app.py
```

> ✅ On first run, it will automatically create the database and a default user.

---

 🔐 Default Admin Login

```
Username: admin
Password: admin
```

You can change or extend this in the `users` table of `database.db`.

---

 📂 Project Structure

```
employee-management-system/
│
├── app.py               # Main application script
├── database.db          # SQLite database (auto-created)
├── README.md            # Project documentation
```



 🔐 Login Screen

A clean and centered login interface.

📋 Employee Dashboard

Add, update, delete, and view employee data.


 🛠️ Future Improvements (Ideas)

* Attendance Check-in / Check-out Feature
* Monthly Attendance Summary
* Role-based Access (Admin / HR / Staff)
* Export to CSV or PDF
* UI theme switcher (Dark/Light)

 🤝 Contributing

Pull requests are welcome! Please fork the repository and submit your changes via a PR. For major changes, open an issue first to discuss what you’d like to change.

 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

