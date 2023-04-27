import datetime
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

# config
db: SQLAlchemy = SQLAlchemy()
bcrypt: Bcrypt = Bcrypt()


class User(db.Model, UserMixin):

    __tablename__: str = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_staff = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    articles = db.relationship('Article', backref='user', lazy=True)

    def __init__(self, name, email, password_hash) -> None:
        self.name = name
        self.email = email
        self.password_hash = password_hash

    def __repr__(self) -> str:
        return f"User('{self.name}' , '{self.email}')"

    def set_password(self, password) -> None:
        self.password_hash = bcrypt.generate_password_hash(
            password).decode('utf-8')

    def check_password(self, password) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def update(self, username, email) -> None:
        self.username = username
        self.email = email

        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def create_admin(cls, username, email, password) -> None:

        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        admin = cls(username=username, email=email,
                    password_hash=password_hash, is_admin=True, is_staff=True)
        db.session.add(admin)
        db.session.commit()
        return admin

    def serialize(self) -> dict[str]:

        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }


class Article(db.Model):

    __tablename__: str = 'article'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unllable=False)
    body = db.Column(db.Text(), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, id, title, body, author_id) -> None:

        self.id = id,
        self.title = title,
        self.body = body,
        self.author_id = author_id

    def __repr__(self) -> str:
        return f"Article('{self.title}', '{self.body}')"

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def update(self, title, body) -> None:
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
