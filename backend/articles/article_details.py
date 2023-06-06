from flask import Blueprint, request, jsonify
from sqlalchemy.orm import aliased

from models.model import Articles, Users, Comments, db

article_details_bp: Blueprint = Blueprint('article_details_bp', __name__)


@article_details_bp.route('/article/details/<int:article_id>', methods=['GET'])
def get_article_details(article_id) -> None:
    try:

        if request.method == 'GET':

            queryset = db.session.query(Articles, Users.username.label('author_name'), Comments.body, Users.username.label('commenter_name'))\
                .join(Users, Articles.author_id == Users.id)\
                .join(Comments, Articles.id == Comments.article_id)\
                .filter(Articles.id == article_id)\
                .filter(Comments.body != None)\
                .filter(Comments.body != '')\
                .filter(Comments.article_id == article_id)\
                .all()

            print(queryset)

            if queryset:

                article = queryset[0][0]
                author_name = queryset[0][1]
                comments = [{'body': comment[2], 'commenter_name': comment[3]}
                            for comment in queryset if comment[2]]

                return jsonify({

                    'success': True,
                    'details': {
                        "article_id": article.id,
                        "title": article.title,
                        "slug": article.slug,
                        "body": article.body,
                        "category": article.category,
                        "created_at": article.created_at,
                        "updated_at": article.updated_at,
                        "author_name": author_name,
                        "comments": comments
                    }
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
