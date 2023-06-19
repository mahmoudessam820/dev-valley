from app.models import Comments


def test_edit_comment(client, app):
    """
    GIVEN a app and a client.
    WHEN the "edit" endpoint is requested with a valid comment ID and updated comment data in JSON format.
    THEN the response status code should be 200, the 'success' field in the response JSON should be True, 
    And the comment should be successfully edited with the new data and saved in the database.
    """

    data = {
        'body': 'testing the edit test route.'
    }

    response = client.put(f'/comment/edit/2', json=data)

    assert response.status_code == 200
    assert response.json['success'] == True
    assert response.json['message'] == 'Comment edited successfully'

    with app.app_context():

        comment = Comments.query.filter_by(id=2).first()

        assert comment.body == data['body']
        assert comment.commenter_id == 3
        assert comment.article_id == 2
