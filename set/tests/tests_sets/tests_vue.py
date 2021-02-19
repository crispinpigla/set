

from django.test import TestCase
from sets.models import *

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




	def test_sets(self):
		""""""

		#  Demande des publications d'un set pour un utilisateur non connecté
		#  Demande des publications d'un set pour un utilisateur connecté n'appartenant pas au set
		#  Demande des publications d'un set pour utilisateur connecté appartenant au set

		#  Demande des utilisateurs d'un set pour un utilisateur non connecté
		#  Demande des utilisateurs d'un set pour un utilsateur connecté n'appartenant pas au set
		#  Demande des utilisateurs d'un set pour un utilisateur connecté apprtenant au set
		
		#  Demande des évènements d'un set pour un utilisateur non connecté
		#  Demande des évènements d'un set pour un utilsateur connecté n'appartenant pas au set
		#  Demande des évènements d'un set pour un utilisateur connecté apprtenant au set

		#  Modification de la description d'un set par un utilisateur non-administrateur du set
		#  Modification de la description d'un set par un utilisateur administrateur du set




	def test_evenements(self):
		""""""

		#  Suppression d'un évènement de set par un utilisateur non-administrateur de l'évènement de set 
		#  Suppression d'un évènement de set par un utilisateur administrateur de l'évènement de set 
		#  Modification de la description d'un évènement de set par un utilisateur non-administrateur de l'évènement de set 
		#  Modification de la description d'un évènement de set par un utilisateur administrateur de l'évènement de set 
		#  Consultation sans publication d'un évènement de set pour les utilisateurs n'appartenents pas au set
		#  Consultation sans publication d'un évènement de set pour les utilisateurs non-connecté
		#  Consultation avec publication d'un évènement de set pour les utilisateurs appartenants au set



	def test_search(self):
		""""""

		#  Recherche de sets pour les utilisateurs non-connectés 
		#  Recherche de sets pour les utilisateurs connectés
		#  Recherche de personnes pour les utilisateurs non-connectés 
		#  Recherche de personnes pour les utilisateurs connectés
		#  Recherche d'évènement pour les utilisateurs non-connectés 
		#  Recherche d'évènement pour les utilisateurs connectés


	def test_update_cover(self):
		""""""

		#  Modification de la couverture d'un set par un utilisateur non-administrateur du set
		#  Modification de la couverture d'un set par un utilisateur administrateur du set


	def test_make_post_set(self):
		""""""

		#  Publication dans un set par un utilisateur n'appartenant pas au set
		#  Publication dans un set par un utilisateur appartenant au set


	def test_make_post_event(self):
		""""""

		#  Publication dans un évènement de set pour les utilisateurs n'appartenents pas au set
		#  Publication dans un évènement de set pour les utilisateurs appartenants au set


	def test_manage_like_post_set(self):
		""""""

		#  Likage d'une publication de set par un utilisateur n'appartenant pas au set
		#  Likage d'une publication de set par un utilisateur appartenant pas au set


	def test_manage_like_post_event(self):
		""""""

		#  Likage d'une publication d'un évènement par un utilisateur n'appartenant pas au set
		#  Likage d'une publication d'un évènement par un utilisateur appartenant pas au set


	def test_delete_add_user_set(self):
		""""""

		#  Suppression d'un set par un utilisateur non-administrateur du set
		#  Suppression d'un set par un utilisateur administrateur du set
		#  Ajout d'un utilisateur dans le set par un utilisateur non-administrateur du set
		#  Ajout d'un utilisateur dans le set par un utilisateur administrateur du set





	def test_creation_set(self)
		""""""

		# Création de set par un utilisateur non connecté
		# Création de set par un utilisateur connecté


	def test_creation_evenement(self)
		""""""

		# Création de set par un utilisateur non connecté
		# Création de set par un utilisateur connecté n'appartenant pas au set pour lequel il veut créer un évènement
		# Création de set par un utilisateur connecté sans set
		# Création de set par un utilisateur connecté appartenant au set pour lequel il veut créer un évènement



