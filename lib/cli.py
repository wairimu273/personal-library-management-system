import click
from sqlalchemy.orm import sessionmaker
from lib.database import engine
from lib.utils import add_book, list_books, search_books, update_book_read_status

Session = sessionmaker(bind=engine)

@click.group()
def cli():
    """Personal Library Management System CLI."""
    pass

@cli.command()
@click.option('--title', prompt='Book title', help='Title of the book')
@click.option('--author', prompt='Author name', help='Author of the book')
@click.option('--genre', prompt='Genre', help='Genre of the book')
@click.option('--year', prompt='Publication year', type=int, help='Publication year')
def add_book_cmd(title, author, genre, year):
    """Add a book to the library."""
    session = Session()
    try:
        book = add_book(session, title, author, genre, year)
        click.echo(f"Added book: {book.title} by {book.author.name} ({book.genre.name}, {book.publication_year})")
    except ValueError as e:
        click.echo(f"Error: {e}")

@cli.command()
def list_books_cmd():
    """List all books in the library."""
    session = Session()
    books = list_books(session)
    if not books:
        click.echo("No books found.")
        return
    for book in books:
        status = "Read" if book.read else "Unread"
        click.echo(f"{book.id}: {book.title} by {book.author.name} ({book.genre.name}, {book.publication_year}) - {status}")

@cli.command()
@click.option('--title', prompt='Search term', help='Search books by title')
def search_books_cmd(title):
    """Search books by title."""
    session = Session()
    results, book_dict = search_books(session, title)
    if not results:
        click.echo("No books found.")
        return
    for book in results:
        click.echo(f"{book.id}: {book.title} by {book.author.name} ({book.genre.name})")

@cli.command()
@click.option('--id', prompt='Book ID', type=int, help='ID of the book to update')
@click.option('--status', prompt='Status (read/unread)', help='Read status of the book')
def update_read_cmd(id, status):
    """Update the read status of a book."""
    session = Session()
    try:
        book = update_book_read_status(session, id, status)
        click.echo(f"Updated {book.title} to {'Read' if book.read else 'Unread'}")
    except ValueError as e:
        click.echo(f"Error: {e}")