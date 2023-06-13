from app.models import Users


def test_login_vaild_user(client, app):
    """
    GIVEN: A registered user with a valid email and password.
    WHEN: The user logs in by sending a POST request to the '/login' endpoint with their email and password.
    THEN: The server should respond with a status code of 200 and a response message of 'Logged in successfully'. 
    Additionally, within the app context, this test queries the User model to check if the returned user has the expected properties like being an admin/staff and active.
    """

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
    """
    GIVEN a client and invalid user login credentials.
    WHEN the user attempts to log in with these credentials.
    THEN the server should return a 401 error response with a failure message.
    """

    user = {
        'email': 'test@gmail.com',
        'password': 'test1234'
    }

    response = client.post('/login', json=user)

    assert response.status_code == 401
    assert response.json['success'] == False
    assert response.json['error'] == 'Invalid Email or Password'
