def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the  hashed_password field are defined correctly
    """

    assert new_user.username == 'Alexa'
    assert new_user.password != 'AWS'
    assert new_user.check_password('AWS') == True
