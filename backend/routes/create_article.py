from flask import (Blueprint, request, jsonify)

from models.model import Articles


create_article_bp = Blueprint('create_article_bp', __name__)


@create_article_bp.route('/new', methods=['POST'])
def create_article():
    try:

        if request.method == 'POST':

            data = request.get_json()

            title = data['title']
            body = data['body']
            category = data['category']
            author = data['author']

            Articles(title=title, body=body,
                     category=category, author_id=author).save()

            return jsonify({
                'success': True,
                'message': 'Successfully created'
            }), 201

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
