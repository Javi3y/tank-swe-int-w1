from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, ForeignKey, DateTime, text

from sqlalchemy.sql.functions import current_timestamp


class Reservation(Base):
    __tablename__ = "reservation"
    client_id = Column(ForeignKey("client.id", ondelete="CASCADE"), nullable=False)
    client = relationship("Client", lazy="selectin")
    book_id = Column(ForeignKey("book.id", ondelete="CASCADE"), nullable=False)
    book = relationship("Book", lazy="selectin")
    start = Column("start", DateTime(), default=current_timestamp(), nullable=False)
    end = Column("end", DateTime(), default=current_timestamp(), nullable=False)
    is_ended = Column(
        "is_ended", Boolean(), server_default=text("false"), nullable=False
    )


class ReservationQueue(Base):
    __tablename__ = "reservation_queue"
    client_id = Column(ForeignKey("client.id", ondelete="CASCADE"), nullable=False)
    client = relationship("Client", lazy="selectin")
    book_id = Column(ForeignKey("book.id", ondelete="CASCADE"), nullable=False)
    book = relationship("Book", lazy="selectin")
