from app.models import Articles


def test_delete_article(client, app):

    response = client.delete(f'/article/delete/1')

    assert response.status_code == 200
    assert response.json['success'] == True
    assert response.json['message'] == 'Article deleted'

    with app.app_context():

        assert Articles.query.get(1) is None


def test_article_not_found(client):

    response = client.delete(f'/article/delete/1')

    assert response.status_code == 404
    assert response.json['success'] == False
    assert response.json['error'] == 'Article not found'
