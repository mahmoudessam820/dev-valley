from app.models import Articles


def test_article_details(client, app):

    response = client.get(f'/article/details/1')

    assert response.status_code == 200
    assert response.json['success'] == True

    with app.app_context():

        article = Articles.query.first()

        assert article.title == '10 Tasks for DevOps Engineers'
        assert article.body == 'I thought I had taken all the necessary precautions'
        assert article.category == 'programming'
        assert article.author_id == 2


def test_article_not_found(client):

    response = client.get(f'/article/details/100')

    assert response.status_code == 404
    assert response.json['success'] == False
    assert response.json['error'] == 'Article not found'
