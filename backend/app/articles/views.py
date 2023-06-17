import string
import random
from sqlalchemy.orm import aliased
from flask import request, jsonify
import functools
from werkzeug.utils import secure_filename
from slugify import slugify

from . import article
from ..models import Articles, Users, db, Comments


def generate_random_string(length) -> str:
    """
    Generate a random string of lowercase letters and digits.
    """
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


@article.route('/new', methods=['POST'])
def create_article():
    try:
        if request.method == 'POST':
            data = request.get_json()

            # Check if all required fields are present and not empty
            required_fields: list[str] = [
                'title', 'body', 'category', 'author']

            if not functools.reduce(lambda x, y: x and y, map(lambda f: f in data, required_fields), True):
                return jsonify({
                    'success': False,
                    'message': 'Missing or invalid required fields'
                }), 400

            title = data['title']
            body = data['body']
            category = data['category']
            author = data['author']

            secure_slug: str = secure_filename(title)
            slug: str = slugify(secure_slug)

            random_string: str = generate_random_string(6)
            slug_with_random: str = f"{slug}-{random_string}"

            Articles(title=title, slug=slug_with_random, body=body,
                     category=category, author_id=author).save()

            return jsonify({
                'success': True,
                'message': 'Article created successfully'
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


@article.route('/article/edit/<int:article_id>', methods=['PUT'])
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


@article.route('/article/details/<int:article_id>', methods=['GET'])
def get_article_details(article_id) -> None:
    try:

        if request.method == 'GET':

            article = Articles.query\
                .join(Users, Articles.author_id == Users.id)\
                .filter(Articles.id == article_id)\
                .with_entities(
                    Articles.id,
                    Articles.title,
                    Articles.slug,
                    Articles.body,
                    Articles.category,
                    Articles.created_at,
                    Articles.updated_at,
                    Articles.author_id,
                    Users.username
                )\
                .first()

            if article is None:
                return jsonify({
                    'success': False,
                    'error': 'Article not found'
                }), 404

            comments_exist = Comments.query.filter_by(
                article_id=article_id).first()

            if comments_exist is None:

                return jsonify({
                    'success': True,
                    'details': article._asdict()
                }), 200

            # Define two aliases for the Users table
            # This allows us to join the Articles and Comments tables with the Users table twice
            author = aliased(Users)
            commenter = aliased(Users)

            # Query the database to find an article and its comments
            article_query = db.session.query(Articles, author.username.label('author_name'), Comments.body, commenter.username.label('commenter_name'))\
                .join(author, Articles.author_id == author.id)\
                .join(Comments, Articles.id == Comments.article_id)\
                .join(commenter, Comments.commenter_id == commenter.id)\
                .filter(Articles.id == article_id)

            # Get all the data from the query
            article_data = article_query.all()

            # If the article was found, create a dictionary representation of it with its comments
            if article_data:

                # Extract the article data and create a dictionary representation of it
                article, author_name, *comments = article_data[0]

                # Create a list of comment dictionaries from the query data
                article_dict = article.serialize()
                comments = [{'body': comment[2], 'commenter_name': comment[3]}
                            for comment in article_data if comment[2]]

                # Add the comments and author name to the article dictionary
                article_dict['comments'] = comments
                article_dict['author_name'] = author_name

                return jsonify({
                    'success': True,
                    'details': article_dict
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


@article.route('/article/delete/<int:article_id>', methods=['DELETE'])
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
