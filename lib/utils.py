from sqlalchemy.exc import IntegrityError
from lib.models import Book, Author, Genre

def add_book(session, title, author_name, genre_name, year):
    """Add a book to the database, creating author/genre if needed."""
    # Tuple: Predefined valid genres
    valid_genres = ('Fiction', 'Non-Fiction', 'Fantasy', 'Sci-Fi', 'Mystery')
    
    # Validate inputs
    if not title or not author_name or not genre_name:
        raise ValueError("Title, author, and genre are required.")
    # Convert input genre to title case for case-insensitive comparison
    genre_name = genre_name.title()
    if genre_name not in valid_genres:
        raise ValueError(f"Genre must be one of {valid_genres}")
    if year and (year < 0 or year > 2025):
        raise ValueError("Invalid publication year.")

    try:
        # Check if author exists, else create
        author = session.query(Author).filter_by(name=author_name).first()
        if not author:
            author = Author(name=author_name, biography="")
            session.add(author)
            session.flush()  # Get author ID

        # Check if genre exists, else create
        genre = session.query(Genre).filter_by(name=genre_name).first()
        if not genre:
            genre = Genre(name=genre_name)
            session.add(genre)
            session.flush()  # Get genre ID

        # Add book
        book = Book(title=title, publication_year=year, author_id=author.id, genre_id=genre.id)
        session.add(book)
        session.commit()
        return book
    except IntegrityError:
        session.rollback()
        raise ValueError("Book with this title already exists.")

def list_books(session):
    """Return a list of all books."""
    return session.query(Book).all()

def search_books(session, search_term):
    """Search books by title, returning a list and dict of results."""
    results = []
    book_dict = {}
    books = session.query(Book).filter(Book.title.ilike(f'%{search_term}%')).all()
    for book in books:
        results.append(book)
        book_dict[book.id] = {'title': book.title, 'author': book.author.name, 'genre': book.genre.name}
    return results, book_dict

def update_book_read_status(session, book_id, status):
    """Update the read status of a book."""
    valid_statuses = ('read', 'unread')  # Tuple for valid statuses
    if status not in valid_statuses:
        raise ValueError(f"Status must be one of {valid_statuses}")
    
    book = session.query(Book).filter_by(id=book_id).first()
    if not book:
        raise ValueError("Book not found.")
    
    book.read = (status == 'read')
    session.commit()
    return book