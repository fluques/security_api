from app import create_app

def test_home_page_get():
    '''
    GIVEN a Flask application
    WHEN the home page is requested (GET)
    THEN check that the response is valid
    '''
    app = create_app()
    client = app.test_client()

    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the API' in response.data



def test_home_page_post():
    '''
    GIVEN a Flask application
    WHEN the home page is requested (POST)
    THEN check that the response is valid
    '''
    app = create_app()
    client = app.test_client()

    response = client.post('/')
    assert response.status_code == 405
    assert b'Welcome to the API' not in response.data