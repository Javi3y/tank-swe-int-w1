from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, String, DateTime, Integer

from sqlalchemy.sql.functions import current_timestamp


class Genre(Base):
    __tablename__ = "genre"
    name = Column(String, nullable=False, unique=True)


class Book(Base):
    __tablename__ = "book"
    title = Column(String, nullable=False)
    isbn = Column(String, nullable=False, unique=True)
    price = Column(Integer, nullable=False)
    units = Column(Integer, nullable=False, default=0)
    description = Column(String, nullable=False)

    authors = relationship(
        "Author", secondary="book_author", back_populates="books", lazy="selectin"
    )


class BookAuthor(Base):
    __tablename__ = "book_author"
    author_id = Column(ForeignKey("author.id", ondelete="CASCADE"), nullable=False)
    author = relationship("Author")
    book_id = Column(ForeignKey("book.id", ondelete="CASCADE"), nullable=False)
    book = relationship("Book")


class BookGenre(Base):
    __tablename__ = "book_genre"
    genre_id = Column(ForeignKey("genre.id", ondelete="CASCADE"), nullable=False)
    genre = relationship("Genre")
    book_id = Column(ForeignKey("book.id", ondelete="CASCADE"), nullable=False)
    book = relationship("Book")


class Reservation(Base):
    __tablename__ = "reservation"
    client_id = Column(ForeignKey("client.id", ondelete="CASCADE"), nullable=False)
    client = relationship("Client")
    book_id = Column(ForeignKey("book.id", ondelete="CASCADE"), nullable=False)
    book = relationship("Book")
    start = Column("start", DateTime(), default=current_timestamp(), nullable=False)
    end = Column("end", DateTime(), default=current_timestamp(), nullable=False)
    price = Column(Integer, nullable=False)
