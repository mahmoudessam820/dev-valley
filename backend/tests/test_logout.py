
def test_logout(client):

    response = client.get('/logout')

    assert response.status_code == 200
    assert response.json['success'] == True
    assert response.json['message'] == 'Logged out successfully'
