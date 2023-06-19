from app.models import Articles


def test_edit_article(client, app):
    """
    GIVEN a app and client.
    WHEN the user sends a put request to edit an article with a specific id, the title, body and category of the article are updated with the new values given in the request.
    THEN the test checks if the response status code is 200 and the success key in the json response is True. 
    It then checks if the values in the database after the update match those given in the request.
    """

    article = {

        "title": "A Visual Guide to Layouts in Next.js 13",
        "body": "A layout in Next.js is a UI component that is shared between multiple pages in an application.",
        "category": "react.js"
    }

    response = client.put(f'/article/edit/1', json=article)

    assert response.status_code == 200
    assert response.json['success'] == True

    with app.app_context():

        article = Articles.query.first()

        assert article.title == 'A Visual Guide to Layouts in Next.js 13'
        assert article.body == 'A layout in Next.js is a UI component that is shared between multiple pages in an application.'
        assert article.category == 'react.js'


def test_edit_article_not_exist(client):
    """
    GIVEN a client.
    WHEN the user sends a put request to edit an article with an ID that does not exist in the database, 
    the response should contain a 404 status code and the success key in the json response should be False.
    THEN the test checks if the error message "Article not found" is also present in the response.
    """

    article = {

        "title": "pytest",
        "body": "learn how to useing pytest",
        "category": "testing"
    }

    response = client.put(f'/article/edit/100', json=article)

    assert response.status_code == 404
    assert response.json['success'] == False
    assert response.json['error'] == 'Article not found'
