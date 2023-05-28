import re
from flask import (jsonify, request, Blueprint)
from flask_login import login_user

from models.model import Users


sign_in_bp: Blueprint = Blueprint('sign_in_bp', __name__)


def is_valid_email(email):
    """
    Validate email format using regex.
    """
    pattern = r'^\S+@\S+\.\S+$'
    return re.match(pattern, email)


@sign_in_bp.route('/signin', methods=['POST'])
def signin() -> None:
    try:
        if request.method == 'POST':

            data = request.get_json()

            username = data['username']
            email = data['email']
            password = data['password']
            image = data['image']
            website = data['website']
            location = data['location']
            bio = data['bio']
            skills_languages = data['skills_languages']

            # Check if email is valid
            if not is_valid_email(email):
                return jsonify({
                    'success': False,
                    'error': 'Invalid email',
                }), 400

            # Chech if the admin already exists
            queryset: Users = Users.query.filter_by(
                is_admin=True, is_staff=True).first()

            if not queryset:

                # Create a new admin
                Users.create_admin(
                    username=username,
                    email=email,
                    password=password,
                    image=image,
                    website=website,
                    location=location,
                    bio=bio,
                    skills_languages=skills_languages
                )

                admin_user: Users = Users.query.first()
                login_user(admin_user)

                return jsonify({
                    'success': True,
                    'message': 'Admin created successfully',
                }), 201

            # Check if the user exists
            existing_user: Users = Users.query.filter_by(email=email).first()

            if existing_user:
                return jsonify({
                    'success': False,
                    'message': 'Email already exists',
                }), 409

            # Create new regular user
            Users.create_user(
                username=username,
                email=email,
                password=password,
                image=image,
                website=website,
                location=location,
                bio=bio,
                skills_languages=skills_languages
            )

            new_user: Users = Users.query.order_by(Users.id.desc()).first()
            login_user(new_user)

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
