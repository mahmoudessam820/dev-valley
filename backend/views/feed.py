from flask import Blueprint, request, jsonify

from models.model import Articles


feed_bp: Blueprint = Blueprint('feed_bp', __name__)


@feed_bp.route('/', methods=['GET'])
@feed_bp.route('/feed')
def feed():
    try:

        if request.method == 'GET':

            articles = Articles.query.all()
            serialized_articles = [article.serialize() for article in articles]

            return jsonify({
                'success': True,
                'articles': serialized_articles,
                'total_articles': len(serialized_articles)
            }), 200

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
