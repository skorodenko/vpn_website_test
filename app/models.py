from app import db
from uuid import UUID, uuid4
from typing_extensions import Annotated
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


pkuuid4 = Annotated[UUID, mapped_column(primary_key=True, default=uuid4)]
str60 = Annotated[str, mapped_column(String(60))]


class User(db.Model):
    __tablename__ = "user"
    
    id: Mapped[pkuuid4]
    authenticated: Mapped[bool] = mapped_column(default=False)
    username: Mapped[str60] = mapped_column(unique=True)
    password: Mapped[str60]
    
    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False
    