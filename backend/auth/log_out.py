from flask import (Blueprint, jsonify)
from flask_login import logout_user


logout_bp: Blueprint = Blueprint('logout_bp', __name__)


@logout_bp.route('/logout', methods=['GET'])
def logout() -> None:

    logout_user()

    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    }), 200
