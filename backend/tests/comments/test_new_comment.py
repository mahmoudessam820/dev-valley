from app.models import Comments


def test_new_comment_success(client, app):
    """
    GIVEN a app and a client object.
    WHEN a POST request is sent to the '/comment/new' endpoint with valid data.
    THEN the response status code should be 201, indicating that the comment was successfully created, and the response message should indicate success. 
    Additionally, the test checks that the newly created comment has the correct body, commenter ID, and article ID.
    """

    data = {
        'body': 'This is a for testing',
        'commenter_id': 3,
        'article_id': 2
    }

    response = client.post('/comment/new', json=data)

    assert response.status_code == 201
    assert response.json['success'] == True
    assert response.json['message'] == 'Comment created successfully'

    with app.app_context():

        comment = Comments.query.filter_by(body=data['body']).first()

        assert comment.body == data['body']
        assert comment.commenter_id == data['commenter_id']
        assert comment.article_id == data['article_id']
