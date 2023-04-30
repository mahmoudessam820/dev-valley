from flask import Blueprint, abort


home_bp = Blueprint('home_bp', __name__)


@home_bp.route('/', methods=['GET'])
@home_bp.route('/home')
def home():
    return '<h1>Hello from fun :)</h1>'
