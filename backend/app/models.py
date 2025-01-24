from .database import Base
from sqlalchemy import (
    Boolean,
    Column,
    String,
)
from sqlalchemy_utils import EmailType, PasswordType

class User(Base):
    __tablename__ = "users"
    email = Column(EmailType, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(
        PasswordType(schemes=["pbkdf2_sha512", "md5_crypt"], deprecated=["md5_crypt"]),
        nullable=False,
    )
    is_supper_user = Column(Boolean, nullable=False, server_default="False")

    def __str__(self):
        return self.username
