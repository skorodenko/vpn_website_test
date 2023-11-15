from app import db
from uuid import UUID, uuid4
from typing import List
from typing_extensions import Annotated
from sqlalchemy import String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


pkuuid4 = Annotated[UUID, mapped_column(primary_key=True, default=uuid4)]
fkuuid4 = Annotated[UUID, mapped_column()]
str60 = Annotated[str, mapped_column(String(60))]
str256 = Annotated[str, mapped_column(String(256))]
data_bytes = Annotated[float, mapped_column(Float(3), default = 0.0)]


class User(db.Model):
    __tablename__ = "user"
    
    id: Mapped[pkuuid4]
    username: Mapped[str60] = mapped_column(unique=True)
    password: Mapped[str60]
    authenticated: Mapped[bool] = mapped_column(default=False)
    websites: Mapped[List["Website"]] = relationship(
        cascade="all, delete-orphan",
        back_populates="user"
    )
    
    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False
 
 
class Website(db.Model):
    __tablename__ = "website"
    
    id: Mapped[pkuuid4]
    url: Mapped[str256]
    user_id: Mapped[fkuuid4] = mapped_column(
        ForeignKey("user.id"), 
    )
    user: Mapped["User"] = relationship(
        back_populates="websites",
        single_parent=True,
    )
    usage: Mapped[List["UsageTrack"]] = relationship(
        back_populates="website", 
        cascade="all, delete-orphan"
    )
    

class UsageTrack(db.Model):
    __tablename__ = "usage_track"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    website_id: Mapped[fkuuid4] = mapped_column(
        ForeignKey("website.id"), 
    )
    website: Mapped["Website"] = relationship(
        back_populates="usage",
        single_parent=True,
    )
    downloaded: Mapped[data_bytes]
    uploaded: Mapped[data_bytes]
    
    