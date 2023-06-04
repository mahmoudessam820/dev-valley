from app.models import Articles


def test_create_new_article(client, app):

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

        article = Articles.query.first()

        assert article.title == '10 Tasks for DevOps Engineers'
        assert article.category == 'programming'
        assert article.author_id == 2


def test_create_article_with_invalid_data(client):

    article = {
        'title': 'Invalid Article',
        "body": '',
        "category": "programming",
    }

    response = client.post('new', json=article)

    assert response.status_code == 400
    assert response.json['success'] == False
    assert response.json['message'] == 'Missing or invalid required fields'
