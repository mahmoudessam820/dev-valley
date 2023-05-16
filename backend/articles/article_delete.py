from flask import Blueprint, request, jsonify


from models.model import Articles

article_delete_bp: Blueprint = Blueprint('article_delete_bp', __name__)


@article_delete_bp.route('/article/delete/<int:article_id>', methods=['DELETE'])
def delete_article(article_id) -> None:
    try:

        if request.method == 'DELETE':

            article = Articles.query.get(int(article_id))

            if article:

                article.delete()

                return jsonify({
                    'success': True,
                    'message': 'Article deleted',
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
