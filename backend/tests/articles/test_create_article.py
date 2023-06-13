from app.models import Articles


def test_create_new_article(client, app):
    """
    GIVEN a client and app.
    WHEN the user submits a POST request to create a new article with a title, body, category, and author information.
    THEN the test function checks if the response status code is 201 (indicating that the request was successful).
    THEN the function uses the Flask application context to query the database for the newly created article.
    """

    article = {
        "title": "10 Tasks for DevOps Engineers",
        "body": "I thought I had taken all the necessary precautions",
        "category": "programming",
        "author": 2
    }

    response = client.post('/new', json=article)

    assert response.status_code == 201
    assert response.json['success'] == True
    assert response.json['message'] == 'Article created successfully'

    with app.app_context():

        article = Articles.query.firest()

        assert article.title == '10 Tasks for DevOps Engineers'
        assert article.category == 'programming'
        assert article.author_id == 2


def test_create_article_with_invalid_data(client):
    """
    GIVEN a client.
    WHEN creating an article with invalid data.
    THEN the server should respond with error status code and message.
    """

    article = {
        'title': 'Invalid Article',
        "body": '',
        "category": "programming",
    }

    response = client.post('new', json=article)

    assert response.status_code == 400
    assert response.json['success'] == False
    assert response.json['message'] == 'Missing or invalid required fields'
