from models import UserModel


def test_new_user():
    '''
    GIVEN a UserModel
    WHEN the user is created
    THEN the user should have the expected attributes
    '''

    user = UserModel(user_name="testuser", password="testpassword",  email="ing.fernando.luque@gmail.com", is_active=True)
    assert user.user_name == "testuser"
    assert user.email == "ing.fernando.luque@gmail.com"
    assert user.is_active is True
    assert user.password is not None  # Password should be hashed, so it won't match the plain text