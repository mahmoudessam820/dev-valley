import re
from . import auth
from flask import request, jsonify
from flask_login import login_user, logout_user
from ..models import Users


def is_valid_email(email):
    """
    Validate email format using regex.
    """
    pattern = r'^\S+@\S+\.\S+$'
    return re.match(pattern, email)


@auth.route('/signin', methods=['POST'])
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


@auth.route('/login', methods=['POST'])
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


@auth.route('/logout', methods=['GET'])
def logout() -> None:

    logout_user()

    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    }), 200


@auth.route('/user/edit/<int:user_id>', methods=['PUT'])
def edit_account(user_id) -> None:
    try:

        if request.method == 'PUT':

            data = request.get_json()
            user = Users.query.get(int(user_id))

            if user:

                user.username = data['username']
                user.email = data['email']
                user.password = data['password']
                user.image = data['image']
                user.website = data['website']
                user.location = data['location']
                user.bio = data['bio']
                user.skills_languages = data['skills_languages']
                user.update()

                return jsonify({
                    'status': True,
                    'message': 'User edited successfully',
                }), 200

            else:
                return jsonify({
                    'success': False,
                    'message': 'User not found'
                }), 404

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


@auth.route('/user/delete/<int:user_id>', methods=['DELETE'])
def delete_account(user_id):
    try:
        if request.method == 'DELETE':

            user: Users = Users.query.get(user_id)

            if user:
                user.delete()
                return jsonify({'message': 'Account deleted'}), 200
            else:
                return jsonify({'message': 'User not found'}), 404

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
