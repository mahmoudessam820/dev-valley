from flask import (Blueprint, request, jsonify)


from models.model import Users

delete_account_bp: Blueprint = Blueprint('delete_account_bp', __name__)


@delete_account_bp.route('/user/delete/<int:user_id>', methods=['DELETE'])
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
