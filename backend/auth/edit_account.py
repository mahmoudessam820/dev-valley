from flask import (Blueprint, request, jsonify)


from models.model import Users


edit_account_bp: Blueprint = Blueprint('edit_account_bp', __name__)


@edit_account_bp.route('/user/edit/<int:user_id>', methods=['PUT'])
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
