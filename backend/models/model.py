import datetime
from sqlalchemy import *
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
    password_hash = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_staff = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    articles = db.relationship('Articles', backref='users', lazy=True)

    def __init__(self, username: str, email: str, password_hash: str, is_active: bool, is_admin: bool, is_staff: bool) -> None:
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.is_active = is_active
        self.is_admin = is_admin
        self.is_staff = is_staff

    def __repr__(self) -> str:
        return f"User('{self.username}' , '{self.email}', '{self.password_hash}')"

    @classmethod
    def create_admin(cls, username: str, email: str, password: str, is_active: bool = True) -> None:
        """
        Creates a Admin and saves it to the database.
        """
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        admin = cls(username=username, email=email,
                    password_hash=password_hash, is_admin=True, is_staff=True, is_active=is_active)
        db.session.add(admin)
        db.session.commit()

    @classmethod
    def create_user(cls, username: str, email: str, password: str, is_active: bool = True) -> None:
        """
        Creates a new regular user and saves it to the database.
        """
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        user = cls(username=username, email=email,
                   password_hash=password_hash, is_admin=False, is_staff=False, is_active=is_active)
        db.session.add(user)
        db.session.commit()

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

    def update(self) -> None:
        self.username
        self.email
        self.password_hash = bcrypt.generate_password_hash(
            self.password_hash).decode('utf-8')

        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def serialize(self) -> dict[str]:

        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }


class Articles(db.Model):

    __tablename__: str = 'articles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text(), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)

    author_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, title: str, body: str, author_id: int) -> None:

        self.title = title,
        self.body = body,
        self.author_id = author_id

    def __repr__(self) -> str:
        return f"Article('{self.title}', '{self.body}')"

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def update(self, title: str, body: str) -> None:
        self.title = title
        self.body = body
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def serialize(self) -> dict[str]:

        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "date_created": self.date_created,
            "author_id": self.author_id,
        }
