from models.model import Users


def test_edit_account_exist(client, app):

    user = {
        'username': 'rook',
        'email': 'rook@gmail.com',
        'password': 'test1234'
    }

    response = client.put(f'/user/edit/2', json=user)

    assert response.status_code == 200
    assert response.json['status'] == True
    assert response.json['message'] == 'User edited successfully'

    with app.app_context():

        user = Users.query.get(2)

        assert user.username == 'rook'
        assert user.email == 'rook@gmail.com'
        assert user.check_password('test1234') == True


def test_edit_account_not_exist(client):

    user = {
        'username': 'ford',
        'email': 'ford@gmail.com',
        'password': 'test1234'
    }

    response = client.put(f'/user/edit/100',  json=user)

    assert response.status_code == 404
    assert response.json['success'] == False
    assert response.json['message'] == 'User not found'
