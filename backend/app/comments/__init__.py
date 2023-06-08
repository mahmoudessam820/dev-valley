from flask import Blueprint


comment: Blueprint = Blueprint('comment', __name__)


from . import views