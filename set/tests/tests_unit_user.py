""""""


import os



from django.test import TestCase, RequestFactory, Client
from user.models import *

class TestsVueUser(TestCase):
    
    def setUp(self):
        """"""
        self.client_0 = Client()
        self.client_1 = Client()
        self.client_unactivate_user = Client()
        self.client_locked_user = Client()
        #self.client_2 = Client()
        #self.client_3 = Client()

        #self.user_0 = Utilisateurs.objects.create(nom="user_0", adresse_mail="user_0@mail.mail", mot_de_passe='user_0')
        self.user_1 = Utilisateurs.objects.create(nom="user_1", adresse_mail="user_1@mail.mail", mot_de_passe='user_1', statut_activation_compte=True)
        self.user_2 = Utilisateurs.objects.create(nom="user_2", adresse_mail="user_2@mail.mail", mot_de_passe='user_2', statut_activation_compte=True)
        self.user_3 = Utilisateurs.objects.create(nom="user_3", adresse_mail="user_3@mail.mail", mot_de_passe='user_3', statut_activation_compte=True)
        self.unactivate_user = Utilisateurs.objects.create(nom="unactivate_user", adresse_mail="unactivate_user@mail.mail", mot_de_passe='unactivate_user', )
        self.locked_user = Utilisateurs.objects.create(nom="locked_user", adresse_mail="locked_user@mail.mail", mot_de_passe='locked_user', statut_blocage_admin=True, statut_activation_compte=True)

        self.contact_user2_for_user1 = Contact.objects.create(contact_owner=self.user_1, contact=self.user_2)
        self.contact_user2_for_unactivate_user = Contact.objects.create(contact_owner=self.unactivate_user, contact=self.user_2)
        self.contact_user2_for_locked_user = Contact.objects.create(contact_owner=self.locked_user, contact=self.user_2)

        self.message_from_user2_to_user1 = Message.objects.create(which_from=self.user_2, which_to=self.user_1, contenu_text='contenu_text_message')
        self.message_from_user2_to_unactivate_user = Message.objects.create(which_from=self.user_2, which_to=self.unactivate_user, contenu_text='contenu_text_message')
        self.message_from_user2_to_locked_user = Message.objects.create(which_from=self.user_2, which_to=self.locked_user, contenu_text='contenu_text_message')

        #self.client_registred_no_set.post('/authentification/connexion/', {'email':'user_registred_no_set@mail.mail', 'password':'user_registred_no_set_password'})
        self.client_1.post('/authentification/connexion/', {'email':'user_1@mail.mail', 'password':'user_1'})
        self.client_unactivate_user.post('/authentification/connexion/', {'email':'unactivate_user@mail.mail', 'password':'unactivate_user'})
        self.client_locked_user.post('/authentification/connexion/', {'email':'locked_user@mail.mail', 'password':'locked_user'})
        #self.client_2.post('/authentification/connexion/', {'email':'user_2@mail.mail', 'password':'user_2'})






    #   -----   Page d'acceuil

    def test_consultation_acceuil_user_connected(self):
        """  Consultation de l'acceuil pour un utilisateur connecté  """
        response = self.client_1.get('/user/home/')
        self.assertTemplateUsed( response, 'acceuil.html')
        self.assertTrue( response.status_code == 200 )

    def test_consultation_acceuil_user_not_connected(self):
        """  Consultation de l'acceuil pour un utilisateur non connecté  """
        response = self.client_0.get('/user/home/')
        self.assertEqual(response.url, '../authentification/connexion/')
        self.assertEqual(response.status_code, 302)

    def test_consultation_acceuil_user_unactivate(self):
        """  Consultation de l'acceuil pour un utilisateur desactivé  """
        response = self.client_unactivate_user.get('/user/home/')
        self.assertTemplateUsed( response, 'compte_inactif.html')
        self.assertTrue( response.status_code == 200 )

    def test_consultation_acceuil_user_locked(self):
        """  Consultation de l'acceuil pour un compte fermé  """
        response = self.client_locked_user.get('/user/home/')
        self.assertTemplateUsed( response, 'compte_ferme.html')
        self.assertTrue( response.status_code == 200 )



    #   -----   Ajout de contact

    def test_manage_contact_ajout_contact_user_connected(self):
    	"""  Ajout d'un contact pour un utilisateur connecté  """
    	contacts_before = len( Contact.objects.filter(contact_owner=self.user_1) )
    	response = self.client_1.get('/user/manage_contact/' + str(self.user_3.id) + '/' )
    	contacts_after = len( Contact.objects.filter(contact_owner=self.user_1) )
    	self.assertTrue( contacts_after == contacts_before + 1 )
    	self.assertTrue( response.content == b'contact_added' )
    	self.assertTrue( response.status_code == 200 )

    def test_manage_contact_ajout_contact_user_not_connected(self):
    	"""  Ajout d'un contact pour un utilisateur non connecté  """
    	contacts_before = len( Contact.objects.all() )
    	response = self.client_0.get('/user/manage_contact/' + str(self.user_3.id) + '/' )
    	contacts_after = len( Contact.objects.all() )
    	self.assertTrue( contacts_after == contacts_before )
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_manage_contact_ajout_contact_user_connected_not_id_contact_int(self):
    	"""  Ajout d'un contact pour un utilisateur connecté avec un id de contact qui n'est pas entier """
    	contacts_before = len( Contact.objects.all() )
    	response = self.client_1.get('/user/manage_contact/' + 'a' + '/' )
    	contacts_after = len( Contact.objects.all() )
    	self.assertTrue( contacts_after == contacts_before )
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_manage_contact_ajout_contact_user_connected_no_contact_in_application(self):
    	"""  Ajout d'un contact pour un utilisateur connecté avec un id de contact qui ne correspond à aucun utilisateur dans l'application """
    	contacts_before = len( Contact.objects.all() )
    	response = self.client_1.get('/user/manage_contact/' + '5000' + '/' )
    	contacts_after = len( Contact.objects.all() )
    	self.assertTrue( contacts_after == contacts_before )
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_manage_contact_ajout_contact_user_unactivate(self):
        """  Ajout d'un contact pour un utilisateur désactivé  """
        contacts_before = len( Contact.objects.filter(contact_owner=self.unactivate_user) )
        response = self.client_unactivate_user.get('/user/manage_contact/' + str(self.user_3.id) + '/' )
        contacts_after = len( Contact.objects.filter(contact_owner=self.unactivate_user) )
        self.assertTrue( contacts_after == contacts_before )
        self.assertTrue( response.content == b'account_unactivate' )
        self.assertTrue( response.status_code == 200 )

    def test_manage_contact_ajout_contact_user_locked(self):
        """  Ajout d'un contact pour un utilisateur fermé  """
        contacts_before = len( Contact.objects.filter(contact_owner=self.locked_user) )
        response = self.client_locked_user.get('/user/manage_contact/' + str(self.user_3.id) + '/' )
        contacts_after = len( Contact.objects.filter(contact_owner=self.locked_user) )
        self.assertTrue( contacts_after == contacts_before )
        self.assertTrue( response.content == b'account_locked' )
        self.assertTrue( response.status_code == 200 )



    #   -----   suppression de contact

    def test_manage_contact_suppression_contact_user_connected(self):
    	"""  Suppression d'un contact pour un utilisateur connecté  """
    	contacts_before = len( Contact.objects.filter(contact_owner=self.user_1) )
    	response = self.client_1.get('/user/manage_contact/' + str(self.user_2.id) + '/' )
    	contacts_after = len( Contact.objects.filter(contact_owner=self.user_1) )
    	self.assertTrue( contacts_after == contacts_before - 1 )
    	self.assertTrue( response.content == b'contact_deleted' )
    	self.assertTrue( response.status_code == 200 )

    def test_manage_contact_suppression_contact_user_not_connected(self):
    	"""  Suppression d'un contact pour un utilisateur non connecté  """
    	contacts_before = len( Contact.objects.all() )
    	response = self.client_0.get('/user/manage_contact/' + str(self.user_2.id) + '/' )
    	contacts_after = len( Contact.objects.all() )
    	self.assertTrue( contacts_after == contacts_before )
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_manage_contact_suppression_contact_user_connected_not_id_contact_int(self):
    	"""  Suppression d'un contact pour un utilisateur connecté avec un id de contact qui n'est pas entier """
    	contacts_before = len( Contact.objects.all() )
    	response = self.client_1.get('/user/manage_contact/' + 'a' + '/' )
    	contacts_after = len( Contact.objects.all() )
    	self.assertTrue( contacts_after == contacts_before )
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_manage_contact_suppression_contact_user_connected_no_contact_in_application(self):
    	"""  Suppression d'un contact pour un utilisateur connecté avec un id de contact qui ne correspond à aucun utilisateur dans l'application """
    	contacts_before = len( Contact.objects.all() )
    	response = self.client_1.get('/user/manage_contact/' + '5000' + '/' )
    	contacts_after = len( Contact.objects.all() )
    	self.assertTrue( contacts_after == contacts_before )
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_manage_contact_suppression_contact_user_unactivate(self):
        """  Suppression d'un contact pour un compte desactivé  """
        contacts_before = len( Contact.objects.filter(contact_owner=self.unactivate_user) )
        response = self.client_unactivate_user.get('/user/manage_contact/' + str(self.user_2.id) + '/' )
        contacts_after = len( Contact.objects.filter(contact_owner=self.unactivate_user) )
        self.assertTrue( contacts_after == contacts_before )
        self.assertTrue( response.content == b'account_unactivate' )
        self.assertTrue( response.status_code == 200 )

    def test_manage_contact_suppression_contact_user_locked(self):
        """  Suppression d'un contact pour un compte fermé  """
        contacts_before = len( Contact.objects.filter(contact_owner=self.locked_user) )
        response = self.client_locked_user.get('/user/manage_contact/' + str(self.user_2.id) + '/' )
        contacts_after = len( Contact.objects.filter(contact_owner=self.locked_user) )
        self.assertTrue( contacts_after == contacts_before )
        self.assertTrue( response.content == b'account_locked' )
        self.assertTrue( response.status_code == 200 )





    #   ----   Consultation de contacts

    def test_consultation_contact_user_connected(self):
    	"""  Consultation de contacts pour un utilisateur connecté  """
    	response = self.client_1.get('/user/contacts/')
    	self.assertTemplateUsed( response, 'contact.html')
    	self.assertTrue( response.status_code == 200 )

    def test_consultation_contact_user_not_connected(self):
    	"""  Consultation de contacts pour un utilisateur non connecté  """
    	response = self.client_0.get('/user/contacts/')
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_consultation_contact_user_unactivate(self):
        """  Consultation de contacts pour un utilisateur desactivé  """
        response = self.client_unactivate_user.get('/user/contacts/')
        self.assertEqual(response.url, '../home/')
        self.assertEqual(response.status_code, 302)

    def test_consultation_contact_user_locked(self):
        """  Consultation de contacts pour un compte fermé  """
        response = self.client_locked_user.get('/user/contacts/')
        self.assertEqual(response.url, '../home/')
        self.assertEqual(response.status_code, 302)


    #   ----   Consultation de messages

    def test_consultation_messages_user_connected(self):
    	"""  Consultation de m€ssages pour un utilisateur connecté  """
    	response = self.client_1.get('/user/messages/')
    	self.assertTemplateUsed( response, 'message.html')
    	self.assertTrue( response.status_code == 200 )

    def test_consultation_messages_user_not_connected(self):
    	"""  Consultation de m€ssages pour un utilisateur non connecté  """
    	response = self.client_0.get('/user/messages/')
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_consultation_messages_user_unactivate(self):
        """  Consultation de messages pour un utilisateur desactivé  """
        response = self.client_unactivate_user.get('/user/messages/')
        self.assertEqual(response.url, '../home/')
        self.assertEqual(response.status_code, 302)

    def test_consultation_messages_user_locked(self):
        """  Consultation de messages pour un compte fermé  """
        response = self.client_locked_user.get('/user/messages/')
        self.assertEqual(response.url, '../home/')
        self.assertEqual(response.status_code, 302)





    #   -----   Consultation des messages échangés

    def test_messages_exchanges_user_connected(self):
    	""" Consultaion des messages échangés pour un utilisateur connecté  """
    	response = self.client_1.get('/user/messages_exchanges/' + str(self.user_2.id) + '/' )
    	self.assertTemplateUsed( response, 'message_exchange.html')
    	self.assertTrue( response.status_code == 200 )

    def test_messages_exchanges_user_connected_with_self(self):
    	""" Consultaion des messages échangés pour un utilisateur connecté avec le correspondant égal à l'utilisateur  """
    	response = self.client_1.get('/user/messages_exchanges/' + str(self.user_1.id) + '/' )
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_messages_exchanges_user_not_connected(self):
    	""" Consultaion des messages échangés pour un utilisateur non connecté  """
    	response = self.client_0.get('/user/messages_exchanges/' + str(self.user_2.id) + '/' )
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_messages_exchanges_user_connected_not_id_correspondant_int(self):
    	""" Consultaion des messages échangés pour un utilisateur connecté avec un id de coreespondant qui n'est pas entier """
    	response = self.client_1.get('/user/messages_exchanges/' + 'a' + '/' )
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_messages_exchanges_user_connected_no_correspondant_in_application(self):
    	""" Consultaion des messages échangés pour un utilisateur connecté avec un id de coreespondant qui ne correspond à aucun utilisateur dans l'application """
    	response = self.client_1.get('/user/messages_exchanges/' + '5000' + '/' )
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_messages_exchanges_user_unactivate(self):
        """  Consultation de messages échangés pour un utilisateur desactivé  """
        response = self.client_unactivate_user.get('/user/messages_exchanges/' + str(self.user_1.id) + '/' )
        self.assertEqual(response.url, '../../../user/home/')
        self.assertEqual(response.status_code, 302)

    def test_messages_exchanges_user_locked(self):
        """  Consultation de messages échangés pour un compte fermé  """
        response = self.client_locked_user.get('/user/messages_exchanges/' + str(self.user_1.id) + '/' )
        self.assertEqual(response.url, '../../../user/home/')
        self.assertEqual(response.status_code, 302)



    #   -----   Envoie de messages

    def test_send_messages_user_connected(self):
    	""" Envoie de messages pour un utilisateur connecté  """
    	messages_before = len( Message.objects.all() )
    	response = self.client_1.get('/user/send_message/' + str(self.user_2.id) + '/?message_text=hello' )
    	messages_after = len( Message.objects.all() )
    	self.assertTrue( messages_after == messages_before + 1 )
    	self.assertTrue( response.content == b'send')
    	self.assertTrue( response.status_code == 200 )

    def test_send_messages_user_connected_with_self(self):
    	""" Envoie de messages pour un utilisateur connecté avec le correspondant égal à l'utilisateur  """
    	messages_before = len( Message.objects.all() )
    	response = self.client_1.get('/user/send_message/' + str(self.user_1.id) + '/?message_text=hello' )
    	messages_after = len( Message.objects.all() )
    	self.assertTrue( messages_after == messages_before )
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_send_messages_user_not_connected(self):
    	""" Envoie de messages pour un utilisateur non connecté  """
    	messages_before = len( Message.objects.all() )
    	response = self.client_0.get('/user/send_message/' + str(self.user_2.id) + '/?message_text=hello' )
    	messages_after = len( Message.objects.all() )
    	self.assertTrue( messages_after == messages_before )
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_send_messages_user_connected_not_id_correspondant_int(self):
    	""" Envoie de messages pour un utilisateur connecté avec un id de coreespondant qui n'est pas entier """
    	messages_before = len( Message.objects.all() )
    	response = self.client_1.get('/user/send_message/' + 'a' + '/?message_text=hello' )
    	messages_after = len( Message.objects.all() )
    	self.assertTrue( messages_after == messages_before )
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_send_messages_user_connected_no_correspondant_in_application(self):
    	""" Envoie de messages pour un utilisateur connecté avec un id de coreespondant qui ne correspond à aucun utilisateur dans l'application """
    	messages_before = len( Message.objects.all() )
    	response = self.client_1.get('/user/send_message/' + '5000' + '/?message_text=hello' )
    	messages_after = len( Message.objects.all() )
    	self.assertTrue( messages_after == messages_before )
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_send_messages_user_unactivate(self):
        """   Envoie de messages pour un utilisateur desactivé  """
        response = self.client_unactivate_user.get('/user/send_message/' + str(self.user_2.id) + '/?message_text=hello' )
        self.assertTrue( response.content == b'account_unactivate' )
        self.assertEqual(response.status_code, 200)

    def test_send_messages_user_locked(self):
        """   Envoie de messages pour un compte fermé  """
        response = self.client_locked_user.get('/user/send_message/' + str(self.user_2.id) + '/?message_text=hello' )
        self.assertTrue( response.content == b'account_locked' )
        self.assertEqual(response.status_code, 200)






    #   -----   Mise à jour des messages échangés

    def test_updates_messages_user_connected(self):
    	""" Mises à jour de messages pour un utilisateur connecté  """
    	response = self.client_1.get('/user/updates_messages_user/' + str(self.user_2.id) + '/?last_message_id=' + str(self.message_from_user2_to_user1.id) )
    	self.assertTemplateUsed( response, 'un_message.html')
    	self.assertTrue( response.status_code == 200 )

    def test_updates_messages_user_connected_with_self(self):
    	""" Mises à jour de messages pour un utilisateur connecté avec le correspondant égal à l'utilisateur  """
    	response = self.client_1.get('/user/updates_messages_user/' + str(self.user_1.id) + '/?last_message_id=' + str(self.message_from_user2_to_user1.id) )
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_updates_messages_user_not_connected(self):
    	""" Mises à jour de messages pour un utilisateur non connecté  """
    	response = self.client_0.get('/user/updates_messages_user/' + str(self.user_2.id) + '/?last_message_id=' + str(self.message_from_user2_to_user1.id) )
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_updates_messages_user_connected_not_id_correspondant_int(self):
    	""" Mises à jour de messages pour un utilisateur connecté avec un id de coreespondant qui n'est pas entier """
    	response = self.client_1.get('/user/updates_messages_user/' + 'a' + '/?last_message_id=' + str(self.message_from_user2_to_user1.id) )
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_updates_messages_user_connected_no_correspondant_in_application(self):
    	""" Mises à jour de messages pour un utilisateur connecté avec un id de correspondant qui ne correspond à aucun utilisateur dans l'application """
    	response = self.client_1.get('/user/updates_messages_user/' + '5000' + '/?last_message_id=' + str(self.message_from_user2_to_user1.id) )
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_updates_messages_user_connected_not_id_last_message_int(self):
    	""" Mises à jour de messages pour un utilisateur connecté avec un id de coreespondant qui n'est pas entier """
    	response = self.client_1.get('/user/updates_messages_user/' + str(self.user_2.id) +  '/?last_message_id=' + 'a' )
    	self.assertTemplateUsed( response, 'un_message.html')
    	self.assertTrue( response.status_code == 200 )

    def test_updates_messages_user_connected_no_last_message_in_application(self):
    	""" Mises à jour de messages pour un utilisateur connecté avec un id de coreespondant qui ne correspond à aucun utilisateur dans l'application """
    	response = self.client_1.get('/user/updates_messages_user/' + str(self.user_2.id) +  '/?last_message_id=' + '0' )
    	self.assertTemplateUsed( response, 'un_message.html')
    	self.assertTrue( response.status_code == 200 )

    def test_update_messages_user_unactivate(self):
        """   Mises à jour de messages pour un utilisateur desactivé  """
        response = self.client_unactivate_user.get('/user/updates_messages_user/' + str(self.user_2.id) + '/?last_message_id=' + str(self.message_from_user2_to_unactivate_user.id) )
        self.assertTrue( response.content == b'account_unactivate' )
        self.assertEqual(response.status_code, 200)

    def test_update_messages_user_locked(self):
        """   Mises à jour de messages pour un compte fermé  """
        response = self.client_locked_user.get('/user/updates_messages_user/' + str(self.user_2.id) + '/?last_message_id=' + str(self.message_from_user2_to_locked_user.id) )
        self.assertTrue( response.content == b'account_locked' )
        self.assertEqual(response.status_code, 200)



    #   -----   Consultation des sets d'un profil

    def test_consultation_sets_profil_user_connected(self):
    	""" Consultation des sets d'un profil par un utilisateur connecté  """
    	response = self.client_1.get('/user/profil/' + str(self.user_2.id) + '/?section_profil=sets' )
    	self.assertTemplateUsed( response, 'profil.html')
    	self.assertTrue( response.status_code == 200 )

    def test_consultation_sets_profil_user_connected_with_self(self):
    	""" Consultation des sets d'un profil par un utilisateur connecté avec le correspondant égal à l'utilisateur  """
    	response = self.client_1.get('/user/profil/' + str(self.user_1.id) + '/?section_profil=sets' )
    	self.assertTemplateUsed( response, 'profil.html')
    	self.assertTrue( response.status_code == 200 )

    def test_consultation_sets_profil_user_not_connected(self):
    	""" Consultation des sets d'un profil par un utilisateur non connecté  """
    	response = self.client_0.get('/user/profil/' + str(self.user_2.id) + '/?section_profil=sets' )
    	self.assertTemplateUsed( response, 'profil.html')
    	self.assertTrue( response.status_code == 200 )

    def test_consultation_sets_profil_user_connected_not_id_correspondant_int(self):
    	""" Consultation des sets d'un profil par un utilisateur connecté avec un id de coreespondant qui n'est pas entier """
    	response = self.client_1.get('/user/profil/' + 'a' + '/?section_profil=sets' )
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_consultation_sets_profil_user_connected_no_correspondant_in_application(self):
    	""" Consultation des sets d'un profil par un utilisateur connecté avec un id de coreespondant qui ne correspond à aucun utilisateur dans l'application """
    	response = self.client_1.get('/user/profil/' + '5000' + '/?section_profil=sets' )
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_consultation_sets_profil_user_unactivate(self):
        """   Consultation des sets d'un profil pour un utilisateur desactivé  """
        response = self.client_unactivate_user.get('/user/profil/' + str(self.user_2.id) + '/?section_profil=sets' )
        self.assertEqual(response.url, '../../home/')
        self.assertEqual(response.status_code, 302)

    def test_consultation_sets_profil_user_locked(self):
        """   Consultation des sets d'un profil pour un compte fermé  """
        response = self.client_locked_user.get('/user/profil/' + str(self.user_2.id) + '/?section_profil=sets' )
        self.assertEqual(response.url, '../../home/')
        self.assertEqual(response.status_code, 302)



    #   -----   Consultation d'un profil avec une section autre que set ou coordonne

    def test_consultation_profil_autre_section_user_connected(self):
    	""" Consultation d'un profil avec une section autre que set ou coordonne par un utilisateur connecté avec un id de coreespondant qui n'est pas entier """
    	response = self.client_1.get('/user/profil/' + str(self.user_2.id) +  '/?section_profil=aaa')
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_consultation_profil_autre_section_user_connected_with_self(self):
    	""" Consultation d'un profil avec une section autre que set ou coordonne par un utilisateur connecté avec un id de coreespondant qui ne correspond à aucun utilisateur dans l'application """
    	response = self.client_1.get('/user/profil/' + str(self.user_2.id) +  '/?section_profil=aaa')
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_consultation_profil_autre_section_user_not_connected_(self):
    	""" Consultation d'un profil avec une section autre que set ou coordonne par un utilisateur connecté avec un id de coreespondant qui ne correspond à aucun utilisateur dans l'application """
    	response = self.client_1.get('/user/profil/' + str(self.user_2.id) +  '/?section_profil=aaa')
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_consultation_profil_autre_section_profil_user_unactivate(self):
        """ Consultation d'un profil avec une section autre que set ou coordonne par un utilisateur connecté  """
        response = self.client_unactivate_user.get('/user/profil/' + str(self.user_2.id) + '/?section_profil=aaa' )
        self.assertEqual(response.url, '../../home/')
        self.assertEqual(response.status_code, 302)

    def test_consultation_profil_autre_section_profil_user_locked(self):
        """ Consultation d'un profil avec une section autre que set ou coordonne par un utilisateur connecté  """
        response = self.client_locked_user.get('/user/profil/' + str(self.user_2.id) + '/?section_profil=aaa' )
        self.assertEqual(response.url, '../../home/')
        self.assertEqual(response.status_code, 302)


    #   -----   Consultation des coordonnés d'un profil

    def test_consultation_coordonnees_profil_user_connected(self):
    	""" Consultation des coordonnés d'un profil par un utilisateur connecté  """
    	response = self.client_1.get('/user/profil/' + str(self.user_2.id) + '/?section_profil=coordonees' )
    	self.assertTemplateUsed( response, 'profil.html')
    	self.assertTrue( response.status_code == 200 )

    def test_consultation_coordonnees_profil_user_connected_with_self(self):
    	""" Consultation des coordonnés d'un profil par un utilisateur connecté avec le correspondant égal à l'utilisateur  """
    	response = self.client_1.get('/user/profil/' + str(self.user_1.id) + '/?section_profil=coordonees' )
    	self.assertTemplateUsed( response, 'profil.html')
    	self.assertTrue( response.status_code == 200 )

    def test_consultation_coordonnees_profil_user_not_connected(self):
    	""" Consultation des coordonnés d'un profil par un utilisateur non connecté  """
    	response = self.client_0.get('/user/profil/' + str(self.user_2.id) + '/?section_profil=coordonees' )
    	self.assertTemplateUsed( response, 'profil.html')
    	self.assertTrue( response.status_code == 200 )

    def test_consultation_coordonnees_profil_user_connected_not_id_correspondant_int(self):
    	""" Consultation des coordonnés d'un profil par un utilisateur connecté avec un id de coreespondant qui n'est pas entier """
    	response = self.client_1.get('/user/profil/' + 'a' + '/?section_profil=coordonees' )
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_consultation_coordonnees_profil_user_connected_no_correspondant_in_application(self):
    	""" Consultation des coordonnés d'un profil par un utilisateur connecté avec un id de coreespondant qui ne correspond à aucun utilisateur dans l'application """
    	response = self.client_1.get('/user/profil/' + '5000' + '/?section_profil=coordonees' )
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_consultation_coordonnees_profil_user_unactivate(self):
        """ Consultation des coordonnés d'un profil par un utilisateur désactivé  """
        response = self.client_unactivate_user.get('/user/profil/' + str(self.user_2.id) + '/?section_profil=coordonees' )
        self.assertEqual(response.url, '../../home/')
        self.assertEqual(response.status_code, 302)

    def test_consultation_coordonnees_profil_user_locked(self):
        """ Consultation des coordonnés d'un profil par un compte fermé  """
        response = self.client_locked_user.get('/user/profil/' + str(self.user_2.id) + '/?section_profil=coordonees' )
        self.assertEqual(response.url, '../../home/')
        self.assertEqual(response.status_code, 302)


    #   ----   Mise à jour de l'image de couverture

    def test_update_image_profil_user_connected(self):
    	"""  Mise à jour de l'image de couverture pour un utilisateur connecté  """
    	image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
    	self.assertTrue( Utilisateurs.objects.get(id=self.user_1.id).image_profil == '' )
    	response = self.client_1.post('/user/update_image_cover/', { 'file': image })
    	self.assertTrue( response.url == "../../user/profil/" + str(self.user_1.id) + "/?section_profil=coordonees" )
    	self.assertTrue( Utilisateurs.objects.get(id=self.user_1.id).image_profil != '' )
    	self.assertTrue( response.status_code == 302 )

    def test_update_image_profil_user_connected_invalid_form(self):
    	"""  Mise à jour de l'image de couverture pour un utilisateur connecté avec un formulaire invalide  """
    	image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
    	self.assertTrue( Utilisateurs.objects.get(id=self.user_1.id).image_profil == '' )
    	response = self.client_1.post('/user/update_image_cover/', { 'file': '' })
    	self.assertTrue( Utilisateurs.objects.get(id=self.user_1.id).image_profil == '' )
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_update_image_profil_user_not_connected(self):
    	"""  Mise à jour de l'image de couverture pour un utilisateur non connecté  """
    	image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
    	response = self.client_0.post('/user/update_image_cover/', { 'file': image })
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_update_image_profil_user_unactivate(self):
        """ Mise à jour de l'image de couverture par un utilisateur connecté  """
        self.assertTrue( Utilisateurs.objects.get(id=self.unactivate_user.id).image_profil == '' )
        image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
        response = self.client_unactivate_user.post('/user/update_image_cover/', { 'file': image })
        self.assertTrue( Utilisateurs.objects.get(id=self.unactivate_user.id).image_profil == '' )
        self.assertEqual(response.url, '../../home/')
        self.assertEqual(response.status_code, 302)

    def test_update_image_profil_user_locked(self):
        """ Mise à jour de l'image de couverture par un utilisateur connecté  """
        self.assertTrue( Utilisateurs.objects.get(id=self.locked_user.id).image_profil == '' )
        image = open(os.path.join(os.getcwd(), "tests/test.png"), 'rb')
        response = self.client_locked_user.post('/user/update_image_cover/', { 'file': image })
        self.assertTrue( Utilisateurs.objects.get(id=self.locked_user.id).image_profil == '' )
        self.assertEqual(response.url, '../../home/')
        self.assertEqual(response.status_code, 302)



    #   ----   Mise à jour du nom d'un profil

    def test_name_profil_user_connected(self):
    	"""  Mise à jour du nom d'un profil pour un utilisateur connecté  """
    	self.assertTrue( Utilisateurs.objects.get(id=self.user_1.id).nom == 'user_1' )
    	response = self.client_1.post('/user/update_profil_name/', { 'name': 'nouveau_user_1' })
    	self.assertTrue( response.url == "../../user/profil/" + str(self.user_1.id) + "/?section_profil=coordonees" )
    	self.assertTrue( Utilisateurs.objects.get(id=self.user_1.id).nom == 'nouveau_user_1' )
    	self.assertTrue( response.status_code == 302 )

    def test_name_profil_user_connected_invalid_form(self):
    	"""  Mise à jour du nom d'un profil pour un utilisateur connecté avec un formulaire invalide  """
    	self.assertTrue( Utilisateurs.objects.get(id=self.user_1.id).nom == 'user_1' )
    	response = self.client_1.post('/user/update_profil_name/', { 'name': '' })
    	self.assertTrue( Utilisateurs.objects.get(id=self.user_1.id).nom == 'user_1' )
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_name_profil_user_not_connected(self):
    	"""  Mise à jour du nom d'un profil pour un utilisateur non connecté  """
    	response = self.client_0.post('/user/update_profil_name/', { 'name': 'nouveau_user_1' })
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_name_profil_user_unactivate(self):
        """  Mise à jour du nom d'un profil pour un utilisateur desactivé  """
        self.assertTrue( Utilisateurs.objects.get(id=self.unactivate_user.id).nom == 'unactivate_user' )
        response = self.client_unactivate_user.post('/user/update_profil_name/', { 'name': 'nouveau' })
        self.assertTrue( Utilisateurs.objects.get(id=self.unactivate_user.id).nom == 'unactivate_user' )
        self.assertEqual(response.url, '../../home/')
        self.assertEqual(response.status_code, 302)

    def test_name_profil_user_locked(self):
        """  Mise à jour du nom d'un profil pour un fermé  """
        self.assertTrue( Utilisateurs.objects.get(id=self.locked_user.id).nom == 'locked_user' )
        response = self.client_locked_user.post('/user/update_profil_name/', { 'name': 'nouveau' })
        self.assertTrue( Utilisateurs.objects.get(id=self.locked_user.id).nom == 'locked_user' )
        self.assertEqual(response.url, '../../home/')
        self.assertEqual(response.status_code, 302)


    #   ----   Mise à jour de l'email d'un profil

    def test_update_mail_profil_user_connected(self):
    	"""  Mise à jour de l'email d'un profil pour un utilisateur connecté  """
    	self.assertTrue( Utilisateurs.objects.get(id=self.user_1.id).adresse_mail == 'user_1@mail.mail' )
    	response = self.client_1.post('/user/update_profil_mail/', { 'mail': 'new_user_1@mail.mail' })
    	self.assertTrue( response.url == "../../user/profil/" + str(self.user_1.id) + "/?section_profil=coordonees" )
    	self.assertTrue( Utilisateurs.objects.get(id=self.user_1.id).adresse_mail == 'new_user_1@mail.mail' )
    	self.assertTrue( response.status_code == 302 )

    def test_update_mail_profil_user_connected_invalid_form(self):
    	"""  Mise à jour de l'email d'un profil pour un utilisateur connecté avec un formulaire invalide  """
    	self.assertTrue( Utilisateurs.objects.get(id=self.user_1.id).adresse_mail == 'user_1@mail.mail' )
    	response = self.client_1.post('/user/update_profil_mail/', { 'mail': '' })
    	self.assertTrue( Utilisateurs.objects.get(id=self.user_1.id).adresse_mail == 'user_1@mail.mail' )
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_update_mail_profil_user_not_connected(self):
    	"""  Mise à jour de l'email d'un profil pour un utilisateur non connecté  """
    	response = self.client_0.post('/user/update_profil_mail/', { 'mail': 'new_user_1@mail.mail' })
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_mail_profil_user_unactivate(self):
        """  Mise à jour de l'email d'un profil pour un utilisateur desactivé  """
        self.assertTrue( Utilisateurs.objects.get(id=self.unactivate_user.id).adresse_mail == 'unactivate_user@mail.mail' )
        response = self.client_unactivate_user.post('/user/update_profil_mail/', { 'name': 'nouveau' })
        self.assertTrue( Utilisateurs.objects.get(id=self.unactivate_user.id).adresse_mail == 'unactivate_user@mail.mail' )
        self.assertEqual(response.url, '../../home/')
        self.assertEqual(response.status_code, 302)

    def test_mail_profil_user_locked(self):
        """  Mise à jour de l'email d'un profil pour un compte fermé  """
        self.assertTrue( Utilisateurs.objects.get(id=self.locked_user.id).adresse_mail == 'locked_user@mail.mail' )
        response = self.client_locked_user.post('/user/update_profil_mail/', { 'name': 'nouveau' })
        self.assertTrue( Utilisateurs.objects.get(id=self.locked_user.id).adresse_mail == 'locked_user@mail.mail' )
        self.assertEqual(response.url, '../../home/')
        self.assertEqual(response.status_code, 302)



    #   ----   Suppression d'un compte

    def test_delete_account_user_connected(self):
    	"""  Suppression d'un compte pour un utilisateur connecté  """
    	self.assertTrue( len(Utilisateurs.objects.filter(id=self.user_1.id)) == 1 )
    	response = self.client_1.get('/user/suppression_compte/')
    	self.assertTrue( response.url == "../../authentification/connexion/" )
    	self.assertTrue( len(Utilisateurs.objects.filter(id=self.user_1.id)) == 0 )
    	self.assertTrue( response.status_code == 302 )

    def test_delete_account_user_not_connected(self):
    	"""  Suppression d'un compte pour un utilisateur non connecté  """
    	response = self.client_0.get('/user/suppression_compte/')
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_delete_account_user_un(self):
        """  Suppression d'un compte pour un utilisateur connecté  """
        self.assertTrue( len(Utilisateurs.objects.filter(id=self.unactivate_user.id)) == 1 )
        response = self.client_unactivate_user.get('/user/suppression_compte/')
        self.assertEqual(response.url, '../../home/')
        self.assertTrue( len(Utilisateurs.objects.filter(id=self.unactivate_user.id)) == 1 )
        self.assertTrue( response.status_code == 302 )

    def test_delete_account_user_connected(self):
        """  Suppression d'un compte pour un utilisateur connecté  """
        self.assertTrue( len(Utilisateurs.objects.filter(id=self.locked_user.id)) == 1 )
        response = self.client_locked_user.get('/user/suppression_compte/')
        self.assertEqual(response.url, '../../home/')
        self.assertTrue( len(Utilisateurs.objects.filter(id=self.locked_user.id)) == 1 )
        self.assertTrue( response.status_code == 302 )





    #   ----   Deconnexion

    def test_deconnexion_account_user_connected(self):
    	"""  deconnexion d'un compte pour un utilisateur connecté  """
    	response = self.client_1.get('/user/deconnexion/')
    	self.assertTrue( response.url == "../../" )
    	self.assertTrue( response.status_code == 302 )

    def test_deconnexion_account_user_not_connected(self):
    	"""  deconnexion d'un compte pour un utilisateur non connecté  """
    	response = self.client_0.get('/user/deconnexion/')
    	self.assertTemplateUsed( response, '404.html')
    	self.assertTrue( response.status_code == 404 )

    def test_deconnexion_account_user_connected(self):
        """  deconnexion d'un compte pour un utilisateur desctivé  """
        response = self.client_unactivate_user.get('/user/deconnexion/')
        self.assertTrue( response.url == "../../" )
        self.assertTrue( response.status_code == 302 )

    def test_deconnexion_account_user_connected(self):
        """  deconnexion d'un compte pour un compte fermé  """
        response = self.client_locked_user.get('/user/deconnexion/')
        self.assertTrue( response.url == "../../" )
        self.assertTrue( response.status_code == 302 )











