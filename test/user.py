from model import UserModel,PetModel,ServeModel, db
import unittest


class TestUser(unittest.TestCase):
    def test_signup_get(self, test_client):
        """
        Test GET request of sign up
        """
        response = test_client.get("/user/sign_up")

        assert response is not None
        assert response.status_code == 200
        assert b"Sign Up" in response.data

    def test_signup_post(self, test_client):
        """
        Test POST request of sign up
        """
        response = test_client.post(
            "/user/sign_up",
            data={
                "email":"Wangyue@qq.com",
                "username": "wangyue",
                "password": "wangyue123",
                "password_confirm": "wangyue123",
            },
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Posts" in response.data


    def test_signin_get(self, test_client):
        """
        Test GET request of sign in
        """
        response = test_client.get("/user/sign_in")

        assert response is not None
        assert response.status_code == 200
        assert b"Login" in response.data


    def test_signin_post(self, test_client):
        """
        Test POST request of sign in
        """
        password = "wangyue123"
        username = "wangyeu"
        email = "wangyue3@qq.com"
        user = UserModel(email=email, username=username, password=password)
        db.session.add(user)
        db.session.commit()

        response = test_client.post(
            "/user/sign_in",
            data={"email": user.email, "password": user.password},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Logout" in response.data

        response = test_client.post(
            "/login",
            data={"email": email, "password": password},
            follow_redirects=True,
        )

        assert response is not None
        assert response.status_code == 200
        assert b"Login" in response.data

    def test_signout_post(self, test_client):
        """
        Test POST request of sign out
        """
        password = "wangyue123"
        email = "wangyue@qq.com"
        user = UserModel(username="wangyue", email=email, password=password)
        db.session.add(user)
        db.session.commit()
        response1 = test_client.get(
            "/user/sign_out",
            follow_redirects=True,
        )

        assert response1 is not None
        assert response1.status_code == 200
        assert b'Home' in response1.data