from flask import (Blueprint, request, jsonify)
from flask_login import login_user

from models.model import Users

login_bp: Blueprint = Blueprint('login_bp', __name__)


@login_bp.route('/login', methods=['POST'])
def login() -> None:
    try:

        data = request.get_json()
        email = data['email']
        password = data['password']

        user: Users = Users.query.filter_by(email=email).first()

        if user and user.check_password(password):

            login_user(user)

            return jsonify({
                'success': True,
                'message': 'Logged in successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid Email or Password'
            }), 401

    except KeyError:
        # Invalid request
        return jsonify({
            'success': False,
            'error': 'Invalid request',
        }), 400
    except Exception as e:
        # Other errors handling
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
