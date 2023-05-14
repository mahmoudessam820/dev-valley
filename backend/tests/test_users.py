from models.model import Users


def test_signin_page(client, app):

    users = [
        {
            'username': 'tito',
            'email': 'tito@gmail.com',
            'password': '123456',
        },
        {
            'username': 'amr',
            'email': 'amr@gmail.com',
            'password': 'password123',
        }
    ]

    for user in users:

        response = client.post('/signin', json=user)

        assert response.status_code == 201
        assert response.json['success'] == True

        with app.app_context():

            admin = Users.query.filter_by(email='tito@gmail.com').first()
            user = Users.query.filter_by(email='amr@gmail.com').first()

            user_count = Users.query.count()
            print(f"User count: {user_count}")

            assert Users.query.count() == 2

            # Admin
            assert admin.username == 'tito'
            assert admin.email == 'tito@gmail.com'
            assert admin.is_admin == True
            assert admin.is_active == True
            assert admin.is_staff == True

            # User
            assert user.username == 'amr'
            assert user.email == 'amr@gmail.com'
            assert user.is_active == True
            assert user.is_admin == False
            assert user.is_staff == False
