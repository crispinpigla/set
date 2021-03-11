""""""

from django.test import TestCase, Client

from user.models import Utilisateurs

class TestsFonctionnels(TestCase):
    """docstring for TestsFonctionnels"""

    def setUp(self):
        """"""
        pass

    def test_fonctionnel_inscription_deconnexion(self):
        """deonnexion d'un utilisateur après son inscription"""
        client_user = Client()
        reponse_inscription = client_user.post(
            "/authentification/inscription/",
            {
                "name": "user",
                "email": "user@mail.mail",
                "password": "user_password",
                "confirmation_password": "user_password",
            },
        )
        self.assertTrue(client_user.session['user_id'] != None )
        reponse_deconnexion = client_user.get('/user/deconnexion/')
        self.assertTrue(client_user.session.get('user_id', None) == None)
        self.assertTrue(reponse_deconnexion.url == '../../')
        self.assertTrue(reponse_deconnexion.status_code == 302)

    def test_fonctionnel_(self):
        """"""
        pass

    def test_fonctionnel_(self):
        """"""
        pass

    def test_fonctionnel_(self):
        """"""
        pass

    def test_fonctionnel_(self):
        """"""
        pass

    def test_fonctionnel_(self):
        """"""
        pass

    def test_fonctionnel_(self):
        """"""
        pass

    def test_fonctionnel_(self):
        """"""
        pass

    def test_fonctionnel_(self):
        """"""
        pass

    def test_fonctionnel_(self):
        """"""
        pass

    def test_fonctionnel_(self):
        """"""
        pass

    def test_fonctionnel_(self):
        """"""
        pass

    def test_fonctionnel_(self):
        """"""
        pass

    def test_fonctionnel_(self):
        """"""
        pass

    def test_fonctionnel_(self):
        """"""
        pass

    def test_fonctionnel_(self):
        """"""
        pass

    def test_fonctionnel_(self):
        """"""
        pass

    def test_fonctionnel_(self):
        """"""
        pass

    def test_fonctionnel_(self):
        """"""
        pass

    def test_fonctionnel_(self):
        """"""
        pass

    def test_fonctionnel_(self):
        """"""
        pass

    def test_fonctionnel_(self):
        """"""
        pass

    def test_fonctionnel_(self):
        """"""
        pass

    def test_fonctionnel_(self):
        """"""
        pass

    def test_fonctionnel_(self):
        """"""
        pass

    def test_fonctionnel_(self):
        """"""
        pass

    def test_fonctionnel_(self):
        """"""
        pass

    def test_fonctionnel_(self):
        """"""
        pass

    def test_fonctionnel_(self):
        """"""
        pass

    def test_fonctionnel_(self):
        """"""
        pass
