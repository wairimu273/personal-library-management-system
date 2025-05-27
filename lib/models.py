from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    biography = Column(String)
    books = relationship("Book", back_populates="author")

    def __repr__(self):
        return f"<Author(name='{self.name}')>"

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    books = relationship("Book", back_populates="genre")

    def __repr__(self):
        return f"<Genre(name='{self.name}')>"

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    publication_year = Column(Integer)
    read = Column(Boolean, default=False)
    author_id = Column(Integer, ForeignKey('authors.id'))
    genre_id = Column(Integer, ForeignKey('genres.id'))
    author = relationship("Author", back_populates="books")
    genre = relationship("Genre", back_populates="books")

    def __repr__(self):
        return f"<Book(title='{self.title}', author='{self.author.name}')>"