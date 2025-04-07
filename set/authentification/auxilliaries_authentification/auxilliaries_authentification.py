"""   """

import os
import requests

from django.template.loader import render_to_string

from django.core.mail import EmailMessage

from django.shortcuts import redirect, render, get_object_or_404

import random

from django.http import HttpResponse, Http404

from user.models import Utilisateurs

from authentification.forms import (
    InscriptionForm,
    ConnexionForm,
    SearchForm,
    InitializePasswordForm,
    LinkResetPasswordForm,
    ResetPasswordForm,
)


class AuxilliariesAuthentification:
    """Traite les requêtes liées à l'authentification"""

    def __init__(self):
        """Init."""
        pass

    def send_mail(self, service, user):
        """Envoie les mails d'activation de compte et de réinitialisation de mot de passe"""
        # print(1, os.environ.get("ENV"))
        if os.environ.get("ENV") == "PRODUCTION":
            host = 'http://%s:8002' % requests.get('https://ifconfig.me').text  # Old ip: "http://34.105.144.166"
            # host = requests.get('https://ifconfig.me').text
            # print(host)
        elif os.environ.get("ENV") == "HEROKU_PRODUCTION":
            host = "https://sets0.herokuapp.com"
        else:
            host = "http://localhost:8000"
        if service == "reinitialisation_password":
            template = "mail_reinitialisation_mot_de_passe.html"
            subject = "Réinitialisation du mot de passe"
        elif service == "activation_account":
            template = "activation_compte.html"
            subject = "Activation du compte"
        html_message = render_to_string(template, {"user": user, "host": host})
        msg = EmailMessage(
            subject=subject, body=html_message, from_email="", bcc=[user.adresse_mail]
        )
        msg.content_subtype = "html"
        out = msg.send()
        return out

    def make_connexion(self, users_in_database, request):
        """Vérifie si l'utilisateur existe dans l'application et crée la connexion"""
        if (
            len(users_in_database) == 0
        ):  # L'email recu ne correspond à aucun utilisateur de l'application
            connexion_form = ConnexionForm()
            search_form = SearchForm()
            context = {
                "connexion_form": connexion_form,
                "search_form": search_form,
                "no_mail_in_application_error": True,
            }
            return render(request, "connexion.html", context)
        else:  # Il existe au moins un utilisateur dans l'application
            if (
                users_in_database[0].mot_de_passe == request.POST["password"]
            ):  # adresse et mot de passe correct
                request.session["user_id"] = users_in_database[0].id
                return redirect("../../user/home/")
            else:  # Mot de passe incorrect
                connexion_form = ConnexionForm()
                search_form = SearchForm()
                context = {
                    "connexion_form": connexion_form,
                    "search_form": search_form,
                    "password_error": True,
                }
                return render(request, "connexion.html", context)

    def make_inscription(self, users_in_database, request):
        """Vérifie si un utilisateur existe avec le mail recu et exécute l'inscription"""
        if len(users_in_database) == 0:
            activation_key = "".join(
                [
                    random.choice(
                        "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    )
                    for _ in range(24)
                ]
            )
            user = Utilisateurs.objects.create(
                nom=request.POST["name"],
                adresse_mail=request.POST["email"],
                mot_de_passe=request.POST["password"],
                cle_dactivation_de_compte=activation_key,
            )
            sent_mail_statut = self.send_mail(
                "activation_account", user
            )  # Envoie de mail
            request.session["user_id"] = user.id  # Création de la session # TO FIX
            return redirect("../../user/home/")
        else:
            inscription_form = InscriptionForm()
            search_form = SearchForm()
            context = {
                "inscription_form": inscription_form,
                "search_form": search_form,
                "already_mail_error": True,
            }
            return render(request, "inscription.html", context)

    def check_form_make_inscription(self, inscription_form, request):
        """Vérifie si le formulaire d'inscription est valide"""
        if inscription_form.is_valid() and (
            request.POST["password"] == request.POST["confirmation_password"]
        ):
            users_in_database = Utilisateurs.objects.filter(
                adresse_mail=request.POST["email"]
            )
            return self.make_inscription(users_in_database, request)
        else:
            if not inscription_form.is_valid():
                # Formulaire pas valide
                context = {
                    "inscription_form": InscriptionForm(),
                    "search_form": SearchForm(),
                    "inscription_form_error": inscription_form.errors.items(),
                }
                return render(request, "inscription.html", context)
            elif request.POST["password"] != request.POST["confirmation_password"]:
                inscription_form = InscriptionForm()
                search_form = SearchForm()
                context = {
                    "inscription_form": inscription_form,
                    "search_form": search_form,
                    "no_match_password_error": True,
                }
                return render(request, "inscription.html", context)

    def render_reinitialize_password(self, user, request):
        """Réinitiialise le mot de passe"""
        reinitialisation_password_key = "".join(
            [
                random.choice(
                    "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
                )
                for _ in range(24)
            ]
        )
        user.cle_de_reinitialisation_de_mot_de_passe = reinitialisation_password_key
        user.save()
        sent_mail_statut = self.send_mail("reinitialisation_password", user)
        link_reset_form = LinkResetPasswordForm()
        search_form = SearchForm()
        context = {
            "link_reset_form": link_reset_form,
            "search_form": search_form,
            "send_mail": sent_mail_statut,
            "user": user,
        }
        return render(
            request, "envoie_lien_reinitialisation_mot_de_passe.html", context
        )

    def render_no_user_found_reinitialize_password(self, mail, request):
        """Envoie une réponse indiquant qu'aucun utilisateur ne correspond au mail recu"""
        link_reset_form = LinkResetPasswordForm()
        search_form = SearchForm()
        context = {
            "link_reset_form": link_reset_form,
            "search_form": search_form,
            "no_user_with_mail_error": True,
            "mail": mail,
        }
        return render(
            request, "envoie_lien_reinitialisation_mot_de_passe.html", context
        )

    def render_no_matched_reinitialize_password(
        self, reset_password_form, search_form, request, user, reset_form
    ):
        """Envoie une réponse indiquant que les mots de passes recus doivent etre identiques"""
        # Mot de passe et confirmation non-identique
        context = {
            "reset_password_form": reset_password_form,
            "search_form": search_form,
            "user": user,
            "password_different_to_confirmation": True,
            "user": user,
            "reset_form": reset_form,
        }
        return render(request, "reinitialisation_mot_de_passe.html", context)

    def render_success_reinitialize_password(
        self, reset_password_form, search_form, request, user, reset_form
    ):
        """Indique à l'utilisateur que le mot de passe a été réinitialisé"""
        # Mot de passe et confirmation identiques et bonne clé
        user.mot_de_passe = request.POST["password"]
        user.cle_de_reinitialisation_de_mot_de_passe = None
        user.save()
        context = {
            "reset_password_form": reset_password_form,
            "search_form": search_form,
            "user": user,
            "state_reinitialisation": True,
            "user": user,
            "reset_form": reset_form,
        }
        return render(request, "reinitialisation_mot_de_passe.html", context)

    def ckeck_machted_passwords_reinitialize_password(
        self, request, search_form, reset_password_form
    ):
        """Vérifie que les mots de passe sont identiques et réinitialise le mot de passe"""
        mail = request.POST["email"]
        user = get_object_or_404(Utilisateurs, adresse_mail=mail)
        reset_form = ResetPasswordForm()
        if (request.POST["password"] == request.POST["confirmation_password"]) and (
            user.cle_de_reinitialisation_de_mot_de_passe == request.POST["reset_key"]
        ):
            return AuxilliariesAuthentification().render_success_reinitialize_password(
                reset_password_form, search_form, request, user, reset_form
            )
        else:
            if (
                user.cle_de_reinitialisation_de_mot_de_passe
                != request.POST["reset_key"]
            ):
                # Mauvaise clé
                raise Http404()
            else:
                return AuxilliariesAuthentification().render_no_matched_reinitialize_password(
                    reset_password_form, search_form, request, user, reset_form
                )

    def check_valid_form_reinitialize_password(self, request):
        """Vérifie que le formulaire de réinitialisation de mot de passe est valide"""
        reset_password_form = ResetPasswordForm(request.POST)
        search_form = SearchForm()
        if reset_password_form.is_valid():  # formulaire valide
            return AuxilliariesAuthentification().ckeck_machted_passwords_reinitialize_password(
                request, search_form, reset_password_form
            )
        else:  # formulaire pas valide
            context = {
                "reset_password_form": reset_password_form,
                "search_form": search_form,
            }
            context["errors"] = reset_password_form.errors.items()
            return render(request, "reinitialisation_mot_de_passe.html", context)

    def make_initialize_password(self, request):
        """Crée un nouveau compte dont les données proviennent de google"""
        activation_key = "".join(
            [
                random.choice(
                    "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
                )
                for _ in range(24)
            ]
        )
        user = Utilisateurs.objects.create(
            nom=request.POST["name"],
            adresse_mail=request.POST["email"],
            mot_de_passe=request.POST["password"],
            cle_dactivation_de_compte=activation_key,
        )
        sent_mail_statut = AuxilliariesAuthentification().send_mail(
            "activation_account", user
        )  # Envoie de mail
        request.session["user_id"] = user.id  # Création de la session
        return redirect("../../user/home/")

    def render_valid_form_or_no_matched_password(self, initialize_form, request):
        """Vérifie si les mots de passes recu pour l'initialisation du mot de passe sont identiques"""
        if not initialize_form.is_valid():  # Formulaire pas valide
            context = {
                "initialize_form": InitializePasswordForm(),
                "search_form": SearchForm(),
                "initialize_password_form_error": initialize_form.errors.items(),
                "mail": request.POST["email"],
                "name": request.POST["name"],
            }
            context["initialize_form_errors"] = initialize_form.errors.items()
            return render(request, "initialisation_mot_de_passe.html", context)
        elif request.POST["password"] != request.POST["confirmation_password"]:
            context = {
                "initialize_form": InitializePasswordForm(),
                "search_form": SearchForm(),
                "no_match_password_error": True,
                "mail": request.POST["email"],
                "name": request.POST["name"],
            }
            return render(request, "initialisation_mot_de_passe.html", context)

    def check_valid_form_initialize_password(self, request):
        """Vérifie si le formulaire d'initialisation de mot de passe est valide"""
        initialize_form = InitializePasswordForm(request.POST)
        if initialize_form.is_valid() and (
            request.POST["password"] == request.POST["confirmation_password"]
        ):
            users_in_database = Utilisateurs.objects.filter(
                adresse_mail=request.POST["email"]
            )
            if len(users_in_database) == 0:  # Aucun utilisateur avec le mail recu
                return AuxilliariesAuthentification().make_initialize_password(request)
            else:  # Le mail recu appartient déjà à un autre utilisateur
                initialize_form = InitializePasswordForm()
                search_form = SearchForm()
                context = {
                    "initialize_form": initialize_form,
                    "search_form": search_form,
                    "mail": request.POST["email"],
                    "name": request.POST["name"],
                    "already_mail_error": True,
                }
                return render(request, "initialisation_mot_de_passe.html", context)
        else:
            return AuxilliariesAuthentification().render_valid_form_or_no_matched_password(
                initialize_form, request
            )
