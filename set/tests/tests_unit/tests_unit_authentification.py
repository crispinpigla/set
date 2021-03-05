""""""
from django.core.mail import outbox

from unittest.mock import patch

import requests

from django.test import TestCase, RequestFactory, Client

from user.models import Utilisateurs

from authentification.views import connexion





class AuthentificationViewsTestCase(TestCase):
	""""""

	def setUp(self):
		""""""

		self.client_not_registred = Client()

		self.user_registred_not_connected = Utilisateurs.objects.create(nom="user_registred_not_connected", adresse_mail="user_registred_not_connected@mail.mail", mot_de_passe='user_registred_not_connected_password', cle_dactivation_de_compte="user_registred_not_connected_cle_dactivation_de_compte"  )
		self.user_registred_not_connected_reset_password = Utilisateurs.objects.create(nom="user_registred_not_connected_reset_password", adresse_mail="user_registred_not_connected_reset_password@mail.mail", mot_de_passe='user_registred_not_connected_reset_password_password', cle_de_reinitialisation_de_mot_de_passe="cle_de_reinitialisation_de_mot_de_passe" )
		self.user_registred_connected = Utilisateurs.objects.create(nom="user_registred_connected", adresse_mail="user_registred_connected@mail.mail", mot_de_passe='user_registred_connected_password', cle_dactivation_de_compte="cle_dactivation_de_compte" )

		self.client_registred_not_connected = Client()

		self.client_registred_not_connected_reset_password = Client()

		self.client_registred_connected = Client()
		self.client_registred_connected.post('/authentification/connexion/', {'email':'user_registred_connected@mail.mail', 'password':'user_registred_connected_password'})


	#   ----- Demande page de connexion

	def test_connexion_ask_page_unconnected_user(self):
		""""""
		#  demande de la page de connexion par un utilisateur non connecté
		response = self.client_registred_not_connected.get('/authentification/connexion/')
		self.assertTemplateUsed(response, 'connexion.html')
		self.assertTrue( response.status_code == 200 )

	def test_connexion_ask_page_connected_user(self):
		""""""
		#  demande de la page de connexion par un utilisateur connecté
		response = self.client_registred_connected.get('/authentification/connexion/')
		self.assertEqual(response.url, '../../user/home/')
		self.assertTemplateNotUsed(response, 'connexion.html')
		self.assertTrue( response.status_code == 302 )



	#   ----- Connexion

	def test_connexion_make_connexion_user_unconnected_success(self):
		""""""
		#  Demande de connexion avec succès d'un utilisateur
		response = self.client_registred_connected.post('/authentification/connexion/', {'email':'user_registred_not_connected@mail.mail', 'password':'user_registred_not_connected_password'})
		self.assertEqual(response.url, '../../user/home/')
		self.assertTemplateNotUsed(response, 'connexion.html')
		self.assertTrue( response.status_code == 302 )

	def test_connexion_make_connexion_user_unconnected_to_no_mail_account_in_application(self):
		""""""
		#  Demande de connexion avec un mail qui ne coresspond à aucun utilisateur de l'application
		response = self.client_registred_not_connected.post('/authentification/connexion/', {'email':'no_mail@mail.mail', 'password':'user_registred_not_connected_password'})
		self.assertTrue( response.context['no_mail_in_application_error'] )
		self.assertTemplateUsed(response, 'connexion.html')
		self.assertTrue( response.status_code == 200 )

	def test_connexion_make_connexion_user_unconnected_invalid_form_mail(self):
		""""""
		#  Demande de connexion avec un mail invalide dans le formulaire
		response = self.client_registred_not_connected.post('/authentification/connexion/', {'email':'user_registred_not_connected@mail', 'password':'user_registred_not_connected_password'})
		self.assertTrue( response.context['form_errors'] )
		self.assertTemplateUsed(response, 'connexion.html')
		self.assertTrue( response.status_code == 200 )

	def test_connexion_make_connexion_user_unconnected_wrong_password(self):
		""""""
		#  Demande de connexion avec un mot de passe incorrect
		response = self.client_registred_not_connected.post('/authentification/connexion/', {'email':'user_registred_not_connected@mail.mail', 'password':'wrong_password'})
		self.assertTrue( response.context['password_error'] )
		self.assertTemplateUsed(response, 'connexion.html')
		self.assertTrue( response.status_code == 200 )


	def test_connexion_make_connexion_user_connected(self):
		""""""
		#  Demande de connexion par un utilisareur connecté
		response = self.client_registred_connected.post('/authentification/connexion/', {'email':'user_registred_not_connected@mail.mail', 'password':'user_registred_not_connected_password'})
		self.assertEqual(response.url, '../../user/home/')
		self.assertTemplateNotUsed(response, 'connexion.html')
		self.assertTrue( response.status_code == 302 )


	#   ----- Demande de la page d'inscription

	def test_inscription_ask_page_unconnected_user(self):
		""""""
		#  Demande de la page d'incription par un utilisateur non connecté
		response = self.client_registred_not_connected.get('/authentification/inscription/')
		self.assertTemplateUsed(response, 'inscription.html')
		self.assertTrue( response.status_code == 200 )

	def test_inscription_ask_page_connected_user(self):
		""""""
		#  Demande de la page d'incription par un utilisateur connecté
		response = self.client_registred_connected.get('/authentification/inscription/')
		self.assertEqual(response.url, '../../user/home/')
		self.assertTemplateNotUsed(response, 'inscription.html')
		self.assertTrue( response.status_code == 302 )


	#   ----- Inscription

	def test_inscription_connected_user(self):
		""""""
		#  Demande d'inscription par un utilisateur connecté
		users_before = len(Utilisateurs.objects.all())
		response = self.client_registred_connected.post('/authentification/inscription/', {'name':'user_not_registred', 'email':'user_not_registred@mail.mail', 'password':'user_not_registred_password', 'confirmation_password':'user_not_registred_password'})
		users_after = len(Utilisateurs.objects.all())
		self.assertTrue( users_after == users_before )
		self.assertEqual(response.url, '../../user/home/')
		self.assertTemplateNotUsed(response, 'inscription.html')
		self.assertTrue( response.status_code == 302 )


	def test_inscription_invalid_form_name(self):
		""""""
		#  Demande d'inscription avec un nom de formulaire invalide
		users_before = len(Utilisateurs.objects.all())
		response = self.client_not_registred.post('/authentification/inscription/', {'name':'', 'email':'user_not_registred@mail.mail', 'password':'user_not_registred_password', 'confirmation_password':'user_not_registred_password'})
		users_after = len(Utilisateurs.objects.all())
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, 'inscription.html')
		self.assertTrue( response.context["inscription_form_error"] )
		self.assertTrue( response.status_code == 200 )

	def test_inscription_invalid_form_mail(self):
		""""""
		#  Demande d'inscription avec un mail de formulaire invalide
		users_before = len(Utilisateurs.objects.all())
		response = self.client_not_registred.post('/authentification/inscription/', {'name':'', 'email':'user_not_registred', 'password':'user_not_registred_password', 'confirmation_password':'user_not_registred_password'})
		users_after = len(Utilisateurs.objects.all())
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, 'inscription.html')
		self.assertTrue( response.context["inscription_form_error"] )
		self.assertTrue( response.status_code == 200 )

	def test_inscription_invalid_form_password(self):
		""""""
		#  Demande d'inscription avec un mot de passe de formulaire invalide
		users_before = len(Utilisateurs.objects.all())
		response = self.client_not_registred.post('/authentification/inscription/', {'name':'user_not_registred', 'email':'user_not_registred@mail.mail', 'password':'', 'confirmation_password':'user_not_registred_password'})
		users_after = len(Utilisateurs.objects.all())
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, 'inscription.html')
		self.assertTrue( response.context["inscription_form_error"] )
		self.assertTrue( response.status_code == 200 )

	def test_inscription_invalid_form_confirmation_password(self):
		""""""
		#  Demande d'inscription avec une confirmation de mot de passe de formulaire invalide
		users_before = len(Utilisateurs.objects.all())
		response = self.client_not_registred.post('/authentification/inscription/', {'name':'user_not_registred', 'email':'user_not_registred@mail.mail', 'password':'user_not_registred_password', 'confirmation_password':''})
		users_after = len(Utilisateurs.objects.all())
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, 'inscription.html')
		self.assertTrue( response.context["inscription_form_error"] )
		self.assertTrue( response.status_code == 200 )

	def test_inscription_no_match_passwords(self):
		""""""
		#  Demande d'inscription avec des mots de passe qui ne sont pas identiques
		users_before = len(Utilisateurs.objects.all())
		response = self.client_not_registred.post('/authentification/inscription/', {'name':'user_not_registred', 'email':'user_not_registred@mail.mail', 'password':'password', 'confirmation_password':'another_password'})
		users_after = len(Utilisateurs.objects.all())
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, 'inscription.html')
		self.assertTrue( response.context["no_match_password_error"] )
		self.assertTrue( response.status_code == 200 )

	def test_inscription_account_already_exist(self):
		""""""
		#  Demande d'inscription avec un compte déjà existant
		users_before = len(Utilisateurs.objects.all())
		response = self.client_not_registred.post('/authentification/inscription/', {'name':'user_not_registred', 'email':'user_registred_not_connected@mail.mail', 'password':'user_not_registred_password', 'confirmation_password':'user_not_registred_password'})
		users_after = len(Utilisateurs.objects.all())
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, 'inscription.html')
		self.assertTrue( response.context["already_mail_error"] )
		self.assertTrue( response.status_code == 200 )

	def test_inscription_success(self):
		""""""
		#  Demande d'inscription avec succès
		users_before = len(Utilisateurs.objects.all())
		response = self.client_not_registred.post('/authentification/inscription/', {'name':'user_not_registred', 'email':'user_not_registred@mail.mail', 'password':'user_not_registred_password', 'confirmation_password':'user_not_registred_password'})
		users_after = len(Utilisateurs.objects.all())
		self.assertTrue( users_after == users_before + 1 )
		self.assertEqual(response.url, '../../user/home/')
		self.assertTrue( response.status_code == 302 )


	#   ----- Demande de la page d'initialisation de mot de passe

	def test_initialisation_mot_de_passe_ask_page_connected_user(self):
		""""""
		#  Demande de la page d'initialisation de mot de passe par un utilisateur connecté
		response = self.client_registred_connected.get('/authentification/initialisation_mot_de_passe/')
		self.assertEqual(response.url, '../../user/home/')
		self.assertTemplateNotUsed(response, 'initialisation_mot_de_passe.html')
		self.assertTrue( response.status_code == 302 )

	def test_initialisation_mot_de_passe_ask_page_unconnected_user(self):
		""""""
		#  Demande de la page d'initialisation de mot de passe par un utilisateur non connecté
		response = self.client_registred_not_connected.get('/authentification/initialisation_mot_de_passe/?name=user_not_registred&mail=user_not_registred@mail.mail')
		self.assertTemplateUsed(response, 'initialisation_mot_de_passe.html')
		self.assertTrue( response.status_code == 200 )



	#   ----- Initialisation de mot de passe

	def test_initialisation_mot_de_passe_connected_user(self):
		""""""
		#  Demande d'initialisation de mot de passe par un utilisateur connecté
		users_before = len(Utilisateurs.objects.all())
		response = self.client_registred_connected.post('/authentification/initialisation_mot_de_passe/', {'name':'user_not_registred', 'email':'user_not_registred@mail.mail', 'password':'user_not_registred_password', 'confirmation_password':'user_not_registred_password'})
		users_after = len(Utilisateurs.objects.all())
		self.assertTrue( users_after == users_before )
		self.assertEqual(response.url, '../../user/home/')
		self.assertTemplateNotUsed(response, 'initialisation_mot_de_passe.html')
		self.assertTrue( response.status_code == 302 )


	def test_initialisation_mot_de_passe_invalid_name_form(self):
		""""""
		#  Demande d'initialisation de mot de passe avec un nom de formulaire invalide
		users_before = len(Utilisateurs.objects.all())
		response = self.client_not_registred.post('/authentification/initialisation_mot_de_passe/', {'name':'', 'email':'user_not_registred@mail.mail', 'password':'user_not_registred_password', 'confirmation_password':'user_not_registred_password'})
		users_after = len(Utilisateurs.objects.all())
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, 'initialisation_mot_de_passe.html')
		self.assertTrue( response.context["initialize_form_errors"] )
		self.assertTrue( response.status_code == 200 )

	def test_initialisation_mot_de_passe_invalid_mail_form(self):
		""""""
		#  Demande d'initialisation de mot de passe avec un mail de formulaire invalide
		users_before = len(Utilisateurs.objects.all())
		response = self.client_not_registred.post('/authentification/initialisation_mot_de_passe/', {'name':'', 'email':'user_not_registred', 'password':'user_not_registred_password', 'confirmation_password':'user_not_registred_password'})
		users_after = len(Utilisateurs.objects.all())
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, 'initialisation_mot_de_passe.html')
		self.assertTrue( response.context["initialize_form_errors"] )
		self.assertTrue( response.status_code == 200 )

	def test_initialisation_mot_de_passe_invalid_password_form(self):
		""""""
		#  Demande d'initialisation de mot de passe avec un mot de passe de formulaire invalide
		users_before = len(Utilisateurs.objects.all())
		response = self.client_not_registred.post('/authentification/initialisation_mot_de_passe/', {'name':'user_not_registred', 'email':'user_not_registred@mail.mail', 'password':'', 'confirmation_password':'user_not_registred_password'})
		users_after = len(Utilisateurs.objects.all())
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, 'initialisation_mot_de_passe.html')
		self.assertTrue( response.context["initialize_form_errors"] )
		self.assertTrue( response.status_code == 200 )

	def test_initialisation_mot_de_passe_invalid_confirmation_password_form(self):
		""""""
		#  Demande d'initialisation de mot de passe avec une confirmation de mot de passe de formulaire invalide
		users_before = len(Utilisateurs.objects.all())
		response = self.client_not_registred.post('/authentification/initialisation_mot_de_passe/', {'name':'user_not_registred', 'email':'user_not_registred@mail.mail', 'password':'user_not_registred_password', 'confirmation_password':''})
		users_after = len(Utilisateurs.objects.all())
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, 'initialisation_mot_de_passe.html')
		self.assertTrue( response.context["initialize_form_errors"] )
		self.assertTrue( response.status_code == 200 )

	def test_initialisation_mot_de_passe_no_match_password(self):
		""""""
		#  Demande d'initialisation de mot de passe avec des mots de passe qui ne sont pas identiques
		users_before = len(Utilisateurs.objects.all())
		response = self.client_not_registred.post('/authentification/initialisation_mot_de_passe/', {'name':'user_not_registred', 'email':'user_not_registred@mail.mail', 'password':'password', 'confirmation_password':'another_password'})
		users_after = len(Utilisateurs.objects.all())
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, 'initialisation_mot_de_passe.html')
		self.assertTrue( response.context["no_match_password_error"] )
		self.assertTrue( response.status_code == 200 )

	def test_initialisation_mot_de_passe_already_mail_account_exist(self):
		""""""
		#  Demande d'initialisation de mot de passe avec un compte déjà existant
		users_before = len(Utilisateurs.objects.all())
		response = self.client_not_registred.post('/authentification/initialisation_mot_de_passe/', {'name':'user_not_registred', 'email':'user_registred_not_connected@mail.mail', 'password':'user_not_registred_password', 'confirmation_password':'user_not_registred_password'})
		users_after = len(Utilisateurs.objects.all())
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, 'initialisation_mot_de_passe.html')
		self.assertTrue( response.context["already_mail_error"] )
		self.assertTrue( response.status_code == 200 )

	def test_initialisation_mot_de_passe_success(self):
		""""""
		#  Demande d'initialisation de mot de passe avec succès
		users_before = len(Utilisateurs.objects.all())
		response = self.client_not_registred.post('/authentification/initialisation_mot_de_passe/', {'name':'user_not_registred', 'email':'user_not_registred@mail.mail', 'password':'user_not_registred_password', 'confirmation_password':'user_not_registred_password'})
		users_after = len(Utilisateurs.objects.all())
		self.assertTrue( users_after == users_before + 1 )
		self.assertEqual(response.url, '../../user/home/')
		self.assertTrue( response.status_code == 302 )



	#   ----- Demande de page d'envoie de lien de réinitialisation de mot passe

	def test_envoie_lien_reinitialisation_password_ask_page_connected_user(self):
		""""""
		#  Demande de page d'envoie de lien de réinitialisation de mot passe par un utilisateur connecté
		response = self.client_registred_connected.get('/authentification/envoie_lien_reinitialisation_password/')
		self.assertEqual(response.url, '../../user/home/')
		self.assertTemplateNotUsed(response, 'envoie_lien_reinitialisation_mot_de_passe.html')
		self.assertTrue( response.status_code == 302 )

	def test_envoie_lien_reinitialisation_password_ask_page_unconnected_user(self):
		""""""
		#  Demande de page d'envoie de lien de réinitialisation de mot passe par un utilisateur non connecté
		response = self.client_registred_not_connected.get('/authentification/envoie_lien_reinitialisation_password/')
		self.assertTemplateUsed(response, 'envoie_lien_reinitialisation_mot_de_passe.html')
		self.assertTrue( response.status_code == 200 )


	#   ----- Envoie de lien de réinitialisation de mot passe

	def test_envoie_lien_reinitialisation_password_user_mail_exist_in_application(self):
		""""""
		#  Envoie de lien de réinitialisation de mot passe pour un compte existant dans l'application
		self.assertTrue( Utilisateurs.objects.get(adresse_mail=self.user_registred_not_connected.adresse_mail).cle_de_reinitialisation_de_mot_de_passe == None )
		response = self.client_registred_not_connected.post('/authentification/envoie_lien_reinitialisation_password/', {'email':'user_registred_not_connected@mail.mail'})
		self.assertTrue( Utilisateurs.objects.get(adresse_mail=self.user_registred_not_connected.adresse_mail).cle_de_reinitialisation_de_mot_de_passe != None )
		self.assertTemplateUsed(response, 'envoie_lien_reinitialisation_mot_de_passe.html')
		self.assertTrue( response.context['send_mail'] )
		self.assertTrue( response.status_code == 200 )

	def test_envoie_lien_reinitialisation_password_user_mail_not_exist_in_application(self):
		""""""
		#  Envoie de lien de réinitialisation de mot passe pour un compte n'existant pas dans l'application
		self.assertTrue( Utilisateurs.objects.get(adresse_mail=self.user_registred_not_connected.adresse_mail).cle_de_reinitialisation_de_mot_de_passe == None )
		response = self.client_registred_not_connected.post('/authentification/envoie_lien_reinitialisation_password/', {'email':'not_exist_account@mail.mail'})
		self.assertTrue( Utilisateurs.objects.get(adresse_mail=self.user_registred_not_connected.adresse_mail).cle_de_reinitialisation_de_mot_de_passe == None )
		self.assertTemplateUsed(response, 'envoie_lien_reinitialisation_mot_de_passe.html')
		self.assertTrue( response.context['no_user_with_mail_error'] )
		self.assertTrue( response.status_code == 200 )



	#   ----- Demande de page de réinitialisation de mot passe

	def test_reinitialisation_mot_de_passe_ask_page_user_connected(self):
		""""""
		#  Demande de page de réinitialisation de mot passe par un utilisateur connecté
		response = self.client_registred_connected.get('/authentification/reinitialisation_password/' )
		self.assertEqual(response.url, '../../user/home/')
		self.assertTemplateNotUsed(response, 'reinitialisation_mot_de_passe.html')
		self.assertTrue( response.status_code == 302 )

	def test_reinitialisation_mot_de_passe_ask_page_user_not_connected_invalid_mail(self):
		""""""
		#  Demande de page de réinitialisation de mot passe avec un mail invalide
		response = self.client_registred_not_connected_reset_password.get('/authentification/reinitialisation_password/?mail=' + 'wrong_mail@mail.mail' + '&key_reinitialisation_password=' + self.user_registred_not_connected_reset_password.cle_de_reinitialisation_de_mot_de_passe )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_reinitialisation_mot_de_passe_ask_page_user_not_connected_invalid_key(self):
		""""""
		#  Demande de page de réinitialisation de mot passe avec une clé invalide
		response = self.client_registred_not_connected_reset_password.get('/authentification/reinitialisation_password/?mail=' + self.user_registred_not_connected_reset_password.adresse_mail + '&key_reinitialisation_password=' + 'wrong_key' )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_reinitialisation_mot_de_passe_ask_page_user_not_connected_success(self):
		""""""
		#  Demande de page de réinitialisation de mot passe avec succes
		response = self.client_registred_not_connected_reset_password.get('/authentification/reinitialisation_password/?mail=' + self.user_registred_not_connected_reset_password.adresse_mail + '&key_reinitialisation_password=' + self.user_registred_not_connected_reset_password.cle_de_reinitialisation_de_mot_de_passe )
		self.assertTemplateUsed(response, 'reinitialisation_mot_de_passe.html')
		self.assertTrue( response.status_code == 200 )



	#   ----- Réinitialisation de mot passe

	def test_reinitialisation_mot_de_passe_connected_user(self):
		""""""
		#  Réinitialisation de mot passe par un utilisateur connecté
		response = self.client_registred_connected.post('/authentification/reinitialisation_password/', {   } )
		self.assertEqual(response.url, '../../user/home/')
		self.assertTemplateNotUsed(response, 'reinitialisation_mot_de_passe.html')
		self.assertTrue( response.status_code == 302 )

	def test_reinitialisation_mot_de_passe_invalid_form_mail(self):
		""""""
		#  Réinitialisation de mot passe avec un mail de formuliare invailde
		self.assertTrue( Utilisateurs.objects.get(adresse_mail=self.user_registred_not_connected_reset_password.adresse_mail).cle_de_reinitialisation_de_mot_de_passe != None )
		response = self.client_registred_not_connected_reset_password.post('/authentification/reinitialisation_password/', {  'reset_key':self.user_registred_not_connected_reset_password.cle_de_reinitialisation_de_mot_de_passe, 'email':'mail', 'password':'new_password', 'confirmation_password':'new_password'  } )
		self.assertTrue( Utilisateurs.objects.get(adresse_mail=self.user_registred_not_connected_reset_password.adresse_mail).cle_de_reinitialisation_de_mot_de_passe != None )
		self.assertTrue( response.context['errors'] )
		self.assertTemplateUsed(response, 'reinitialisation_mot_de_passe.html')
		self.assertTrue( response.status_code == 200 )

	def test_reinitialisation_mot_de_passe_invalid_form_password(self):
		""""""
		#  Réinitialisation de mot passe avec un mot de passe de formuliare invailde 
		self.assertTrue( Utilisateurs.objects.get(adresse_mail=self.user_registred_not_connected_reset_password.adresse_mail).cle_de_reinitialisation_de_mot_de_passe != None )
		response = self.client_registred_not_connected_reset_password.post('/authentification/reinitialisation_password/', {  'reset_key':self.user_registred_not_connected_reset_password.cle_de_reinitialisation_de_mot_de_passe, 'email':self.user_registred_not_connected_reset_password.adresse_mail, 'password':'', 'confirmation_password':'new_password'  } )
		self.assertTrue( Utilisateurs.objects.get(adresse_mail=self.user_registred_not_connected_reset_password.adresse_mail).cle_de_reinitialisation_de_mot_de_passe != None )
		self.assertTrue( response.context['errors'] )
		self.assertTemplateUsed(response, 'reinitialisation_mot_de_passe.html')
		self.assertTrue( response.status_code == 200 )

	def test_reinitialisation_mot_de_passe_invalid_form_confirmation_password(self):
		""""""
		#  Réinitialisation de mot passe avec une confirmation de mail de formuliare invailde
		self.assertTrue( Utilisateurs.objects.get(adresse_mail=self.user_registred_not_connected_reset_password.adresse_mail).cle_de_reinitialisation_de_mot_de_passe != None )
		response = self.client_registred_not_connected_reset_password.post('/authentification/reinitialisation_password/', {  'reset_key':self.user_registred_not_connected_reset_password.cle_de_reinitialisation_de_mot_de_passe, 'email':self.user_registred_not_connected_reset_password.adresse_mail, 'password':'new_password', 'confirmation_password':''  } )
		self.assertTrue( Utilisateurs.objects.get(adresse_mail=self.user_registred_not_connected_reset_password.adresse_mail).cle_de_reinitialisation_de_mot_de_passe != None )
		self.assertTrue( response.context['errors'] )
		self.assertTemplateUsed(response, 'reinitialisation_mot_de_passe.html')
		self.assertTrue( response.status_code == 200 )

	def test_reinitialisation_mot_de_passe_no_matched_password(self):
		""""""
		#  Réinitialisation de mot passe avec des mots de passe qui ne correspondent pas
		self.assertTrue( Utilisateurs.objects.get(adresse_mail=self.user_registred_not_connected_reset_password.adresse_mail).cle_de_reinitialisation_de_mot_de_passe != None )
		response = self.client_registred_not_connected_reset_password.post('/authentification/reinitialisation_password/', {  'reset_key':self.user_registred_not_connected_reset_password.cle_de_reinitialisation_de_mot_de_passe, 'email':self.user_registred_not_connected_reset_password.adresse_mail, 'password':'one_password', 'confirmation_password':'another_password'  } )
		self.assertTrue( Utilisateurs.objects.get(adresse_mail=self.user_registred_not_connected_reset_password.adresse_mail).cle_de_reinitialisation_de_mot_de_passe != None )
		self.assertTrue( response.context['password_different_to_confirmation'] )
		self.assertTemplateUsed(response, 'reinitialisation_mot_de_passe.html')
		self.assertTrue( response.status_code == 200 )

	def test_reinitialisation_mot_de_passe_success(self):
		""""""
		#  Réinitialisation de mot passe reussie
		self.assertTrue( Utilisateurs.objects.get(adresse_mail=self.user_registred_not_connected_reset_password.adresse_mail).cle_de_reinitialisation_de_mot_de_passe != None )
		response = self.client_registred_not_connected_reset_password.post('/authentification/reinitialisation_password/', {  'reset_key':self.user_registred_not_connected_reset_password.cle_de_reinitialisation_de_mot_de_passe, 'email':self.user_registred_not_connected_reset_password.adresse_mail, 'password':'new_password', 'confirmation_password':'new_password'  } )
		self.assertTrue( Utilisateurs.objects.get(adresse_mail=self.user_registred_not_connected_reset_password.adresse_mail).cle_de_reinitialisation_de_mot_de_passe == None )
		self.assertTrue( response.context['state_reinitialisation'] )
		self.assertTemplateUsed(response, 'reinitialisation_mot_de_passe.html')
		self.assertTrue( response.status_code == 200 )


	#   ----- Connexion google

	@patch('authentification.views.requests.get')
	def test_google_connect_success(self, mock_get):
		""""""
		#  Connexion google reussie
		class MockRequest():
			"""docstring for MockRequess"""
			def __init__(self, mail):
				""""""
				self.status_code = 200
				self.mail = mail
			def json(self):
				""""""
				return {'email': self.mail }
		mock_get.return_value = MockRequest(self.user_registred_not_connected.adresse_mail)
		response = self.client_registred_not_connected.post('/authentification/google_connect/?token=1234')
		self.assertTrue( response.content == b'Connexion done' )
		self.assertTrue( response.status_code == 200 )

	@patch('authentification.views.requests.get')
	def test_google_connect_connected_user(self, mock_get):
		""""""
		#  Connexion google par un utilisateur connecte
		class MockRequest():
			"""docstring for MockRequess"""
			def __init__(self, mail):
				""""""
				self.status_code = 200
				self.mail = mail
			def json(self):
				""""""
				return {'email': self.mail }
		mock_get.return_value = MockRequest(self.user_registred_connected.adresse_mail)
		response = self.client_registred_connected.post('/authentification/google_connect/?token=1234')
		self.assertTrue( response.url == '../../user/home/' )
		self.assertTrue( response.status_code == 302 )

	@patch('authentification.views.requests.get')
	def test_google_connect_no_user_mail(self, mock_get):
		""""""
		#  Connexion google avec un mail qui correspond à aucun compte de l'application
		class MockRequest():
			"""docstring for MockRequess"""
			def __init__(self, mail):
				""""""
				self.status_code = 200
				self.mail = mail
			def json(self):
				""""""
				return {'email': self.mail }
		mock_get.return_value = MockRequest('mail_who_dont_exist_in_application@mail.mail')
		response = self.client_registred_not_connected.post('/authentification/google_connect/?token=1234')
		self.assertTrue( response.content == b"Aucun utilisateur n'existe avec ce compte google" )
		self.assertTrue( response.status_code == 200 )

	@patch('authentification.views.requests.get')
	def test_google_connect_call_google_api_fail(self, mock_get):
		""""""
		#  Connexion google avec un echec dans la réponse de l'api google
		class MockRequest():
			"""docstring for MockRequess"""
			def __init__(self, mail):
				""""""
				self.status_code = 400
				self.mail = mail
			def json(self):
				""""""
				return {'email': self.mail }
		mock_get.return_value = MockRequest('')
		response = self.client_registred_not_connected.post('/authentification/google_connect/?token=1234')
		self.assertTemplateUsed( response, "404.html" )
		self.assertTrue( response.status_code == 404 )



	#   ----- Envoie de lien d'activation de compte

	def test_envoie_activation_compte_unconnected_user(self):
		""""""
		#  Envoie de lien d'activation de compte par un utilisateur non connecté
		activation_key_before = Utilisateurs.objects.get(adresse_mail=self.user_registred_not_connected.adresse_mail).cle_dactivation_de_compte
		response = self.client_registred_not_connected.post('/authentification/envoie_activation_compte/')
		activation_key_after = Utilisateurs.objects.get(adresse_mail=self.user_registred_not_connected.adresse_mail).cle_dactivation_de_compte
		self.assertTrue( activation_key_before == activation_key_after )
		self.assertTemplateUsed( response, '404.html' )
		self.assertTrue( response.status_code == 404 )

	def test_envoie_activation_compte_success(self):
		""""""
		#  Envoie de lien d'activation de compte reussie
		activation_key_before = Utilisateurs.objects.get(adresse_mail=self.user_registred_connected.adresse_mail).cle_dactivation_de_compte
		response = self.client_registred_connected.post('/authentification/envoie_activation_compte/')
		activation_key_after = Utilisateurs.objects.get(adresse_mail=self.user_registred_connected.adresse_mail).cle_dactivation_de_compte
		self.assertTrue( activation_key_before != activation_key_after )
		self.assertTrue( response.url == '../../user/home/' )
		self.assertTrue( response.status_code == 302 )


	#   ----- Activation de compte

	def test_activation_compte_unconnected_user(self):
		""""""
		#  Activation de compte par un utilisateur non connecté
		activation_key_before = Utilisateurs.objects.get(adresse_mail=self.user_registred_not_connected.adresse_mail).cle_dactivation_de_compte
		response = self.client_registred_not_connected.post('/authentification/activation_compte/?mail=' + self.user_registred_not_connected.adresse_mail + '&key_activation=' + self.user_registred_not_connected.cle_dactivation_de_compte )
		activation_key_after = Utilisateurs.objects.get(adresse_mail=self.user_registred_not_connected.adresse_mail).cle_dactivation_de_compte
		self.assertTrue( activation_key_before == activation_key_after )
		self.assertTrue(response.url == '../../authentification/connexion/')
		self.assertTrue( response.status_code == 302 )

	def test_activation_compte_wrong_mail(self):
		""""""
		#  Activation de compte avec un mauvais mail
		activation_key_before = Utilisateurs.objects.get(adresse_mail=self.user_registred_connected.adresse_mail).cle_dactivation_de_compte
		response = self.client_registred_connected.post('/authentification/activation_compte/?mail=' + 'wrong_mail' + '&key_activation=' + self.user_registred_connected.cle_dactivation_de_compte )
		activation_key_after = Utilisateurs.objects.get(adresse_mail=self.user_registred_connected.adresse_mail).cle_dactivation_de_compte
		self.assertTrue( activation_key_before == activation_key_after )
		self.assertTemplateUsed( response, '404.html' )
		self.assertTrue( response.status_code == 404 )

	def test_activation_compte_wrong_key(self):
		""""""
		#  Activation de compte avec une mauvaise clé
		activation_key_before = Utilisateurs.objects.get(adresse_mail=self.user_registred_connected.adresse_mail).cle_dactivation_de_compte
		response = self.client_registred_connected.post('/authentification/activation_compte/?mail=' + self.user_registred_connected.adresse_mail + '&key_activation=' + 'wrong_key' )
		activation_key_after = Utilisateurs.objects.get(adresse_mail=self.user_registred_connected.adresse_mail).cle_dactivation_de_compte
		self.assertTrue( activation_key_before == activation_key_after )
		self.assertTemplateUsed( response, '404.html' )
		self.assertTrue( response.status_code == 404 )

	def test_activation_compte_success(self):
		""""""
		#  Activation de compte reussie
		activation_key_before = Utilisateurs.objects.get(adresse_mail=self.user_registred_connected.adresse_mail).cle_dactivation_de_compte
		response = self.client_registred_connected.post('/authentification/activation_compte/?mail=' + self.user_registred_connected.adresse_mail + '&key_activation=' + self.user_registred_connected.cle_dactivation_de_compte )
		activation_key_after = Utilisateurs.objects.get(adresse_mail=self.user_registred_connected.adresse_mail).cle_dactivation_de_compte
		self.assertTrue( activation_key_after == None )
		self.assertTrue( activation_key_before != activation_key_after )
		self.assertTrue(response.url == '../../user/home/')
		self.assertTrue( response.status_code == 302 )




