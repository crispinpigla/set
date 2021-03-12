""""""

from django.test import TestCase, Client

from unittest.mock import patch

from user.models import Utilisateurs, Contact, Message

from sets.models import Sets, Evenements, PublicationSet, JaimePublicationSet, PublicationEvenement, JaimePublicationEvenement, SetUtilisateurs

import os

class TestsIntegrations(TestCase):
    """docstring for TestsFonctionnels"""

    def setUp(self):
        """"""
        pass

    def test_integration_inscription_deconnexion(self):
        """deconnexion d'un utilisateur après son inscription"""
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


    def test_integration_connexion_deconnexion(self):
        """connexion d'un utilisateur après son inscription"""

        client_user = Client()
        reponse_inscription = client_user.post(
            "/authentification/inscription/",
            {
                "name": "user",
                "email": "user@mail.mail",
                "password": "user_password",
                "confirmation_password": "user_password",
            },
        )    # Inscription
        self.assertTrue(client_user.session['user_id'] != None )
        reponse_deconnexion = client_user.get('/user/deconnexion/')	    # Deconnexion
        self.assertTrue(client_user.session.get('user_id', None) == None)
        reponse_connexion = client_user.post(
            "/authentification/connexion/",
            {
                "email": "user@mail.mail",
                "password": "user_password",
            },
        )			    # Connexion
        self.assertTrue(client_user.session['user_id'] != None )
        self.assertTrue(reponse_connexion.url == '../../user/home/' )
        reponse_deconnexion = client_user.get('/user/deconnexion/')		# Deconnexion
        self.assertTrue(client_user.session.get('user_id', None) == None)
        self.assertTrue(reponse_deconnexion.url == '../../')
        self.assertTrue(reponse_deconnexion.status_code == 302)

    def test_integration_envoie_lien_reinitialisation_mot_de_passe(self):
        """envoir du lien de éinitialisation de mot de passe"""
        client_user = Client()
        reponse_inscription = client_user.post(
            "/authentification/inscription/",
            {
                "name": "user",
                "email": "user@mail.mail",
                "password": "user_password",
                "confirmation_password": "user_password",
            },
        )    # Inscription
        reponse_deconnexion = client_user.get('/user/deconnexion/')	    # Deconnexion
        self.assertTrue(
            Utilisateurs.objects.get(
                adresse_mail='user@mail.mail'
            ).cle_de_reinitialisation_de_mot_de_passe
            == None
        )
        response_envoie_lien = client_user.post(
            "/authentification/envoie_lien_reinitialisation_password/",
            {"email": "user@mail.mail"},
        )		# envoie de lien de réinitilaisation de mot de passe
        self.assertTrue(
            Utilisateurs.objects.get(
                adresse_mail='user@mail.mail'
            ).cle_de_reinitialisation_de_mot_de_passe
            != None
        )
        self.assertTemplateUsed(
            response_envoie_lien, "envoie_lien_reinitialisation_mot_de_passe.html"
        )
        self.assertTrue(response_envoie_lien.context["send_mail"])
        self.assertTrue(response_envoie_lien.status_code == 200)

    def test_integration_reinitialisation_mot_de_passe(self):
        """Réinitialisation de mot de passe"""
        client_user = Client()
        reponse_inscription = client_user.post(
            "/authentification/inscription/",
            {
                "name": "user",
                "email": "user@mail.mail",
                "password": "user_password",
                "confirmation_password": "user_password",
            },
        )    # Inscription
        reponse_deconnexion = client_user.get('/user/deconnexion/')	    # Deconnexion

        response_envoie_lien = client_user.post(
            "/authentification/envoie_lien_reinitialisation_password/",
            {"email": "user@mail.mail"},
        )		# envoie de lien de réinitilaisation de mot de passe

        key = Utilisateurs.objects.get(
                adresse_mail='user@mail.mail'
            ).cle_de_reinitialisation_de_mot_de_passe  # Clé de réinitialisation

        self.assertTrue( key != None )

        response_reinitialisation = client_user.post(
            "/authentification/reinitialisation_password/",
            {
                "reset_key": key,
                "email": "user@mail.mail",
                "password": "new_password",
                "confirmation_password": "new_password",
            },
        )		#	Réinitialisation
        self.assertTrue(
            Utilisateurs.objects.get(
                adresse_mail='user@mail.mail'
            ).cle_de_reinitialisation_de_mot_de_passe
            == None
        )
        self.assertTrue(
            Utilisateurs.objects.get(
                adresse_mail='user@mail.mail'
            ).mot_de_passe
            == "new_password"
        )
        self.assertTrue(response_reinitialisation.context["state_reinitialisation"])
        self.assertTemplateUsed(response_reinitialisation, "reinitialisation_mot_de_passe.html")
        self.assertTrue(response_reinitialisation.status_code == 200)

    def test_integration_activation_compte(self):
        """Activation du compte"""
        client_user = Client()
        reponse_inscription = client_user.post(
            "/authentification/inscription/",
            {
                "name": "user",
                "email": "user@mail.mail",
                "password": "user_password",
                "confirmation_password": "user_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user.post(
            "/authentification/activation_compte/?mail="
            + "user@mail.mail"
            + "&key_activation="
            + activation_key_before
        )
        activation_key_after = Utilisateurs.objects.get(
            adresse_mail="user@mail.mail"
        ).cle_dactivation_de_compte
        self.assertTrue(activation_key_after == None)
        self.assertTrue(activation_key_before != activation_key_after)
        self.assertTrue(response.url == "../../user/home/")
        self.assertTrue(response.status_code == 302)

    @patch("authentification.views.requests.get")
    def test_integration_google_connect(self, mock_get):
        """Connection par un compte google"""
        client_user = Client()
        reponse_inscription = client_user.post(
            "/authentification/inscription/",
            {
                "name": "user",
                "email": "user@mail.mail",
                "password": "user_password",
                "confirmation_password": "user_password",
            },
        )    # Inscription
        reponse_deconnexion = client_user.get('/user/deconnexion/')	    # Deconnexion

        #  Connexion google reussie
        class MockRequest:
            """docstring for MockRequess"""

            def __init__(self, mail):
                """"""
                self.status_code = 200
                self.mail = mail

            def json(self):
                """"""
                return {"email": self.mail}

        mock_get.return_value = MockRequest(
            "user@mail.mail",
        )
        response = client_user.post(
            "/authentification/google_connect/?token=1234"
        )
        self.assertTrue(response.content == b"Connexion done")
        self.assertTrue(response.status_code == 200)


    def test_integration_envoie_lien_dactivation(self):
        """Envoie d'un lien d'activation"""
        client_user = Client()
        reponse_inscription = client_user.post(
            "/authentification/inscription/",
            {
                "name": "user",
                "email": "user@mail.mail",
                "password": "user_password",
                "confirmation_password": "user_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user.post(
            "/authentification/envoie_activation_compte/"
        )
        activation_key_after = Utilisateurs.objects.get(
            adresse_mail="user@mail.mail"
        ).cle_dactivation_de_compte
        self.assertTrue(activation_key_before != activation_key_after)
        self.assertTrue(response.url == "../../user/home/")
        self.assertTrue(response.status_code == 302)

    def test_integration_creation_set(self):
        """Création d'un set"""
        client_user = Client()
        reponse_inscription = client_user.post(
            "/authentification/inscription/",
            {
                "name": "user",
                "email": "user@mail.mail",
                "password": "user_password",
                "confirmation_password": "user_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user.post(
            "/authentification/activation_compte/?mail="
            + "user@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte

        sets_before = len(Sets.objects.all())
        image = open(os.path.join(os.getcwd(), "tests/test.png"), "rb")
        response_creation_set = client_user.post(
            "/sets/creation_set/",
            {
                "name": "set_0",
                "file": image,
                "type_set": "Entreprise",
                "description": "description set_0",
            },
        )	#	Création de set

        sets_after = len(Sets.objects.all())
        self.assertEqual(sets_before + 1, sets_after)
        self.assertTrue("../../sets/set/" in response_creation_set.url)

    def test_integration_creation_evenement(self):
        """Création d'évènement"""
        client_user = Client()
        reponse_inscription = client_user.post(
            "/authentification/inscription/",
            {
                "name": "user",
                "email": "user@mail.mail",
                "password": "user_password",
                "confirmation_password": "user_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user.post(
            "/authentification/activation_compte/?mail="
            + "user@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte

        sets_before = len(Sets.objects.all())
        image = open(os.path.join(os.getcwd(), "tests/test.png"), "rb")
        response_creation_set = client_user.post(
            "/sets/creation_set/",
            {
                "name": "set_0",
                "file": image,
                "type_set": "Entreprise",
                "description": "description set_0",
            },
        )	#	Création de set

        set_id = response_creation_set.url.split('/')[-2]

        events_before = len(Evenements.objects.all())
        response_event = client_user.post(
            "/sets/creation_evenement/" + set_id + "/",
            {"name": "event_0", "description": "description event_0"},
        )	# Création d'évènement
        events_after = len(Evenements.objects.all())
        self.assertTrue(events_after == events_before + 1)
        self.assertTrue("../../sets/event/" in response_event.url)
        self.assertTrue(response_event.status_code == 302)

    def test_integration_update_cover(self):
        """Mise à jour de limage de couverture"""
        client_user = Client()
        reponse_inscription = client_user.post(
            "/authentification/inscription/",
            {
                "name": "user",
                "email": "user@mail.mail",
                "password": "user_password",
                "confirmation_password": "user_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user.post(
            "/authentification/activation_compte/?mail="
            + "user@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte

        sets_before = len(Sets.objects.all())
        image0 = open(os.path.join(os.getcwd(), "tests/test.png"), "rb")
        response_creation_set = client_user.post(
            "/sets/creation_set/",
            {
                "name": "set_0",
                "file": image0,
                "type_set": "Entreprise",
                "description": "description set_0",
            },
        )	#	Création de set

        set_id = response_creation_set.url.split('/')[-2]

        image1 = open(os.path.join(os.getcwd(), "tests/test.png"), "rb")
        cover_before = Sets.objects.get(id=set_id).image_couverture
        response_update = client_user.post(
            "/sets/update_cover/?set_id=" + set_id, {"file": image1}
        )		#	Mise à jour de la couverture
        cover_after = Sets.objects.get(id=set_id).image_couverture
        self.assertTrue(
            cover_before != cover_after
        )
        self.assertEqual(response_update.url, "../../sets/set/" + set_id + "/")
        self.assertEqual(response_update.status_code, 302)

    def test_integration_update_description(self):
        """Mise à jour de la description"""
        client_user = Client()
        reponse_inscription = client_user.post(
            "/authentification/inscription/",
            {
                "name": "user",
                "email": "user@mail.mail",
                "password": "user_password",
                "confirmation_password": "user_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user.post(
            "/authentification/activation_compte/?mail="
            + "user@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte

        sets_before = len(Sets.objects.all())
        image0 = open(os.path.join(os.getcwd(), "tests/test.png"), "rb")
        response_creation_set = client_user.post(
            "/sets/creation_set/",
            {
                "name": "set_0",
                "file": image0,
                "type_set": "Entreprise",
                "description": "description set_0",
            },
        )	#	Création de set

        set_id = response_creation_set.url.split('/')[-2]

        description_before = Sets.objects.get(id=set_id).description
        response_update = client_user.post(
            "/sets/update_description_set/?set_id=" + set_id,
            {"description": "nouvelle description du set"},
        )		#    Mise à jour de la description du set
        description_after = Sets.objects.get(id=set_id).description
        self.assertTrue(
            description_before != description_after
        )
        self.assertEqual(response_update.url, "../../sets/set/" + set_id + "/")
        self.assertEqual(response_update.status_code, 302)


    def test_integration_make_post_set(self):
        """Publier dans un set"""
        client_user = Client()
        reponse_inscription = client_user.post(
            "/authentification/inscription/",
            {
                "name": "user",
                "email": "user@mail.mail",
                "password": "user_password",
                "confirmation_password": "user_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user.post(
            "/authentification/activation_compte/?mail="
            + "user@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte

        sets_before = len(Sets.objects.all())
        image0 = open(os.path.join(os.getcwd(), "tests/test.png"), "rb")
        response_creation_set = client_user.post(
            "/sets/creation_set/",
            {
                "name": "set_0",
                "file": image0,
                "type_set": "Entreprise",
                "description": "description set_0",
            },
        )	#	Création de set

        set_id = response_creation_set.url.split('/')[-2]

        posts_before = len(PublicationSet.objects.all())
        image1 = open(os.path.join(os.getcwd(), "tests/test.png"), "rb")
        image2 = open(os.path.join(os.getcwd(), "tests/test.png"), "rb")
        response = client_user.post(
            "/sets/make_post_set/" + set_id + "/",
            {
                "publication_text": "text de la publication",
                "file_1": image1,
                "file_2": image2,
            },
        )		# Publication dans le set
        posts_after = len(PublicationSet.objects.all())
        self.assertTrue(posts_after == posts_before + 1)
        self.assertTrue(response.url == "../../set/" + set_id + "/")
        self.assertTrue(response.status_code == 302)

    def test_integration_make_post_event(self):
        """Publier dans un évènement"""
        client_user = Client()
        reponse_inscription = client_user.post(
            "/authentification/inscription/",
            {
                "name": "user",
                "email": "user@mail.mail",
                "password": "user_password",
                "confirmation_password": "user_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user.post(
            "/authentification/activation_compte/?mail="
            + "user@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte

        sets_before = len(Sets.objects.all())
        image = open(os.path.join(os.getcwd(), "tests/test.png"), "rb")
        response_creation_set = client_user.post(
            "/sets/creation_set/",
            {
                "name": "set_0",
                "file": image,
                "type_set": "Entreprise",
                "description": "description set_0",
            },
        )	#	Création de set

        set_id = response_creation_set.url.split('/')[-2]

        response_event = client_user.post(
            "/sets/creation_evenement/" + set_id + "/",
            {"name": "event_0", "description": "description event_0"},
        )	# Création d'évènement

        event_id = response_event.url.split('/')[-2]

        posts_before = len(PublicationEvenement.objects.all())
        image1 = open(os.path.join(os.getcwd(), "tests/test.png"), "rb")
        image2 = open(os.path.join(os.getcwd(), "tests/test.png"), "rb")
        response = client_user.post(
            "/sets/make_post_event/" + event_id + "/",
            {
                "publication_text": "text de la publication",
                "file_1": image1,
                "file_2": image2,
            },
        )	#	Publication dans l'évènement
        posts_after = len(PublicationEvenement.objects.all())
        self.assertTrue(posts_after == posts_before + 1)
        self.assertTrue(
            response.url == "../../event/" + event_id + "/"
        )
        self.assertTrue(response.status_code == 302)

    def test_integration_manage_like_post_set(self):
        """Gestion de like d'une publication de set"""
        client_user = Client()
        reponse_inscription = client_user.post(
            "/authentification/inscription/",
            {
                "name": "user",
                "email": "user@mail.mail",
                "password": "user_password",
                "confirmation_password": "user_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user.post(
            "/authentification/activation_compte/?mail="
            + "user@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte

        sets_before = len(Sets.objects.all())
        image0 = open(os.path.join(os.getcwd(), "tests/test.png"), "rb")
        response_creation_set = client_user.post(
            "/sets/creation_set/",
            {
                "name": "set_0",
                "file": image0,
                "type_set": "Entreprise",
                "description": "description set_0",
            },
        )	#	Création de set

        set_id = response_creation_set.url.split('/')[-2]

        posts_before = len(PublicationSet.objects.all())
        image1 = open(os.path.join(os.getcwd(), "tests/test.png"), "rb")
        image2 = open(os.path.join(os.getcwd(), "tests/test.png"), "rb")
        response = client_user.post(
            "/sets/make_post_set/" + set_id + "/",
            {
                "publication_text": "text de la publication",
                "file_1": image1,
                "file_2": image2,
            },
        )		# Publication dans le set

        publication = PublicationSet.objects.all().order_by('-date')[len(PublicationSet.objects.all())-1]

        likes_before = len(JaimePublicationSet.objects.all())
        response = client_user.post(
            "/sets/manage_like_post_set/" + str(publication.id) + "/"
        )
        likes_intermediary = len(JaimePublicationSet.objects.all())
        self.assertTrue(likes_intermediary == likes_before + 1)
        self.assertTrue(response.content == b"like_make")
        self.assertTrue(response.status_code == 200)
        response = client_user.post(
            "/sets/manage_like_post_set/" + str(publication.id) + "/"
        )
        likes_after = len(JaimePublicationSet.objects.all())
        self.assertTrue(likes_after == likes_intermediary - 1)
        self.assertTrue(response.content == b"unlike_make")
        self.assertTrue(response.status_code == 200)

    def test_integration_manage_like_post_event(self):
        """Gestion de like d'une publication d'un évènem€nt"""
        client_user = Client()
        reponse_inscription = client_user.post(
            "/authentification/inscription/",
            {
                "name": "user",
                "email": "user@mail.mail",
                "password": "user_password",
                "confirmation_password": "user_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user.post(
            "/authentification/activation_compte/?mail="
            + "user@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte

        sets_before = len(Sets.objects.all())
        image0 = open(os.path.join(os.getcwd(), "tests/test.png"), "rb")
        response_creation_set = client_user.post(
            "/sets/creation_set/",
            {
                "name": "set_0",
                "file": image0,
                "type_set": "Entreprise",
                "description": "description set_0",
            },
        )	#	Création de set

        set_id = response_creation_set.url.split('/')[-2]

        response_event = client_user.post(
            "/sets/creation_evenement/" + set_id + "/",
            {"name": "event_0", "description": "description event_0"},
        )	# Création d'évènement

        event_id = response_event.url.split('/')[-2]

        posts_before = len(PublicationEvenement.objects.all())
        image1 = open(os.path.join(os.getcwd(), "tests/test.png"), "rb")
        image2 = open(os.path.join(os.getcwd(), "tests/test.png"), "rb")
        response = client_user.post(
            "/sets/make_post_event/" + event_id + "/",
            {
                "publication_text": "text de la publication",
                "file_1": image1,
                "file_2": image2,
            },
        )	#	Publication dans l'évènement

        publication = PublicationEvenement.objects.all().order_by('-date')[len(PublicationEvenement.objects.all())-1]

        likes_before = len(JaimePublicationEvenement.objects.all())
        response = client_user.post(
            "/sets/manage_like_post_event/"
            + str(publication.id)
            + "/"
        )
        likes_intermediary = len(JaimePublicationEvenement.objects.all())
        self.assertTrue(likes_intermediary == likes_before + 1)
        self.assertTrue(response.content == b"like_make")
        self.assertTrue(response.status_code == 200)
        response = client_user.post(
            "/sets/manage_like_post_event/"
            + str(publication.id)
            + "/"
        )
        likes_after = len(JaimePublicationEvenement.objects.all())
        self.assertTrue(likes_after == likes_intermediary - 1)
        self.assertTrue(response.content == b"unlike_make")
        self.assertTrue(response.status_code == 200)

    def test_integration_delete_add_set(self):
        """Ajout ett suppression d'un utilisateur dans le set"""
        client_user0 = Client()
        reponse_inscription = client_user0.post(
            "/authentification/inscription/",
            {
                "name": "user0",
                "email": "user0@mail.mail",
                "password": "user0_password",
                "confirmation_password": "user0_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user0@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user0.post(
            "/authentification/activation_compte/?mail="
            + "user0@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte

        client_user1 = Client()
        reponse_inscription = client_user1.post(
            "/authentification/inscription/",
            {
                "name": "user1",
                "email": "user1@mail.mail",
                "password": "user1_password",
                "confirmation_password": "user1_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user1@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user1.post(
            "/authentification/activation_compte/?mail="
            + "user1@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte

        image0 = open(os.path.join(os.getcwd(), "tests/test.png"), "rb")
        response_creation_set = client_user1.post(
            "/sets/creation_set/",
            {
                "name": "set_0",
                "file": image0,
                "type_set": "Entreprise",
                "description": "description set_0",
            },
        )	#	Création de set

        set_id = response_creation_set.url.split('/')[-2]

        users_before = len(SetUtilisateurs.objects.all())
        response_delet_add = client_user1.post(
            "/sets/delete_add_user_set/"
            + set_id
            + "/"
            + str(client_user0.session['user_id'])
            + "/"
        )	# Ajout d'un nouvel utilisateur
        users_intermediary = len(SetUtilisateurs.objects.all())
        self.assertTrue(users_intermediary == (users_before + 1))
        self.assertTrue(response_delet_add.content == b"user_added")
        self.assertTrue(
            SetUtilisateurs.objects.get(
                set0=set_id, utilisateur=client_user0.session['user_id']
            ).statut
            == "attente_validation"
        )
        self.assertTrue(response_delet_add.status_code == 200)
        response_delet_add = client_user1.post(
            "/sets/delete_add_user_set/"
            + set_id
            + "/"
            + str(client_user0.session['user_id'])
            + "/"
        )	#	Suppression d'un nouvel utilisateur
        users_after = len(SetUtilisateurs.objects.all())
        self.assertTrue(users_after == (users_intermediary - 1))
        self.assertTrue(response_delet_add.content == b"user_deleted")

    def test_integration_manage_enter_set(self):
        """Gestion d'entrer dans un set"""
        client_user0 = Client()
        reponse_inscription = client_user0.post(
            "/authentification/inscription/",
            {
                "name": "user0",
                "email": "user0@mail.mail",
                "password": "user0_password",
                "confirmation_password": "user0_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user0@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user0.post(
            "/authentification/activation_compte/?mail="
            + "user0@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte

        client_user1 = Client()
        reponse_inscription = client_user1.post(
            "/authentification/inscription/",
            {
                "name": "user1",
                "email": "user1@mail.mail",
                "password": "user1_password",
                "confirmation_password": "user1_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user1@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user1.post(
            "/authentification/activation_compte/?mail="
            + "user1@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte

        client_user2 = Client()
        reponse_inscription = client_user2.post(
            "/authentification/inscription/",
            {
                "name": "user2",
                "email": "user2@mail.mail",
                "password": "user2_password",
                "confirmation_password": "user2_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user2@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user2.post(
            "/authentification/activation_compte/?mail="
            + "user2@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte

        image0 = open(os.path.join(os.getcwd(), "tests/test.png"), "rb")
        response_creation_set = client_user1.post(
            "/sets/creation_set/",
            {
                "name": "set_0",
                "file": image0,
                "type_set": "Entreprise",
                "description": "description set_0",
            },
        )	#	Création de set

        set_id = response_creation_set.url.split('/')[-2]

        response_delet_add = client_user1.post(
            "/sets/delete_add_user_set/"
            + set_id
            + "/"
            + str(client_user0.session['user_id'])
            + "/"
        )	#	Ajout d'un nouvel utilisateur

        response_delet_add = client_user1.post(
            "/sets/delete_add_user_set/"
            + set_id
            + "/"
            + str(client_user2.session['user_id'])
            + "/"
        )	#	Ajout d'un nouvel utilisateur

        self.assertTrue(
            SetUtilisateurs.objects.get(utilisateur=client_user0.session['user_id']).statut
            == "attente_validation"
        )
        response = client_user0.post(
            "/sets/manage_enter_user_set/" + set_id + "/?confirm_enter=yes"
        )		#	Confirmation d'entrée dans le set
        self.assertTrue(
            SetUtilisateurs.objects.get(utilisateur=client_user0.session['user_id']).statut == "dans_set"
        )
        self.assertTrue(response.content == b"added_done")
        self.assertTrue(response.status_code == 200)

        self.assertTrue(
            SetUtilisateurs.objects.get(utilisateur=client_user2.session['user_id']).statut
            == "attente_validation"
        )
        response = client_user2.post(
            "/sets/manage_enter_user_set/" + set_id + "/?confirm_enter=no"
        )		#	Refus d'entrée dans le set
        self.assertTrue(
            len(SetUtilisateurs.objects.filter(utilisateur=client_user2.session['user_id'])) == 0
        )
        self.assertTrue(response.content == b"delete_done")
        self.assertTrue(response.status_code == 200)

    def test_integration_exit_set(self):
        """Sortie d'un set"""
        client_user = Client()
        reponse_inscription = client_user.post(
            "/authentification/inscription/",
            {
                "name": "user",
                "email": "user@mail.mail",
                "password": "user_password",
                "confirmation_password": "user_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user.post(
            "/authentification/activation_compte/?mail="
            + "user@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte

        sets_before = len(Sets.objects.all())
        image0 = open(os.path.join(os.getcwd(), "tests/test.png"), "rb")
        response_creation_set = client_user.post(
            "/sets/creation_set/",
            {
                "name": "set_0",
                "file": image0,
                "type_set": "Entreprise",
                "description": "description set_0",
            },
        )	#	Création de set

        set_id = response_creation_set.url.split('/')[-2]

        users_before = len(SetUtilisateurs.objects.all())
        response = client_user.post(
            "/sets/exit_set/" + set_id + "/"
        )
        users_after = len(SetUtilisateurs.objects.all())
        self.assertTrue(users_after == users_before - 1)
        self.assertTrue(response.content == b"delete_done_and_set_delete_done")
        self.assertTrue(response.status_code == 200)

    def test_integration_delete_set(self):
        """Suppression d'un set"""
        client_user = Client()
        reponse_inscription = client_user.post(
            "/authentification/inscription/",
            {
                "name": "user",
                "email": "user@mail.mail",
                "password": "user_password",
                "confirmation_password": "user_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user.post(
            "/authentification/activation_compte/?mail="
            + "user@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte

        sets_before = len(Sets.objects.all())
        image0 = open(os.path.join(os.getcwd(), "tests/test.png"), "rb")
        response_creation_set = client_user.post(
            "/sets/creation_set/",
            {
                "name": "set_0",
                "file": image0,
                "type_set": "Entreprise",
                "description": "description set_0",
            },
        )	#	Création de set

        set_id = response_creation_set.url.split('/')[-2]

        sets_before = len(Sets.objects.all())
        response = client_user.post(
            "/sets/delete_set/" + set_id + "/"
        )
        sets_after = len(Sets.objects.all())
        self.assertTrue(sets_after == sets_before - 1)
        self.assertTrue(response.url == "../../../user/home/")
        self.assertTrue(response.status_code == 302)

    def test_integration_delete_event(self):
        """Suppression d'un évènement"""
        client_user = Client()
        reponse_inscription = client_user.post(
            "/authentification/inscription/",
            {
                "name": "user",
                "email": "user@mail.mail",
                "password": "user_password",
                "confirmation_password": "user_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user.post(
            "/authentification/activation_compte/?mail="
            + "user@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte

        sets_before = len(Sets.objects.all())
        image = open(os.path.join(os.getcwd(), "tests/test.png"), "rb")
        response_creation_set = client_user.post(
            "/sets/creation_set/",
            {
                "name": "set_0",
                "file": image,
                "type_set": "Entreprise",
                "description": "description set_0",
            },
        )	#	Création de set

        set_id = response_creation_set.url.split('/')[-2]

        response_event = client_user.post(
            "/sets/creation_evenement/" + set_id + "/",
            {"name": "event_0", "description": "description event_0"},
        )	# Création d'évènement

        event_id = response_event.url.split('/')[-2]

        events_before = len(Evenements.objects.all())
        response = client_user.post(
            "/sets/delete_event/" + event_id + "/"
        )
        events_after = len(Evenements.objects.all())
        self.assertTrue(events_after == events_before - 1)
        self.assertTrue(
            response.url == "../../set/" + set_id + "/"
        )
        self.assertTrue(response.status_code == 302)

    def test_integration_manage_contact(self):
        """Ajout et suppression de contacts"""
        client_user0 = Client()
        reponse_inscription = client_user0.post(
            "/authentification/inscription/",
            {
                "name": "user0",
                "email": "user0@mail.mail",
                "password": "user0_password",
                "confirmation_password": "user0_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user0@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user0.post(
            "/authentification/activation_compte/?mail="
            + "user0@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte

        client_user1 = Client()
        reponse_inscription = client_user1.post(
            "/authentification/inscription/",
            {
                "name": "user1",
                "email": "user1@mail.mail",
                "password": "user1_password",
                "confirmation_password": "user1_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user1@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user1.post(
            "/authentification/activation_compte/?mail="
            + "user1@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte

        contacts_before = len(Contact.objects.filter(contact_owner=client_user0.session['user_id']))
        response = client_user0.get(
            "/user/manage_contact/" + str(client_user1.session['user_id']) + "/"
        )
        contacts_intermediary = len(Contact.objects.filter(contact_owner=client_user0.session['user_id']))
        self.assertTrue(contacts_intermediary == contacts_before + 1)
        self.assertTrue(response.content == b"contact_added")
        self.assertTrue(response.status_code == 200)
        response = client_user0.get(
            "/user/manage_contact/" + str(client_user1.session['user_id']) + "/"
        )
        contacts_after = len(Contact.objects.filter(contact_owner=client_user0.session['user_id']))
        self.assertTrue(contacts_after == contacts_intermediary - 1)
        self.assertTrue(response.content == b"contact_deleted")
        self.assertTrue(response.status_code == 200)

    def test_integration_contacts(self):
        """Consultation des contacts"""
        client_user0 = Client()
        reponse_inscription = client_user0.post(
            "/authentification/inscription/",
            {
                "name": "user0",
                "email": "user0@mail.mail",
                "password": "user0_password",
                "confirmation_password": "user0_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user0@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user0.post(
            "/authentification/activation_compte/?mail="
            + "user0@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte

        response = client_user0.get("/user/contacts/")
        self.assertTemplateUsed(response, "contact.html")
        self.assertTrue(response.status_code == 200)

    def test_integration_messages(self):
        """Consultation des messages"""
        client_user0 = Client()
        reponse_inscription = client_user0.post(
            "/authentification/inscription/",
            {
                "name": "user0",
                "email": "user0@mail.mail",
                "password": "user0_password",
                "confirmation_password": "user0_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user0@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user0.post(
            "/authentification/activation_compte/?mail="
            + "user0@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte

        response = client_user0.get("/user/messages/")
        self.assertTemplateUsed(response, "message.html")
        self.assertTrue(response.status_code == 200)

    def test_integration_messages_exchanges(self):
        """Consultation de messages échangés"""
        client_user0 = Client()
        reponse_inscription = client_user0.post(
            "/authentification/inscription/",
            {
                "name": "user0",
                "email": "user0@mail.mail",
                "password": "user0_password",
                "confirmation_password": "user0_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user0@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user0.post(
            "/authentification/activation_compte/?mail="
            + "user0@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte

        client_user1 = Client()
        reponse_inscription = client_user1.post(
            "/authentification/inscription/",
            {
                "name": "user1",
                "email": "user1@mail.mail",
                "password": "user1_password",
                "confirmation_password": "user1_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user1@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user1.post(
            "/authentification/activation_compte/?mail="
            + "user1@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte

        response = client_user0.get(
            "/user/messages_exchanges/" + str(client_user1.session['user_id']) + "/"
        )
        self.assertTemplateUsed(response, "message_exchange.html")
        self.assertTrue(response.status_code == 200)



    def test_integration_send_message(self):
        """Envoie d'un message"""
        client_user0 = Client()
        reponse_inscription = client_user0.post(
            "/authentification/inscription/",
            {
                "name": "user0",
                "email": "user0@mail.mail",
                "password": "user0_password",
                "confirmation_password": "user0_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user0@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user0.post(
            "/authentification/activation_compte/?mail="
            + "user0@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte

        client_user1 = Client()
        reponse_inscription = client_user1.post(
            "/authentification/inscription/",
            {
                "name": "user1",
                "email": "user1@mail.mail",
                "password": "user1_password",
                "confirmation_password": "user1_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user1@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user1.post(
            "/authentification/activation_compte/?mail="
            + "user1@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte

        messages_before = len(Message.objects.all())
        response = client_user0.get(
            "/user/send_message/" + str(client_user1.session['user_id']) + "/?message_text=hello"
        )
        messages_after = len(Message.objects.all())
        self.assertTrue(messages_after == messages_before + 1)
        self.assertTrue(response.content == b"send")
        self.assertTrue(response.status_code == 200)

    def test_integration_updates_messages(self):
        """Mise a jour des messages de la discussion"""
        client_user0 = Client()
        reponse_inscription = client_user0.post(
            "/authentification/inscription/",
            {
                "name": "user0",
                "email": "user0@mail.mail",
                "password": "user0_password",
                "confirmation_password": "user0_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user0@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user0.post(
            "/authentification/activation_compte/?mail="
            + "user0@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte

        client_user1 = Client()
        reponse_inscription = client_user1.post(
            "/authentification/inscription/",
            {
                "name": "user1",
                "email": "user1@mail.mail",
                "password": "user1_password",
                "confirmation_password": "user1_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user1@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user1.post(
            "/authentification/activation_compte/?mail="
            + "user1@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte

        response = client_user0.get(
            "/user/updates_messages_user/"
            + str(client_user1.session['user_id'])
            + "/?last_message_id="
            + '0'
        )
        self.assertTemplateUsed(response, "un_message.html")
        self.assertTrue(response.status_code == 200)

    def test_integration_update_image_cover(self):
        """Mise à jour de l'image de profil"""
        client_user0 = Client()
        reponse_inscription = client_user0.post(
            "/authentification/inscription/",
            {
                "name": "user0",
                "email": "user0@mail.mail",
                "password": "user0_password",
                "confirmation_password": "user0_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user0@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user0.post(
            "/authentification/activation_compte/?mail="
            + "user0@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte

        image = open(os.path.join(os.getcwd(), "tests/test.png"), "rb")
        image_before = Utilisateurs.objects.get(id=client_user0.session['user_id']).image_profil
        response = client_user0.post("/user/update_image_cover/", {"file": image})
        self.assertTrue(
            response.url
            == "../../user/profil/"
            + str(client_user0.session['user_id'])
            + "/?section_profil=coordonees"
        )
        image_after = Utilisateurs.objects.get(id=client_user0.session['user_id']).image_profil
        self.assertTrue( image_before != image_after )
        self.assertTrue(response.status_code == 302)

    def test_integration_update_profil_name(self):
        """Mise à jour du nom du compte"""
        client_user0 = Client()
        reponse_inscription = client_user0.post(
            "/authentification/inscription/",
            {
                "name": "user0",
                "email": "user0@mail.mail",
                "password": "user0_password",
                "confirmation_password": "user0_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user0@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user0.post(
            "/authentification/activation_compte/?mail="
            + "user0@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte
        nom_before = Utilisateurs.objects.get(id=client_user0.session['user_id']).nom
        response = client_user0.post(
            "/user/update_profil_name/", {"name": "nouveau_user"}
        )
        self.assertTrue(
            response.url
            == "../../user/profil/"
            + str(client_user0.session['user_id'])
            + "/?section_profil=coordonees"
        )
        nom_after = Utilisateurs.objects.get(id=client_user0.session['user_id']).nom
        self.assertTrue( nom_before != nom_after )
        self.assertTrue(
            Utilisateurs.objects.get(id=client_user0.session['user_id']).nom == "nouveau_user"
        )
        self.assertTrue(response.status_code == 302)

    def test_integration_update_profil_mail(self):
        """Mise à jour des mails du compte"""
        client_user0 = Client()
        reponse_inscription = client_user0.post(
            "/authentification/inscription/",
            {
                "name": "user0",
                "email": "user0@mail.mail",
                "password": "user0_password",
                "confirmation_password": "user0_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user0@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user0.post(
            "/authentification/activation_compte/?mail="
            + "user0@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte

        mail_before = Utilisateurs.objects.get(id=client_user0.session['user_id']).adresse_mail
        response = client_user0.post(
            "/user/update_profil_mail/", {"mail": "new_user@mail.mail"}
        )
        self.assertTrue(
            response.url
            == "../../user/profil/"
            + str(client_user0.session['user_id'])
            + "/?section_profil=coordonees"
        )
        mail_after = Utilisateurs.objects.get(id=client_user0.session['user_id']).adresse_mail
        self.assertTrue( mail_before != mail_after )
        self.assertTrue(
            Utilisateurs.objects.get(id=client_user0.session['user_id']).adresse_mail == "new_user@mail.mail"
        )
        self.assertTrue(response.status_code == 302)

    def test_integration_suppression_compte(self):
        """Suppression du compte"""
        client_user0 = Client()
        reponse_inscription = client_user0.post(
            "/authentification/inscription/",
            {
                "name": "user0",
                "email": "user0@mail.mail",
                "password": "user0_password",
                "confirmation_password": "user0_password",
            },
        )    # Inscription

        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user0@mail.mail"
        ).cle_dactivation_de_compte
        response = client_user0.post(
            "/authentification/activation_compte/?mail="
            + "user0@mail.mail"
            + "&key_activation="
            + activation_key_before
        )		#	Activation du compte
        users_before = len(Utilisateurs.objects.all())
        response = client_user0.get("/user/suppression_compte/")
        users_after = len(Utilisateurs.objects.all())
        self.assertTrue( users_after == users_before - 1 )
        self.assertTrue(response.url == "../../authentification/connexion/")
        self.assertTrue(response.status_code == 302)
