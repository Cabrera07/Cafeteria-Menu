# ☕ Cafeteria Menu Management App

[![Python](https://img.shields.io/badge/Python-3.12.3-336ea0?labelColor=000000&style=for-the-badge&logo=python&logoColor=FFFFFF&link=https://www.python.org/downloads/release/python-3123/)](https://www.python.org/downloads/release/python-3123/)
[![PySide6](https://img.shields.io/badge/PySide6-UI%20Framework-21aa66?labelColor=000000&style=for-the-badge&logo=qt&logoColor=FFFFFF&link=https://pypi.org/project/PySide6/)](https://pypi.org/project/PySide6/)
[![MySQL](https://img.shields.io/badge/MySQL-Database-bf720d?labelColor=000000&style=for-the-badge&logo=mysql&logoColor=FFFFFF&link=https://www.mysql.com/)](https://www.mysql.com/)

A **Python desktop app** for managing cafeteria menu items with CRUD operations and PDF generation.  
Ideal for developers and learners exploring database integration, GUI design, and PDF handling.

![alt text](/assets/images/mockup-main.png)

## ✨ Features

### 🛠 CRUD Functionality for Cafeteria Menu

- Add, update, delete, and view menu items seamlessly.
- **Store detailed information for each menu item, including:**
  - 📸 Image
  - 💲 Price
  - 🏷 Name and ID
  - 📝 Description
  - 📂 Category

### 🔍 Search & Navigate Records

- 🔍 **Search:** Quickly find items with a real-time search field.
- 🔄 **Navigate:** Move through items effortlessly using "Next" and "Previous" buttons.
- 🧹 **Clear Fields:** Reset form fields easily for new data entry.

### 🖨 Generate PDF Reports

- 📝 **Print Single Items:** Generate detailed PDFs for menu items.
- 👁️ **Preview & Print:** View, zoom, save, and print item details directly from the app.

## 🧰 Technologies Used

- 🎨 **[PySide6](https://pypi.org/project/PySide6/)**: For building the user interface.
- 🗄️ **[MySQL](https://www.mysql.com/)**: To manage menu item data efficiently.
- 🖨️ **[ReportLab](https://docs.reportlab.com/)** and **[PyMuPDF](https://pymupdf.readthedocs.io/)**: For generating and previewing PDF reports.

## 📋 Getting Started

***Follow these steps to set up the project on your local machine:***

### 🔧 Prerequisites

- **Python 3.12.3** installed on your system.
- **MySQL server** installed and configured.
- A **virtual environment** (optional but recommended).

### 📦 Installation

1. **Clone this repository:**

    ```bash
    git clone https://github.com/Cabrera07/Cafeteria-Menu.git
    cd CRUD-Menu
    ```

2. **Set up a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    ```

3. **Activate the virtual environment:**

   - On macOS/Linux:
  
        ```bash
        source venv/bin/activate
        ```

   - On Windows:

        ```bash
        venv\Scripts\activate
        ```

4. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Set up the Database:**
    - Import the schema **`from db/schema.sql`** into your MySQL server.
    - Update the database connection details in **`db/config.json`**.

6. **Run the Application:**

    ```bash
    python main.py
    ```

## 🗂 Project Folder Structure

```bash
CRUD-Menu/
│
├── src/                     # Core application files
│   ├── main.py              # Main entry point
│   ├── database.py          # Database functions
│   ├── ui_main.py           # UI setup and logic
│   ├── pdf_generator.py     # PDF creation logic
│   ├── ui_preview.py        # PDF preview functionality
│
├── assets/                  # UI assets (images/icons)
│   └── images/              # Screenshots and logos
│   └── icons/               # App icons
│
├── db/                      # Database files
│   ├── schema.sql           # SQL schema for setup
│   └── config.json          # Database configuration
│
├── LICENSE                  # License for the project
├── README.md                # Project documentation
├── requirements.txt         # Python dependencies           
```

## 📷 Screenshots

***Visualization of the main menu screen and the PDF preview screen:***

![alt text](/assets/images/mockup-2.png)

## 🤝 Contributing

***Contributions are welcome! If you'd like to contribute:***

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch-name`).
3. Commit your changes (`git commit -m "Brief description of changes"`).
4. Push to the branch (`git push origin feature-branch-name`).
5. Open a pull request.

Feel free to report issues or suggest features via the [Issues](https://github.com/Cabrera07/Cafeteria-Menu/issues) tab.

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
