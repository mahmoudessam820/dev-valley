from app.models import Articles


def test_delete_article(client, app):
    """
    GIVEN a app and client.
    WHEN the user sends a delete request to delete an article with a specific id, 
    The article with the given ID should be deleted from the database.
    THEN the test checks if the response status code is 200 and the success key in the json response is True. 
    It also checks if the message key in the json response is 'Article deleted'. 
    Finally, it verifies that the article with the given ID no longer exists in the database after the deletion.
    """

    response = client.delete(f'/article/delete/1')

    assert response.status_code == 200
    assert response.json['success'] == True
    assert response.json['message'] == 'Article deleted'

    with app.app_context():

        assert Articles.query.get(1) is None


def test_article_not_found(client):
    """
    GIVEN a client.
    WHEN the user sends a delete request to delete an article with an ID that does not exist in the database, the response should contain a 404 status code and the success key in the json response should be False.
    THEN the test checks if the error message "Article not found" is also present in the response.
    """

    response = client.delete(f'/article/delete/1')

    assert response.status_code == 404
    assert response.json['success'] == False
    assert response.json['error'] == 'Article not found'
