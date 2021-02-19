""""""

from django.test import TestCase, RequestFactory, Client

from user.models import Utilisateurs

from authentification.views import connexion


class AuthentificationViewsTestCase(TestCase):
	""""""

	def setUp(self):
		""""""
		self.factory = RequestFactory()
		self.client = Client()

		Utilisateurs.objects.create(nom="nom", adresse_mail="mail@mail.mail", mot_de_passe='password')


	def test_connexion_0(self):
		""""""
		#  Connexion reussie
		response = self.client.post('/authentification/connexion/', {'email':'mail@mail.mail', 'password':'password'})
		self.assertEqual(response.url, '../../user/home/')




	def test_connexion_1(self):
		""""""

		#  Connexion avec une adresse email qui n'existe pas
		response = self.client.post('/authentification/connexion/', {'email':'mail0@mail0.mail0', 'password':'password'})
		self.assertEqual(response.content, b'Aucun utilisateur ne possede un compte avec cette adresse mail')



	def test_connexion_2(self):
		""""""

		#  Connexion avec un mauvais mot de passe
		response = self.client.post('/authentification/connexion/', {'email':'mail@mail.mail', 'password':'passwo'})
		self.assertEqual(response.content, b"Mot de passe incorrect")



	def test_connexion_3(self):
		""""""

    	#  Connexion avec un formulaire invalide
		response = self.client.post('/authentification/connexion/', {'email':'mail@mail', 'password':'password'})
		self.assertEqual(response.content, b"Formulaire pas valide")

		


	def test_inscription_0(self):
		""""""
		#  Inscription reussie
		response = self.client.post('/authentification/inscription/', {'name':'name', 'email':'mail0@mail0.mail0', 'password':'password', 'confirmation_password':'password'})
		self.assertEqual(response.url, '../../user/home/')


	def test_inscription_1(self):
		""""""
		#  Insription avec un email qui appartient déjà à un utilisateur
		response = self.client.post('/authentification/inscription/', {'name':'name', 'email':'mail@mail.mail', 'password':'password', 'confirmation_password':'password'})
		self.assertEqual(response.content, b"Un compte possedant cette adresse mail existe deja")

	def test_inscription_2(self):
		""""""
		#  Inscription avec un mot de passe qui ne correspond pas la confirmation du mot de passe
		response = self.client.post('/authentification/inscription/', {'name':'name', 'email':'mail0@mail0.mail0', 'password':'password', 'confirmation_password':'confirmation_password'})
		self.assertEqual(response.content, b"Mot de passe different de la confirmation")


	def test_envoie_lien_reinitialisation_password(self):
		""""""

		#  ...
		pass


	def test_reinitialisation_mot_de_passe_0(self):
		""""""
		#  Réinitialisation si l'utilisateur est connecté
		#  response = self.client.post('/authentification/reinitialisation_password/', {'password':'password', 'confirmation_password':'password'})
		#  Réinitialisation réussi
		#  Réinitialisation avec des mots passe qui ne correspondent pas
		#  Réinitialisation avec un formulaire invalide ( qui contient au moins un champs vide )
		pass


	def test_reinitialisation_mot_de_passe_1(self):
		""""""
		#  Réinitialisation si l'utilisateur est connecté
		#  Réinitialisation réussi
		#  response = self.client.post('/authentification/reinitialisation_password/', {'password':'password', 'confirmation_password':'password'})
		#  Réinitialisation avec des mots passe qui ne correspondent pas
		#  Réinitialisation avec un formulaire invalide ( qui contient au moins un champs vide )
		pass


	def test_reinitialisation_mot_de_passe_2(self):
		""""""
		#  Réinitialisation si l'utilisateur est connecté
		#  Réinitialisation réussi
		#  Réinitialisation avec des mots passe qui ne correspondent pas
		#  Réinitialisation avec un formulaire invalide ( qui contient au moins un champs vide )
		pass


	def test_reinitialisation_mot_de_passe_3(self):
		""""""
		#  Réinitialisation réussi
		#  Réinitialisation avec des mots passe qui ne correspondent pas
		#  Réinitialisation avec un formulaire invalide ( qui contient au moins un champs vide )
		pass


	def test_initialisation_mot_de_passe_0(self):
		""""""
    	#  Réinitialisation réussi
    	#  Réinitialisation avec des mots passe qui ne correspondent pas
    	#  Réinitialisation avec un formulaire invalide ( qui contient au moins un champs vide )
		pass

	def test_initialisation_mot_de_passe_1(self):
		""""""
    	#  Réinitialisation réussi
    	#  Réinitialisation avec des mots passe qui ne correspondent pas
    	#  Réinitialisation avec un formulaire invalide ( qui contient au moins un champs vide )
		pass

	def test_initialisation_mot_de_passe_2(self):
		""""""
    	#  Réinitialisation réussi
    	#  Réinitialisation avec des mots passe qui ne correspondent pas
    	#  Réinitialisation avec un formulaire invalide ( qui contient au moins un champs vide )
		pass


