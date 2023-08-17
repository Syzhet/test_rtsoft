from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


group_image_association = Table(
    'group_image_association',
    Base.metadata,
    Column('group_id', Integer, ForeignKey('groups.id')),
    Column('image_id', Integer, ForeignKey('images.id'))
)


class Image(Base):
    """Сlass for representing a image in database."""

    __tablename__ = 'images'

    id = Column(Integer(), primary_key=True, unique=True)
    image_url = Column(String(200), nullable=False, unique=True)
    count = Column(Integer(), nullable=False)

    groups = relationship(
        "Group",
        secondary=group_image_association,
        back_populates='images',
        cascade='merge',
        lazy='joined'
    )

    def __str__(self):
        return f'id: {self.id}, image_url: {self.image_url}'


class Group(Base):
    """Сlass for representing a group in database."""

    __tablename__ = 'groups'

    id = Column(Integer(), primary_key=True)
    title = Column(String(), nullable=False, unique=True)
    updated_on = Column(DateTime(), server_default=func.now())
    images = relationship(
        "Image",
        secondary=group_image_association,
        back_populates='groups',
        cascade='merge',
        lazy='joined'
    )

    __mapper_args__ = {"eager_defaults": True}

    def __str__(self):
        return f'id: {self.id}, title: {self.title}'
