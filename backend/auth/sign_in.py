from flask import (jsonify, request, Blueprint)
from flask_login import login_user

from models.model import Users, db


sign_in_bp: Blueprint = Blueprint('sign_in_bp', __name__)


@sign_in_bp.route('/signin', methods=['POST'])
def signin() -> None:
    try:
        if request.method == 'POST':

            data = request.get_json()
            username = data['username']
            email = data['email']
            password = data['password']

            # Chech if the admin already exists
            admin_user = Users.query.filter_by(
                is_admin=True, is_staff=True).first()

            if not admin_user:
                # Create a new admin
                Users.create_admin(
                    username=username, email=email, password=password)

                return jsonify({
                    'success': True,
                    'message': 'Admin created successfully',
                }), 201

            # Check if the user exists
            existing_user: Users = Users.query.filter_by(email=email).first()

            if existing_user:
                return jsonify({
                    'success': False,
                    'message': 'User already exists',
                }), 409

            # Create new regular user
            Users.create_user(
                username=username, email=email, password=password)
            return jsonify({
                'success': True,
                'message': 'User created successfully',
            }), 201

    except KeyError:
        # Invalid request body
        return jsonify({
            'success': False,
            'error': 'Invalid request body',
        }), 400
    except Exception as e:
        # Other errors handling
        return jsonify({
            'success': False,
            'error': str(e),
        }), 500
