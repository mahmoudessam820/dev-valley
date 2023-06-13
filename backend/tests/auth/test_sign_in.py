from app.models import Users


def test_create_admin_user(client, app):
    """
    GIVEN app and client.
    WHEN the test_create_admin_user function is called with a dictionary of user data including a username, email, password, profile image URL, website URL, location, bio, and skills/languages.
    THEN the function sends a POST request to the '/signin' endpoint with the user data and checks that the response status code is 201 (success), the success flag is True, and the message indicates that an admin user was created successfully. 
    The function then gets the newly created admin user from the database using the app context and asserts that all fields match the corresponding values in the original user dictionary, as well as asserting that some boolean fields are True indicating the user's role and status.
    """

    user = {
        "username": "tito",
        "email": "tito@gmail.com",
        "password": "123456",
        "image": "73683",
        "website": "https://clear-sleet.surge.sh/",
        "location": "Egypt",
        "bio": "I'm admin",
        "skills_languages": "Python, Javascript, Flask"
    }

    response = client.post('/signin', json=user)

    assert response.status_code == 201
    assert response.json['success'] == True
    assert response.json['message'] == 'Admin created successfully'

    with app.app_context():

        admin = Users.query.filter_by(email='tito@gmail.com').first()

        assert admin.username == "tito"
        assert admin.email == "tito@gmail.com"
        assert admin.image == "73683"
        assert admin.website == "https://clear-sleet.surge.sh/"
        assert admin.location == "Egypt"
        assert admin.bio == "I'm admin"
        assert admin.skills_languages == 'Python, Javascript, Flask'
        assert admin.is_admin == True
        assert admin.is_active == True
        assert admin.is_staff == True


def test_create_regular_user(client, app):
    """
    GIVEN a client and an app, the test_create_regular_user function tests the ability of the system to create a regular user.

    WHEN a JSON object containing the user's details (such as their username, email, password, image, website, location, bio, and skills_languages) is sent to the '/signin' endpoint using a POST request.

    THEN the function checks if the response status code is 201, indicating that the user was created successfully. 

    It also verifies if the 'success' key in the response JSON object reads True and if the 'message' key reads 'User created successfully'.
    THEN it checks if the user's information has been correctly stored in the database by querying the Users table using the provided email address. 

    Assertions are made to ensure that the username, email, image, website, location, bio, and skills_languages match the values provided when creating the user. 
    The function also checks if the default values for is_admin, is_active, and is_staff are False, True, and False respectively.
    """

    user = {
        "username": "amr",
        "email": "amr@gmail.com",
        "password": "amr1234",
        "image": "",
        "website": "https://test.com",
        "location": "UK",
        "bio": "I'm frontend developer",
        "skills_languages": "HTML, Javascript, CSS"
    }

    response = client.post('/signin', json=user)

    assert response.status_code == 201
    assert response.json['success'] == True
    assert response.json['message'] == 'User created successfully'

    with app.app_context():

        user = Users.query.filter_by(email='amr@gmail.com').first()

        assert user.username == "amr"
        assert user.email == "amr@gmail.com"
        assert user.image == ""
        assert user.website == "https://test.com"
        assert user.location == "UK"
        assert user.bio == "I'm frontend developer"
        assert user.skills_languages == "HTML, Javascript, CSS"
        assert user.is_admin == False
        assert user.is_active == True
        assert user.is_staff == False


def test_create_user_with_valid_email(client):
    """
    GIVEN a client object and user data containing valid email, username, password, image, website, location, bio, and skills_language.
    WHEN the 'test_create_user_with_valid_email' function is executed using the client's post method with the user data as json.
    THEN it should return a response with a status code of 201 indicating the successful creation of the user. 
    The response message should also indicate that the user was created successfully and the 'success' key in the response JSON should be True.
    """

    user = {
        "username": "tony",
        "email": "tony@gmail.com",
        "password": "test123",
        "image": "",
        "website": "https://tony.com",
        "location": "USA",
        "bio": "I'm full stack developer",
        "skills_languages": "HTML, Javascript, CSS, Python, Flask"
    }

    response = client.post('/signin', json=user)

    assert response.status_code == 201
    assert response.json['success'] == True
    assert response.json['message'] == 'User created successfully'


def test_create_user_with_invalid_email(client):
    """
    GIVEN a client instance.
    WHEN the test_create_user_with_invalid_email function is called with an invalid email address in the user data.
    THEN it should return a response with status code 400, and a JSON object that contains success as False and error message as 'Invalid email'.
    """

    user = {
        "username": "fake",
        "email": "fake",
        "password": "fake123",
        "image": "",
        "website": "https://fake.com",
        "location": "fake",
        "bio": "I'm frontend developer",
        "skills_languages": "HTML, Javascript, CSS"
    }

    response = client.post('/signin', json=user)

    assert response.status_code == 400
    assert response.json['success'] == False
    assert response.json['error'] == 'Invalid email'
