from app.models import Users


def test_create_admin_user(client, app):

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
