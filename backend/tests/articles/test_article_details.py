from app.models import Articles


def test_article_details(client, app):
    """
    GIVEN a app and a client.
    WHEN a request is made to retrieve details of article with ID 2.
    THEN the response status code should be 200, and the JSON response should contain a 'success' key with value True. 
    """

    response = client.get(f'/article/details/2')

    assert response.status_code == 200
    assert response.json['success'] == True

    with app.app_context():

        article = Articles.query.get(2)

        assert article.title == 'Prometheus vs Thanos'
        assert article.body == 'Prometheus and Thanos have emerged as two powerful tools for handling time series data. '
        assert article.category == 'cloud'
        assert article.author_id == 1


def test_article_not_found(client):
    """
    GIVEN client.
    WHEN a request is made to retrieve details of an article with a non-existent ID 100.
    THEN the response status code should be 404, and the JSON response should contain a 'success' key with value False,
    and an 'error' key with value 'Article not found'.
    """

    response = client.get(f'/article/details/100')

    assert response.status_code == 404
    assert response.json['success'] == False
    assert response.json['error'] == 'Article not found'
