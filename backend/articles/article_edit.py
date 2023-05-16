from flask import Blueprint, request, jsonify

from models.model import Articles


article_edit_bp: Blueprint = Blueprint('article_edit_bp', __name__)


@article_edit_bp.route('/article/edit/<int:article_id>', methods=['PUT'])
def edit_article(article_id):
    try:

        if request.method == 'PUT':

            data = request.get_json()
            article = Articles.query.get(int(article_id))

            if article:

                article.title = data['title']
                article.body = data['body']
                article.category = data['category']
                article.update()

                return jsonify({
                    'success': True,
                    'details': article.serialize(),
                    'message': 'Article updated successfully'
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
