from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, ForeignKey, DateTime, Integer, text

from sqlalchemy.sql.functions import current_timestamp

class Reservation(Base):
    __tablename__ = "reservation"
    client_id = Column(ForeignKey("client.id", ondelete="CASCADE"), nullable=False)
    client = relationship("Client")
    book_id = Column(ForeignKey("book.id", ondelete="CASCADE"), nullable=False)
    book = relationship("Book")
    start = Column("start", DateTime(), default=current_timestamp(), nullable=False)
    end = Column("end", DateTime(), default=current_timestamp(), nullable=False)
    price = Column(Integer, nullable=False)
    position = Column(Integer, nullable=False, server_default=text("0"))
    is_satisfied = Column(Boolean, nullable=False, server_default=text("false"))
    is_done = Column(Boolean, nullable=False, server_default=text("false"))
