# ☕ Cafeteria Menu Management App

[![Python](https://img.shields.io/badge/Python-3.12.3-336ea0?labelColor=000000&style=for-the-badge&logo=python&logoColor=FFFFFF&link=https://www.python.org/downloads/release/python-3123/)](https://www.python.org/downloads/release/python-3123/)
[![PySide6](https://img.shields.io/badge/PySide6-UI%20Framework-21aa66?labelColor=000000&style=for-the-badge&logo=qt&logoColor=FFFFFF&link=https://pypi.org/project/PySide6/)](https://pypi.org/project/PySide6/)
[![MySQL](https://img.shields.io/badge/MySQL-Database-bf720d?labelColor=000000&style=for-the-badge&logo=mysql&logoColor=FFFFFF&link=https://www.mysql.com/)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-5d0000?labelColor=000000&style=for-the-badge&logo=opensourceinitiative&logoColor=FFFFFF)](LICENSE)

A **Python desktop application** for managing and printing individual menu items with ease. This app provides an intuitive interface for handling **CRUD operations** (Create, Read, Update, Delete) and includes features like **PDF generation** and **print preview** included to provide additional features.

![alt text](/assets/images/mockup-main.png)

## 📚 Table of Contents

- [☕ Cafeteria Menu Management App](#-cafeteria-menu-management-app)
  - [📚 Table of Contents](#-table-of-contents)
  - [✨ Features](#-features)
    - [🛠 CRUD Functionality for Cafeteria Menu](#-crud-functionality-for-cafeteria-menu)
    - [🔍 Search \& Navigate Records](#-search--navigate-records)
    - [🖨 Generate PDF Reports](#-generate-pdf-reports)
  - [🧰 Technologies Used](#-technologies-used)
  - [📋 Getting Started](#-getting-started)
    - [🔧 Prerequisites](#-prerequisites)
    - [📦 Installation](#-installation)
  - [📋 Usage](#-usage)
  - [🗂 Project Folder Structure](#-project-folder-structure)
  - [📷 Screenshots](#-screenshots)
  - [🤝 Contributing](#-contributing)
    - [📝 Reporting Issues](#-reporting-issues)
    - [🔧 Submitting Code Changes](#-submitting-code-changes)
  - [📜 License](#-license)

## ✨ Features

### 🛠 CRUD Functionality for Cafeteria Menu

- Add, update, delete, and view menu items seamlessly.
- Store detailed information for each menu item, including:
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

- 📝 **Print Single Items:** Create a detailed PDF report for individual menu items.
- 👁️ **Preview & Print:** View, zoom, save, and print item details directly from the app.

## 🧰 Technologies Used

***This application uses modern tools and libraries to deliver a robust user experience:***

- 🎨 **PySide6**: For building the user interface.
- 🗄️ **MySQL**: To manage menu item data efficiently.
- 🖨️ **ReportLab** and **PyMuPDF**: For generating and previewing PDF reports.

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

## 📋 Usage

***Here’s how you can use the app:***

- ✏️ **CRUD Operations**: Add, update, delete, or view menu items.
- 🔎 **Search**: Use the search bar to find items by name or category.
- 🖨️ **Preview & Print**: Preview a PDF of item details and print it.
- ⬅️➡️ **Navigation**: Use "Next" and "Previous" to browse menu items.

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

**Contributions are welcome! To contribute:**

### 📝 Reporting Issues

***If you encounter a bug or have a feature request, you can:***

1. Go to the **[Issues](https://github.com/Cabrera07/Cafeteria-Menu/issues)** tab.
2. Click **New Issue** and provide a clear description of the problem or suggestion.
3. Use labels like `bug`, `enhancement`, or `question` to categorize your issue.

### 🔧 Submitting Code Changes

1. **Fork the repository**.
2. **Create a new branch** (`git switch -c feature-branch`).
3. Make your changes and **use Conventional Commits** for your commit messages:
    - **`feat:`** A new feature.
    - **`fix:`** A bug fix.
    - **`docs:`** Documentation changes.
    - **`style:`** Code style changes.
    - **`refactor:`** Refactoring existing code.
    - **`test:`** Adding or updating tests.

4. **Follow Branch Structure**:
    - **`main:`** The stable branch for production-ready code.
    - **`develop:`** The development branch where new features and bug fixes are merged before going to main.
    - **`feature:`** Feature-specific branches, each created off develop.

5. **Create a Pull Request**:
   - Push your branch to your forked repository.
   - Open a **pull request** to the `develop` branch in this repository.
   - Provide a clear description of your changes, linking to related issues if applicable.

6. **Wait for Review**:
   - Your pull request will be reviewed, and feedback may be provided.
   - Once approved, your changes will be merged.

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
