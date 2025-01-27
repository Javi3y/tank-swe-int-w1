from app.database import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Column, ForeignKey, String, Enum, DateTime, Integer
import enum
from sqlalchemy_utils import EmailType, PasswordType, URLType

from sqlalchemy.sql.functions import current_timestamp


class Typ(enum.Enum):
    client = "client"
    author = "author"
    admin = "admin"


class User(Base):
    __tablename__ = "user"
    email = Column(EmailType, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    sur_name = Column(String, nullable=False)
    password = Column(
        PasswordType(schemes=["pbkdf2_sha512", "md5_crypt"], deprecated=["md5_crypt"]),
        nullable=False,
    )
    phone_number = Column(String, nullable=False)
    typ = Column(Enum(Typ), nullable=False)
    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": "typ",
    }

    def __str__(self):
        return self.username


class City(Base):
    __tablename__ = "city"
    name = Column(String, nullable=False, unique=True)


class Author(User):
    __tablename__ = "author"
    id = mapped_column(ForeignKey("user.id"), primary_key=True)
    city_id = Column(ForeignKey("city.id", ondelete="CASCADE"), nullable=False)
    city = relationship("City", lazy="selectin")
    goodreads = Column(URLType, nullable=False, unique=True)
    bank_acount = Column(String, nullable=False, unique=True)

    books = relationship(
        "Book", secondary="book_author", back_populates="authors", lazy="selectin"
    )

    __mapper_args__ = {
        "polymorphic_identity": Typ("author"),
    }


class SubscriptionEnum(enum.Enum):
    free = 1
    plus = 2
    premium = 3


class Admin(User):
    __tablename__ = "admin"
    id = mapped_column(ForeignKey("user.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": Typ("admin"),
    }


class Client(User):
    __tablename__ = "client"
    id = mapped_column(ForeignKey("user.id"), primary_key=True)
    balance = Column(Integer, nullable=False, default=0)
    __mapper_args__ = {
        "polymorphic_identity": Typ("client"),
    }


class Subscription(Base):
    __tablename__ = "subscription"
    client_id = Column(ForeignKey("client.id", ondelete="CASCADE"), nullable=False)
    client = relationship("Client")
    subscription_model = Column(Enum(SubscriptionEnum), nullable=False)
    start = Column("start", DateTime(), default=current_timestamp(), nullable=False)
    end = Column("end", DateTime(), default=current_timestamp(), nullable=False)
