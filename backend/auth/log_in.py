from flask import (Blueprint, request, jsonify)


from models.model import Users

login_bp: Blueprint = Blueprint('login_bp', __name__)


@login_bp.route('/login', methods=['POST'])
def login() -> None:
    try:
        pass
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
            'error': str(e)
        }), 500
