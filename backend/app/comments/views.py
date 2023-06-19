from flask import request, jsonify

from . import comment
from ..models import Comments, Users, Articles


@comment.route('/comment/new', methods=['POST'])
def new_comment() -> None:
    try:

        if request.method == 'POST':

            data = request.get_json()

            body = data['body']
            commenter_id = data['commenter_id']
            article_id = data['article_id']

            # check if the comment body is not empty.
            if not body:
                return jsonify({
                    'success': False,
                    'error': "Comment body can't be blank",
                }), 400

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


@comment.route('/comment/edit/<int:comment_id>', methods=['PUT'])
def edit_comment(comment_id) -> None:
    try:

        if request.method == 'PUT':

            data = request.get_json()

            comment = Comments.query.get(int(comment_id))
            body = data['body']

            comment.body = body
            comment.update()

            return jsonify({
                'success': True,
                'message': 'Comment edited successfully',
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


@comment.route('/comment/delete/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id) -> None:
    try:

        if request.method == 'DELETE':

            comment = Comments.query.get(int(comment_id))

            comment.delete()

            return jsonify({
                'success': True,
                'message': 'Comment deleted successfully',
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
