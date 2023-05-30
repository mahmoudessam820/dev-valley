import functools
import random
import string
from werkzeug.utils import secure_filename
from slugify import slugify
from flask import (Blueprint, request, jsonify)


from models.model import Articles


create_article_bp: Blueprint = Blueprint('create_article_bp', __name__)


def generate_random_string(length) -> str:
    """
    Generate a random string of lowercase letters and digits.
    """
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


@create_article_bp.route('/new', methods=['POST'])
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
