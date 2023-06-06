<<<<<<< HEAD:backend/views/feed.py
from flask import Blueprint, request, jsonify


from models.model import Articles, Users
=======
from . import main
from flask import request, jsonify
from ..models import Articles
>>>>>>> refs/remotes/origin/main:backend/app/main/views.py


@main.route('/', methods=['GET'])
@main.route('/feed')
def feed():
    try:

        if request.method == 'GET':

            articles = Articles.query.join(Users).add_columns(
                Users.id, Users.username).limit(50).all()

            serialized_articles = [{
                'article_id': article.id,
                'title': article.title,
                'slug': article.slug,
                'body': article.body,
                'category': article.category,
                'created_at': article.created_at,
                'updated_at': article.updated_at,
                'author_id': id,
                'author_name': username
            } for (article, id, username) in articles]

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
