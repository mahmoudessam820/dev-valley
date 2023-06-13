
def test_logout(client):
    """
    GIVEN a client is logged in.
    WHEN the "/logout" endpoint is visited.
    THEN ensure that the response status code is 200,
    ensure that the 'success' key in the response JSON equals True, and
    ensure that the 'message' key in the response JSON equals 'Logged out successfully'.
    """

    response = client.get('/logout')

    assert response.status_code == 200
    assert response.json['success'] == True
    assert response.json['message'] == 'Logged out successfully'
