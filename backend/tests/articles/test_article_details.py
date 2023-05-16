from models.model import Articles


def test_article_details(client, app):

    response = client.get(f'/article/details/1')

    assert response.status_code == 200
    assert response.json['success'] == True

    with app.app_context():

        article = Articles.query.first()

        assert article.title == 'learn how to build website like dev.to'
        assert article.body == 'dev.to should be something'
        assert article.category == 'web development'


def test_article_not_found(client):

    response = client.get(f'/article/details/100')

    assert response.status_code == 404
    assert response.json['success'] == False
    assert response.json['error'] == 'Article not found'
