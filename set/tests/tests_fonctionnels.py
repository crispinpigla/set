import os, time

from django.core.files import File

from django.test import LiveServerTestCase, RequestFactory

from user.models import Utilisateurs, Contact, Message

from unittest.mock import patch

from django.test import Client

from sets.models import (
    Sets,
    Evenements,
    PublicationSet,
    JaimePublicationSet,
    PublicationEvenement,
    JaimePublicationEvenement,
    SetUtilisateurs,
)

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
        options.add_argument("-headless")
        self.driver = webdriver.Firefox(executable_path=PATH, options=options)
        # self.driver = FirefoxBinary()
        if os.environ.get("ENV") == "PRODUCTION":
            self.domain = "http://34.105.144.166"
        else:
            self.domain = self.live_server_url
        # self.driver.maximize_window()
        self.driver.get(self.domain)

        self.waiteur = WebDriverWait(self.driver, 30)

    def tearDown(self):
        """Teardown"""
        self.driver.quit()

    def test_fonctionnel_inscription_deconnexion(self):
        """Test inscription deconnexion"""

        # Inscription - deconnexion
        inscription_link = self.driver.find_element_by_link_text("S'inscrire")
        inscription_link.click()
        element = self.waiteur.until(EC.presence_of_element_located((By.ID, "id_name")))
        users_before = len(Utilisateurs.objects.all())
        name_input = self.driver.find_element_by_name("name")
        mail_input = self.driver.find_element_by_name("email")
        password_input = self.driver.find_element_by_name("password")
        confirm_password_input = self.driver.find_element_by_name(
            "confirmation_password"
        )
        name_input.send_keys("user")
        mail_input.send_keys("user@mail.mail")
        password_input.send_keys("user_password")
        confirm_password_input.send_keys("user_password")
        confirm_password_input.submit()
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "inactive_account"))
        )
        users_after = len(Utilisateurs.objects.all())
        deconnexion = self.driver.find_element_by_css_selector("#deconnexion_button")
        deconnexion.click()
        self.assertTrue(users_after == users_before + 1)
        self.assertEqual(
            self.driver.current_url, self.domain + "/authentification/connexion/"
        )

    def test_fonctionnels_connexion_deconnexion(self):
        """connexion d'un utilisateur après son inscription"""
        inscription_link = self.driver.find_element_by_link_text("S'inscrire")
        inscription_link.click()
        element = self.waiteur.until(EC.presence_of_element_located((By.ID, "id_name")))
        users_before = len(Utilisateurs.objects.all())
        name_input = self.driver.find_element_by_name("name")
        mail_input = self.driver.find_element_by_name("email")
        password_input = self.driver.find_element_by_name("password")
        confirm_password_input = self.driver.find_element_by_name(
            "confirmation_password"
        )
        name_input.send_keys("user")
        mail_input.send_keys("user@mail.mail")
        password_input.send_keys("user_password")
        confirm_password_input.send_keys("user_password")
        confirm_password_input.submit()  #    Création du compte
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "inactive_account"))
        )
        users_after = len(Utilisateurs.objects.all())
        self.assertTrue(users_after == users_before + 1)
        deconnexion = self.driver.find_element_by_css_selector("#deconnexion_button")
        deconnexion.click()  # Déconnexion
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "id_email"))
        )
        mail_input = self.driver.find_element_by_name("email")
        password_input = self.driver.find_element_by_name("password")
        mail_input.send_keys("user@mail.mail")
        password_input.send_keys("user_password")
        password_input.submit()  #   Connexion
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "inactive_account"))
        )
        self.assertEqual(self.driver.current_url, self.domain + "/user/home/")
        deconnexion = self.driver.find_element_by_css_selector("#deconnexion_button")
        deconnexion.click()  #   Déconnexion
        self.assertEqual(
            self.driver.current_url, self.domain + "/authentification/connexion/"
        )

    def test_fonctionnels_envoie_lien_reinitialisation_mot_de_passe(self):
        """Réinitialisation de mot de passe après une inscription et deconnexion"""
        inscription_link = self.driver.find_element_by_link_text("S'inscrire")
        inscription_link.click()
        element = self.waiteur.until(EC.presence_of_element_located((By.ID, "id_name")))
        users_before = len(Utilisateurs.objects.all())
        name_input = self.driver.find_element_by_name("name")
        mail_input = self.driver.find_element_by_name("email")
        password_input = self.driver.find_element_by_name("password")
        confirm_password_input = self.driver.find_element_by_name(
            "confirmation_password"
        )
        name_input.send_keys("user")
        mail_input.send_keys("user@mail.mail")
        password_input.send_keys("user_password")
        confirm_password_input.send_keys("user_password")
        confirm_password_input.submit()  #    Création du compte
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "inactive_account"))
        )
        users_after = len(Utilisateurs.objects.all())
        self.assertTrue(users_after == users_before + 1)
        deconnexion = self.driver.find_element_by_css_selector("#deconnexion_button")
        deconnexion.click()  # Déconnexion
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
        mail_input.submit()  #    Envoie du lien
        element = self.waiteur.until(
            EC.presence_of_element_located((By.CLASS_NAME, "send_mail"))
        )  # Succès de l'envoie

    def test_fonctionnels_reinitialisation_mot_de_passe(self):
        """Réinitialisation du mot de passe"""
        inscription_link = self.driver.find_element_by_link_text("S'inscrire")
        inscription_link.click()
        element = self.waiteur.until(EC.presence_of_element_located((By.ID, "id_name")))
        users_before = len(Utilisateurs.objects.all())
        name_input = self.driver.find_element_by_name("name")
        mail_input = self.driver.find_element_by_name("email")
        password_input = self.driver.find_element_by_name("password")
        confirm_password_input = self.driver.find_element_by_name(
            "confirmation_password"
        )
        name_input.send_keys("user")
        mail_input.send_keys("user@mail.mail")
        password_input.send_keys("user_password")
        confirm_password_input.send_keys("user_password")
        confirm_password_input.submit()  #    Création du compte
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "inactive_account"))
        )
        users_after = len(Utilisateurs.objects.all())
        self.assertTrue(users_after == users_before + 1)
        deconnexion = self.driver.find_element_by_css_selector("#deconnexion_button")
        deconnexion.click()  # Déconnexion
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
        mail_input.submit()  #    Envoie du lien
        element = self.waiteur.until(
            EC.presence_of_element_located((By.CLASS_NAME, "send_mail"))
        )  # Succès de l'envoie
        key = Utilisateurs.objects.get(
            adresse_mail="user@mail.mail"
        ).cle_de_reinitialisation_de_mot_de_passe  # Clé de réinitialisation
        self.driver.get(
            self.domain
            + "/authentification/reinitialisation_password/?"
            + "mail=user@mail.mail&key_reinitialisation_password="
            + key
        )
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "id_email"))
        )
        password_input = self.driver.find_element_by_name("password")
        confirm_password_input = self.driver.find_element_by_name(
            "confirmation_password"
        )
        password_input.send_keys("new_user_password")
        confirm_password_input.send_keys("new_user_password")
        confirm_password_input.submit()  #    Réinitialisation du mot de passe
        element = self.waiteur.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "confirmation_reinitilisation")
            )
        )  # Succès de la réinitialisation

    def test_fonctionnels_activation_compte(self):
        """Activation du compte"""
        inscription_link = self.driver.find_element_by_link_text("S'inscrire")
        inscription_link.click()
        element = self.waiteur.until(EC.presence_of_element_located((By.ID, "id_name")))
        users_before = len(Utilisateurs.objects.all())
        name_input = self.driver.find_element_by_name("name")
        mail_input = self.driver.find_element_by_name("email")
        password_input = self.driver.find_element_by_name("password")
        confirm_password_input = self.driver.find_element_by_name(
            "confirmation_password"
        )
        name_input.send_keys("user")
        mail_input.send_keys("user@mail.mail")
        password_input.send_keys("user_password")
        confirm_password_input.send_keys("user_password")
        confirm_password_input.submit()  #    Création du compte
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "inactive_account"))
        )
        activation_key = Utilisateurs.objects.get(
            adresse_mail="user@mail.mail"
        ).cle_dactivation_de_compte
        self.driver.get(
            self.domain
            + "/authentification/activation_compte/?mail="
            + "user@mail.mail"
            + "&key_activation="
            + activation_key
        )
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "publication_home_contain"))
        )  # Succès de l'activation du compte

    def test_fonctionnels_envoie_lien_dactivation(self):
        """Envoie du lien d'activation du compte"""
        inscription_link = self.driver.find_element_by_link_text("S'inscrire")
        inscription_link.click()
        element = self.waiteur.until(EC.presence_of_element_located((By.ID, "id_name")))
        users_before = len(Utilisateurs.objects.all())
        name_input = self.driver.find_element_by_name("name")
        mail_input = self.driver.find_element_by_name("email")
        password_input = self.driver.find_element_by_name("password")
        confirm_password_input = self.driver.find_element_by_name(
            "confirmation_password"
        )
        name_input.send_keys("user")
        mail_input.send_keys("user@mail.mail")
        password_input.send_keys("user_password")
        confirm_password_input.send_keys("user_password")
        confirm_password_input.submit()  #    Création du compte
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "inactive_account"))
        )
        activation_key_before = Utilisateurs.objects.get(
            adresse_mail="user@mail.mail"
        ).cle_dactivation_de_compte  # clé avant
        activation_link = self.driver.find_element_by_link_text(
            "renvoyer un lien d'activation"
        )
        activation_link.click()  #   Envoie d'un nouveau lien
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "inactive_account"))
        )
        activation_key_after = Utilisateurs.objects.get(
            adresse_mail="user@mail.mail"
        ).cle_dactivation_de_compte  # clé après
        self.assertTrue(activation_key_before != activation_key_after)

    def test_fonctionnels_creation_set(self):
        """Création d'un set"""
        inscription_link = self.driver.find_element_by_link_text("S'inscrire")
        inscription_link.click()
        element = self.waiteur.until(EC.presence_of_element_located((By.ID, "id_name")))
        users_before = len(Utilisateurs.objects.all())
        name_input = self.driver.find_element_by_name("name")
        mail_input = self.driver.find_element_by_name("email")
        password_input = self.driver.find_element_by_name("password")
        confirm_password_input = self.driver.find_element_by_name(
            "confirmation_password"
        )
        name_input.send_keys("user")
        mail_input.send_keys("user@mail.mail")
        password_input.send_keys("user_password")
        confirm_password_input.send_keys("user_password")
        confirm_password_input.submit()  #    Création du compte
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "inactive_account"))
        )
        activation_key = Utilisateurs.objects.get(
            adresse_mail="user@mail.mail"
        ).cle_dactivation_de_compte
        self.driver.get(
            self.domain
            + "/authentification/activation_compte/?mail="
            + "user@mail.mail"
            + "&key_activation="
            + activation_key
        )
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "publication_home_contain"))
        )  # Succès de l'activation du compte
        create_set_link = self.driver.find_element_by_link_text("Créer un set")
        create_set_link.click()  #   Accèss à la page de création du set
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "ecran_previsualisation"))
        )
        sets_before = len(Sets.objects.all())
        image_input_create_set = self.driver.find_element_by_name("file")
        nom_input_create_set = self.driver.find_element_by_name("name")
        type_input_create_set = self.driver.find_element_by_name("type_set")
        description_input_create_set = self.driver.find_element_by_name("description")
        image_input_create_set.send_keys(os.path.join(os.getcwd(), "tests/test.png"))
        nom_input_create_set.send_keys("nom_set")
        type_input_create_set.send_keys("type_set")
        description_input_create_set.send_keys("description_set")
        description_input_create_set.submit()  #   création du set
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "contain_description"))
        )
        sets_after = len(Sets.objects.all())
        self.assertTrue(sets_after == sets_before + 1)

    def test_fonctionnels_creation_evenement(self):
        """Création d'un évènement"""
        inscription_link = self.driver.find_element_by_link_text("S'inscrire")
        inscription_link.click()
        element = self.waiteur.until(EC.presence_of_element_located((By.ID, "id_name")))
        users_before = len(Utilisateurs.objects.all())
        name_input = self.driver.find_element_by_name("name")
        mail_input = self.driver.find_element_by_name("email")
        password_input = self.driver.find_element_by_name("password")
        confirm_password_input = self.driver.find_element_by_name(
            "confirmation_password"
        )
        name_input.send_keys("user")
        mail_input.send_keys("user@mail.mail")
        password_input.send_keys("user_password")
        confirm_password_input.send_keys("user_password")
        confirm_password_input.submit()  #    Création du compte
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "inactive_account"))
        )
        activation_key = Utilisateurs.objects.get(
            adresse_mail="user@mail.mail"
        ).cle_dactivation_de_compte
        self.driver.get(
            self.domain
            + "/authentification/activation_compte/?mail="
            + "user@mail.mail"
            + "&key_activation="
            + activation_key
        )
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "publication_home_contain"))
        )  # Succès de l'activation du compte
        create_set_link = self.driver.find_element_by_link_text("Créer un set")
        create_set_link.click()  #   Accèss à la page de création du set
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "ecran_previsualisation"))
        )
        image_input_create_set = self.driver.find_element_by_name("file")
        nom_input_create_set = self.driver.find_element_by_name("name")
        type_input_create_set = self.driver.find_element_by_name("type_set")
        description_input_create_set = self.driver.find_element_by_name("description")
        image_input_create_set.send_keys(os.path.join(os.getcwd(), "tests/test.png"))
        nom_input_create_set.send_keys("nom_set")
        type_input_create_set.send_keys("type_set")
        description_input_create_set.send_keys("description_set")
        description_input_create_set.submit()  #   création du set
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "contain_description"))
        )
        events_sets_link = self.driver.find_element_by_link_text("Evènements")
        events_sets_link.click()  #   Accès à la page des évènements du set
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "contain_create_event"))
        )
        create_event_link = self.driver.find_element_by_link_text(
            "Créer un nouvel évènement"
        )
        create_event_link.click()  #   Accèss à la page de création du set
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "ecran_previsualisation"))
        )
        events_before = len(Evenements.objects.all())
        nom_input_create_event = self.driver.find_element_by_name("name")
        description_input_create_event = self.driver.find_element_by_name("description")
        nom_input_create_event.send_keys("nom_set")
        description_input_create_event.send_keys("description_set")
        description_input_create_event.submit()  #   création de l'évènement
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "suppression_event"))
        )
        events_after = len(Evenements.objects.all())
        self.assertTrue(events_after == events_before + 1)

    def test_fonctionnels_update_cover(self):
        """Mise à jour de la couverture d'un set"""
        inscription_link = self.driver.find_element_by_link_text("S'inscrire")
        inscription_link.click()
        element = self.waiteur.until(EC.presence_of_element_located((By.ID, "id_name")))
        users_before = len(Utilisateurs.objects.all())
        name_input = self.driver.find_element_by_name("name")
        mail_input = self.driver.find_element_by_name("email")
        password_input = self.driver.find_element_by_name("password")
        confirm_password_input = self.driver.find_element_by_name(
            "confirmation_password"
        )
        name_input.send_keys("user")
        mail_input.send_keys("user@mail.mail")
        password_input.send_keys("user_password")
        confirm_password_input.send_keys("user_password")
        confirm_password_input.submit()  #    Création du compte
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "inactive_account"))
        )
        activation_key = Utilisateurs.objects.get(
            adresse_mail="user@mail.mail"
        ).cle_dactivation_de_compte
        self.driver.get(
            self.domain
            + "/authentification/activation_compte/?mail="
            + "user@mail.mail"
            + "&key_activation="
            + activation_key
        )
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "publication_home_contain"))
        )  # Succès de l'activation du compte
        create_set_link = self.driver.find_element_by_link_text("Créer un set")
        create_set_link.click()  #   Accèss à la page de création du set
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "ecran_previsualisation"))
        )
        image_input_create_set = self.driver.find_element_by_name("file")
        nom_input_create_set = self.driver.find_element_by_name("name")
        type_input_create_set = self.driver.find_element_by_name("type_set")
        description_input_create_set = self.driver.find_element_by_name("description")
        image_input_create_set.send_keys(os.path.join(os.getcwd(), "tests/test.png"))
        nom_input_create_set.send_keys("nom_set")
        type_input_create_set.send_keys("type_set")
        description_input_create_set.send_keys("description_set")
        description_input_create_set.submit()  #   création du set
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "contain_description"))
        )
        set_id = self.driver.current_url.split("/")[-2]
        new_cover = os.path.join(os.getcwd(), "tests/test0.png")
        new_cover_input = self.driver.find_element_by_name("file")
        new_cover_input.send_keys(new_cover)
        new_cover_input.submit()  #   mise à jour de la couverture du set

    def test_fonctionnels_update_description(self):
        """Mise à jour de la description d'un set"""
        inscription_link = self.driver.find_element_by_link_text("S'inscrire")
        inscription_link.click()
        element = self.waiteur.until(EC.presence_of_element_located((By.ID, "id_name")))
        users_before = len(Utilisateurs.objects.all())
        name_input = self.driver.find_element_by_name("name")
        mail_input = self.driver.find_element_by_name("email")
        password_input = self.driver.find_element_by_name("password")
        confirm_password_input = self.driver.find_element_by_name(
            "confirmation_password"
        )
        name_input.send_keys("user")
        mail_input.send_keys("user@mail.mail")
        password_input.send_keys("user_password")
        confirm_password_input.send_keys("user_password")
        confirm_password_input.submit()  #    Création du compte
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "inactive_account"))
        )
        activation_key = Utilisateurs.objects.get(
            adresse_mail="user@mail.mail"
        ).cle_dactivation_de_compte
        self.driver.get(
            self.domain
            + "/authentification/activation_compte/?mail="
            + "user@mail.mail"
            + "&key_activation="
            + activation_key
        )
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "publication_home_contain"))
        )  # Succès de l'activation du compte
        create_set_link = self.driver.find_element_by_link_text("Créer un set")
        create_set_link.click()  #   Accèss à la page de création du set
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "ecran_previsualisation"))
        )
        image_input_create_set = self.driver.find_element_by_name("file")
        nom_input_create_set = self.driver.find_element_by_name("name")
        type_input_create_set = self.driver.find_element_by_name("type_set")
        description_input_create_set = self.driver.find_element_by_name("description")
        image_input_create_set.send_keys(os.path.join(os.getcwd(), "tests/test.png"))
        nom_input_create_set.send_keys("nom_set")
        type_input_create_set.send_keys("type_set")
        description_input_create_set.send_keys("description_set")
        description_input_create_set.submit()  #   création du set
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "contain_description"))
        )
        set_id = self.driver.current_url.split("/")[-2]
        modification_description = self.driver.find_element_by_css_selector(
            "#modification_description"
        )
        modification_description.click()
        new_description_input = self.driver.find_element_by_name("description")
        new_description_input.send_keys("new_description")
        new_description_input.submit()  #   mise à jour de la couverture du set

    def test_fonctionnels_make_post_set(self):
        """Publication dans un set"""
        inscription_link = self.driver.find_element_by_link_text("S'inscrire")
        inscription_link.click()
        element = self.waiteur.until(EC.presence_of_element_located((By.ID, "id_name")))
        users_before = len(Utilisateurs.objects.all())
        name_input = self.driver.find_element_by_name("name")
        mail_input = self.driver.find_element_by_name("email")
        password_input = self.driver.find_element_by_name("password")
        confirm_password_input = self.driver.find_element_by_name(
            "confirmation_password"
        )
        name_input.send_keys("user")
        mail_input.send_keys("user@mail.mail")
        password_input.send_keys("user_password")
        confirm_password_input.send_keys("user_password")
        confirm_password_input.submit()  #    Création du compte
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "inactive_account"))
        )
        activation_key = Utilisateurs.objects.get(
            adresse_mail="user@mail.mail"
        ).cle_dactivation_de_compte
        self.driver.get(
            self.domain
            + "/authentification/activation_compte/?mail="
            + "user@mail.mail"
            + "&key_activation="
            + activation_key
        )
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "publication_home_contain"))
        )  # Succès de l'activation du compte
        create_set_link = self.driver.find_element_by_link_text("Créer un set")
        create_set_link.click()  #   Accèss à la page de création du set
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "ecran_previsualisation"))
        )
        image_input_create_set = self.driver.find_element_by_name("file")
        nom_input_create_set = self.driver.find_element_by_name("name")
        type_input_create_set = self.driver.find_element_by_name("type_set")
        description_input_create_set = self.driver.find_element_by_name("description")
        image_input_create_set.send_keys(os.path.join(os.getcwd(), "tests/test.png"))
        nom_input_create_set.send_keys("nom_set")
        type_input_create_set.send_keys("type_set")
        description_input_create_set.send_keys("description_set")
        description_input_create_set.submit()  #   création du set
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "contain_description"))
        )
        set_id = self.driver.current_url.split("/")[-2]
        contenu_text_publication_set = self.driver.find_element_by_name(
            "publication_text"
        )
        file1_publication_set = self.driver.find_element_by_name("file_1")
        file2_publication_set = self.driver.find_element_by_name("file_2")
        contenu_text_publication_set.send_keys("le texte dune publication")
        file1_publication_set.send_keys(os.path.join(os.getcwd(), "tests/test.png"))
        file2_publication_set.send_keys(os.path.join(os.getcwd(), "tests/test.png"))
        file2_publication_set.submit()  #   création de la publication

    def test_fonctionnels_make_post_event(self):
        """Publication dans un évènement"""
        inscription_link = self.driver.find_element_by_link_text("S'inscrire")
        inscription_link.click()
        element = self.waiteur.until(EC.presence_of_element_located((By.ID, "id_name")))
        users_before = len(Utilisateurs.objects.all())
        name_input = self.driver.find_element_by_name("name")
        mail_input = self.driver.find_element_by_name("email")
        password_input = self.driver.find_element_by_name("password")
        confirm_password_input = self.driver.find_element_by_name(
            "confirmation_password"
        )
        name_input.send_keys("user")
        mail_input.send_keys("user@mail.mail")
        password_input.send_keys("user_password")
        confirm_password_input.send_keys("user_password")
        confirm_password_input.submit()  #    Création du compte
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "inactive_account"))
        )
        activation_key = Utilisateurs.objects.get(
            adresse_mail="user@mail.mail"
        ).cle_dactivation_de_compte
        self.driver.get(
            self.domain
            + "/authentification/activation_compte/?mail="
            + "user@mail.mail"
            + "&key_activation="
            + activation_key
        )
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "publication_home_contain"))
        )  # Succès de l'activation du compte
        create_set_link = self.driver.find_element_by_link_text("Créer un set")
        create_set_link.click()  #   Accèss à la page de création du set
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "ecran_previsualisation"))
        )
        image_input_create_set = self.driver.find_element_by_name("file")
        nom_input_create_set = self.driver.find_element_by_name("name")
        type_input_create_set = self.driver.find_element_by_name("type_set")
        description_input_create_set = self.driver.find_element_by_name("description")
        image_input_create_set.send_keys(os.path.join(os.getcwd(), "tests/test.png"))
        nom_input_create_set.send_keys("nom_set")
        type_input_create_set.send_keys("type_set")
        description_input_create_set.send_keys("description_set")
        description_input_create_set.submit()  #   création du set
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "contain_description"))
        )
        events_sets_link = self.driver.find_element_by_link_text("Evènements")
        events_sets_link.click()  #   Accès à la page des évènements du set
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "contain_create_event"))
        )
        create_event_link = self.driver.find_element_by_link_text(
            "Créer un nouvel évènement"
        )
        create_event_link.click()  #   Accèss à la page de création du set
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "ecran_previsualisation"))
        )
        nom_input_create_event = self.driver.find_element_by_name("name")
        description_input_create_event = self.driver.find_element_by_name("description")
        nom_input_create_event.send_keys("nom_set")
        description_input_create_event.send_keys("description_set")
        description_input_create_event.submit()  #   création de l'évènement
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "suppression_event"))
        )
        contenu_text_publication_evenement = self.driver.find_element_by_name(
            "publication_text"
        )
        file1_publication_evenement = self.driver.find_element_by_name("file_1")
        file2_publication_evenement = self.driver.find_element_by_name("file_2")
        contenu_text_publication_evenement.send_keys("le texte dune publication")
        file1_publication_evenement.send_keys(os.path.join(os.getcwd(), "tests/test.png"))
        file2_publication_evenement.send_keys(os.path.join(os.getcwd(), "tests/test.png"))
        file2_publication_evenement.submit()  #   création de la publication

    def test_fonctionnels_manage_like_post_set(self):
        """Gestion de like d'une publication dans un set"""
        inscription_link = self.driver.find_element_by_link_text("S'inscrire")
        inscription_link.click()
        element = self.waiteur.until(EC.presence_of_element_located((By.ID, "id_name")))
        users_before = len(Utilisateurs.objects.all())
        name_input = self.driver.find_element_by_name("name")
        mail_input = self.driver.find_element_by_name("email")
        password_input = self.driver.find_element_by_name("password")
        confirm_password_input = self.driver.find_element_by_name(
            "confirmation_password"
        )
        name_input.send_keys("user")
        mail_input.send_keys("user@mail.mail")
        password_input.send_keys("user_password")
        confirm_password_input.send_keys("user_password")
        confirm_password_input.submit()  #    Création du compte
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "inactive_account"))
        )
        activation_key = Utilisateurs.objects.get(
            adresse_mail="user@mail.mail"
        ).cle_dactivation_de_compte
        self.driver.get(
            self.domain
            + "/authentification/activation_compte/?mail="
            + "user@mail.mail"
            + "&key_activation="
            + activation_key
        )
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "publication_home_contain"))
        )  # Succès de l'activation du compte
        create_set_link = self.driver.find_element_by_link_text("Créer un set")
        create_set_link.click()  #   Accèss à la page de création du set
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "ecran_previsualisation"))
        )
        image_input_create_set = self.driver.find_element_by_name("file")
        nom_input_create_set = self.driver.find_element_by_name("name")
        type_input_create_set = self.driver.find_element_by_name("type_set")
        description_input_create_set = self.driver.find_element_by_name("description")
        image_input_create_set.send_keys(os.path.join(os.getcwd(), "tests/test.png"))
        nom_input_create_set.send_keys("nom_set")
        type_input_create_set.send_keys("type_set")
        description_input_create_set.send_keys("description_set")
        description_input_create_set.submit()  #   création du set
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "contain_description"))
        )
        set_id = self.driver.current_url.split("/")[-2]
        contenu_text_publication_set = self.driver.find_element_by_name(
            "publication_text"
        )
        file1_publication_set = self.driver.find_element_by_name("file_1")
        file2_publication_set = self.driver.find_element_by_name("file_2")
        contenu_text_publication_set.send_keys("le texte dune publication")
        file1_publication_set.send_keys(os.path.join(os.getcwd(), "tests/test.png"))
        file2_publication_set.send_keys(os.path.join(os.getcwd(), "tests/test.png"))
        file2_publication_set.submit()  #   création de la publication
        element = self.waiteur.until(
            EC.presence_of_element_located((By.CLASS_NAME, "make_like"))
        )
        like_publication = self.driver.find_element_by_css_selector(".make_like")
        unlike_publication = self.driver.find_element_by_css_selector(".make_unlike")
        like_publication.click()
        element = self.waiteur.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "make_unlike"))
        )
        unlike_publication.click()
        element = self.waiteur.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "make_like"))
        )

    def test_fonctionnels_manage_like_post_event(self):
        """Gestion de like d'une publication dans un évènement"""
        inscription_link = self.driver.find_element_by_link_text("S'inscrire")
        inscription_link.click()
        element = self.waiteur.until(EC.presence_of_element_located((By.ID, "id_name")))
        users_before = len(Utilisateurs.objects.all())
        name_input = self.driver.find_element_by_name("name")
        mail_input = self.driver.find_element_by_name("email")
        password_input = self.driver.find_element_by_name("password")
        confirm_password_input = self.driver.find_element_by_name(
            "confirmation_password"
        )
        name_input.send_keys("user")
        mail_input.send_keys("user@mail.mail")
        password_input.send_keys("user_password")
        confirm_password_input.send_keys("user_password")
        confirm_password_input.submit()  #    Création du compte
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "inactive_account"))
        )
        activation_key = Utilisateurs.objects.get(
            adresse_mail="user@mail.mail"
        ).cle_dactivation_de_compte
        self.driver.get(
            self.domain
            + "/authentification/activation_compte/?mail="
            + "user@mail.mail"
            + "&key_activation="
            + activation_key
        )
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "publication_home_contain"))
        )  # Succès de l'activation du compte
        create_set_link = self.driver.find_element_by_link_text("Créer un set")
        create_set_link.click()  #   Accèss à la page de création du set
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "ecran_previsualisation"))
        )
        image_input_create_set = self.driver.find_element_by_name("file")
        nom_input_create_set = self.driver.find_element_by_name("name")
        type_input_create_set = self.driver.find_element_by_name("type_set")
        description_input_create_set = self.driver.find_element_by_name("description")
        image_input_create_set.send_keys(os.path.join(os.getcwd(), "tests/test.png"))
        nom_input_create_set.send_keys("nom_set")
        type_input_create_set.send_keys("type_set")
        description_input_create_set.send_keys("description_set")
        description_input_create_set.submit()  #   création du set
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "contain_description"))
        )
        events_sets_link = self.driver.find_element_by_link_text("Evènements")
        events_sets_link.click()  #   Accès à la page des évènements du set
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "contain_create_event"))
        )
        create_event_link = self.driver.find_element_by_link_text(
            "Créer un nouvel évènement"
        )
        create_event_link.click()  #   Accèss à la page de création du set
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "ecran_previsualisation"))
        )
        nom_input_create_event = self.driver.find_element_by_name("name")
        description_input_create_event = self.driver.find_element_by_name("description")
        nom_input_create_event.send_keys("nom_set")
        description_input_create_event.send_keys("description_set")
        description_input_create_event.submit()  #   création de l'évènement
        element = self.waiteur.until(
            EC.presence_of_element_located((By.ID, "suppression_event"))
        )
        contenu_text_publication_evenement = self.driver.find_element_by_name(
            "publication_text"
        )
        file1_publication_evenement = self.driver.find_element_by_name("file_1")
        file2_publication_evenement = self.driver.find_element_by_name("file_2")
        contenu_text_publication_evenement.send_keys("le texte dune publication")
        file1_publication_evenement.send_keys(os.path.join(os.getcwd(), "tests/test.png"))
        file2_publication_evenement.send_keys(os.path.join(os.getcwd(), "tests/test.png"))
        file2_publication_evenement.submit()  #   création de la publication
        element = self.waiteur.until(
            EC.presence_of_element_located((By.CLASS_NAME, "make_like"))
        )
        like_publication = self.driver.find_element_by_css_selector(".make_like")
        unlike_publication = self.driver.find_element_by_css_selector(".make_unlike")
        like_publication.click()
        element = self.waiteur.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "make_unlike"))
        )
        unlike_publication.click()
        element = self.waiteur.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "make_like")))

