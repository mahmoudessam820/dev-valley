from app.models import Users


def test_delete_account_exist(client, app):

    response = client.delete(f'/user/delete/3')

    assert response.status_code == 200
    assert response.json['message'] == 'Account deleted'

    with app.app_context():

        assert Users.query.get(3) is None


def test_delete_account_not_exist(client):

    response = client.delete(f'/user/delete/100')

    assert response.status_code == 404
    assert response.json['message'] == 'User not found'
