# personal-library-management-system

Personal Library Management System
A command-line interface (CLI) application for managing a personal book library, built with Python, SQLAlchemy, and Click. Users can add, list, search, and update books, with data stored in a SQLite database.
Setup Instructions

Clone the repository: git clone https://github.com/<your-username>/personal-library-management-system.git
Navigate to the project directory: cd personal-library-management-system
Install Pipenv: pip install pipenv
Activate the virtual environment: pipenv shell
Install dependencies: pipenv install
Run the CLI: python main.py

Usage

Add a book: python main.py add-book --title "Book Title" --author "Author Name" --genre "Genre" --year 2020
List all books: python main.py list-books
Search books by title: python main.py search-books --title "keyword"
Update read status: python main.py update-read --id 1 --status read

Project Structure

lib/: Contains models, database setup, CLI commands, and utilities.
tests/: Unit tests for the application.
main.py: Entry point for the CLI.
