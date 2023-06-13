from app.models import Users


def test_delete_account_exist(client, app):
    """
    GIVEN a client is logged in and an account with the ID 3 exists.
    WHEN the "/user/delete/3" endpoint is visited with DELETE request method.
    THEN ensure that the response status code is 200,
    ensure that the 'message' key in the response JSON equals 'Account deleted', and
    ensure that the user account with ID 3 no longer exists.
    """

    response = client.delete(f'/user/delete/3')

    assert response.status_code == 200
    assert response.json['message'] == 'Account deleted'

    with app.app_context():

        assert Users.query.get(3) is None


def test_delete_account_not_exist(client):
    """
    GIVEN a client is logged in.
    WHEN the "/user/delete/100" endpoint is visited with DELETE request method.
    THEN ensure that the response status code is 404 and
    ensure that the 'message' key in the response JSON equals 'User not found'.
    """

    response = client.delete(f'/user/delete/100')

    assert response.status_code == 404
    assert response.json['message'] == 'User not found'
