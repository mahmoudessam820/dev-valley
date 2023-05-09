from flask import Blueprint, abort


feed_bp = Blueprint('feed_bp', __name__)


@feed_bp.route('/', methods=['GET'])
@feed_bp.route('/home')
def home():
    return '<h1>Hello world!!</h1>'
