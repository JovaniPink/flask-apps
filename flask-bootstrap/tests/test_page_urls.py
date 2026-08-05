# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

def test_page_urls(app, client):
    assert app.config["SECURITY_WEBAUTHN"] is False

    # Visit home page
    response = client.get('/', follow_redirects=True)
    assert response.status_code==200

    # Try to login with wrong email
    response = client.post('/user/sign-in', follow_redirects=True,
                           data=dict(email='non_member@example.com', password='Password1'))
    assert response.status_code==200
    assert b"Sign In to your account" in response.data

    # Login as user and visit User page
    response = client.post('/user/sign-in', follow_redirects=True,
                           data=dict(email='member@example.com', password='Password1'))
    assert response.status_code==200
    assert b"Sign In to your account" not in response.data

    response = client.get('/', follow_redirects=True)
    assert response.status_code==200
    assert b"Code Explorer" in response.data

    # Members cannot access the admin area.
    response = client.get('/admin')
    assert response.status_code == 403

    # Edit User Profile page
    response = client.get('/pages/profile', follow_redirects=True)
    assert response.status_code==200
    assert b"User Profile" in response.data
    assert b"First name" in response.data
    assert b"Member" in response.data

    response = client.post('/pages/profile', follow_redirects=True,
                           data=dict(first_name='User', last_name='User'))
    assert response.status_code == 200
    assert b"Code Explorer" in response.data

    response = client.get('/', follow_redirects=True)
    assert response.status_code==200
    assert b"User Profile" not in response.data
    assert b"First name" not in response.data
    assert b"Code Explorer" in response.data

    # Logout
    response = client.get('/user/sign-out', follow_redirects=True)
    assert response.status_code==200
    assert b"Sign In / Signup" in response.data

    # Login as admin and visit Admin page
    response = client.post('/user/sign-in', follow_redirects=True,
                           data=dict(email='admin@example.com', password='Password1'))
    assert response.status_code==200
    assert b"Sign In to your account" not in response.data

    response = client.get('/admin', follow_redirects=True)
    assert response.status_code==200
    assert b"System Users" in response.data
    assert b"Create User" in response.data

    # Logout
    response = client.get('/user/sign-out', follow_redirects=True)
    assert response.status_code==200
    assert b"Sign In / Signup" in response.data
