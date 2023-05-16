from models.model import Users


def test_create_admin_user(client, app):

    user = {
        'username': 'tito',
        'email': 'tito@gmail.com',
        'password': '123456',
    }

    response = client.post('/signin', json=user)

    assert response.status_code == 201
    assert response.json['success'] == True
    assert response.json['message'] == 'Admin created successfully'

    with app.app_context():

        admin = Users.query.filter_by(email='tito@gmail.com').first()

        assert admin.username == 'tito'
        assert admin.email == 'tito@gmail.com'
        assert admin.is_admin == True
        assert admin.is_active == True
        assert admin.is_staff == True


def test_create_regular_user(client, app):

    user = {
        'username': 'amr',
        'email': 'amr@gmail.com',
        'password': 'amr1234'
    }

    response = client.post('/signin', json=user)

    assert response.status_code == 201
    assert response.json['success'] == True
    assert response.json['message'] == 'User created successfully'

    with app.app_context():

        user = Users.query.filter_by(email='amr@gmail.com').first()

        assert user.username == 'amr'
        assert user.email == 'amr@gmail.com'
        assert user.is_admin == False
        assert user.is_active == True
        assert user.is_staff == False


def test_create_user_with_valid_email(client):

    user = {
        'username': 'tony',
        'email': 'tony@gmail.com',
        'password': 'test123'
    }

    response = client.post('/signin', json=user)

    assert response.status_code == 201
    assert response.json['success'] == True
    assert response.json['message'] == 'User created successfully'


def test_create_user_with_invalid_email(client):

    user = {
        'username': 'amr',
        'email': 'amr',
        'password': 'amr1234'
    }

    response = client.post('/signin', json=user)

    assert response.status_code == 400
    assert response.json['success'] == False
    assert response.json['error'] == 'Invalid email'
