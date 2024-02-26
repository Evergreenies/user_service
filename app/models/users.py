import re
from typing import Any
import argon2

from datetime import datetime
from uuid import uuid4

from marshmallow import Schema, fields
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates

try:
    from config import EMAIL_REGEX
    from models.database_setup import Base
except ImportError:
    from app.config import EMAIL_REGEX
    from app.models.database_setup import Base


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    deleted_at = Column(DateTime, default=datetime.utcnow)

    @validates("email")
    def validates_email(self, key: str, value: str) -> str:
        if not re.match(EMAIL_REGEX, value):
            raise ValueError("Invalid email format.")
        return value

    @validates("password")
    def set_password(self, key: str, value: str) -> str:
        return argon2.PasswordHasher().hash(value)

    def check_password(self, value: str) -> bool:
        try:
            print("PASSSWORD CHECK ======> ", value, self.password)
            return argon2.PasswordHasher().verify(self.password, value)
        except:
            return False

    def __repr__(self) -> str:
        return f"<User {self.username} {self.email}>"


class UserSchema(Schema):
    id = fields.UUID()
    username = fields.String()
    email = fields.Email()
    first_name = fields.String()
    last_name = fields.String()
    created_at = fields.DateTime()
    deleted_at = fields.DateTime()
