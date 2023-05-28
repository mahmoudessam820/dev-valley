from models.model import Users


def test_login_vaild_user(client, app):

    user = {
        'email': 'tito@gmail.com',
        'password': '123456'
    }

    response = client.post('/login', json=user)

    assert response.status_code == 200
    assert response.json['message'] == 'Logged in successfully'

    with app.app_context():

        user = Users.query.filter_by(email='tito@gmail.com').first()

        assert user.email == "tito@gmail.com"
        assert user.is_admin == True
        assert user.is_staff == True
        assert user.is_active == True


def test_login_invalid_user(client):

    user = {
        'email': 'test@gmail.com',
        'password': 'test1234'
    }

    response = client.post('/login', json=user)

    assert response.status_code == 401
    assert response.json['success'] == False
    assert response.json['error'] == 'Invalid Email or Password'
