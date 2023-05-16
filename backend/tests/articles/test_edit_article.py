from models.model import Articles


def test_edit_article(client, app):

    article = {

        "title": "learn how to build website like dev.to",
        "body": "dev.to should be something",
        "category": "web development"
    }

    response = client.put(f'/article/edit/1', json=article)

    assert response.status_code == 200
    assert response.json['success'] == True

    with app.app_context():

        article = Articles.query.first()

        assert article.title == 'learn how to build website like dev.to'
        assert article.body == 'dev.to should be something'
        assert article.category == 'web development'


def test_edit_article_not_exist(client):

    article = {

        "title": "pytest",
        "body": "learn how to useing pytest",
        "category": "testing"
    }

    response = client.put(f'/article/edit/100', json=article)

    assert response.status_code == 404
    assert response.json['success'] == False
    assert response.json['error'] == 'Article not found'
