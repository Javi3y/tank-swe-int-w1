from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey
from app.models.users import Author

from sqlalchemy.sql.functions import current_timestamp
class BookAuthor(Base):
    __tablename__ = "book_author"
    author_id = Column(ForeignKey("author.id", ondelete="CASCADE"), nullable=False)
    author = relationship("Author")
    book_id = Column(ForeignKey("book.id", ondelete="CASCADE"), nullable=False)
    book = relationship("Book")
