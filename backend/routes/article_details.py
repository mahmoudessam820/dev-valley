from flask import Blueprint, request, jsonify

from models.model import Articles


article_details_bp: Blueprint = Blueprint('article_details_bp', __name__)


@article_details_bp.route('/article/<int:article_id>', methods=['GET'])
def get_article_details(article_id) -> None:
    try:

        if request.method == 'GET':

            article = Articles.query.get(int(article_id))

            if article:
                return jsonify({
                    'success': True,
                    'details': article.serialize()
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'error': 'Article not found'
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
