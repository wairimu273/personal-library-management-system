import pytest
from sqlalchemy.orm import sessionmaker
from lib.database import engine
from lib.models import Book, Author, Genre
from lib.utils import add_book, list_books, search_books, update_book_read_status

Session = sessionmaker(bind=engine)

@pytest.fixture
def db_session():
    session = Session()
    yield session
    session.query(Book).delete()
    session.query(Author).delete()
    session.query(Genre).delete()
    session.commit()
    session.close()

def test_add_book(db_session):
    book = add_book(db_session, "Test Book", "Test Author", "Fiction", 2020)
    assert book.title == "Test Book"
    assert book.author.name == "Test Author"
    assert book.genre.name == "Fiction"
    assert book.publication_year == 2020
    assert book.read is False

def test_list_books(db_session):
    add_book(db_session, "Book One", "Author One", "Fiction", 2020)
    add_book(db_session, "Book Two", "Author Two", "Sci-Fi", 2021)
    books = list_books(db_session)
    assert len(books) == 2
    assert books[0].title == "Book One"
    assert books[1].title == "Book Two"

def test_search_books(db_session):
    add_book(db_session, "Python Programming", "John Doe", "Non-Fiction", 2022)
    results, book_dict = search_books(db_session, "Python")
    assert len(results) == 1
    assert results[0].title == "Python Programming"
    assert book_dict[results[0].id]['title'] == "Python Programming"

def test_update_book_read_status(db_session):
    book = add_book(db_session, "Test Book", "Test Author", "Fiction", 2020)
    update_book_read_status(db_session, book.id, "read")
    updated_book = db_session.query(Book).filter_by(id=book.id).first()
    assert updated_book.read is True
    update_book_read_status(db_session, book.id, "unread")
    updated_book = db_session.query(Book).filter_by(id=book.id).first()
    assert updated_book.read is False