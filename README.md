# ☕ Cafeteria Menu Management App

A desktop application built in Python to manage a cafeteria menu. This system provides a simple, user-friendly interface for managing menu items with full CRUD (Create, Read, Update, Delete) functionality. It also includes options for PDF generation and print preview.

![alt text](/assets/images/mockup-main.png)

## ✨ Features

### 🛠 CRUD Functionality for Cafeteria Menu

- **Add, Update, Delete, and View** menu items from a single screen.
- Each menu item includes:
  - 📸 Image
  - 💲 Price
  - 🏷 Name and ID
  - 📝 Description
  - 📂 Category

### 🔍 Search & Navigation

- 🔍 **Search:** Quickly find menu items with a convenient search field.
- 🔄 **Navigation:** Move through records using “Next” and “Previous” buttons.
- 🧹 **Clear Fields:** Easily clear input fields to reset or add new information.

### 🖨 Print and PDF Generation

- 📝 **Print Information:** Generate a detailed PDF report of any menu item, including its image and details.
- 👁️ **Preview & Print:** Preview the PDF, zoom in/out, save, and print directly from the app with print-specific formatting.

## 🧰 Technologies Used

- 🎨 **PySide6:** For the UI components and layout.
- 🗄️ **MySQL:** Database management.
- 🖨️ **ReportLab & PyMuPDF:** PDF generation and preview with print support.

## 📋 Getting Started

Follow these steps to set up the project on your local machine.

### 🔧 Prerequisites

- **Python 3.12.3** installed on your system (developed and tested with Python 3.12.3).
- **MySQL server installed** and configured.
- **Virtual environment** (optional but recommended) to manage dependencies.

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

4. **Install required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Set up the Database:**
    - Import the schema provided in **`db/schema.sql`** into your MySQL server.
    - Update the database connection details in **`db/config.json`**.

6. **Run the Application:**

    ```bash
    python main.py
    ```

## 📋 Usage

- ✏️ CRUD Operations: Add, update, delete, or view any menu item in the system.
- 🔎 Search: Use the search bar to find specific items quickly.
- 🖨️ Preview and Print: Preview the PDF of any item’s details and print directly from the app.
- ⬅️➡️ Navigation: Easily move between records using the “Next” and “Previous” buttons.

## 🗂 Project Folder Structure

```bash
CRUD-Menu/
│
├── src/                     
│   ├── main.py              # Main entry point for the application
│   ├── database.py          # Database connection and CRUD functions
│   ├── ui_main.py           # PySide UI setup and logic (manual UI creation)
│   ├── pdf_generator.py     # PDF generation with ReportLab
│   ├── ui_preview.py        # PDF preview with zoom, save, and printing options
│   ├── resources_rc.py      
│   ├── resources_rc.qrc     
│
├── assets/                  
│   └── images/              # Contains UI screenshots, logo
│   └── icons/               # UI icons
│
├── db/                      
│   ├── schema.sql           # Database schema setup
│   └── config.json          # Database configuration (e.g., credentials)
│
├── README.md                # Project description and usage guide
└── requirements.txt         # Python dependencies for the project                 
```

## 📷 Screenshots

***Visualization of the main menu screen and the PDF preview screen:***

![alt text](/assets/images/mockup-2.png)

## 🤝 Contributing

Contributions are welcome! To contribute:

1. **Fork the repository**.
2. **Create a new branch** (`git switch -c feature-branch`).
3. **Use Conventional Commits** for your commit messages:
    - **`feat:`** A new feature.

    - **`fix:`** A bug fix.

    - **`docs:`** Documentation changes.

    - **`style:`** Code style changes.

    - **`refactor:`** Refactoring existing code.

    - **`test:`** Adding or updating tests.

4. **Branch Structure:**

    - **`main:`** The stable branch for production-ready code.
  
    - **`develop:`** The development branch where new features and bug fixes are merged before going to main.
  
    - **`feature:`** Feature-specific branches, each created off develop.

5. **Create a Pull Request** from your feature branch to the **`develop`** branch once your changes are ready for review.

6. **Submit your pull** request for review.
