from app.models import Comments


def test_delete_comment(client, app):
    """
    GIVEN a client and app.
    WHEN a DELETE request is sent to '/comment/delete/2'.
    THEN the comment with id=2 should be deleted and return a 200 status code with message 'Comment deleted successfully'.
    """

    response = client.delete(f'/comment/delete/2')

    assert response.status_code == 200
    assert response.json['message'] == 'Comment deleted successfully'

    with app.app_context():

        assert Comments.query.get(2) is None
