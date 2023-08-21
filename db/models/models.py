from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func

Base = declarative_base()


category_image_association: Table = Table(
    'category_image_association',
    Base.metadata,
    Column('category_id', Integer, ForeignKey('categories.id')),
    Column('image_id', Integer, ForeignKey('images.id'))
)


class DateBase(Base):
    """
    Абстрактный класс для добавления поля даты
    в классы где это необходимо.
    """

    __abstract__ = True

    updated_on = Column(
        DateTime(),
        server_default=func.now(),
        onupdate=func.now()
    )


class Image(DateBase):
    """Класс для работы с данными изображений."""

    __tablename__ = 'images'

    id = Column(Integer(), primary_key=True, unique=True)
    image_url = Column(String(200), nullable=False, unique=True)
    count = Column(Integer(), nullable=False)

    categories = relationship(
        "Category",
        secondary=category_image_association,
        back_populates='images',
        cascade='merge',
        lazy='joined'
    )

    @validates('categories')
    def validate_categories(self, key, value):
        if len(self.categories) >= 10:
            raise SQLAlchemyError(
                f"Изображение ({self.image_url.split('/')[-1]}) "
                "не может быть связано более чем с 10 категориями."
            )
        return value

    def __str__(self):
        return f'id: {self.id}, image_url: {self.image_url}'


class Category(DateBase):
    """Класс для работы с данными категорий."""

    __tablename__ = 'categories'

    id = Column(Integer(), primary_key=True)
    title = Column(String(100), nullable=False, unique=True)
    images = relationship(
        "Image",
        secondary=category_image_association,
        back_populates='categories',
        cascade='merge',
        lazy='joined'
    )

    __mapper_args__ = {"eager_defaults": True}

    def __str__(self):
        return f'id: {self.id}, title: {self.title}'
