import os, time

from django.test import LiveServerTestCase, RequestFactory

from user.models import Utilisateurs, Contact, Message

from unittest.mock import patch

from django.test import Client

from sets.models import Sets, Evenements, PublicationSet, JaimePublicationSet, PublicationEvenement, JaimePublicationEvenement, SetUtilisateurs

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium import webdriver

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys


class TestsFonctionnels(LiveServerTestCase):
    """docstring for TestsParcoursUsers"""

    def setUp(self):
        """Setup"""
        # binary = FirefoxBinary('./geckodriver-v0.28.0-linux32/geckodriver')
        super().setUpClass()

        #  support of request
        self.factory = RequestFactory()

        PATH = "tests/geckodriver/geckodriver"
        options = webdriver.firefox.options.Options()
        #options.add_argument("-headless")
        self.driver = webdriver.Firefox(executable_path=PATH, options=options)
        #self.driver = FirefoxBinary()
        if os.environ.get("ENV") == "PRODUCTION":
            self.domain = "http://34.105.144.166"
        else:
            self.domain = self.live_server_url
        #self.driver.maximize_window()
        self.driver.get(self.domain)

        self.waiteur = WebDriverWait(self.driver, 30)

    def tearDown(self):
        """Teardown"""
        self.driver.quit()

    def test_fonctionnel_inscription_deconnexion(self):
        """Test inscription deconnexion"""

        # Inscription - deconnexion
        print("Test du parcour Iscription - deconnexion")
        inscription_link = self.driver.find_element_by_link_text("S'inscrire")
        inscription_link.click()
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "id_name"))
        )
        users_before = len( Utilisateurs.objects.all() )
        name_input = self.driver.find_element_by_name("name")
        mail_input = self.driver.find_element_by_name("email")
        password_input = self.driver.find_element_by_name("password")
        confirm_password_input = self.driver.find_element_by_name("confirmation_password")
        name_input.send_keys("user")
        mail_input.send_keys("user@mail.mail")
        password_input.send_keys("user_password")
        confirm_password_input.send_keys("user_password")
        confirm_password_input.submit()
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "inactive_account"))
        )
        users_after = len( Utilisateurs.objects.all() )
        deconnexion = self.driver.find_element_by_css_selector('#deconnexion_button')
        deconnexion.click()
        self.assertTrue( users_after == users_before + 1 )
        self.assertEqual(self.driver.current_url, self.domain + "/authentification/connexion/")



    def test_fonctionnels_connexion_deconnexion(self):
        """connexion d'un utilisateur après son inscription"""
        print("Test du parcour Inscription - deconnexion - connexion - inscription")
        inscription_link = self.driver.find_element_by_link_text("S'inscrire")
        inscription_link.click()
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "id_name"))
        )
        users_before = len( Utilisateurs.objects.all() )
        name_input = self.driver.find_element_by_name("name")
        mail_input = self.driver.find_element_by_name("email")
        password_input = self.driver.find_element_by_name("password")
        confirm_password_input = self.driver.find_element_by_name("confirmation_password")
        name_input.send_keys("user")
        mail_input.send_keys("user@mail.mail")
        password_input.send_keys("user_password")
        confirm_password_input.send_keys("user_password")
        confirm_password_input.submit()     #    Création du compte
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "inactive_account"))
        )
        users_after = len( Utilisateurs.objects.all() )
        self.assertTrue( users_after == users_before + 1 )
        deconnexion = self.driver.find_element_by_css_selector('#deconnexion_button')
        deconnexion.click()           # Déconnexion
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "id_email"))
        )
        mail_input = self.driver.find_element_by_name("email")
        password_input = self.driver.find_element_by_name("password")
        mail_input.send_keys("user@mail.mail")
        password_input.send_keys("user_password")
        password_input.submit()     #   Connexion
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "inactive_account"))
        )
        self.assertEqual(self.driver.current_url, self.domain + "/user/home/")
        deconnexion = self.driver.find_element_by_css_selector('#deconnexion_button')
        deconnexion.click()     #   Déconnexion
        self.assertEqual(self.driver.current_url, self.domain + "/authentification/connexion/")

    def test_fonctionnels_envoie_lien_reinitialisation_mot_de_passe(self):
        """Réinitialisation de mot de passe après une inscription et deconnexion"""
        print("Test du parcour Inscription - deconnexion - envoi de lien de réinitialisation de mot de passe")
        inscription_link = self.driver.find_element_by_link_text("S'inscrire")
        inscription_link.click()
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "id_name"))
        )
        users_before = len( Utilisateurs.objects.all() )
        name_input = self.driver.find_element_by_name("name")
        mail_input = self.driver.find_element_by_name("email")
        password_input = self.driver.find_element_by_name("password")
        confirm_password_input = self.driver.find_element_by_name("confirmation_password")
        name_input.send_keys("user")
        mail_input.send_keys("user@mail.mail")
        password_input.send_keys("user_password")
        confirm_password_input.send_keys("user_password")
        confirm_password_input.submit()     #    Création du compte
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "inactive_account"))
        )
        users_after = len( Utilisateurs.objects.all() )
        self.assertTrue( users_after == users_before + 1 )
        deconnexion = self.driver.find_element_by_css_selector('#deconnexion_button')
        deconnexion.click()           # Déconnexion
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "id_email"))
        )
        envoie_lien_link = self.driver.find_element_by_link_text("Mot de passe oublié")
        envoie_lien_link.click()
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "id_email"))
        )
        mail_input = self.driver.find_element_by_name("email")
        mail_input.send_keys("user@mail.mail")
        mail_input.submit()     #    Envoie du lien
        element = self.waiteur.until(
            EC.presence_of_element_located((By.CLASS_NAME, "send_mail"))
        )      # Succès de l'envoie


    def test_fonctionnels_reinitialisation_mot_de_passe(self):
        """Réinitialisation du mot de passe"""
        print("Test du parcour Inscription - deconnexion - envoi de lien de réinitialisation de mot de passe - réinitialisation de mot de passe")
        inscription_link = self.driver.find_element_by_link_text("S'inscrire")
        inscription_link.click()
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "id_name"))
        )
        users_before = len( Utilisateurs.objects.all() )
        name_input = self.driver.find_element_by_name("name")
        mail_input = self.driver.find_element_by_name("email")
        password_input = self.driver.find_element_by_name("password")
        confirm_password_input = self.driver.find_element_by_name("confirmation_password")
        name_input.send_keys("user")
        mail_input.send_keys("user@mail.mail")
        password_input.send_keys("user_password")
        confirm_password_input.send_keys("user_password")
        confirm_password_input.submit()     #    Création du compte
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "inactive_account"))
        )
        users_after = len( Utilisateurs.objects.all() )
        self.assertTrue( users_after == users_before + 1 )
        deconnexion = self.driver.find_element_by_css_selector('#deconnexion_button')
        deconnexion.click()           # Déconnexion
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "id_email"))
        )
        envoie_lien_link = self.driver.find_element_by_link_text("Mot de passe oublié")
        envoie_lien_link.click()
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "id_email"))
        )
        mail_input = self.driver.find_element_by_name("email")
        mail_input.send_keys("user@mail.mail")
        mail_input.submit()     #    Envoie du lien
        element = self.waiteur.until(
            EC.presence_of_element_located((By.CLASS_NAME, "send_mail"))
        )      # Succès de l'envoie
        key = Utilisateurs.objects.get(
                adresse_mail='user@mail.mail'
            ).cle_de_reinitialisation_de_mot_de_passe  # Clé de réinitialisation
        self.driver.get(self.domain + '/authentification/reinitialisation_password/?' + 'mail=user@mail.mail&key_reinitialisation_password=' + key )
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "id_email"))
        )
        password_input = self.driver.find_element_by_name("password")
        confirm_password_input = self.driver.find_element_by_name("confirmation_password")
        password_input.send_keys("new_user_password")
        confirm_password_input.send_keys("new_user_password")
        confirm_password_input.submit()     #    Réinitialisation du mot de passe
        element = self.waiteur.until(
            EC.presence_of_element_located((By.CLASS_NAME, "confirmation_reinitilisation"))
        )      # Succès de la réinitialisation

    def test_fonctionnels_activation_compte(self):
        """"""
        print("Test du parcour Inscription - activation de compte")
        inscription_link = self.driver.find_element_by_link_text("S'inscrire")
        inscription_link.click()
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "id_name"))
        )
        users_before = len( Utilisateurs.objects.all() )
        name_input = self.driver.find_element_by_name("name")
        mail_input = self.driver.find_element_by_name("email")
        password_input = self.driver.find_element_by_name("password")
        confirm_password_input = self.driver.find_element_by_name("confirmation_password")
        name_input.send_keys("user")
        mail_input.send_keys("user@mail.mail")
        password_input.send_keys("user_password")
        confirm_password_input.send_keys("user_password")
        confirm_password_input.submit()     #    Création du compte
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "inactive_account"))
        )
        activation_key = Utilisateurs.objects.get(
            adresse_mail="user@mail.mail"
        ).cle_dactivation_de_compte
        self.driver.get(self.domain + "/authentification/activation_compte/?mail="
            + "user@mail.mail"
            + "&key_activation="
            + activation_key)
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "publication_home_contain"))
        )      # Succès de l'activation du compte

    def test_fonctionnels_envoie_lien_dactivation(self):
        """"""
        pass

    def test_fonctionnels_creation_set(self):
        """"""
        pass

    def test_fonctionnels_creation_evenement(self):
        """"""
        pass

    def test_fonctionnels_update_cover(self):
        """"""
        pass

    def test_fonctionnels_update_description(self):
        """"""
        pass

    def test_fonctionnels_make_post_set(self):
        """"""
        pass

    def test_fonctionnels_make_post_event(self):
        """"""
        pass

    def test_fonctionnels_manage_like_post_set(self):
        """"""
        pass

    def test_fonctionnels_manage_like_post_event(self):
        """"""
        pass

    def test_fonctionnels_delete_add_set(self):
        """"""
        pass

    def test_fonctionnels_manage_enter_set(self):
        """"""
        pass

    def test_fonctionnels_exit_set(self):
        """"""
        pass

    def test_fonctionnels_delete_set(self):
        """"""
        pass

    def test_fonctionnels_delete_event(self):
        """"""
        pass

    def test_fonctionnels_manage_contact(self):
        """"""
        pass

    def test_fonctionnels_contacts(self):
        """"""
        pass

    def test_fonctionnels_messages(self):
        """"""
        pass

    def test_fonctionnels_messages_exchanges(self):
        """"""
        pass

    def test_fonctionnels_send_message(self):
        """"""
        pass

    def test_fonctionnels_updates_messages(self):
        """"""
        pass

    def test_fonctionnels_update_image_cover(self):
        """"""
        pass

    def test_fonctionnels_update_profil_name(self):
        """"""
        pass

    def test_fonctionnels_update_profil_mail(self):
        """"""
        pass

    def test_fonctionnels_suppression_compte(self):
        """"""
        pass














