from django.test import TestCase
from user.models import *

class AnimalTestCase(TestCase):
    def setUp(self):
        Animal.objects.create(name="lion", sound="roar")
        Animal.objects.create(name="cat", sound="meow")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Animal.objects.get(name="lion")
        cat = Animal.objects.get(name="cat")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')



	def test_home(self)
		""""""

		# Demande de l'acceuil personnonalisé pour un utilisateur connecté
		# Demande de l'acceuil personnonalisé pour un utilisateur non-connecté



	def test_contacts(self)
		""""""

		# Demande de contact pour un utilisateur connecté
		# Demande de contact pour un utilisateur non-connecté



	def test_message(self)
		""""""

		# Demande de message pour un utilisateur connecté
		# Demande de message pour un utilisateur non-connecté



	def test_messages_exchanges(self)
		""""""

		# Demande de messages échangés pour un utilisateur connecté
		# Demande de messages échangés pour un utilisateur non-connecté



	def test_updates_messages(self)
		""""""

		# Demande de mises à jour des messages d'une discussion pour utilisateur connecté et un last_id_message correspondant à un message d'une discussion de l'utilisateur
		# Demande de mises à jour des messages d'une discussion pour utilisateur connecté et un last_id_message ne correspondant pas à un message d'une discussion de l'utilisateur
		# Demande de mises à jour des messages d'une discussion pour utilisateur connecté sans last_id_message
		# Demande de mises à jour des messages d'une discussion pour utilisateur non connecté


	def test_send_message(self)
		""""""

		# Envoie de message pour un utilisateur non connecté 
		# Envoie de message pour un utilisateur connecté avec un destinataire renseigné
		# Envoie de message vide pour un utilisateur connecté avec un destinataire renseigné
		# Envoie de message pour un utilisateur connecté avec un destinataire non-renseigné



	def test_deconnexion(self)
		""""""

		# Déconnexion pour un utilisateur connecté
		# Déconnexion pour un utilisateur non connecté



	def test_manage_contact(self)
		""""""

		# Demande de gestion d'un contact pour utilisateur non connecté
		# Demande de gestion d'un contact pour utilisateur connecté et un contact non existant
		# Demande d'ajout d'un contact pour utilisateur connecté
		# Demande de suppression d'un contact pour utilisateur connecté



	def test_profil(self)
		""""""

		# Demande de coordonnées d'une page de profil d'un tiers par un utilisateur non connecté
		# Demande de sets d'une page de profil d'un tiers par un utilisateur non connecté
		# Demande de coordonnées d'une page de profil d'un tiers par un utilisateur connecté
		# Demande de sets d'une page de profil d'un tiers par un utilisateur connecté
		# Demande de coordonnées de sa page de profil d'un utilisateur connecté
		# Demande de sets de sa page de profil d'un utilisateur connecté



	def test_update_image_cover(self)
		""""""

		# Demande de mise mise à jour de l'image de profil par un utilisateur connecté avec un formulaire valide ( vide )
		# Demande de mise mise à jour de l'image de profil par un utilisateur connecté avec un formulaire invalide
		# Demande de mise mise à jour de l'image de profil par un utilisateur non connecté



	def test_update_profil_name(self)
		""""""

		# Demande de mise mise à jour du nom de profil par un utilisateur connecté avec un formulaire valide ( vide )
		# Demande de mise mise à jour du nom de profil par un utilisateur connecté avec un formulaire invalide
		# Demande de mise mise à jour du nom de profil par un utilisateur non connecté



	def test_update_profil_mail(self)
		""""""

		# Demande de mise mise à jour de l'email de profil par un utilisateur connecté avec un formulaire valide ( vide )
		# Demande de mise mise à jour de l'email de profil par un utilisateur connecté avec un formulaire invalide
		# Demande de mise mise à jour de l'email de profil par un utilisateur non connecté



	def test_suppression_compte(self)
		""""""

		# Demande de suppression d'un compte par un utilisateur connecté
		# Demande de suppression d'un compte par un utilisateur non connecté


