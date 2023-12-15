from sqlalchemy import (Column, DateTime, ForeignKey, Integer, LargeBinary,
                        String, func)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Image(Base):
    __tablename__ = "images"

    id = Column(String(64), primary_key=True)
    data = Column(LargeBinary)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    faces = relationship("Face", backref="image", lazy="joined")


class Face(Base):
    __tablename__ = "faces"

    id = Column(String(64), primary_key=True)

    x = Column(Integer)
    y = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    image_id = Column(
        String(64), ForeignKey("images.id", ondelete="CASCADE"), nullable=False
    )
