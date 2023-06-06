from flask import (request, jsonify, Blueprint)


from models.model import Comments, Users, Articles


create_comment_bp = Blueprint('create_comment_bp', __name__)


@create_comment_bp.route('/comment/new', methods=['POST'])
def create_comment():
    try:

        if request.method == 'POST':

            data = request.get_json()

            body = data['body']
            commenter_id = data['commenter_id']
            article_id = data['article_id']

            user = Users.query.get(int(commenter_id))
            article = Articles.query.get(int(article_id))

            new_comment = Comments(
                body=body, commenter_id=user.id, article_id=article.id)

            new_comment.save()

            return jsonify({
                'success': True,
                'message': 'Comment created successfully',
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
