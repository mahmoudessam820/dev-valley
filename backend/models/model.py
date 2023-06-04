import datetime
# from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin


db: SQLAlchemy = SQLAlchemy()
bcrypt: Bcrypt = Bcrypt()


class Users(db.Model, UserMixin):

    __tablename__: str = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    image = db.Column(db.String(), nullable=True)
    website = db.Column(db.String(), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text(), nullable=True)
    skills_languages = db.Column(db.Text(), nullable=True)
    joined_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now)
    is_active = db.Column(db.Boolean, default=True)
    is_staff = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships
    articles = db.relationship(
        'Articles', backref='users', lazy=True, cascade='all, delete')
    comments = db.relationship(
        'Comments', backref='users', lazy=True, cascade='all, delete')

    def __init__(self, **data: dict[str, dict]) -> None:

        self.username: str = data.get('username')
        self.email: str = data.get('email')
        self.password: str = data.get('password')
        self.image: str = data.get('image')
        self.website: str = data.get('website')
        self.location: str = data.get('location')
        self.bio: str = data.get('bio')
        self.skills_languages: str = data.get('skills_languages')
        self.is_active: bool = data.get('is_active', True)
        self.is_staff: bool = data.get('is_staff', False)
        self.is_admin: bool = data.get('is_admin', False)

    def __repr__(self) -> str:
        return f"User('{self.username}' , '{self.email}', '{self.password}')"

    @classmethod
    def create_admin(cls, **kwargs: dict[str, str]) -> None:
        """
        Creates a Admin and saves it to the database.
        """
        password = bcrypt.generate_password_hash(
            kwargs.get('password')).decode('utf-8')
        admin = cls(
            username=kwargs.get('username'),
            email=kwargs.get('email'),
            password=password,
            image=kwargs.get('image'),
            website=kwargs.get('website'),
            location=kwargs.get('location'),
            bio=kwargs.get('bio'),
            skills_languages=kwargs.get('skills_languages'),
            is_admin=True,
            is_staff=True,
            is_active=True
        )
        db.session.add(admin)
        db.session.commit()

    @classmethod
    def create_user(cls, **kwargs: dict[str, str]) -> None:
        """
        Creates a new regular user and saves it to the database.
        """
        password = bcrypt.generate_password_hash(
            kwargs.get('password')).decode('utf-8')
        user = cls(
            username=kwargs.get('username'),
            email=kwargs.get('email'),
            password=password,
            image=kwargs.get('image'),
            website=kwargs.get('website'),
            location=kwargs.get('location'),
            bio=kwargs.get('bio'),
            skills_languages=kwargs.get('skills_languages'),
            is_active=True,
            is_staff=False,
            is_admin=False
        )
        db.session.add(user)
        db.session.commit()

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password, password)

    def update(self) -> None:
        self.username
        self.email
        self.password = bcrypt.generate_password_hash(
            self.password).decode('utf-8')
        self.image
        self.website
        self.location
        self.bio
        self.skills_languages

        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def serialize(self) -> dict[str]:

        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "image": self.image,
            "website": self.website,
            "location": self.location,
            "bio": self.bio,
            "skills_languages": self.skills_languages,
        }


class Premissions:
    pass


class Articles(db.Model):

    __tablename__: str = 'articles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    body = db.Column(db.Text(), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now)

    # Foreign Keys
    author_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    commetns = db.relationship(
        'Comments', backref='articles', lazy=True, cascade='all, delete')

    def __init__(self, **data: dict[str, str]) -> None:

        self.title = data.get('title')
        self.slug = data.get('slug')
        self.body = data.get('body')
        self.category = data.get('category')
        self.author_id = data.get('author_id')

    def __repr__(self) -> str:
        return f"Article('{self.title}', '{self.slug}', '{self.body}')"

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def update(self) -> None:
        self.title
        self.slug
        self.body
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def serialize(self) -> dict[str]:

        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "body": self.body,
            "category": self.category,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "author_id": self.author_id,
        }


class Comments(db.Model):

    __tablename__: str = 'comments'

    id = db.Column(db.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    body = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now)

    # Foreign Keys
    commenter_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)
    article_id = db.Column(
        db.Integer, db.ForeignKey('articles.id'), nullable=False)
