
import os

from django.core.files import File

from django.conf import settings

from django.test import TestCase, RequestFactory, Client
from sets.models import Sets, Evenements, SetUtilisateurs, PublicationSet, JaimePublicationSet, PublicationEvenement, JaimePublicationEvenement
from user.models import Utilisateurs, Contact, Message

class TestsVueSet(TestCase):
	"""docstring for TestsVueSet"""

	def setUp(self):
		""""""
		image = File(open(os.path.join(settings.BASE_DIR, "media/test.png"), 'rb'))

		self.client_not_registred = Client()
		self.client_registred_no_set = Client()
		self.client_registred_wait_set = Client()
		self.client_registred_member_set = Client()
		self.client_registred_administrator_set = Client()
		self.client_unactivate_user = Client()
		self.client_locked_user = Client()

		self.user_registred_no_set = Utilisateurs.objects.create(nom="user_registred_no_set_name", adresse_mail="user_registred_no_set@mail.mail", mot_de_passe='user_registred_no_set_password', statut_activation_compte=True)
		self.user_registred_wait_set = Utilisateurs.objects.create(nom="user_registred_wait_set_name", adresse_mail="user_registred_wait_set@mail.mail", mot_de_passe='user_registred_wait_set_password', statut_activation_compte=True)
		self.user_registred_member_set = Utilisateurs.objects.create(nom="user_registred_member_set_name", adresse_mail="user_registred_member_set@mail.mail", mot_de_passe='user_registred_member_set_password', statut_activation_compte=True)
		self.user_registred_administrator_set = Utilisateurs.objects.create(nom="user_registred_administrator_set_name", adresse_mail="user_registred_administrator_set@mail.mail", mot_de_passe='user_registred_administrator_set_password', statut_activation_compte=True)
		self.user_unactivate = Utilisateurs.objects.create(nom="user_unactivate", adresse_mail="user_unactivate@mail.mail", mot_de_passe='user_unactivate_password')
		self.user_locked = Utilisateurs.objects.create(nom="user_locked", adresse_mail="user_locked@mail.mail", mot_de_passe='user_locked_password', statut_blocage_admin=True)

		self.set = Sets.objects.create(nom="set", type0="Entreprise", description="description de set", image_couverture=image,)
		self.set_locked = Sets.objects.create(nom="set_locked", type0="Entreprise", description="description de set fermé", image_couverture=image, statut_fermeture_admin=True)
		
		self.image_cover_set = self.set.image_couverture
		self.image_cover_set_locked = self.set_locked.image_couverture

		self.set_user_administrator = SetUtilisateurs.objects.create(set0=self.set, utilisateur=self.user_registred_administrator_set, statut="administrateur",)
		self.set_user_wait = SetUtilisateurs.objects.create(set0=self.set, utilisateur=self.user_registred_wait_set, statut="attente_validation",)
		self.set_user_member = SetUtilisateurs.objects.create(set0=self.set, utilisateur=self.user_registred_member_set, statut="dans_set",)
		self.set_user_unactivate = SetUtilisateurs.objects.create(set0=self.set, utilisateur=self.user_unactivate, statut="administrateur",)
		self.set_user_locked = SetUtilisateurs.objects.create(set0=self.set, utilisateur=self.user_locked, statut="administrateur",)

		self.set_locked_user_administrator = SetUtilisateurs.objects.create(set0=self.set_locked, utilisateur=self.user_registred_administrator_set, statut="administrateur",)
		self.set_locked_user_wait = SetUtilisateurs.objects.create(set0=self.set_locked, utilisateur=self.user_registred_wait_set, statut="attente_validation",)
		self.set_locked_user_member = SetUtilisateurs.objects.create(set0=self.set_locked, utilisateur=self.user_registred_member_set, statut="dans_set",)

		self.event_administrator =  Evenements.objects.create(set0=self.set, administrateur=self.user_registred_administrator_set, nom="event_user_registred_administrator_set",description="description event_user_registred_administrator_set")
		self.event_member =  Evenements.objects.create(set0=self.set, administrateur=self.user_registred_member_set, nom="event_user_registred_member_set",description="description event_user_registred_member_set")

		self.event_locked_member =  Evenements.objects.create(set0=self.set, administrateur=self.user_registred_member_set, nom="event_locked_user_registred_administrator_set",description="description event_locked_user_registred_administrator_set", statut_fermeture_admin=True)
		self.event_set_locked_member =  Evenements.objects.create(set0=self.set_locked, administrateur=self.user_registred_member_set, nom="event_set_locked_user_registred_administrator_set",description="description event_set_locked_user_registred_administrator_set")

		self.client_registred_no_set.post('/authentification/connexion/', {'email':'user_registred_no_set@mail.mail', 'password':'user_registred_no_set_password'})
		self.client_registred_wait_set.post('/authentification/connexion/', {'email':'user_registred_wait_set@mail.mail', 'password':'user_registred_wait_set_password'})
		self.client_registred_member_set.post('/authentification/connexion/', {'email':'user_registred_member_set@mail.mail', 'password':'user_registred_member_set_password'})
		self.client_registred_administrator_set.post('/authentification/connexion/', {'email':'user_registred_administrator_set@mail.mail', 'password':'user_registred_administrator_set_password'})
		self.client_unactivate_user.post('/authentification/connexion/', {'email':'user_unactivate@mail.mail', 'password':'user_unactivate_password'})
		self.client_locked_user.post('/authentification/connexion/', {'email':'user_locked@mail.mail', 'password':'user_locked_password'})

		self.publication_set_admin_set = PublicationSet.objects.create(set0= self.set, auteur=self.user_registred_administrator_set , contenu_text='Une publication dans un set de ladmin du set' )
		self.jaime_publication_set_admin = JaimePublicationSet.objects.create(publication_set=self.publication_set_admin_set, jaimeur=self.user_registred_administrator_set)
		self.jaime_publication_set_user_unactivate = JaimePublicationSet.objects.create(publication_set=self.publication_set_admin_set, jaimeur=self.user_unactivate)
		self.jaime_publication_set_user_locked = JaimePublicationSet.objects.create(publication_set=self.publication_set_admin_set, jaimeur=self.user_locked)
	
		self.publication_set_locked_admin_set = PublicationSet.objects.create(set0= self.set_locked, auteur=self.user_registred_administrator_set , contenu_text='Une publication dans un set fermé de ladmin du set' )
		self.jaime_publication_set_locked_admin = JaimePublicationSet.objects.create(publication_set=self.publication_set_locked_admin_set, jaimeur=self.user_registred_administrator_set)

		self.publication_set_user = PublicationSet.objects.create(set0= self.set, auteur=self.user_registred_member_set , contenu_text='Une publication dans un set du user du set' )
		self.jaime_publication_set_user = JaimePublicationSet.objects.create(publication_set=self.publication_set_user, jaimeur=self.user_registred_member_set)

		self.publication_set_locked_user = PublicationSet.objects.create(set0= self.set_locked, auteur=self.user_registred_member_set , contenu_text='Une publication dans un set fermé du user du set' )
		self.jaime_publication_set_locked_user = JaimePublicationSet.objects.create(publication_set=self.publication_set_locked_user, jaimeur=self.user_registred_member_set)

		self.publication_event_admin_event = PublicationEvenement.objects.create(evenement= self.event_member, auteur=self.user_registred_member_set , contenu_text='Une publication dans un evenement de pas ladmin de levent' )
		self.jaime_publication_event_admin_event = JaimePublicationEvenement.objects.create(publication_evenement=self.publication_event_admin_event, jaimeur=self.user_registred_member_set)
		self.jaime_publication_event_user_unactivate = JaimePublicationEvenement.objects.create(publication_evenement=self.publication_event_admin_event, jaimeur=self.user_unactivate)
		self.jaime_publication_event_user_locked = JaimePublicationEvenement.objects.create(publication_evenement=self.publication_event_admin_event, jaimeur=self.user_locked)

		self.publication_event_no_admin_event = PublicationEvenement.objects.create(evenement= self.event_member, auteur=self.user_registred_administrator_set , contenu_text='Une publication dans un evenement de ladmin de levent' )
		self.jaime_publication_event_user_event = JaimePublicationEvenement.objects.create(publication_evenement=self.publication_event_no_admin_event, jaimeur=self.user_registred_administrator_set)

		self.publication_event_locked_admin_event = PublicationEvenement.objects.create(evenement= self.event_locked_member, auteur=self.user_registred_member_set , contenu_text='Une publication dans un evenement fermé de pas ladmin de levent' )
		self.jaime_publication_event_locked_admin_event = JaimePublicationEvenement.objects.create(publication_evenement=self.publication_event_locked_admin_event, jaimeur=self.user_registred_member_set)

		self.publication_event_locked_no_admin_event = PublicationEvenement.objects.create(evenement= self.event_locked_member, auteur=self.user_registred_member_set , contenu_text='Une publication dans un evenement fermé de ladmin de levent' )
		self.jaime_publication_event_locked_user_event = JaimePublicationEvenement.objects.create(publication_evenement=self.publication_event_locked_no_admin_event, jaimeur=self.user_registred_administrator_set)

		self.publication_event_set_locked_user_member = PublicationEvenement.objects.create(evenement= self.event_set_locked_member, auteur=self.user_registred_administrator_set , contenu_text='Une publication dans un evenement fermé de ladmin de levent' )
		self.jaime_publication_event_set_locked_user_member = JaimePublicationEvenement.objects.create(publication_evenement=self.publication_event_set_locked_user_member, jaimeur=self.user_registred_administrator_set)
		self.jaime_publication_event_set_locked_user_unactivate = JaimePublicationEvenement.objects.create(publication_evenement=self.publication_event_set_locked_user_member, jaimeur=self.user_unactivate)
		self.jaime_publication_event_set_locked_user_locked = JaimePublicationEvenement.objects.create(publication_evenement=self.publication_event_set_locked_user_member, jaimeur=self.user_locked)




	# ----- Consultation des publications d'un set

	def test_sets_consultation_publication_set_utilisateur_non_inscrit(self):
		""""""
		#  Demande des publications d'un set pour un utilisateur non inscrit
		response = self.client_not_registred.get('/sets/set/' + str(self.set.id) + '/?section=publications')
		self.assertTemplateUsed(response, 'section_no_access_publications_set.html')
		self.assertTemplateNotUsed(response, 'section_publications_set.html')
		self.assertEqual(response.status_code, 200)

	def test_sets_consultation_publication_set_utilisateur_inscrit_no_set(self):
		""""""
		#  Demande des publications d'un set pour un utilisateur inscrit n'appartenant pas au set
		response = self.client_registred_no_set.get('/sets/set/' + str(self.set.id) + '/?section=publications')
		self.assertTemplateUsed(response, 'section_no_access_publications_set.html')
		self.assertTemplateNotUsed(response, 'section_publications_set.html')
		self.assertEqual(response.status_code, 200)

	def test_sets_consultation_publication_set_utilisateur_inscrit_admin_set(self):
		""""""
    	#  Demande des publications d'un set pour utilisateur inscrit appartenant au set et etant administrateur du set
		response = self.client_registred_administrator_set.get('/sets/set/' + str(self.set.id) + '/?section=publications')
		self.assertTemplateUsed(response, 'section_publications_set.html')
		self.assertEqual(response.status_code, 200)

	def test_sets_consultation_publication_set_utilisateur_inscrit_admin_set_no_int_id(self):
		""""""
    	#  Demande des publications d'un set avec un identifiant set qui n'est pas un nombre entier
		response = self.client_registred_administrator_set.get('/sets/set/' + 'aaaaaa' + '/?section=publications')
		self.assertTemplateUsed(response, '404.html')
		self.assertEqual(response.status_code, 404)

	def test_sets_consultation_publication_set_utilisateur_inscrit_admin_set_not_set_in_application(self):
		""""""
    	#  Demande des publications d'un set dont l'identifiant ne correspond à aucun set de l'application
		response = self.client_registred_administrator_set.get('/sets/set/' + '1000' + '/?section=publications')
		self.assertTemplateUsed(response, '404.html')
		self.assertEqual(response.status_code, 404)
    	

	def test_sets_consultation_publication_set_utilisateur_inscrit_user_set(self):
		""""""
		#  Demande des publications d'un set pour utilisateur inscrit appartenant au set et etant simple membre du set
		response = self.client_registred_member_set.get('/sets/set/' + str(self.set.id) + '/?section=publications')
		self.assertTemplateUsed(response, 'section_publications_set.html')
		self.assertEqual(response.status_code, 200)

	def test_sets_consultation_publication_set_utilisateur_inscrit_wait_set(self):
		""""""
		#  Demande des publications d'un set pour utilisateur inscrit appartenant au set et etant en attente de validation d'entrée dans le set
		response = self.client_registred_wait_set.get('/sets/set/' + str(self.set.id) + '/?section=publications')
		self.assertTemplateUsed(response, 'section_publications_users_wait_set.html')
		self.assertEqual(response.status_code, 200)

	def test_sets_consultation_publication_set_user_unactivate(self):
		""""""
		#   Demande des publication d'un set par un compte non activé
		response = self.client_unactivate_user.get('/sets/set/' + str(self.set.id) + '/?section=publications')
		self.assertEqual(response.url, '../../../user/home/')
		self.assertEqual(response.status_code, 302)

	def test_sets_consultation_publication_set_user_locked(self):
		""""""
		#   Demande des publications d'un set par un compte bloqué
		response = self.client_locked_user.get('/sets/set/' + str(self.set.id) + '/?section=publications')
		self.assertEqual(response.url, '../../../user/home/')
		self.assertEqual(response.status_code, 302)

	def test_sets_consultation_publication_set_locked(self):
		""""""
		#   Demande des publications d'un set Fermé
		response = self.client_registred_administrator_set.get('/sets/set/' + str(self.set_locked.id) + '/?section=publications')
		self.assertTemplateUsed(response, 'set_ferme.html')
		self.assertEqual(response.status_code, 200)


	#  ----- Consultation des utilisateur d'un set

	def test_sets_consultation_utilisateurs_set_utilisateur_non_inscrit(self):
		""""""
		#  Demande des utilisateurs d'un set pour un utilisateur non inscrit
		response = self.client_not_registred.get('/sets/set/' + str(self.set.id) + '/?section=personnes')
		self.assertTemplateUsed(response, 'section_personnes_set.html')
		self.assertEqual(response.status_code, 200)

	def test_sets_consultation_utilisateurs_set_utilisateur_inscrit_no_set(self):
		""""""
		#  Demande des utilisateurs d'un set pour un utilsateur inscrit n'appartenant pas au set
		response = self.client_registred_no_set.get('/sets/set/' + str(self.set.id) + '/?section=personnes')
		self.assertTemplateUsed(response, 'section_personnes_set.html')
		self.assertEqual(response.status_code, 200)

	def test_sets_consultation_utilisateurs_set_utilisateur_inscrit_admin_set(self):
		""""""
    	#  Demande des utilisateurs d'un set pour un utilisateur inscrit  appartenant au set et etant administrateur du set
		response = self.client_registred_administrator_set.get('/sets/set/' + str(self.set.id) + '/?section=personnes')
		self.assertTemplateUsed(response, 'section_personnes_set.html')
		self.assertEqual(response.status_code, 200)

	def test_sets_consultation_utilisateur_set_utilisateur_inscrit_admin_set_no_int_id(self):
		""""""
    	#  Demande des utilisateurs d'un set avec un identifiant set qui n'est pas un nombre entier
		response = self.client_registred_administrator_set.get('/sets/set/' + 'aaaaaa' + '/?section=personnes')
		self.assertTemplateUsed(response, '404.html')
		self.assertEqual(response.status_code, 404)

	def test_sets_consultation_utilisateur_set_utilisateur_inscrit_admin_set_not_set_in_application(self):
		""""""
    	#  Demande des utilisateurs d'un set dont l'identifiant ne correspond à aucun set de l'application
		response = self.client_registred_administrator_set.get('/sets/set/' + '1000' + '/?section=personnes')
		self.assertTemplateUsed(response, '404.html')
		self.assertEqual(response.status_code, 404)

	def test_sets_consultation_utilisateurs_set_utilisateur_inscrit_user_set(self):
		""""""
    	#  Demande des utilisateurs d'un set pour un utilisateur non inscrit  appartenant au set et etant simple membre du set
		response = self.client_registred_member_set.get('/sets/set/' + str(self.set.id) + '/?section=personnes')
		self.assertTemplateUsed(response, 'section_personnes_set.html')
		self.assertEqual(response.status_code, 200)

	def test_sets_consultation_utilisateurs_set_utilisateur_inscrit_wait_set(self):
		""""""
    	#  Demande des utilisateurs d'un set pour un utilsateur inscrit  appartenant au set et etant en attente de validation d'entrée dans le set
		response = self.client_registred_wait_set.get('/sets/set/' + str(self.set.id) + '/?section=personnes')
		self.assertTemplateUsed(response, 'section_personnes_set.html')
		self.assertEqual(response.status_code, 200)

	def test_sets_consultation_utilisateur_set_user_unactivate(self):
		""""""
		#   Demande des utilisateurs d'un set par un compte non activé
		response = self.client_unactivate_user.get('/sets/set/' + str(self.set.id) + '/?section=personnes')
		self.assertEqual(response.url, '../../../user/home/')
		self.assertEqual(response.status_code, 302)

	def test_sets_consultation_utilisateur_set_user_locked(self):
		""""""
		#   Demande des utilisateurs d'un set par un compte bloqué
		response = self.client_locked_user.get('/sets/set/' + str(self.set.id) + '/?section=personnes')
		self.assertEqual(response.url, '../../../user/home/')
		self.assertEqual(response.status_code, 302)

	def test_sets_consultation_utilisateur_set_locked(self):
		""""""
		#   Demande des utilisateurs d'un set Fermé
		response = self.client_registred_administrator_set.get('/sets/set/' + str(self.set_locked.id) + '/?section=personnes')
		self.assertTemplateUsed(response, 'set_ferme.html')
		self.assertEqual(response.status_code, 200)



	#  ----- Consultation des évènements d'un set

	def test_sets_consultation_evenements_set_utilisateur_non_inscrit(self):
		""""""
		#  Demande des évènements d'un set pour un utilisateur non inscrit
		response = self.client_not_registred.get('/sets/set/' + str(self.set.id) + '/?section=evenements')
		self.assertTemplateUsed(response, 'section_evenements_set_out_set.html')
		self.assertEqual(response.status_code, 200)

	def test_sets_consultation_evenements_set_utilisateur_inscrit_no_set(self):
		""""""
		#  Demande des évènements d'un set pour un utilsateur inscrit n'appartenant pas au set
		response = self.client_registred_no_set.get('/sets/set/' + str(self.set.id) + '/?section=evenements')
		self.assertTemplateUsed(response, 'section_evenements_set_out_set.html')
		self.assertEqual(response.status_code, 200)

	def test_sets_consultation_evenements_set_utilisateur_inscrit_admin_set(self):
		""""""
    	#  Demande des évènements d'un set pour un utilisateur inscrit  appartenant au set et etant administrateur du set
		response = self.client_registred_administrator_set.get('/sets/set/' + str(self.set.id) + '/?section=evenements')
		self.assertTemplateUsed(response, 'section_evenements_set.html')
		self.assertEqual(response.status_code, 200)

	def test_sets_consultation_evenements_set_utilisateur_inscrit_admin_set_no_int_id(self):
		""""""
    	#  Demande des evenements d'un set avec un identifiant set qui n'est pas un nombre entier
		response = self.client_registred_administrator_set.get('/sets/set/' + 'aaaaaa' + '/?section=personnes')
		self.assertTemplateUsed(response, '404.html')
		self.assertEqual(response.status_code, 404)

	def test_sets_consultation_evenements_set_utilisateur_inscrit_admin_set_not_set_in_application(self):
		""""""
    	#  Demande des evenements d'un set dont l'identifiant ne correspond à aucun set de l'application
		response = self.client_registred_administrator_set.get('/sets/set/' + '1000' + '/?section=personnes')
		self.assertTemplateUsed(response, '404.html')
		self.assertEqual(response.status_code, 404)

	def test_sets_consultation_evenements_set_utilisateur_inscrit_user_set(self):
		""""""
    	#  Demande des évènements d'un set pour un utilisateur non inscrit  appartenant au set et etant simple membre du set
		response = self.client_registred_member_set.get('/sets/set/' + str(self.set.id) + '/?section=evenements')
		self.assertTemplateUsed(response, 'section_evenements_set.html')
		self.assertEqual(response.status_code, 200)

	def test_sets_consultation_evenements_set_utilisateur_inscrit_wait_set(self):
		""""""
    	#  Demande des évènements d'un set pour un utilsateur inscrit  appartenant au set et etant en attente de validation d'entrée dans le set
		response = self.client_registred_wait_set.get('/sets/set/' + str(self.set.id) + '/?section=evenements')
		self.assertTemplateUsed(response, 'section_evenements_set_out_set.html')
		self.assertEqual(response.status_code, 200)

	def test_sets_consultation_evenement_set_user_unactivate(self):
		""""""
		#   Demande des évènements d'un set par un compte non activé
		response = self.client_unactivate_user.get('/sets/set/' + str(self.set.id) + '/?section=evenements')
		self.assertEqual(response.url, '../../../user/home/')
		self.assertEqual(response.status_code, 302)

	def test_sets_consultation_evenement_set_user_locked(self):
		""""""
		#   Demande des évènements d'un set par un compte bloqué
		response = self.client_locked_user.get('/sets/set/' + str(self.set.id) + '/?section=evenements')
		self.assertEqual(response.url, '../../../user/home/')
		self.assertEqual(response.status_code, 302)

	def test_sets_consultation_evenement_set_locked(self):
		""""""
		#   Demande des évènements d'un set Fermé
		response = self.client_registred_administrator_set.get('/sets/set/' + str(self.set_locked.id) + '/?section=evenements')
		self.assertTemplateUsed(response, 'set_ferme.html')
		self.assertEqual(response.status_code, 200)




	#  ----- Modification de la couverture d'un set

	def test_sets_modification_couverture_set_utilisateur_non_inscrit(self):
		""""""
		#  Demande de modification de la couverture d'un set par un utilisateur non inscrit
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		self.assertTrue(Sets.objects.get(id=self.set.id).image_couverture == self.image_cover_set)
		response = self.client_not_registred.post('/sets/update_cover/?set_id=' + str(self.set.id), {'file': image} )
		self.assertTrue(Sets.objects.get(id=self.set.id).image_couverture == self.image_cover_set)
		self.assertEqual(response.url, '../../authentification/connexion/')

	def test_sets_modification_couverture_set_utilisateur_inscrit_no_set(self):
		""""""
		#  Demande de modification de la couverture d'un set par un utilsateur inscrit n'appartenant pas au set
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		self.assertTrue(Sets.objects.get(id=self.set.id).image_couverture == self.image_cover_set)
		response = self.client_registred_no_set.post('/sets/update_cover/?set_id=' + str(self.set.id), {'file': image} )
		self.assertTrue(Sets.objects.get(id=self.set.id).image_couverture == self.image_cover_set)
		self.assertEqual(response.url, '../../user/home/')

	def test_sets_modification_couverture_set_utilisateur_inscrit_admin_set(self):
		""""""
    	#  Demande de modification de la couverture d'un set par un utilisateur inscrit  appartenant au set et etant administrateur du set
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		self.assertTrue(Sets.objects.get(id=self.set.id).image_couverture == self.image_cover_set)
		response = self.client_registred_administrator_set.post('/sets/update_cover/?set_id=' + str(self.set.id), {'file': image} )
		self.assertTrue(Sets.objects.get(id=self.set.id).image_couverture != self.image_cover_set)
		self.assertEqual(response.url, '../../sets/set/'+ str(self.set.id) +'/')
		self.assertEqual(response.status_code, 302)

	def test_sets_modification_couverture_set_utilisateur_inscrit_admin_set_no_id_int(self):
		""""""
    	#  Demande de modification de la couverture d'un set avec un identifiant set qui n'est pas un nombre entier
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		self.assertTrue(Sets.objects.get(id=self.set.id).image_couverture == self.image_cover_set)
		response = self.client_registred_administrator_set.post('/sets/update_cover/?set_id=' + 'a', {'file': image} )
		self.assertTrue(Sets.objects.get(id=self.set.id).image_couverture == self.image_cover_set)
		self.assertTemplateUsed(response, '404.html')
		self.assertEqual(response.status_code, 404)

	def test_sets_modification_couverture_set_utilisateur_inscrit_admin_set_no_set_in_application(self):
		""""""
    	#  Demande de modification de la couverture d'un set dont l'identifiant ne correspond à aucun set de l'application
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		self.assertTrue(Sets.objects.get(id=self.set.id).image_couverture == self.image_cover_set)
		response = self.client_registred_administrator_set.post('/sets/update_cover/?set_id=' + '1000', {'file': image} )
		self.assertTrue(Sets.objects.get(id=self.set.id).image_couverture == self.image_cover_set)
		self.assertTemplateUsed(response, '404.html')
		self.assertEqual(response.status_code, 404)

	def test_sets_modification_couverture_set_utilisateur_inscrit_admin_set_invalid_form(self):
		""""""
    	#  Demande de modification de la couverture d'un set avec un formulaire invalide
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		self.assertTrue(Sets.objects.get(id=self.set.id).image_couverture == self.image_cover_set)
		response = self.client_registred_administrator_set.post('/sets/update_cover/?set_id=' + str(self.set.id), {'file': ''} )
		self.assertTrue(Sets.objects.get(id=self.set.id).image_couverture == self.image_cover_set)
		self.assertTemplateUsed(response, '404.html')
		self.assertEqual(response.status_code, 404)

	def test_sets_modification_couverture_set_utilisateur_inscrit_user_set(self):
		""""""
    	#  Demande de modification de la couverture d'un set par un utilisateur non inscrit  appartenant au set et etant simple membre du set
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		self.assertTrue(Sets.objects.get(id=self.set.id).image_couverture == self.image_cover_set)
		response = self.client_registred_member_set.post('/sets/update_cover/?set_id=' + str(self.set.id), {'file': image} )
		self.assertTrue(Sets.objects.get(id=self.set.id).image_couverture == self.image_cover_set)
		self.assertEqual(response.url, '../../sets/set/' + str(self.set.id) + '/')

	def test_sets_modification_couverture_set_utilisateur_inscrit_wait_set(self):
		""""""
    	#  Demande de modification de la couverture d'un set par un utilsateur inscrit  appartenant au set et etant en attente de validation d'entrée dans le set
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		self.assertTrue(Sets.objects.get(id=self.set.id).image_couverture == self.image_cover_set)
		response = self.client_registred_wait_set.post('/sets/update_cover/?set_id=' + str(self.set.id), {'file': image} )
		self.assertTrue(Sets.objects.get(id=self.set.id).image_couverture == self.image_cover_set)
		self.assertEqual(response.url, '../../sets/set/' + str(self.set.id) + '/')

	def test_sets_modification_couverture_set_user_unactive(self):
		""""""
    	#   Demande de modification de la couverture d'un set par un compte non activé
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		self.assertTrue(Sets.objects.get(id=self.set.id).image_couverture == self.image_cover_set)
		response = self.client_unactivate_user.post('/sets/update_cover/?set_id=' + str(self.set.id), {'file': image} )
		self.assertTrue(Sets.objects.get(id=self.set.id).image_couverture == self.image_cover_set)
		self.assertEqual(response.url, '../../../user/home/')
		self.assertEqual(response.status_code, 302)

	def test_sets_modification_couverture_set_user_locked(self):
		""""""
    	#   Demande de modification de la couverture d'un set par un compte bloqué
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		self.assertTrue(Sets.objects.get(id=self.set.id).image_couverture == self.image_cover_set)
		response = self.client_locked_user.post('/sets/update_cover/?set_id=' + str(self.set.id), {'file': image} )
		self.assertTrue(Sets.objects.get(id=self.set.id).image_couverture == self.image_cover_set)
		self.assertEqual(response.url, '../../../user/home/')
		self.assertEqual(response.status_code, 302)

	def test_sets_modification_couverture_set_locked(self):
		""""""
    	#   Demande de modification de la couverture d'un set fermé
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		self.assertTrue(Sets.objects.get(id=self.set_locked.id).image_couverture == self.image_cover_set_locked)
		response = self.client_registred_administrator_set.post('/sets/update_cover/?set_id=' + str(self.set_locked.id), {'file': image} )
		self.assertTrue(Sets.objects.get(id=self.set_locked.id).image_couverture == self.image_cover_set_locked)
		self.assertEqual(response.url, '../../../user/home/')
		self.assertEqual(response.status_code, 302)



	#  -----  Modification de description d'un set

	def test_sets_modification_description_set_utilisateur_non_inscrit(self):
		""""""
		#  Demande de modification de la description d'un set par un utilisateur non inscrit
		self.assertTrue(Sets.objects.get(id=self.set.id).description == 'description de set')
		response = self.client_not_registred.post('/sets/update_description_set/?set_id=' + str(self.set.id), {'description': "nouvelle description du set"} )
		self.assertTrue(Sets.objects.get(id=self.set.id).description == 'description de set')
		self.assertEqual(response.url, '../../authentification/connexion/')

	def test_sets_modification_description_set_utilisateur_inscrit_no_set(self):
		""""""
		#  Demande de modification de la description d'un set par un utilsateur inscrit n'appartenant pas au set
		self.assertTrue(Sets.objects.get(id=self.set.id).description == 'description de set')
		response = self.client_registred_no_set.post('/sets/update_description_set/?set_id=' + str(self.set.id), {'description': "nouvelle description du set"} )
		self.assertTrue(Sets.objects.get(id=self.set.id).description == 'description de set')
		self.assertEqual(response.url, '../../user/home/')

	def test_sets_modification_description_set_utilisateur_inscrit_admin_set(self):
		""""""
    	#  Demande de modification de la description d'un set par un utilisateur inscrit  appartenant au set et etant administrateur du set
		self.assertTrue(Sets.objects.get(id=self.set.id).description == 'description de set')
		response = self.client_registred_administrator_set.post('/sets/update_description_set/?set_id=' + str(self.set.id), {'description': "nouvelle description du set"} )
		self.assertTrue(Sets.objects.get(id=self.set.id).description == 'nouvelle description du set')
		self.assertEqual(response.url, '../../sets/set/'+ str(self.set.id) +'/')
		self.assertEqual(response.status_code, 302)

	def test_sets_modification_description_set_utilisateur_inscrit_admin_set_no_id_int(self):
		""""""
    	#  Demande de modification de la description d'un set avec un identifiant set qui n'est pas un nombre entier
		self.assertTrue(Sets.objects.get(id=self.set.id).image_couverture == self.image_cover_set)
		response = self.client_registred_administrator_set.post('/sets/update_description_set/?set_id=' + 'a', {'description': "nouvelle description du set"} )
		self.assertTrue(Sets.objects.get(id=self.set.id).image_couverture == self.image_cover_set)
		self.assertTemplateUsed(response, '404.html')
		self.assertEqual(response.status_code, 404)

	def test_sets_modification_description_set_utilisateur_inscrit_admin_set_no_set_in_application(self):
		""""""
    	#  Demande de modification de la description d'un set dont l'identifiant ne correspond à aucun set de l'application
		self.assertTrue(Sets.objects.get(id=self.set.id).image_couverture == self.image_cover_set)
		response = self.client_registred_administrator_set.post('/sets/update_description_set/?set_id=' + '1000', {'description': "nouvelle description du set"} )
		self.assertTrue(Sets.objects.get(id=self.set.id).image_couverture == self.image_cover_set)
		self.assertTemplateUsed(response, '404.html')
		self.assertEqual(response.status_code, 404)

	def test_sets_modification_description_set_utilisateur_inscrit_admin_set_invalid_form(self):
		""""""
    	#  Demande de modification de la description d'un set avec un formulaire invalide
		self.assertTrue(Sets.objects.get(id=self.set.id).image_couverture == self.image_cover_set)
		response = self.client_registred_administrator_set.post('/sets/update_description_set/?set_id=' + str(self.set.id), {'description': ''} )
		self.assertTrue(Sets.objects.get(id=self.set.id).image_couverture == self.image_cover_set)
		self.assertTemplateUsed(response, '404.html')
		self.assertEqual(response.status_code, 404)

	def test_sets_modification_description_set_utilisateur_inscrit_user_set(self):
		""""""
    	#  Demande de modification de la description d'un set par un utilisateur non inscrit  appartenant au set et etant simple membre du set
		self.assertTrue(Sets.objects.get(id=self.set.id).description == 'description de set')
		response = self.client_registred_member_set.post('/sets/update_description_set/?set_id=' + str(self.set.id), {'description': "nouvelle description du set"} )
		self.assertTrue(Sets.objects.get(id=self.set.id).description == 'description de set')
		self.assertEqual(response.url, '../../sets/set/' + str(self.set.id) + '/')

	def test_sets_modification_description_set_utilisateur_inscrit_wait_set(self):
		""""""
    	#  Demande de modification de la description d'un set par un utilsateur inscrit  appartenant au set et etant en attente de validation d'entrée dans le set
		self.assertTrue(Sets.objects.get(id=self.set.id).description == 'description de set')
		response = self.client_registred_wait_set.post('/sets/update_description_set/?set_id=' + str(self.set.id), {'description': "nouvelle description du set"} )
		self.assertTrue(Sets.objects.get(id=self.set.id).description == 'description de set')
		self.assertEqual(response.url, '../../sets/set/' + str(self.set.id) + '/')

	def test_sets_modification_description_set_user_unactivate(self):
		""""""
    	#   Demande de modification de la description d'un set par un compte non activé
		description_before = Sets.objects.get(id=self.set.id).description
		response = self.client_unactivate_user.post('/sets/update_description_set/?set_id=' + str(self.set.id), {'description': "nouvelle description du set"} )
		description_after = Sets.objects.get(id=self.set.id).description
		self.assertTrue( description_after == description_before )
		self.assertEqual(response.url, '../../user/home/')
		self.assertEqual(response.status_code, 302)

	def test_sets_modification_description_set_user_locked(self):
		""""""
    	#   Demande de modification de la description d'un set par un compte bloqué
		description_before = Sets.objects.get(id=self.set.id).description
		response = self.client_locked_user.post('/sets/update_description_set/?set_id=' + str(self.set.id), {'description': "nouvelle description du set"} )
		description_after = Sets.objects.get(id=self.set.id).description
		self.assertTrue( description_after == description_before )
		self.assertEqual(response.url, '../../user/home/')
		self.assertEqual(response.status_code, 302)

	def test_sets_modification_description_set_locked(self):
		""""""
    	#   Demande de modification de la description d'un set fermé
		description_before = Sets.objects.get(id=self.set_locked.id).description
		response = self.client_registred_administrator_set.post('/sets/update_description_set/?set_id=' + str(self.set_locked.id), {'description': "nouvelle description du set"} )
		description_after = Sets.objects.get(id=self.set_locked.id).description
		self.assertTrue( description_after == description_before )
		self.assertEqual(response.url, '../../sets/set/' + str(self.set_locked.id) + '/')
		self.assertEqual(response.status_code, 302)


	#  -----  Page de création de set

	def test_sets_page_creation_set_utilisateur_non_inscrit(self):
		""""""
		#  Demande de la page de creation d'un set par un utilisateur non inscrit
		response = self.client_not_registred.get('/sets/creation_set/')
		self.assertEqual(response.url, '../../authentification/connexion/')

	def test_sets_page_creation_set_utilisateur_inscrit_no_set(self):
		""""""
		#  Demande de la page de creation d'un set par un utilsateur inscrit n'appartenant pas au set
		response = self.client_registred_no_set.get('/sets/creation_set/')
		self.assertTemplateUsed(response, 'creation_set.html')
		self.assertEqual(response.status_code, 200)

	def test_sets_page_creation_set_utilisateur_inscrit_admin_set(self):
		""""""
    	#  Demande de la page de creation d'un set par un utilisateur inscrit  appartenant au set et etant administrateur du set
		response = self.client_registred_administrator_set.get('/sets/creation_set/')
		self.assertTemplateUsed(response, 'creation_set.html')
		self.assertEqual(response.status_code, 200)

	def test_sets_page_creation_set_utilisateur_inscrit_user_set(self):
		""""""
    	#  Demande de la page de creation d'un set par un utilisateur non inscrit  appartenant au set et etant simple membre du set
		response = self.client_registred_member_set.get('/sets/creation_set/')
		self.assertTemplateUsed(response, 'creation_set.html')
		self.assertEqual(response.status_code, 200)

	def test_sets_page_creation_set_utilisateur_inscrit_wait_set(self):
		""""""
    	#  Demande de la page de creation d'un set par un utilsateur inscrit  appartenant au set et etant en attente de validation d'entrée dans le set
		response = self.client_registred_wait_set.get('/sets/creation_set/')
		self.assertTemplateUsed(response, 'creation_set.html')
		self.assertEqual(response.status_code, 200)

	def test_sets_page_creation_set_user_unactivate(self):
		""""""
		#   Demande de la page de creation d'un set par un compte non activé
		response = self.client_unactivate_user.get('/sets/creation_set/')
		self.assertEqual(response.url, '../../user/home/')
		self.assertEqual(response.status_code, 302)

	def test_sets_page_creation_set_user_locked(self):
		""""""
		#   Demande de la page de creation d'un set par un compte bloqué
		response = self.client_locked_user.get('/sets/creation_set/')
		self.assertEqual(response.url, '../../user/home/')
		self.assertEqual(response.status_code, 302)


	#  ----- Creation d'un set

	def test_sets_creation_set_utilisateur_non_inscrit(self):
		""""""
		#  Demande de creation d'un set par un utilisateur non inscrit
		sets_before = len(Sets.objects.all())
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_not_registred.post('/sets/creation_set/', {'name': "set_0", "file":image, "type_set":"Entreprise", "description":"description set_0"} )
		sets_after = len(Sets.objects.all())
		self.assertEqual(sets_before, sets_after)
		self.assertEqual(response.url, '../../authentification/connexion/')

	def test_sets_creation_set_utilisateur_inscrit_no_set(self):
		""""""
		#  Demande de creation d'un set par un utilsateur inscrit n'appartenant pas au set
		sets_before = len(Sets.objects.all())
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_no_set.post('/sets/creation_set/', {'name': "set_0", "file":image, "type_set":"Entreprise", "description":"description set_0"} )
		sets_after = len(Sets.objects.all())
		self.assertEqual(sets_before + 1 , sets_after)
		self.assertTrue( '../../sets/set/' in response.url )

	def test_sets_creation_set_utilisateur_inscrit_admin_set(self):
		""""""
    	#  Demande de creation d'un set par un utilisateur inscrit  appartenant au set et etant administrateur du set
		sets_before = len(Sets.objects.all())
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/creation_set/', {'name': "set_0", "file":image, "type_set":"Entreprise", "description":"description set_0"} )
		sets_after = len(Sets.objects.all())
		self.assertEqual(sets_before + 1 , sets_after)
		self.assertTrue( '../../sets/set/' in response.url )

	def test_sets_creation_set_utilisateur_inscrit_admin_set_invalid_name_form(self):
		""""""
    	#  Demande de création d'un set avec un nom dans le formulaire invalide
		sets_before = len(Sets.objects.all())
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/creation_set/', {'name': "", "file":image, "type_set":"Entreprise", "description":"description set_0"} )
		sets_after = len(Sets.objects.all())
		self.assertEqual(sets_before , sets_after)
		self.assertTemplateUsed(response, 'creation_set.html')

	def test_sets_creation_set_utilisateur_inscrit_admin_set_invalid_cover_form(self):
		""""""
    	#  Demande de création d'un set avec une couverture dans le formulaire invalide
		sets_before = len(Sets.objects.all())
		response = self.client_registred_administrator_set.post('/sets/creation_set/', {'name': "set_0", "file":'', "type_set":"Entreprise", "description":"description set_0"} )
		sets_after = len(Sets.objects.all())
		self.assertEqual(sets_before , sets_after)
		self.assertTemplateUsed(response, 'creation_set.html')

	def test_sets_creation_set_utilisateur_inscrit_admin_set_invalid_type_form(self):
		""""""
    	#  Demande de création d'un set avec un type dans le formulaire invalide
		sets_before = len(Sets.objects.all())
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/creation_set/', {'name': "set_0", "file":image, "type_set":"NoEntreprise", "description":"description set_0"} )
		sets_after = len(Sets.objects.all())
		self.assertEqual(sets_before , sets_after)
		self.assertTemplateUsed(response, 'creation_set.html')

	def test_sets_creation_set_utilisateur_inscrit_admin_set_invalid_description_form(self):
		""""""
    	#  Demande de création d'un set avec une description formulaire invalide
		sets_before = len(Sets.objects.all())
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/creation_set/', {'name': "set_0", "file":image, "type_set":"Entreprise", "description":""} )
		sets_after = len(Sets.objects.all())
		self.assertEqual(sets_before , sets_after)
		self.assertTemplateUsed(response, 'creation_set.html')

	def test_sets_creation_set_utilisateur_inscrit_user_set(self):
		""""""
    	#  Demande de creation d'un set par un utilisateur non inscrit  appartenant au set et etant simple membre du set
		sets_before = len(Sets.objects.all())
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_member_set.post('/sets/creation_set/', {'name': "set_0", "file":image, "type_set":"Entreprise", "description":"description set_0"} )
		sets_after = len(Sets.objects.all())
		self.assertEqual(sets_before + 1 , sets_after)
		self.assertTrue( '../../sets/set/' in response.url )

	def test_sets_creation_set_utilisateur_inscrit_wait_set(self):
		""""""
    	#  Demande de creation d'un set par un utilsateur inscrit  appartenant au set et etant en attente de validation d'entrée dans le set
		sets_before = len(Sets.objects.all())
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_wait_set.post('/sets/creation_set/', {'name': "set_0", "file":image, "type_set":"Entreprise", "description":"description set_0"} )
		sets_after = len(Sets.objects.all())
		self.assertEqual(sets_before + 1 , sets_after)
		self.assertTrue( '../../sets/set/' in response.url )

	def test_sets_creation_set_user_unactivate(self):
		""""""
    	#   Demande de creation d'un set par un compte non activé
		sets_before = len(Sets.objects.all())
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_unactivate_user.post('/sets/creation_set/', {'name': "set_0", "file":image, "type_set":"Entreprise", "description":"description set_0"} )
		sets_after = len(Sets.objects.all())
		self.assertEqual(sets_before , sets_after)
		self.assertEqual(response.url, '../../user/home/')
		self.assertEqual(response.status_code, 302)

	def test_sets_creation_set_user_locked(self):
		""""""
    	#   Demande de creation d'un set par un compte bloqué
		sets_before = len(Sets.objects.all())
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_locked_user.post('/sets/creation_set/', {'name': "set_0", "file":image, "type_set":"Entreprise", "description":"description set_0"} )
		sets_after = len(Sets.objects.all())
		self.assertEqual(sets_before , sets_after)
		self.assertEqual(response.url, '../../user/home/')
		self.assertEqual(response.status_code, 302)


	#  -----  Page de création d'un évènement

	def test_sets_page_creation_evenement_utilisateur_non_inscrit(self):
		""""""
		#  Demande de la page de creation d'un évènement par un utilisateur non inscrit
		response = self.client_not_registred.get('/sets/creation_evenement/')
		self.assertEqual(response.url, 'authentification/connexion/')
		self.assertTemplateNotUsed(response, 'creation_evenement.html')

	def test_sets_page_creation_evenement_utilisateur_inscrit_no_set(self):
		""""""
		#  Demande de la page de creation d'un évènement par un utilsateur inscrit n'appartenant pas au set
		response = self.client_registred_no_set.get('/sets/creation_evenement/' + str(self.set.id) + '/')
		self.assertTrue('../../sets/set/' + str(self.set.id) + '/' == response.url)
		self.assertTemplateNotUsed(response, 'creation_evenement.html')

	def test_sets_page_creation_evenement_utilisateur_inscrit_admin_set(self):
		""""""
    	#  Demande de la page de creation d'un évènement par un utilisateur inscrit  appartenant au set et etant administrateur du set
		response = self.client_registred_administrator_set.get('/sets/creation_evenement/' + str(self.set.id) + '/' )
		self.assertTemplateUsed(response, 'creation_evenement.html')
		self.assertTrue( response.status_code == 200 )

	def test_sets_page_creation_evenement_utilisateur_inscrit_admin_set_id_not_int(self):
		""""""
    	#  Demande de la page création d'un évènement avec un identifiant set qui n'est pas un nombre entier
		response = self.client_registred_administrator_set.get('/sets/creation_evenement/' + 'a' + '/' )
		self.assertTemplateNotUsed(response, 'creation_evenement.html')
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_page_creation_evenement_utilisateur_inscrit_admin_set_not_sets_in_application(self):
		""""""
    	#  Demande de la page création d'un évènement dont l'identifiant ne correspond à aucun set de l'application
		response = self.client_registred_administrator_set.get('/sets/creation_evenement/' + '1000' + '/' )
		self.assertTemplateNotUsed(response, 'creation_evenement.html')
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_page_creation_evenement_utilisateur_inscrit_user_set(self):
		""""""
    	#  Demande de la page de creation d'un évènement par un utilisateur non inscrit  appartenant au set et etant simple membre du set
		response = self.client_registred_member_set.get('/sets/creation_evenement/' + str(self.set.id) + '/' )
		self.assertTemplateUsed(response, 'creation_evenement.html')
		self.assertTrue( response.status_code == 200 )

	def test_sets_page_creation_evenement_utilisateur_inscrit_wait_set(self):
		""""""
    	#  Demande de la page de creation d'un évènement par un utilsateur inscrit  appartenant au set et etant en attente de validation d'entrée dans le set
		response = self.client_registred_wait_set.get('/sets/creation_evenement/' + str(self.set.id) + '/' )
		self.assertTrue('../../sets/set/' + str(self.set.id) + '/' == response.url)
		self.assertTemplateNotUsed(response, 'creation_evenement.html')

	def test_sets_page_creation_evenement_user_unactivate(self):
		""""""
    	#   Demande de la page de creation d'un évènement par un compte non activé
		response = self.client_unactivate_user.get('/sets/creation_evenement/' + str(self.set.id) + '/' )
		self.assertEqual(response.url, '../../../user/home/')
		self.assertEqual(response.status_code, 302)

	def test_sets_page_creation_evenement_user_locked(self):
		""""""
    	#   Demande de la page de creation d'un évènement par un compte bloqué
		response = self.client_locked_user.get('/sets/creation_evenement/' + str(self.set.id) + '/' )
		self.assertEqual(response.url, '../../../user/home/')
		self.assertEqual(response.status_code, 302)

	def test_sets_page_creation_evenement_set_locked(self):
		""""""
    	#   Demande de la page de creation d'un évènement d'un set fermé
		response = self.client_registred_administrator_set.get('/sets/creation_evenement/' + str(self.set_locked.id) + '/' )
		self.assertTemplateUsed(response, 'set_ferme.html')
		self.assertTrue( response.status_code == 200 )





	#  ----- Création d'un évènement


	def test_sets_creation_evenement_utilisateur_non_inscrit(self):
		""""""
		#  Demande de creation d'un évènement par un utilisateur non inscrit
		events_before = len(Evenements.objects.all())
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_not_registred.post('/sets/creation_evenement/'  + str(self.set.id) + '/' , {'name': "set_0", "description":"description event_0"} )
		events_after = len(Evenements.objects.all())
		self.assertTrue( events_after == events_before )
		self.assertEqual(response.url, '../../authentification/connexion/')

	def test_sets_creation_evenement_utilisateur_inscrit_no_set(self):
		""""""
		#  Demande de creation d'un évènement par un utilsateur inscrit n'appartenant pas au set
		events_before = len(Evenements.objects.all())
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_no_set.post('/sets/creation_evenement/'  + str(self.set.id) + '/' , {'name': "set_0", "description":"description event_0"} )
		events_after = len(Evenements.objects.all())
		self.assertTrue( events_after == events_before )
		self.assertTrue( '../../sets/set/'+ str(self.set.id) + '/' == response.url )

	def test_sets_creation_evenement_utilisateur_inscrit_admin_set(self):
		""""""
    	#  Demande de creation d'un évènement par un utilisateur inscrit  appartenant au set et etant administrateur du set
		events_before = len(Evenements.objects.all())
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/creation_evenement/'  + str(self.set.id) + '/' , {'name': "set_0", "description":"description event_0"} )
		events_after = len(Evenements.objects.all())
		self.assertTrue( events_after == events_before + 1 )
		self.assertTrue('../../sets/event/' in response.url )
		self.assertTrue( response.status_code == 302 )

	def test_sets_creation_evenement_utilisateur_inscrit_admin_set_id_not_int(self):
		""""""
    	#  Demande de création d'un évènement avec un identifiant set qui n'est pas un nombre entier
		events_before = len(Evenements.objects.all())
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/creation_evenement/'  + 'a' + '/' , {'name': "set_0", "description":"description event_0"} )
		events_after = len(Evenements.objects.all())
		self.assertTrue( events_after == events_before )
		self.assertTemplateNotUsed(response, 'creation_evenement.html')
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_creation_evenement_utilisateur_inscrit_admin_set_not_sets_in_application(self):
		""""""
    	#  Demande de création d'un évènement dont l'identifiant ne correspond à aucun set de l'application
		events_before = len(Evenements.objects.all())
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/creation_evenement/'  + '1000' + '/' , {'name': "set_0", "description":"description event_0"} )
		events_after = len(Evenements.objects.all())
		self.assertTrue( events_after == events_before )
		self.assertTemplateNotUsed(response, 'creation_evenement.html')
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_creation_evenement_utilisateur_inscrit_admin_set_invalid_name_form(self):
		""""""
    	#  Demande de création de la description d'un set avec un nom dans le formulaire invalide
		events_before = len(Evenements.objects.all())
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/creation_evenement/'  + str(self.set.id) + '/' , {'name': "", "description":"description event_0"} )
		events_after = len(Evenements.objects.all())
		self.assertTrue( events_after == events_before )
		self.assertTemplateUsed(response, 'creation_evenement.html')

	def test_sets_creation_evenement_utilisateur_inscrit_admin_set_invalid_description_form(self):
		""""""
    	#  Demande de création de la description d'un set avec une description formulaire invalide
		events_before = len(Evenements.objects.all())
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/creation_evenement/'  + str(self.set.id) + '/' , {'name': "set_0", "description":""} )
		events_after = len(Evenements.objects.all())
		self.assertTrue( events_after == events_before )
		self.assertTemplateUsed(response, 'creation_evenement.html')

	def test_sets_creation_evenement_utilisateur_inscrit_user_set(self):
		""""""
    	#  Demande de creation d'un évènement par un utilisateur non inscrit  appartenant au set et etant simple membre du set
		events_before = len(Evenements.objects.all())
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_member_set.post('/sets/creation_evenement/'  + str(self.set.id) + '/' , {'name': "set_0", "description":"description event_0"} )
		events_after = len(Evenements.objects.all())
		self.assertTrue( events_after == events_before + 1 )
		self.assertTrue('../../sets/event/' in response.url )
		self.assertTrue( response.status_code == 302 )

	def test_sets_creation_evenement_utilisateur_inscrit_wait_set(self):
		""""""
    	#  Demande de creation d'un évènement par un utilsateur inscrit  appartenant au set et etant en attente de validation d'entrée dans le set
		events_before = len(Evenements.objects.all())
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_wait_set.post('/sets/creation_evenement/'  + str(self.set.id) + '/' , {'name': "set_0", "description":"description event_0"} )
		events_after = len(Evenements.objects.all())
		self.assertTrue( events_after == events_before )
		self.assertTrue('../../sets/set/'+ str(self.set.id) + '/' == response.url )

	def test_sets_creation_evenement_user_unactivate(self):
		""""""
    	#   Demande de creation d'un évènement par un compte non activé
		events_before = len(Evenements.objects.all())
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_unactivate_user.post('/sets/creation_evenement/'  + str(self.set.id) + '/' , {'name': "set_0", "description":"description event_0"} )
		events_after = len(Evenements.objects.all())
		self.assertTrue( events_after == events_before )
		self.assertEqual(response.url, '../../../user/home/')
		self.assertEqual(response.status_code, 302)

	def test_sets_creation_evenement_user_locked(self):
		""""""
    	#   Demande de creation d'un évènement par un compte bloqué
		events_before = len(Evenements.objects.all())
		image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_locked_user.post('/sets/creation_evenement/'  + str(self.set.id) + '/' , {'name': "set_0", "description":"description event_0"} )
		events_after = len(Evenements.objects.all())
		self.assertTrue( events_after == events_before )
		self.assertEqual(response.url, '../../../user/home/')
		self.assertEqual(response.status_code, 302)

	def test_sets_creation_evenement_set_locked(self):
		""""""
    	#   Demande de creation d'un évènement d'un set Fermé
		response = self.client_registred_administrator_set.get('/sets/creation_evenement/' + str(self.set_locked.id) + '/', {'name': "set_0", "description":"description event_0"} )
		self.assertTemplateUsed(response, 'set_ferme.html')
		self.assertTrue( response.status_code == 200 )




	#  ----- Rechercher de set

	def test_sets_recherche_set_utilisateur_non_inscrit(self):
		""""""
		#  Demande de recherche d'un set pour un utilisateur non inscrit
		response = self.client_registred_no_set.post('/sets/search/?search_input=set&section=sets')
		self.assertTemplateUsed(response, 'search.html')
		self.assertTrue( response.status_code == 200 )

	def test_sets_recherche_set_utilisateur_inscrit_no_set(self):
		""""""
		#  Demande de recherche d'un set pour un utilisateur inscrit n'appartenant pas au set
		response = self.client_registred_no_set.post('/sets/search/?search_input=set&section=sets')
		self.assertTemplateUsed(response, 'search.html')
		self.assertTrue( response.status_code == 200 )

	def test_sets_recherche_set_utilisateur_inscrit_admin_set(self):
		""""""
    	#  Demande  de recherche d'un set pour utilisateur inscrit appartenant au set et etant administrateur du set
		response = self.client_registred_no_set.post('/sets/search/?search_input=set&section=sets')
		self.assertTemplateUsed(response, 'search.html')
		self.assertTrue( response.status_code == 200 )

	def test_sets_recherche_set_utilisateur_inscrit_user_set(self):
		""""""
		#  Demande  de recherche d'un set pour utilisateur inscrit appartenant au set et etant simple membre du set
		response = self.client_registred_no_set.post('/sets/search/?search_input=set&section=sets')
		self.assertTemplateUsed(response, 'search.html')
		self.assertTrue( response.status_code == 200 )

	def test_sets_recherche_set_utilisateur_inscrit_wait_set(self):
		""""""
		#  Demande  de recherche d'un set pour utilisateur inscrit appartenant au set et etant en attente de validation d'entrée dans le set
		response = self.client_registred_no_set.post('/sets/search/?search_input=set&section=sets')
		self.assertTemplateUsed(response, 'search.html')
		self.assertTrue( response.status_code == 200 )

	def test_sets_recherche_set_user_unactivate(self):
		""""""
		#   Demande de recherche d'un set par un compte non activé
		response = self.client_unactivate_user.post('/sets/search/?search_input=set&section=sets')
		self.assertEqual(response.url, '../../../user/home/')
		self.assertEqual(response.status_code, 302)

	def test_sets_recherche_set_user_locked(self):
		""""""
		#   Demande de recherche d'un set par un compte bloqué
		response = self.client_locked_user.post('/sets/search/?search_input=set&section=sets')
		self.assertEqual(response.url, '../../../user/home/')
		self.assertEqual(response.status_code, 302)


	#  ----- Recherche d'évènements

	def test_sets_recherche_evenements_utilisateur_non_inscrit(self):
		""""""
		#  Demande de recherche d'un évènement pour un utilisateur non inscrit
		response = self.client_not_registred.post('/sets/search/?search_input=set&section=evenements')
		self.assertTemplateUsed(response, 'search.html')
		self.assertTrue( response.status_code == 200 )

	def test_sets_recherche_evenements_utilisateur_inscrit_no_set(self):
		""""""
		#  Demande de recherche d'un évènement pour un utilsateur inscrit n'appartenant pas au set
		response = self.client_registred_no_set.post('/sets/search/?search_input=set&section=evenements')
		self.assertTemplateUsed(response, 'search.html')
		self.assertTrue( response.status_code == 200 )

	def test_sets_recherche_evenements_utilisateur_inscrit_admin_set(self):
		""""""
    	#  Demande de recherche d'un évènement pour un utilisateur inscrit  appartenant au set et etant administrateur du set
		response = self.client_registred_administrator_set.post('/sets/search/?search_input=set&section=evenements')
		self.assertTemplateUsed(response, 'search.html')
		self.assertTrue( response.status_code == 200 )

	def test_sets_recherche_evenements_utilisateur_inscrit_user_set(self):
		""""""
    	#  Demande de recherche d'un évènement pour un utilisateur non inscrit  appartenant au set et etant simple membre du set
		response = self.client_registred_member_set.post('/sets/search/?search_input=set&section=evenements')
		self.assertTemplateUsed(response, 'search.html')
		self.assertTrue( response.status_code == 200 )

	def test_sets_recherche_evenements_utilisateur_inscrit_wait_set(self):
		""""""
    	#  Demande de recherche d'un évènement pour un utilsateur inscrit  appartenant au set et etant en attente de validation d'entrée dans le set
		response = self.client_registred_wait_set.post('/sets/search/?search_input=set&section=evenements')
		self.assertTemplateUsed(response, 'search.html')
		self.assertTrue( response.status_code == 200 )

	def test_sets_recherche_evenement_user_unactivate(self):
		""""""
		#   Demande de recherche d'un évènement par un compte non activé
		response = self.client_unactivate_user.post('/sets/search/?search_input=set&section=evenements')
		self.assertEqual(response.url, '../../../user/home/')
		self.assertEqual(response.status_code, 302)

	def test_sets_recherche_evenement_user_locked(self):
		""""""
		#   Demande de recherche d'un évènement par un compte bloqué
		response = self.client_locked_user.post('/sets/search/?search_input=set&section=evenements')
		self.assertEqual(response.url, '../../../user/home/')
		self.assertEqual(response.status_code, 302)



	#  ----- Recherche d'évènements

	def test_sets_recherche_personnes_utilisateur_non_inscrit(self):
		""""""
		#  Demande de recherche d'un évènement pour un utilisateur non inscrit
		response = self.client_not_registred.post('/sets/search/?search_input=set&section=personnes')
		self.assertTemplateUsed(response, 'search.html')
		self.assertTrue( response.status_code == 200 )

	def test_sets_recherche_personnes_utilisateur_inscrit_no_set(self):
		""""""
		#  Demande de recherche d'un évènement pour un utilsateur inscrit n'appartenant pas au set
		response = self.client_registred_no_set.post('/sets/search/?search_input=set&section=personnes')
		self.assertTemplateUsed(response, 'search.html')
		self.assertTrue( response.status_code == 200 )

	def test_sets_recherche_personnes_utilisateur_inscrit_admin_set(self):
		""""""
    	#  Demande de recherche d'un évènement pour un utilisateur inscrit  appartenant au set et etant administrateur du set
		response = self.client_registred_administrator_set.post('/sets/search/?search_input=set&section=personnes')
		self.assertTemplateUsed(response, 'search.html')
		self.assertTrue( response.status_code == 200 )

	def test_sets_recherche_personnes_utilisateur_inscrit_user_set(self):
		""""""
    	#  Demande de recherche d'un évènement pour un utilisateur non inscrit  appartenant au set et etant simple membre du set
		response = self.client_registred_member_set.post('/sets/search/?search_input=set&section=personnes')
		self.assertTemplateUsed(response, 'search.html')
		self.assertTrue( response.status_code == 200 )

	def test_sets_recherche_personnes_utilisateur_inscrit_wait_set(self):
		""""""
    	#  Demande de recherche d'un évènement pour un utilsateur inscrit  appartenant au set et etant en attente de validation d'entrée dans le set
		response = self.client_registred_wait_set.post('/sets/search/?search_input=set&section=personnes')
		self.assertTemplateUsed(response, 'search.html')
		self.assertTrue( response.status_code == 200 )

	def test_sets_recherche_personnes_user_unactivate(self):
		""""""
		#   Demande de recherche d'un évènement par un compte non activé
		response = self.client_unactivate_user.post('/sets/search/?search_input=set&section=personnes')
		self.assertEqual(response.url, '../../../user/home/')
		self.assertEqual(response.status_code, 302)

	def test_sets_recherche_personnes_user_locked(self):
		""""""
		#   Demande de recherche d'un évènement par un compte bloqué
		response = self.client_locked_user.post('/sets/search/?search_input=set&section=personnes')
		self.assertEqual(response.url, '../../../user/home/')
		self.assertEqual(response.status_code, 302)



	#  ----- Consultation des publications d'un évènement


	def test_sets_consultation_publication_evenement_utilisateur_non_inscrit(self):
		""""""
		#  Demande de consultaion des publications d'un évènement pour un utilisateur non inscrit
		response = self.client_not_registred.get('/sets/event/' + str(self.event_member.id)  + '/' )
		self.assertTemplateUsed(response, 'evenement_no_access_event.html')
		self.assertTrue( response.status_code == 200 )

	def test_sets_consultation_publication_evenement_utilisateur_inscrit_no_set(self):
		""""""
		#  Demande de consultaion des publications d'un évènement pour un utilisateur inscrit n'appartenant pas au set
		response = self.client_registred_no_set.get('/sets/event/' + str(self.event_member.id)  + '/' )
		self.assertTemplateUsed(response, 'evenement_no_access_event.html')
		self.assertTrue( response.status_code == 200 )

	def test_sets_consultation_publication_evenement_utilisateur_inscrit_admin_set_not_admin_event(self):
		""""""
    	#  Demande de consultaion des publications d'un évènement pour utilisateur inscrit appartenant au set et etant administrateur du set
		response = self.client_registred_administrator_set.get('/sets/event/' + str(self.event_member.id) + '/' )
		self.assertTemplateUsed(response, 'evenement_no_administrator_event.html')
		self.assertTrue( response.status_code == 200 )

	def test_sets_consultation_publication_evenement_utilisateur_inscrit_user_set_admin_event(self):
		""""""
		#  Demande de consultaion des publications d'un évènement pour utilisateur inscrit appartenant au set et etant simple membre du set
		response = self.client_registred_member_set.get('/sets/event/' + str(self.event_member.id)  + '/' )
		self.assertTemplateUsed(response, 'evenement_administrator_event.html')
		self.assertTrue( response.status_code == 200 )

	def test_sets_consultation_publication_evenement_utilisateur_inscrit_user_set_admin_event_no_id_int(self):
		""""""
		#  Demande de consultaion des publications d'un évènement avec un identifiant évènement qui n'est pas un nombre entier
		response = self.client_registred_member_set.get('/sets/event/' + 'a'  + '/' )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_consultation_publication_evenement_utilisateur_inscrit_user_set_admin_event_not_event_in_application(self):
		""""""
		#  Demande de consultaion des publications d'un évènement dont l'identifiant ne correspond à aucun évènement de l'application
		response = self.client_registred_member_set.get('/sets/event/' + '1000'  + '/' )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_consultation_publication_evenement_utilisateur_inscrit_wait_set(self):
		""""""
		#  Demande de consultaion des publications d'un évènement pour utilisateur inscrit appartenant au set et etant en attente de validation d'entrée dans le set
		response = self.client_registred_wait_set.get('/sets/event/' + str(self.event_member.id)  + '/' )
		self.assertTemplateUsed(response, 'evenement_await_enter_set.html')
		self.assertTrue( response.status_code == 200 )

	def test_sets_consultation_publication_evenement_user_unactivate(self):
		""""""
		#   Demande consultation des publications d'un évènement par un compte non activé
		response = self.client_unactivate_user.get('/sets/event/' + str(self.event_member.id)  + '/' )
		self.assertEqual(response.url, '../../../user/home/')
		self.assertEqual(response.status_code, 302)
	
	def test_sets_consultation_publication_evenement_user_locked(self):
		""""""
		#   Demande consultation des publications d'un évènement par un compte bloqué
		response = self.client_locked_user.get('/sets/event/' + str(self.event_member.id)  + '/' )
		self.assertEqual(response.url, '../../../user/home/')
		self.assertEqual(response.status_code, 302)

	def test_sets_consultation_publication_evenement_set_locked(self):
		""""""
		#   Demande consultation des publications d'un évènement d'un set fermé
		response = self.client_registred_member_set.get('/sets/event/' + str(self.event_set_locked_member.id)  + '/' )
		self.assertTemplateUsed(response, 'evenement_ferme.html')
		self.assertTrue( response.status_code == 200 )
	
	def test_sets_consultation_publication_evenement_locked(self):
		""""""
		#   Demande consultation des publications d'un évènement fermé
		response = self.client_registred_member_set.get('/sets/event/' + str(self.event_locked_member.id)  + '/' )
		self.assertTemplateUsed(response, 'evenement_ferme.html')
		self.assertTrue( response.status_code == 200 )



	#  -----  Make post set

	def test_sets_publier_dans_set_utilisateur_non_inscrit(self):
		""""""
		#  Demande création de publication dans un set par un utilisateur non inscrit
		posts_before =  len(PublicationSet.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_not_registred.post('/sets/make_post_set/'  + str(self.set.id) + '/' , {'publication_text': "text de la publication", "file_1":image1, "file_2":image2 } )
		posts_after =  len(PublicationSet.objects.all())
		self.assertTrue( posts_before == posts_after)
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_publier_dans_set_utilisateur_inscrit_no_set(self):
		""""""
		#  Demande création de publication dans un set par un utilsateur inscrit n'appartenant pas au set
		posts_before =  len(PublicationSet.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_no_set.post('/sets/make_post_set/'  + str(self.set.id) + '/' , {'publication_text': "text de la publication", "file_1":image1, "file_2":image2 } )
		posts_after =  len(PublicationSet.objects.all())
		self.assertTrue( posts_before == posts_after)
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_publier_dans_set_utilisateur_inscrit_admin_set(self):
		""""""
    	#  Demande création de publication dans un set par un utilisateur inscrit  appartenant au set et etant administrateur du set
		posts_before =  len(PublicationSet.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/make_post_set/'  + str(self.set.id) + '/' , {'publication_text': "text de la publication", "file_1":image1, "file_2":image2 } )
		posts_after =  len(PublicationSet.objects.all())
		self.assertTrue( posts_after == posts_before + 1)
		self.assertTrue( response.url == '../../set/' + str(self.set.id) + '/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_publier_dans_set_utilisateur_inscrit_admin_set_not_id_int(self):
		""""""
    	#  Demande création de publication dans un set avec un identifiant set qui n'est pas un nombre entier
		posts_before =  len(PublicationSet.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/make_post_set/'  + 'a' + '/' , {'publication_text': "text de la publication", "file_1":image1, "file_2":image2 } )
		posts_after =  len(PublicationSet.objects.all())
		self.assertTrue( posts_before == posts_after)
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_publier_dans_set_utilisateur_inscrit_admin_set_not_set_in_application(self):
		""""""
    	#  Demande création de publication dans un set dont l'identifiant ne correspond à aucun set de l'application
		posts_before =  len(PublicationSet.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/make_post_set/'  + '1000' + '/' , {'publication_text': "text de la publication", "file_1":image1, "file_2":image2 } )
		posts_after =  len(PublicationSet.objects.all())
		self.assertTrue( posts_before == posts_after)
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_publier_dans_set_utilisateur_inscrit_admin_set_form_empty_000(self):
		""""""
    	#  Demande création de publication dans un set avec un formulaire vide
		posts_before =  len(PublicationSet.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/make_post_set/'  + str(self.set.id) + '/' , {'publication_text': "", "file_1":"", "file_2":"" } )
		posts_after =  len(PublicationSet.objects.all())
		self.assertTrue( posts_before == posts_after)
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_publier_dans_set_utilisateur_inscrit_admin_set_form_empty_011(self):
		""""""
    	#  Demande création de publication dans un set avec un text de formulaire vide
		posts_before =  len(PublicationSet.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/make_post_set/'  + str(self.set.id) + '/' , {'publication_text': "", "file_1":image1, "file_2":image2 } )
		posts_after =  len(PublicationSet.objects.all())
		self.assertTrue( posts_after == posts_before + 1)
		self.assertTrue( response.url == '../../set/' + str(self.set.id) + '/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_publier_dans_set_utilisateur_inscrit_admin_set_form_empty_101(self):
		""""""
    	#  Demande création de publication dans un set avec le premier fichier du formulaire vide
		posts_before =  len(PublicationSet.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/make_post_set/'  + str(self.set.id) + '/' , {'publication_text': "text de la publication", "file_1":"", "file_2":image2 } )
		posts_after =  len(PublicationSet.objects.all())
		self.assertTrue( posts_after == posts_before + 1)
		self.assertTrue( response.url == '../../set/' + str(self.set.id) + '/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_publier_dans_set_utilisateur_inscrit_admin_set_form_empty_110(self):
		""""""
    	#  Demande création de publication dans un set avec le deuxième fichier de formulaire vide
		posts_before =  len(PublicationSet.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/make_post_set/'  + str(self.set.id) + '/' , {'publication_text': "text de la publication", "file_1":image1, "file_2":"" } )
		posts_after =  len(PublicationSet.objects.all())
		self.assertTrue( posts_after == posts_before + 1)
		self.assertTrue( response.url == '../../set/' + str(self.set.id) + '/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_publier_dans_set_utilisateur_inscrit_admin_set_form_empty_100(self):
		""""""
    	#  Demande création de publication dans un set avec les deux fichier du formulaire vide
		posts_before =  len(PublicationSet.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/make_post_set/'  + str(self.set.id) + '/' , {'publication_text': "text de la publication", "file_1":"", "file_2":"" } )
		posts_after =  len(PublicationSet.objects.all())
		self.assertTrue( posts_after == posts_before + 1)
		self.assertTrue( response.url == '../../set/' + str(self.set.id) + '/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_publier_dans_set_utilisateur_inscrit_admin_set_form_empty_010(self):
		""""""
    	#  Demande création de publication dans un set avec le text et le deuxème fichier du formulaire vide
		posts_before =  len(PublicationSet.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/make_post_set/'  + str(self.set.id) + '/' , {'publication_text': "", "file_1":image1, "file_2":"" } )
		posts_after =  len(PublicationSet.objects.all())
		self.assertTrue( posts_after == posts_before + 1)
		self.assertTrue( response.url == '../../set/' + str(self.set.id) + '/' )

	def test_sets_publier_dans_set_utilisateur_inscrit_admin_set_form_empty_001(self):
		""""""
    	#  Demande création de publication dans un set avec le text et le premier fichier du formulaire vide
		posts_before =  len(PublicationSet.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/make_post_set/'  + str(self.set.id) + '/' , {'publication_text': "", "file_1":"", "file_2":image2 } )
		posts_after =  len(PublicationSet.objects.all())
		self.assertTrue( posts_after == posts_before + 1)
		self.assertTrue( response.url == '../../set/' + str(self.set.id) + '/' )

	def test_sets_publier_dans_set_utilisateur_inscrit_user_set(self):
		""""""
    	#  Demande création de publications dans un set par un utilisateur inscrit appartenant au set et etant simple membre du set
		posts_before =  len(PublicationSet.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_member_set.post('/sets/make_post_set/'  + str(self.set.id) + '/' , {'publication_text': "text de la publication", "file_1":image1, "file_2":image2 } )
		posts_after =  len(PublicationSet.objects.all())
		self.assertTrue( posts_after == posts_before + 1)
		self.assertTrue( response.url == '../../set/' + str(self.set.id) + '/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_publier_dans_set_utilisateur_inscrit_wait_set(self):
		""""""
    	#  Demande création de publications dans un set par un utilsateur inscrit  appartenant au set et etant en attente de validation d'entrée dans le set
		posts_before =  len(PublicationSet.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_wait_set.post('/sets/make_post_set/'  + str(self.set.id) + '/' , {'publication_text': "text de la publication", "file_1":image1, "file_2":image2 } )
		posts_after =  len(PublicationSet.objects.all())
		self.assertTrue( posts_before == posts_after)
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )


		#_____________________________________________


		#_____________________________________________


	def test_sets_publier_dans_set_user_unactivate(self):
		""""""
    	#   Demande de création de publications dans un set par un compte non activé
		posts_before =  len(PublicationSet.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_unactivate_user.post('/sets/make_post_set/'  + str(self.set.id) + '/' , {'publication_text': "text de la publication", "file_1":image1, "file_2":image2 } )
		posts_after =  len(PublicationSet.objects.all())
		self.assertTrue( posts_after == posts_before)
		self.assertTrue( response.url == '../../../user/home/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_publier_dans_set_user_locked(self):
		""""""
    	#   Demande de création de publications dans un set par un compte bloqué
		posts_before =  len(PublicationSet.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_locked_user.post('/sets/make_post_set/'  + str(self.set.id) + '/' , {'publication_text': "text de la publication", "file_1":image1, "file_2":image2 } )
		posts_after =  len(PublicationSet.objects.all())
		self.assertTrue( posts_after == posts_before)
		self.assertTrue( response.url == '../../../user/home/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_publier_dans_set_set_locked(self):
		""""""
    	#   Demande de création de publications dans un set fermé
		posts_before =  len(PublicationSet.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/make_post_set/'  + str(self.set_locked.id) + '/' , {'publication_text': "text de la publication", "file_1":image1, "file_2":image2 } )
		posts_after =  len(PublicationSet.objects.all())
		self.assertTrue( posts_after == posts_before)
		self.assertTrue( response.url == '../../sets/set/' + str(self.set_locked.id) + '/' )
		self.assertTrue( response.status_code == 302 )



	#  ----- Make post event

	def test_sets_publier_dans_evenement_utilisateur_non_inscrit(self):
		""""""
		#  Demande de création publication dans un évènement par un utilisateur non inscrit
		posts_before =  len(PublicationEvenement.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_not_registred.post('/sets/make_post_event/'  + str(self.event_member.id) + '/' , {'publication_text': "text de la publication", "file_1":image1, "file_2":image2 } )
		posts_after =  len(PublicationEvenement.objects.all())
		self.assertTrue( posts_before == posts_after)
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_publier_dans_evenement_utilisateur_inscrit_no_set(self):
		""""""
		#  Demande de création publication dans un évènement par un utilsateur inscrit n'appartenant pas au set
		posts_before =  len(PublicationEvenement.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_no_set.post('/sets/make_post_event/'  + str(self.event_member.id) + '/' , {'publication_text': "text de la publication", "file_1":image1, "file_2":image2 } )
		posts_after =  len(PublicationEvenement.objects.all())
		self.assertTrue( posts_before == posts_after)
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_publier_dans_evenement_utilisateur_inscrit_admin_set(self):
		""""""
    	#  Demande de création publication dans un évènement par un utilisateur inscrit  appartenant au set et etant administrateur du set
		posts_before =  len(PublicationEvenement.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/make_post_event/'  + str(self.event_member.id) + '/' , {'publication_text': "text de la publication", "file_1":image1, "file_2":image2 } )
		posts_after =  len(PublicationEvenement.objects.all())
		self.assertTrue( posts_after == posts_before + 1)
		self.assertTrue( response.url == '../../event/' + str(self.event_member.id) + '/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_publier_dans_evenement_utilisateur_inscrit_admin_set_not_id_int(self):
		""""""
    	#  Demande de création publication dans un évènement avec un identifiant évènement qui n'est pas un nombre entier
		posts_before =  len(PublicationEvenement.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/make_post_event/'  + 'a' + '/' , {'publication_text': "text de la publication", "file_1":image1, "file_2":image2 } )
		posts_after =  len(PublicationEvenement.objects.all())
		self.assertTrue( posts_before == posts_after)
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_publier_dans_evenement_utilisateur_inscrit_admin_set_not_set_in_application(self):
		""""""
    	#  Demande de création publication dans un évènement dont l'identifiant ne correspond à aucun set de l'application
		posts_before =  len(PublicationEvenement.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/make_post_event/'  + '1000' + '/' , {'publication_text': "text de la publication", "file_1":image1, "file_2":image2 } )
		posts_after =  len(PublicationEvenement.objects.all())
		self.assertTrue( posts_before == posts_after)
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_publier_dans_evenement_utilisateur_inscrit_admin_set_form_empty_000(self):
		""""""
    	#  Demande de création publication dans un évènement avec un formulaire vide
		posts_before =  len(PublicationEvenement.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/make_post_event/'  + str(self.event_member.id) + '/' , {'publication_text': "", "file_1":"", "file_2":"" } )
		posts_after =  len(PublicationEvenement.objects.all())
		self.assertTrue( posts_before == posts_after)
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_publier_dans_evenement_utilisateur_inscrit_admin_set_form_empty_011(self):
		""""""
    	#  Demande de création publication dans un évènement avec un text de formulaire vide
		posts_before =  len(PublicationEvenement.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/make_post_event/'  + str(self.event_member.id) + '/' , {'publication_text': "", "file_1":image1, "file_2":image2 } )
		posts_after =  len(PublicationEvenement.objects.all())
		self.assertTrue( posts_after == posts_before + 1)
		self.assertTrue( response.url == '../../event/' + str(self.event_member.id) + '/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_publier_dans_evenement_utilisateur_inscrit_admin_set_form_empty_101(self):
		""""""
    	#  Demande de création publication dans un évènement avec le premier fichier du formulaire vide
		posts_before =  len(PublicationEvenement.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/make_post_event/'  + str(self.event_member.id) + '/' , {'publication_text': "text de la publication", "file_1":"", "file_2":image2 } )
		posts_after =  len(PublicationEvenement.objects.all())
		self.assertTrue( posts_after == posts_before + 1)
		self.assertTrue( response.url == '../../event/' + str(self.event_member.id) + '/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_publier_dans_evenement_utilisateur_inscrit_admin_set_form_empty_110(self):
		""""""
    	#  Demande de création publication dans un évènement avec le deuxième fichier de formulaire vide
		posts_before =  len(PublicationEvenement.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/make_post_event/'  + str(self.event_member.id) + '/' , {'publication_text': "text de la publication", "file_1":image1, "file_2":"" } )
		posts_after =  len(PublicationEvenement.objects.all())
		self.assertTrue( posts_after == posts_before + 1)
		self.assertTrue( response.url == '../../event/' + str(self.event_member.id) + '/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_publier_dans_evenement_utilisateur_inscrit_admin_set_form_empty_100(self):
		""""""
    	#  Demande de création publication dans un évènement avec les deux fichier du formulaire vide
		posts_before =  len(PublicationEvenement.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/make_post_event/'  + str(self.event_member.id) + '/' , {'publication_text': "text de la publication", "file_1":"", "file_2":"" } )
		posts_after =  len(PublicationEvenement.objects.all())
		self.assertTrue( posts_after == posts_before + 1)
		self.assertTrue( response.url == '../../event/' + str(self.event_member.id) + '/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_publier_dans_evenement_utilisateur_inscrit_admin_set_form_empty_010(self):
		""""""
    	#  Demande de création publication dans un évènement avec le text et le deuxème fichier du formulaire vide
		posts_before =  len(PublicationEvenement.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/make_post_event/'  + str(self.event_member.id) + '/' , {'publication_text': "", "file_1":image1, "file_2":"" } )
		posts_after =  len(PublicationEvenement.objects.all())
		self.assertTrue( posts_after == posts_before + 1)
		self.assertTrue( response.url == '../../event/' + str(self.event_member.id) + '/' )

	def test_sets_publier_dans_evenement_utilisateur_inscrit_admin_set_form_empty_001(self):
		""""""
    	#  Demande de création publication dans un évènement avec le text et le premier fichier du formulaire vide
		posts_before =  len(PublicationEvenement.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/make_post_event/'  + str(self.event_member.id) + '/' , {'publication_text': "", "file_1":"", "file_2":image2 } )
		posts_after =  len(PublicationEvenement.objects.all())
		self.assertTrue( posts_after == posts_before + 1)
		self.assertTrue( response.url == '../../event/' + str(self.event_member.id) + '/' )

	def test_sets_publier_dans_evenement_utilisateur_inscrit_user_set(self):
		""""""
    	#  Demande de création publication dans un évènement par un utilisateur inscrit appartenant au set et etant simple membre du set
		posts_before =  len(PublicationEvenement.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_member_set.post('/sets/make_post_event/'  + str(self.event_member.id) + '/' , {'publication_text': "text de la publication", "file_1":image1, "file_2":image2 } )
		posts_after =  len(PublicationEvenement.objects.all())
		self.assertTrue( posts_after == posts_before + 1)
		self.assertTrue( response.url == '../../event/' + str(self.event_member.id) + '/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_publier_dans_evenement_utilisateur_inscrit_wait_set(self):
		""""""
    	#  Demande de création publication dans un évènement par un utilsateur inscrit appartenant au set et etant en attente de validation d'entrée dans le set
		posts_before =  len(PublicationEvenement.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_wait_set.post('/sets/make_post_event/'  + str(self.event_member.id) + '/' , {'publication_text': "text de la publication", "file_1":image1, "file_2":image2 } )
		posts_after =  len(PublicationEvenement.objects.all())
		self.assertTrue( posts_before == posts_after)
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_publier_dans_evenement_user_unactivate(self):
		""""""
    	#   Demande de publication dans un évènement par un compte non activé
		posts_before =  len(PublicationEvenement.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_unactivate_user.post('/sets/make_post_event/'  + str(self.event_member.id) + '/' , {'publication_text': "text de la publication", "file_1":image1, "file_2":image2 } )
		posts_after =  len(PublicationEvenement.objects.all())
		self.assertTrue( posts_after == posts_before )
		self.assertTrue( response.url == '../../../user/home/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_publier_dans_evenement_user_locked(self):
		""""""
    	#   Demande de publication dans un évènement par un compte bloqué
		posts_before =  len(PublicationEvenement.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_locked_user.post('/sets/make_post_event/'  + str(self.event_member.id) + '/' , {'publication_text': "text de la publication", "file_1":image1, "file_2":image2 } )
		posts_after =  len(PublicationEvenement.objects.all())
		self.assertTrue( posts_after == posts_before )
		self.assertTrue( response.url == '../../../user/home/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_publier_dans_evenement_set_locked(self):
		""""""
    	#   Demande de publication dans un évènement d'un set fermé
		posts_before =  len(PublicationEvenement.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/make_post_event/'  + str(self.event_locked_member.id) + '/' , {'publication_text': "text de la publication", "file_1":image1, "file_2":image2 } )
		posts_after =  len(PublicationEvenement.objects.all())
		self.assertTrue( posts_after == posts_before )
		self.assertTrue( response.url == '../../../sets/event/' + str(self.event_locked_member.id) + '/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_publier_dans_evenement_locked(self):
		""""""
    	#   Demande de publication dans un évènement fermé
		posts_before =  len(PublicationEvenement.objects.all())
		image1 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		image2 = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
		response = self.client_registred_administrator_set.post('/sets/make_post_event/'  + str(self.event_locked_member.id) + '/' , {'publication_text': "text de la publication", "file_1":image1, "file_2":image2 } )
		posts_after =  len(PublicationEvenement.objects.all())
		self.assertTrue( posts_after == posts_before )
		self.assertTrue( response.url == '../../../sets/event/' + str(self.event_locked_member.id) + '/' )
		self.assertTrue( response.status_code == 302 )




	#  ----- Manage like post set

	def test_sets_likage_publication_set_utilisateur_non_inscrit(self):
		""""""
		#  Demande de like d'une publication d'un set par un utilisateur non inscrit
		likes_before = len( JaimePublicationSet.objects.all() )
		response = self.client_not_registred.post('/sets/manage_like_post_set/'  + str(self.publication_set_user.id) + '/' )
		likes_after = len( JaimePublicationSet.objects.all() )
		self.assertTrue( likes_after == likes_before)
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_likage_publication_set_utilisateur_inscrit_no_set(self):
		""""""
		#  Demande de like d'une publication d'un set par un utilsateur inscrit n'appartenant pas au set
		likes_before = len( JaimePublicationSet.objects.all() )
		response = self.client_registred_no_set.post('/sets/manage_like_post_set/'  + str(self.publication_set_user.id) + '/' )
		likes_after = len( JaimePublicationSet.objects.all() )
		self.assertTrue( likes_after == likes_before)
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_likage_publication_set_utilisateur_inscrit_admin_set(self):
		""""""
    	#  Demande de like d'une publication d'un set par un utilisateur inscrit  appartenant au set et etant administrateur du set
		likes_before = len( JaimePublicationSet.objects.all() )
		response = self.client_registred_administrator_set.post('/sets/manage_like_post_set/'  + str(self.publication_set_user.id) + '/' )
		likes_after = len( JaimePublicationSet.objects.all() )
		self.assertTrue( likes_after == likes_before + 1  )
		self.assertTrue( response.content == b'like_make' )
		self.assertTrue( response.status_code == 200 )

	def test_sets_likage_publication_set_utilisateur_inscrit_user_set_not_id_int(self):
		""""""
    	#  Demande de like d'une publication d'un set avec un identifiant publication set qui n'est pas un nombre entier
		likes_before = len( JaimePublicationSet.objects.all() )
		response = self.client_registred_administrator_set.post('/sets/manage_like_post_set/'  + 'a' + '/' )
		likes_after = len( JaimePublicationSet.objects.all() )
		self.assertTrue( likes_after == likes_before)
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_likage_publication_set_utilisateur_inscrit_wait_set_not_post_in_application(self):
		""""""
    	#  Demande de like d'une publication d'un set dont l'identifiant ne correspond à aucune publication de set de l'application
		likes_before = len( JaimePublicationSet.objects.all() )
		response = self.client_registred_administrator_set.post('/sets/manage_like_post_set/'  + '1000' + '/' )
		likes_after = len( JaimePublicationSet.objects.all() )
		self.assertTrue( likes_after == likes_before)
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_likage_publication_set_utilisateur_inscrit_user_set(self):
		""""""
    	#  Demande de like d'une publication d'un set par un utilisateur inscrit  appartenant au set et etant simple membre du set
		likes_before = len( JaimePublicationSet.objects.all() )
		response = self.client_registred_member_set.post('/sets/manage_like_post_set/'  + str(self.publication_set_admin_set.id) + '/' )
		likes_after = len( JaimePublicationSet.objects.all() )
		self.assertTrue( likes_after == ( likes_before + 1 ) )
		self.assertTrue( response.content == b'like_make' )
		self.assertTrue( response.status_code == 200 )


	def test_sets_likage_publication_set_utilisateur_inscrit_wait_set(self):
		""""""
    	#  Demande de like d'une publication d'un set par un utilsateur inscrit  appartenant au set et etant en attente de validation d'entrée dans le set
		likes_before = len( JaimePublicationSet.objects.all() )
		response = self.client_registred_wait_set.post('/sets/manage_like_post_set/'  + str(self.publication_set_user.id) + '/' )
		likes_after = len( JaimePublicationSet.objects.all() )
		self.assertTrue( likes_after == likes_before )
		self.assertTrue( response.content == b'validate_enter_set_first' )
		self.assertTrue( response.status_code == 200 )

	def test_sets_likage_publication_set_utilisateur_unactivate(self):
		""""""
    	#   Demande de like d'une publication d'un set par un compte non activé
		likes_before = len( JaimePublicationSet.objects.all() )
		response = self.client_unactivate_user.post('/sets/manage_like_post_set/'  + str(self.publication_set_user.id) + '/' )
		likes_after = len( JaimePublicationSet.objects.all() )
		self.assertTrue( likes_after == likes_before )
		self.assertTrue( response.url == '../../../user/home/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_likage_publication_set_utilisateur_locked(self):
		""""""
    	#   Demande de like d'une publication d'un set par un compte bloqué
		likes_before = len( JaimePublicationSet.objects.all() )
		response = self.client_locked_user.post('/sets/manage_like_post_set/'  + str(self.publication_set_user.id) + '/' )
		likes_after = len( JaimePublicationSet.objects.all() )
		self.assertTrue( likes_after == likes_before )
		self.assertTrue( response.url == '../../../user/home/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_likage_publication_set_utilisateur_set_locked(self):
		""""""
    	#   Demande de like d'une publication d'un set fermé
		likes_before = len( JaimePublicationSet.objects.all() )
		response = self.client_registred_administrator_set.post('/sets/manage_like_post_set/'  + str(self.publication_set_locked_user.id) + '/' )
		likes_after = len( JaimePublicationSet.objects.all() )
		self.assertTrue( likes_after == likes_before )
		self.assertTrue( response.url == '../../sets/set/' + str(self.publication_set_locked_user.set0.id) + '/' )
		self.assertTrue( response.status_code == 302 )


	
	#  ----- Manage dislike post set

	def test_sets_dislikage_publication_set_utilisateur_non_inscrit(self):
		""""""
		#  Demande de dislike d'une publication d'un set par un utilisateur non inscrit
		likes_before = len( JaimePublicationSet.objects.all() )
		response = self.client_not_registred.post('/sets/manage_like_post_set/'  + str(self.publication_set_admin_set.id) + '/' )
		likes_after = len( JaimePublicationSet.objects.all() )
		self.assertTrue( likes_after == likes_before)
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )


	def test_sets_dislikage_publication_set_utilisateur_inscrit_no_set(self):
		""""""
		#  Demande de dislike d'une publication d'un set par un utilsateur inscrit n'appartenant pas au set
		likes_before = len( JaimePublicationSet.objects.all() )
		response = self.client_registred_no_set.post('/sets/manage_like_post_set/'  + str(self.publication_set_admin_set.id) + '/' )
		likes_after = len( JaimePublicationSet.objects.all() )
		self.assertTrue( likes_after == likes_before)
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_dislikage_publication_set_utilisateur_inscrit_admin_set(self):
		""""""
    	#  Demande de dislike d'une publication d'un set par un utilisateur inscrit  appartenant au set et etant administrateur du set
		likes_before = len( JaimePublicationSet.objects.all() )
		response = self.client_registred_administrator_set.post('/sets/manage_like_post_set/'  + str(self.publication_set_admin_set.id) + '/' )
		likes_after = len( JaimePublicationSet.objects.all() )
		self.assertTrue( likes_after == ( likes_before - 1 ) )
		self.assertTrue( response.content == b'unlike_make' )
		self.assertTrue( response.status_code == 200 )

	def test_sets_dislikage_publication_set_utilisateur_inscrit_user_set_not_id_int(self):
		""""""
    	#  Demande de dislike d'une publication d'un set avec un identifiant publication set qui n'est pas un nombre entier
		likes_before = len( JaimePublicationSet.objects.all() )
		response = self.client_registred_administrator_set.post('/sets/manage_like_post_set/'  + 'a' + '/' )
		likes_after = len( JaimePublicationSet.objects.all() )
		self.assertTrue( likes_after == likes_before)
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_dislikage_publication_set_utilisateur_inscrit_wait_set_not_post_in_application(self):
		""""""
    	#  Demande de dislike d'une publication d'un set dont l'identifiant ne correspond à aucune publication de set de l'application
		likes_before = len( JaimePublicationSet.objects.all() )
		response = self.client_registred_administrator_set.post('/sets/manage_like_post_set/'  + '1000' + '/' )
		likes_after = len( JaimePublicationSet.objects.all() )
		self.assertTrue( likes_after == likes_before)
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_dislikage_publication_set_utilisateur_inscrit_user_set(self):
		""""""
    	#  Demande de dislike d'une publication d'un set par un utilisateur inscrit  appartenant au set et etant simple membre du set
		likes_before = len( JaimePublicationSet.objects.all() )
		response = self.client_registred_member_set.post('/sets/manage_like_post_set/'  + str(self.publication_set_user.id) + '/' )
		likes_after = len( JaimePublicationSet.objects.all() )
		self.assertTrue( likes_after == ( likes_before - 1 ) )
		self.assertTrue( response.content == b'unlike_make' )
		self.assertTrue( response.status_code == 200 )

	def test_sets_dislikage_publication_set_utilisateur_inscrit_wait_set(self):
		""""""
    	#  Demande de dislike d'une publication d'un set par un utilsateur inscrit  appartenant au set et etant en attente de validation d'entrée dans le set
		likes_before = len( JaimePublicationSet.objects.all() )
		response = self.client_registred_wait_set.post('/sets/manage_like_post_set/'  + str(self.publication_set_admin_set.id) + '/' )
		likes_after = len( JaimePublicationSet.objects.all() )
		self.assertTrue( likes_after == likes_before )
		self.assertTrue( response.content == b'validate_enter_set_first' )
		self.assertTrue( response.status_code == 200 )

	def test_sets_dislikage_publication_set_utilisateur_unactivate(self):
		""""""
    	#   Demande de dislike d'une publication d'un set par un compte non activé
		likes_before = len( JaimePublicationSet.objects.all() )
		response = self.client_unactivate_user.post('/sets/manage_like_post_set/'  + str(self.publication_set_admin_set.id) + '/' )
		likes_after = len( JaimePublicationSet.objects.all() )
		self.assertTrue( likes_after == likes_before )
		self.assertTrue( response.url == '../../../user/home/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_dislikage_publication_set_utilisateur_locked(self):
		""""""
    	#   Demande de dislike d'une publication d'un set par un compte bloqué
		likes_before = len( JaimePublicationSet.objects.all() )
		response = self.client_locked_user.post('/sets/manage_like_post_set/'  + str(self.publication_set_admin_set.id) + '/' )
		likes_after = len( JaimePublicationSet.objects.all() )
		self.assertTrue( likes_after == likes_before )
		self.assertTrue( response.url == '../../../user/home/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_dislikage_publication_set_utilisateur_set_locked(self):
		""""""
    	#   Demande de dislike d'une publication d'un set fermé
		likes_before = len( JaimePublicationSet.objects.all() )
		response = self.client_registred_administrator_set.post('/sets/manage_like_post_set/'  + str(self.publication_set_locked_user.id) + '/' )
		likes_after = len( JaimePublicationSet.objects.all() )
		self.assertTrue( likes_after == likes_before )
		self.assertTrue( response.url == '../../sets/set/' + str(self.publication_set_locked_user.set0.id) + '/' )
		self.assertTrue( response.status_code == 302 )




	#  ----- Manage like post event

	def test_sets_likage_publication_evenement_utilisateur_non_inscrit(self):
		""""""
		#  Demande de like d'une publication d'un évènement par un utilisateur non inscrit

		likes_before = len( JaimePublicationEvenement.objects.all() )
		response = self.client_not_registred.post('/sets/manage_like_post_event/'  + str(self.publication_event_admin_event.id) + '/' )
		likes_after = len( JaimePublicationEvenement.objects.all() )
		self.assertTrue( likes_after == likes_before)
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_likage_publication_evenement_utilisateur_inscrit_no_set(self):
		""""""
		#  Demande de like d'une publication d'un évènement par un utilsateur inscrit n'appartenant pas au set

		likes_before = len( JaimePublicationEvenement.objects.all() )
		response = self.client_registred_no_set.post('/sets/manage_like_post_event/'  + str(self.publication_event_admin_event.id) + '/' )
		likes_after = len( JaimePublicationEvenement.objects.all() )
		self.assertTrue( likes_after == likes_before)
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_likage_publication_evenement_utilisateur_inscrit_admin_set(self):
		""""""
    	#  Demande de like d'une publication d'un évènement par un utilisateur inscrit  appartenant au set et etant administrateur du set
		likes_before = len( JaimePublicationEvenement.objects.all() )
		response = self.client_registred_administrator_set.post('/sets/manage_like_post_event/'  + str(self.publication_event_admin_event.id) + '/' )
		likes_after = len( JaimePublicationEvenement.objects.all() )
		self.assertTrue( likes_after == ( likes_before + 1 ) )
		self.assertTrue( response.content == b'like_make' )
		self.assertTrue( response.status_code == 200 )

	def test_sets_likage_publication_evenement_utilisateur_inscrit_user_set_not_id_int(self):
		""""""
    	#  Demande de like d'une publication d'un évènement avec un identifiant publication évènement qui n'est pas un nombre entier
		likes_before = len( JaimePublicationEvenement.objects.all() )
		response = self.client_registred_administrator_set.post('/sets/manage_like_post_event/'  + 'a' + '/' )
		likes_after = len( JaimePublicationEvenement.objects.all() )
		self.assertTrue( likes_after == likes_before)
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_likage_publication_evenement_utilisateur_inscrit_wait_set_not_post_in_application(self):
		""""""
    	#  Demande de like d'une publication d'un évènement dont l'identifiant ne correspond à aucune publication d'évènement de l'application
		likes_before = len( JaimePublicationEvenement.objects.all() )
		response = self.client_registred_administrator_set.post('/sets/manage_like_post_event/'  + '1000' + '/' )
		likes_after = len( JaimePublicationEvenement.objects.all() )
		self.assertTrue( likes_after == likes_before)
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_likage_publication_evenement_utilisateur_inscrit_user_set(self):
		""""""
    	#  Demande de like d'une publication d'un évènement par un utilisateur inscrit  appartenant au set et etant simple membre du set
		likes_before = len( JaimePublicationEvenement.objects.all() )
		response = self.client_registred_member_set.post('/sets/manage_like_post_event/'  + str(self.publication_event_no_admin_event.id) + '/' )
		likes_after = len( JaimePublicationEvenement.objects.all() )
		self.assertTrue( likes_after == ( likes_before + 1 ) )
		self.assertTrue( response.content == b'like_make' )
		self.assertTrue( response.status_code == 200 )


	def test_sets_likage_publication_evenement_utilisateur_inscrit_wait_set(self):
		""""""
    	#  Demande de like d'une publication d'un évènement par un utilsateur inscrit  appartenant au set et etant en attente de validation d'entrée dans le set
		likes_before = len( JaimePublicationEvenement.objects.all() )
		response = self.client_registred_wait_set.post('/sets/manage_like_post_event/'  + str(self.publication_event_no_admin_event.id) + '/' )
		likes_after = len( JaimePublicationEvenement.objects.all() )
		self.assertTrue( likes_after == likes_before )
		self.assertTrue( response.content == b'validate_enter_set_first' )

	def test_sets_likage_publication_evenement_user_unactivate(self):
		""""""
    	#   Demande de like d'une publication d'un évènement par un compte non activé
		likes_before = len( JaimePublicationEvenement.objects.all() )
		response = self.client_unactivate_user.post('/sets/manage_like_post_event/'  + str(self.publication_event_no_admin_event.id) + '/' )
		likes_after = len( JaimePublicationEvenement.objects.all() )
		self.assertTrue( likes_after == ( likes_before ) )
		self.assertTrue( response.url == '../../../user/home/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_likage_publication_evenement_user_locked(self):
		""""""
    	#   Demande de like d'une publication d'un évènement par un compte bloqué
		likes_before = len( JaimePublicationEvenement.objects.all() )
		response = self.client_unactivate_user.post('/sets/manage_like_post_event/'  + str(self.publication_event_no_admin_event.id) + '/' )
		likes_after = len( JaimePublicationEvenement.objects.all() )
		self.assertTrue( likes_after == ( likes_before ) )
		self.assertTrue( response.url == '../../../user/home/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_likage_publication_evenement_set_locked(self):
		""""""
    	#   Demande de like d'une publication d'un évènement d'un set fermé
		likes_before = len( JaimePublicationEvenement.objects.all() )
		response = self.client_registred_administrator_set.post('/sets/manage_like_post_event/'  + str(self.publication_event_set_locked_user_member.id) + '/' )
		likes_after = len( JaimePublicationEvenement.objects.all() )
		self.assertTrue( likes_after == ( likes_before ) )
		self.assertTrue( response.url == '../../../sets/event/' + str(self.publication_event_set_locked_user_member.evenement.id) + '/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_likage_publication_evenement_locked(self):
		""""""
    	#   Demande de like d'une publication d'un évènement fermé
		likes_before = len( JaimePublicationEvenement.objects.all() )
		response = self.client_registred_administrator_set.post('/sets/manage_like_post_event/'  + str(self.publication_event_locked_admin_event.id) + '/' )
		likes_after = len( JaimePublicationEvenement.objects.all() )
		self.assertTrue( likes_after == ( likes_before ) )
		self.assertTrue( response.url == '../../../sets/event/' + str(self.publication_event_locked_admin_event.evenement.id) + '/' )
		self.assertTrue( response.status_code == 302 )




	#  ----- Manage dislike post event

	def test_sets_dislikage_publication_evenement_utilisateur_non_inscrit(self):
		""""""
		#  Demande de dislike d'une publication d'un évènement par un utilisateur non inscrit
		likes_before = len( JaimePublicationEvenement.objects.all() )
		response = self.client_not_registred.post('/sets/manage_like_post_event/'  + str(self.publication_event_no_admin_event.id) + '/' )
		likes_after = len( JaimePublicationEvenement.objects.all() )
		self.assertTrue( likes_after == likes_before )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )


	def test_sets_dislikage_publication_evenement_utilisateur_inscrit_no_set(self):
		""""""
		#  Demande de dislike d'une publication d'un évènement par un utilsateur inscrit n'appartenant pas au set
		likes_before = len( JaimePublicationEvenement.objects.all() )
		response = self.client_registred_no_set.post('/sets/manage_like_post_event/'  + str(self.publication_event_no_admin_event.id) + '/' )
		likes_after = len( JaimePublicationEvenement.objects.all() )
		self.assertTrue( likes_after == likes_before )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_dislikage_publication_evenement_utilisateur_inscrit_admin_set(self):
		""""""
    	#  Demande de dislike d'une publication d'un évènement par un utilisateur inscrit  appartenant au set et etant administrateur du set
		likes_before = len( JaimePublicationEvenement.objects.all() )
		response = self.client_registred_administrator_set.post('/sets/manage_like_post_event/'  + str(self.publication_event_no_admin_event.id) + '/' )
		likes_after = len( JaimePublicationEvenement.objects.all() )
		self.assertTrue( likes_after == ( likes_before - 1 ) )
		self.assertTrue( response.content == b'unlike_make' )
		self.assertTrue( response.status_code == 200 )

	def test_sets_dislikage_publication_evenement_utilisateur_inscrit_user_set_not_id_int(self):
		""""""
    	#  Demande de like d'une publication d'un évènement avec un identifiant publication évènement qui n'est pas un nombre entier
		likes_before = len( JaimePublicationEvenement.objects.all() )
		response = self.client_registred_administrator_set.post('/sets/manage_like_post_event/'  + 'a' + '/' )
		likes_after = len( JaimePublicationEvenement.objects.all() )
		self.assertTrue( likes_after == likes_before)
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_dislikage_publication_evenement_utilisateur_inscrit_wait_set_not_post_in_application(self):
		""""""
    	#  Demande de like d'une publication d'un évènement dont l'identifiant ne correspond à aucune publication d'évènement de l'application
		likes_before = len( JaimePublicationEvenement.objects.all() )
		response = self.client_registred_administrator_set.post('/sets/manage_like_post_event/'  + '1000' + '/' )
		likes_after = len( JaimePublicationEvenement.objects.all() )
		self.assertTrue( likes_after == likes_before)
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_dislikage_publication_evenement_utilisateur_inscrit_user_set(self):
		""""""
    	#  Demande de dislike d'une publication d'un évènement par un utilisateur inscrit  appartenant au set et etant simple membre du set
		likes_before = len( JaimePublicationEvenement.objects.all() )
		response = self.client_registred_member_set.post('/sets/manage_like_post_event/'  + str(self.publication_event_admin_event.id) + '/' )
		likes_after = len( JaimePublicationEvenement.objects.all() )
		self.assertTrue( likes_after == ( likes_before - 1 ) )
		self.assertTrue( response.content == b'unlike_make' )
		self.assertTrue( response.status_code == 200 )

	def test_sets_dislikage_publication_evenement_utilisateur_inscrit_wait_set(self):
		""""""
    	#  Demande de dislike d'une publication d'un évènement par un utilsateur inscrit  appartenant au set et etant en attente de validation d'entrée dans le set
		likes_before = len( JaimePublicationEvenement.objects.all() )
		response = self.client_registred_wait_set.post('/sets/manage_like_post_event/'  + str(self.publication_event_no_admin_event.id) + '/' )
		likes_after = len( JaimePublicationEvenement.objects.all() )
		self.assertTrue( likes_after == likes_before )
		self.assertTrue( response.content == b'validate_enter_set_first' )

	def test_sets_dislikage_publication_evenement_user_unactivate(self):
		""""""
    	#   Demande de dislike d'une publication d'un évènement par un compte non activé
		likes_before = len( JaimePublicationEvenement.objects.all() )
		response = self.client_unactivate_user.post('/sets/manage_like_post_event/'  + str(self.publication_event_admin_event.id) + '/' )
		likes_after = len( JaimePublicationEvenement.objects.all() )
		self.assertTrue( likes_after == ( likes_before ) )
		self.assertTrue( response.url == '../../../user/home/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_dislikage_publication_evenement_user_locked(self):
		""""""
    	#   Demande de dislike d'une publication d'un évènement par un compte bloqué
		likes_before = len( JaimePublicationEvenement.objects.all() )
		response = self.client_locked_user.post('/sets/manage_like_post_event/'  + str(self.publication_event_admin_event.id) + '/' )
		likes_after = len( JaimePublicationEvenement.objects.all() )
		self.assertTrue( likes_after == ( likes_before ) )
		self.assertTrue( response.url == '../../../user/home/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_dislikage_publication_evenement_set_locked(self):
		""""""
    	#   Demande de dislike d'une publication d'un évènement d'un set fermé
		likes_before = len( JaimePublicationEvenement.objects.all() )
		response = self.client_registred_administrator_set.post('/sets/manage_like_post_event/'  + str(self.publication_event_set_locked_user_member.id) + '/' )
		likes_after = len( JaimePublicationEvenement.objects.all() )
		self.assertTrue( likes_after == likes_before )
		self.assertTrue( response.url == '../../../sets/event/' + str(self.publication_event_set_locked_user_member.evenement.id) + '/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_dislikage_publication_evenement_locked(self):
		""""""
    	#   Demande de dislike d'une publication d'un évènement fermé
		likes_before = len( JaimePublicationEvenement.objects.all() )
		response = self.client_registred_member_set.post('/sets/manage_like_post_event/'  + str(self.publication_event_locked_admin_event.id) + '/' )
		likes_after = len( JaimePublicationEvenement.objects.all() )
		self.assertTrue( likes_after == likes_before )
		self.assertTrue( response.url == '../../../sets/event/' + str(self.publication_event_locked_admin_event.evenement.id) + '/' )
		self.assertTrue( response.status_code == 302 )




	#  ----- Add user in set


	def test_sets_add_user_set_utilisateur_non_inscrit(self):
		""""""
		#  Demande d'ajout d'un utilisateur dans un set par un utilisateur non inscrit
		users_before = len( SetUtilisateurs.objects.all() )
		response = self.client_not_registred.post('/sets/delete_add_user_set/' + str(self.set.id) + '/'  + str(self.user_registred_no_set.id) + '/' )
		users_after = len( SetUtilisateurs.objects.all() )
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )


	def test_sets_add_user_set_utilisateur_inscrit_no_set(self):
		""""""
		#  Demande d'ajout d'un utilisateur dans un set par un utilsateur inscrit n'appartenant pas au set
		users_before = len( SetUtilisateurs.objects.all() )
		response = self.client_registred_no_set.post('/sets/delete_add_user_set/' + str(self.set.id) + '/'  + str(self.user_registred_no_set.id) + '/' )
		users_after = len( SetUtilisateurs.objects.all() )
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_add_user_set_utilisateur_inscrit_admin_set(self):
		""""""
    	#  Demande d'ajout d'un utilisateur dans un set par un utilisateur inscrit  appartenant au set et etant administrateur du set
		users_before = len( SetUtilisateurs.objects.all() )
		response = self.client_registred_administrator_set.post('/sets/delete_add_user_set/'  + str(self.set.id) + '/'  + str(self.user_registred_no_set.id) + '/' )
		users_after = len( SetUtilisateurs.objects.all() )
		self.assertTrue( users_after == ( users_before + 1 ) )
		self.assertTrue( response.content == b'user_added' )
		self.assertTrue( SetUtilisateurs.objects.get(set0=self.set.id, utilisateur=self.user_registred_no_set.id).statut == 'attente_validation' )
		self.assertTrue( response.status_code == 200 )

	def test_sets_add_user_set_utilisateur_inscrit_admin_set_not_id_set_int(self):
		""""""
    	#  Demande d'ajout d'un utilisateur dans un set avec un identifiant set qui n'est pas un nombre entier
		users_before = len( SetUtilisateurs.objects.all() )
		response = self.client_registred_administrator_set.post('/sets/delete_add_user_set/'  + '5000' + '/'  + str(self.user_registred_no_set.id) + '/' )
		users_after = len( SetUtilisateurs.objects.all() )
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_add_user_set_utilisateur_inscrit_admin_set_not_set_int_appliation(self):
		""""""
    	#  Demande d'ajout d'un utilisateur dans un set dont l'identifiant ne correspond à aucun set de l'application
		users_before = len( SetUtilisateurs.objects.all() )
		response = self.client_registred_administrator_set.post('/sets/delete_add_user_set/'  + str(self.set.id) + '/'  + '5000' + '/' )
		users_after = len( SetUtilisateurs.objects.all() )
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_add_user_set_utilisateur_inscrit_admin_set_not_id_user_int(self):
		""""""
    	#  Demande d'ajout d'un utilisateur dans un set avec un identifiant utilisateur qui n'est pas un nombre entier
		users_before = len( SetUtilisateurs.objects.all() )
		response = self.client_registred_administrator_set.post('/sets/delete_add_user_set/'  + '5000' + '/'  + str(self.user_registred_no_set.id) + '/' )
		users_after = len( SetUtilisateurs.objects.all() )
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_add_user_set_utilisateur_inscrit_admin_set_not_user_in_application(self):
		""""""
    	#  Demande d'ajout d'un utilisateur dans un set dont l'identifiant ne correspond à aucun utilisateur de l'application
		users_before = len( SetUtilisateurs.objects.all() )
		response = self.client_registred_administrator_set.post('/sets/delete_add_user_set/'  + str(self.set.id) + '/'  + '5000' + '/' )
		users_after = len( SetUtilisateurs.objects.all() )
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_add_user_set_utilisateur_inscrit_user_set(self):
		""""""
    	#  Demande d'ajout d'un utilisateur dans un set par un utilisateur inscrit  appartenant au set et etant simple membre du set
		users_before = len( SetUtilisateurs.objects.all() )
		response = self.client_registred_member_set.post('/sets/delete_add_user_set/' + str(self.set.id) + '/'  + str(self.user_registred_no_set.id) + '/' )
		users_after = len( SetUtilisateurs.objects.all() )
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_add_user_set_utilisateur_inscrit_wait_set(self):
		""""""
    	#  Demande d'ajout d'un utilisateur dans un set par un utilsateur inscrit  appartenant au set et etant en attente de validation d'entrée dans le set
		users_before = len( SetUtilisateurs.objects.all() )
		response = self.client_registred_wait_set.post('/sets/delete_add_user_set/' + str(self.set.id) + '/'  + str(self.user_registred_no_set.id) + '/' )
		users_after = len( SetUtilisateurs.objects.all() )
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )



		#_____________________________________________


		#_____________________________________________


	def test_sets_add_user_set_user_unactivate(self):
		""""""
    	#   Demande d'ajout d'un utilisateur dans un set par un compte non activé
		users_before = len( SetUtilisateurs.objects.all() )
		response = self.client_unactivate_user.post('/sets/delete_add_user_set/'  + str(self.set.id) + '/'  + str(self.user_registred_no_set.id) + '/' )
		users_after = len( SetUtilisateurs.objects.all() )
		self.assertTrue( users_after == users_before )
		self.assertTrue( response.url == '../../../../user/home/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_add_user_set_user_locked(self):
		""""""
    	#   Demande d'ajout d'un utilisateur dans un set par un compte bloqué
		users_before = len( SetUtilisateurs.objects.all() )
		response = self.client_locked_user.post('/sets/delete_add_user_set/'  + str(self.set.id) + '/'  + str(self.user_registred_no_set.id) + '/' )
		users_after = len( SetUtilisateurs.objects.all() )
		self.assertTrue( users_after == users_before )
		self.assertTrue( response.url == '../../../../user/home/' )
		self.assertTrue( response.status_code == 302 )

	def test_sets_add_user_set_locked(self):
		""""""
    	#   Demande d'ajout d'un utilisateur dans un set fermé
		users_before = len( SetUtilisateurs.objects.all() )
		response = self.client_registred_administrator_set.post('/sets/delete_add_user_set/'  + str(self.set_locked.id) + '/'  + str(self.user_registred_no_set.id) + '/' )
		users_after = len( SetUtilisateurs.objects.all() )
		self.assertTrue( users_after == users_before )
		self.assertTrue( response.url == "../../../../sets/set/" + str(self.set_locked.id) + "/" )
		self.assertTrue( response.status_code == 302 )











	#  ----- Delete user in set


	def test_sets_delete_user_set_utilisateur_non_inscrit(self):
		""""""
		#  Demande de suppression d'un utilisateur dans un set par un utilisateur non inscrit
		users_before = len( SetUtilisateurs.objects.all() )
		response = self.client_not_registred.post('/sets/delete_add_user_set/' + str(self.set.id) + '/'  + str(self.user_registred_member_set.id) + '/' )
		users_after = len( SetUtilisateurs.objects.all() )
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )


	def test_sets_delete_user_set_utilisateur_inscrit_no_set(self):
		""""""
		#  Demande de suppression d'un utilisateur dans un set par un utilsateur inscrit n'appartenant pas au set
		users_before = len( SetUtilisateurs.objects.all() )
		response = self.client_registred_no_set.post('/sets/delete_add_user_set/' + str(self.set.id) + '/'  + str(self.user_registred_member_set.id) + '/' )
		users_after = len( SetUtilisateurs.objects.all() )
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )


	def test_sets_delete_user_set_utilisateur_inscrit_admin_set(self):
		""""""
    	#  Demande de suppression d'un utilisateur dans un set par un utilisateur inscrit  appartenant au set et etant administrateur du set
		users_before = len( SetUtilisateurs.objects.all() )
		response = self.client_registred_administrator_set.post('/sets/delete_add_user_set/'  + str(self.set.id) + '/'  + str(self.user_registred_member_set.id) + '/' )
		users_after = len( SetUtilisateurs.objects.all() )
		self.assertTrue( users_after == ( users_before - 1 ) )
		self.assertTrue( response.content == b'user_deleted' )
		self.assertTrue( response.status_code == 200 )

	def test_sets_delete_user_set_utilisateur_inscrit_admin_set_not_id_set_int(self):
		""""""
    	#  Demande de suppression d'un utilisateur dans un set avec un identifiant set qui n'est pas un nombre entier
		users_before = len( SetUtilisateurs.objects.all() )
		response = self.client_registred_administrator_set.post('/sets/delete_add_user_set/'  + '5000' + '/'  + str(self.user_registred_member_set.id) + '/' )
		users_after = len( SetUtilisateurs.objects.all() )
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_delete_user_set_utilisateur_inscrit_admin_set_not_set_int_appliation(self):
		""""""
    	#  Demande de suppression d'un utilisateur dans un set dont l'identifiant ne correspond à aucun set de l'application
		users_before = len( SetUtilisateurs.objects.all() )
		response = self.client_registred_administrator_set.post('/sets/delete_add_user_set/'  + str(self.set.id) + '/'  + '5000' + '/' )
		users_after = len( SetUtilisateurs.objects.all() )
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_delete_user_set_utilisateur_inscrit_admin_set_not_id_user_int(self):
		""""""
    	#  Demande de suppression d'un utilisateur dans un set avec un identifiant utilisateur qui n'est pas un nombre entier
		users_before = len( SetUtilisateurs.objects.all() )
		response = self.client_registred_administrator_set.post('/sets/delete_add_user_set/'  + '5000' + '/'  + str(self.user_registred_member_set.id) + '/' )
		users_after = len( SetUtilisateurs.objects.all() )
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_delete_user_set_utilisateur_inscrit_admin_set_not_user_in_application(self):
		""""""
    	#  Demande de suppression d'un utilisateur dans un set dont l'identifiant ne correspond à aucun utilisateur du set
		users_before = len( SetUtilisateurs.objects.all() )
		response = self.client_registred_administrator_set.post('/sets/delete_add_user_set/'  + str(self.set.id) + '/'  + '5000' + '/' )
		users_after = len( SetUtilisateurs.objects.all() )
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_delete_user_set_utilisateur_inscrit_user_set(self):
		""""""
    	#  Demande de suppression d'un utilisateur dans un set par un utilisateur inscrit  appartenant au set et etant simple membre du set
		users_before = len( SetUtilisateurs.objects.all() )
		response = self.client_registred_member_set.post('/sets/delete_add_user_set/' + str(self.set.id) + '/'  + str(self.user_registred_no_set.id) + '/' )
		users_after = len( SetUtilisateurs.objects.all() )
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_delete_user_set_utilisateur_inscrit_wait_set(self):
		""""""
    	#  Demande de suppression d'un utilisateur dans un set par un utilsateur inscrit  appartenant au set et etant en attente de validation d'entrée dans le set
		users_before = len( SetUtilisateurs.objects.all() )
		response = self.client_registred_wait_set.post('/sets/delete_add_user_set/' + str(self.set.id) + '/'  + str(self.user_registred_no_set.id) + '/' )
		users_after = len( SetUtilisateurs.objects.all() )
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )




		#_____________________________________________

		#   Demande de suppression d'un utilisateur dans un set par un compte non activé
		#   Demande de suppression d'un utilisateur dans un set par un compte bloqué
		#   Demande de suppression d'un utilisateur dans un set fermé
		#_____________________________________________





	#  ----- Confirmation de l'entrée d'un utilisateur dans un set

	def test_sets_confirmation_enter_user_set_utilisateur_non_inscrit(self):
		""""""
		# Confirmation de l'entrée dans un set par un utilisateur non inscrit
		response = self.client_not_registred.post('/sets/manage_enter_user_set/' + str(self.set.id) + '/?confirm_enter=yes' )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_confirmation_enter_user_set_utilisateur_inscrit_no_set(self):
		""""""
		# Confirmation de l'entrée dans un set par un utilsateur inscrit n'appartenant pas au set
		response = self.client_registred_no_set.post('/sets/manage_enter_user_set/' + str(self.set.id) + '/?confirm_enter=yes' )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_confirmation_enter_user_set_utilisateur_inscrit_admin_set(self):
		""""""
		# Confirmation de l'entrée dans un set par un utilisateur inscrit  appartenant au set et etant administrateur du set
		response = self.client_registred_administrator_set.post('/sets/manage_enter_user_set/' + str(self.set.id) + '/?confirm_enter=yes' )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_confirmation_enter_user_set_utilisateur_inscrit_user_set(self):
		""""""
		# Confirmation de l'entrée dans un set par un utilisateur inscrit  appartenant au set et etant simple membre du set
		response = self.client_registred_member_set.post('/sets/manage_enter_user_set/' + str(self.set.id) + '/?confirm_enter=yes' )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_confirmation_enter_user_set_utilisateur_inscrit_wait_set(self):
		""""""
		# Confirmation de l'entrée dans un set par un utilsateur inscrit  appartenant au set et etant en attente de validation d'entrée dans le set
		self.assertTrue( SetUtilisateurs.objects.get(id=self.set_user_wait.id).statut == 'attente_validation'  )
		response = self.client_registred_wait_set.post('/sets/manage_enter_user_set/' + str(self.set.id) + '/?confirm_enter=yes' )
		self.assertTrue( SetUtilisateurs.objects.get(id=self.set_user_wait.id).statut == 'dans_set'  )
		self.assertTrue(response.content == b'added_done')
		self.assertTrue( response.status_code == 200 )

	def test_sets_confirmation_enter_user_set_utilisateur_inscrit_wait_set(self):
		""""""
		#  Confirmation de l'entrée dans un set par un utilsateur inscrit  appartenant au set et etant en attente de validation d'entrée dans le set avec un identifiant de set qui n'est pas un entier
		self.assertTrue( SetUtilisateurs.objects.get(id=self.set_user_wait.id).statut == 'attente_validation'  )
		response = self.client_registred_wait_set.post('/sets/manage_enter_user_set/' + 'a' + '/?confirm_enter=yes' )
		self.assertTrue( SetUtilisateurs.objects.get(id=self.set_user_wait.id).statut == 'attente_validation'  )
		self.assertTemplateUsed(response, '404.html')

	def test_sets_confirmation_enter_user_set_utilisateur_inscrit_wait_set(self):
		""""""
		#  Confirmation de l'entrée dans un set par un utilsateur inscrit  appartenant au set et etant en attente de validation d'entrée dans le set avec un set qui n'existe pas dans l'application
		self.assertTrue( SetUtilisateurs.objects.get(id=self.set_user_wait.id).statut == 'attente_validation'  )
		response = self.client_registred_wait_set.post('/sets/manage_enter_user_set/' + '5000' + '/?confirm_enter=yes' )
		self.assertTrue( SetUtilisateurs.objects.get(id=self.set_user_wait.id).statut == 'attente_validation'  )
		self.assertTrue( response.status_code == 404 )


	
	

		#_____________________________________________

		#   Confirmation de l'entrée dans un set par un compte non activé
		#   Confirmation de l'entrée dans un set par un compte bloqué
		#   Confirmation de l'entrée dans un set fermé
		#_____________________________________________






	#  ----- Refus de l'entrée d'un utilisateur dans un set

	def test_sets_confirmation_enter_user_set_utilisateur_non_inscrit(self):
		""""""
		# Refus d'entrée dans un set par un utilisateur non inscrit
		response = self.client_not_registred.post('/sets/manage_enter_user_set/' + str(self.set.id) + '/?confirm_enter=no' )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_confirmation_enter_user_set_utilisateur_inscrit_no_set(self):
		""""""
		# Refus d'entrée dans un set par un utilsateur inscrit n'appartenant pas au set
		response = self.client_registred_no_set.post('/sets/manage_enter_user_set/' + str(self.set.id) + '/?confirm_enter=no' )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_confirmation_enter_user_set_utilisateur_inscrit_admin_set(self):
		""""""
		# Refus d'entrée dans un set par un utilisateur inscrit  appartenant au set et etant administrateur du set
		response = self.client_registred_administrator_set.post('/sets/manage_enter_user_set/' + str(self.set.id) + '/?confirm_enter=no' )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_confirmation_enter_user_set_utilisateur_inscrit_user_set(self):
		""""""
		# Refus d'entrée dans un set par un utilisateur inscrit  appartenant au set et etant simple membre du set
		response = self.client_registred_member_set.post('/sets/manage_enter_user_set/' + str(self.set.id) + '/?confirm_enter=no' )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_confirmation_enter_user_set_utilisateur_inscrit_wait_set(self):
		""""""
		# Refus d'entrée dans un set par un utilsateur inscrit  appartenant au set et etant en attente de validation d'entrée dans le set
		self.assertTrue( len(SetUtilisateurs.objects.get(id=self.set_user_wait.id) ) == 1  )
		response = self.client_registred_wait_set.post('/sets/manage_enter_user_set/' + str(self.set.id) + '/?confirm_enter=no' )
		self.assertTrue( len(SetUtilisateurs.objects.filter(id=self.set_user_wait.id)) == 0  )
		self.assertTrue(response.content == b'delete_done')
		self.assertTrue( response.status_code == 200 )

	def test_sets_confirmation_enter_user_set_utilisateur_inscrit_wait_set(self):
		""""""
		#  Refus d'entrée dans un set par un utilsateur inscrit  appartenant au set et etant en attente de validation d'entrée dans le set avec un identifiant de set qui n'est pas un entier
		self.assertTrue( SetUtilisateurs.objects.get(id=self.set_user_wait.id).statut == 'attente_validation'  )
		response = self.client_registred_wait_set.post('/sets/manage_enter_user_set/' + 'a' + '/?confirm_enter=no' )
		self.assertTrue( SetUtilisateurs.objects.get(id=self.set_user_wait.id).statut == 'attente_validation'  )
		self.assertTemplateUsed(response, '404.html')

	def test_sets_confirmation_enter_user_set_utilisateur_inscrit_wait_set(self):
		""""""
		#  Refus d'entrée dans un set par un utilsateur inscrit  appartenant au set et etant en attente de validation d'entrée dans le set avec un set qui n'existe pas dans l'application
		self.assertTrue( SetUtilisateurs.objects.get(id=self.set_user_wait.id).statut == 'attente_validation'  )
		response = self.client_registred_wait_set.post('/sets/manage_enter_user_set/' + '5000' + '/?confirm_enter=no' )
		self.assertTrue( SetUtilisateurs.objects.get(id=self.set_user_wait.id).statut == 'attente_validation'  )
		self.assertTrue( response.status_code == 404 )




		#_____________________________________________

		#   Refus d'entrée dans un set par un compte non activé
		#   Refus d'entrée dans un set par un compte bloqué
		#   Refus d'entrée dans un set fermé
		#_____________________________________________





	#  ----- Sortie d'un utilisateur dans un set

	def test_sets_exit_user_set_utilisateur_non_inscrit(self):
		""""""
		#  sortie d'un utilisateur dans un set par un utilisateur non inscrit
		response = self.client_not_registred.post('/sets/exit_set/' + str(self.set.id) + '/')
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_exit_user_set_utilisateur_inscrit_no_set(self):
		""""""
		#  sortie d'un utilisateur dans un set par un utilsateur inscrit n'appartenant pas au set
		response = self.client_registred_no_set.post('/sets/exit_set/' + str(self.set.id) + '/' )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_exit_user_set_utilisateur_inscrit_admin_set(self):
		""""""
		#  sortie d'un utilisateur dans un set par un utilisateur inscrit  appartenant au set et etant administrateur du set
		users_before = len(SetUtilisateurs.objects.all())
		response = self.client_registred_administrator_set.post('/sets/exit_set/' + str(self.set.id) + '/' )
		users_after = len(SetUtilisateurs.objects.all())
		self.assertTrue( users_after == users_before - 1 )
		self.assertTrue( response.content == b'delete_done' )
		self.assertTrue( response.status_code == 200 )

	def test_sets_exit_user_set_utilisateur_inscrit_user_set(self):
		""""""
		#  sortie d'un utilisateur dans un set par un utilisateur inscrit  appartenant au set et etant simple membre du set
		users_before = len(SetUtilisateurs.objects.all())
		response = self.client_registred_member_set.post('/sets/exit_set/' + str(self.set.id) + '/' )
		users_after = len(SetUtilisateurs.objects.all())
		self.assertTrue( users_after == users_before - 1 )
		self.assertTrue( response.content == b'delete_done' )
		self.assertTrue( response.status_code == 200 )

	def test_sets_exit_user_set_utilisateur_inscrit_user_set_not_int_id(self):
		""""""
		#  sortie d'un utilisateur dans un set par un utilisateur inscrit appartenant au set et etant simple membre du set avec un id de set non entier
		users_before = len(SetUtilisateurs.objects.all())
		self.assertTrue( len(SetUtilisateurs.objects.filter(id=self.set_user_wait.id) ) == 1  )
		response = self.client_registred_member_set.post('/sets/exit_set/' + 'a' + '/' )
		users_after = len(SetUtilisateurs.objects.all())
		self.assertTrue( users_after == users_before  )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_exit_user_set_utilisateur_inscrit_user_set_no_set_in_application(self):
		""""""
		#  sortie d'un utilisateur dans un set par un utilisateur inscrit  appartenant au set et etant simple membre du set avec un id de set qui ne correspond à aucun set dans l'application
		users_before = len(SetUtilisateurs.objects.all())
		self.assertTrue( len(SetUtilisateurs.objects.filter(id=self.set_user_wait.id) ) == 1  )
		response = self.client_registred_member_set.post('/sets/exit_set/' + '5000' + '/' )
		users_after = len(SetUtilisateurs.objects.all())
		self.assertTrue( users_after == users_before )
		self.assertTemplateUsed(response, '404.html')
		self.assertTrue( response.status_code == 404 )

	def test_sets_exit_user_set_utilisateur_inscrit_user_set_last_user_set(self):
		""""""
		#  sortie d'un utilisateur dans un set par un utilisateur inscrit appartenant au set etant admministrateur et dernier membre du set
		users_before = len(SetUtilisateurs.objects.all())
		self.assertTrue( len(SetUtilisateurs.objects.filter(id=self.set_user_wait.id) ) == 1  )
		response0 = self.client_registred_member_set.post('/sets/exit_set/' + str(self.set.id) + '/' )
		response1 = self.client_registred_wait_set.post('/sets/exit_set/' + str(self.set.id) + '/' )
		response2 = self.client_registred_administrator_set.post('/sets/exit_set/' + str(self.set.id) + '/' )
		users_after = len(SetUtilisateurs.objects.all())
		self.assertTrue( users_after == users_before - 3 )
		self.assertTrue( len(SetUtilisateurs.objects.filter(set0=self.set)) == 0 )
		self.assertTrue( response0.content == b'delete_done' )
		self.assertTrue( response1.content == b'delete_done' )
		self.assertTrue( response2.content == b'delete_done_and_set_delete_done' )
		self.assertTrue( response0.status_code == 200 )
		self.assertTrue( response1.status_code == 200 )
		self.assertTrue( response2.status_code == 200 )

	def test_sets_exit_user_set_utilisateur_inscrit_wait_set(self):
		""""""
		#  sortie d'un utilisateur dans un set par un utilsateur inscrit  appartenant au set et etant en attente de validation d'entrée dans le set
		users_before = len(SetUtilisateurs.objects.all())
		self.assertTrue( len(SetUtilisateurs.objects.filter(id=self.set_user_wait.id) ) == 1  )
		response = self.client_registred_wait_set.post('/sets/exit_set/' + str(self.set.id) + '/' )
		users_after = len(SetUtilisateurs.objects.all())
		self.assertTrue( users_after == users_before - 1 )
		self.assertTrue( response.content == b'delete_done' )
		self.assertTrue( response.status_code == 200 )





		#_____________________________________________

		#   sortie d'un utilisateur dans un set par un compte non activé
		#   sortie d'un utilisateur dans un set par un compte bloqué
		#   sortie d'un utilisateur dans un set fermé
		#_____________________________________________





