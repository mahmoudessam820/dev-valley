from flask import request, jsonify

from . import comment
from ..models import Comments, Users, Articles


@comment.route('/comment/new', methods=['POST'])
def new_comment():
    try:

        if request.method == 'POST':

            data = request.get_json()

            body = data['body']
            commenter_id = data['commenter_id']
            article_id = data['article_id']

            user = Users.query.get(int(commenter_id))
            article = Articles.query.get(int(article_id))

            create_comment = Comments(
                body=body, commenter_id=user.id, article_id=article.id)

            create_comment.save()

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
