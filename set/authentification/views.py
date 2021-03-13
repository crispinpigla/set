"""  Vue de l'application authentification  """


import random

import requests


from django.shortcuts import get_object_or_404

from django.shortcuts import redirect, render

from django.http import HttpResponse, Http404

from user.models import Utilisateurs

from user.auxilliaries_user.auxilliaries_user import AuxilliariesUser
from .auxilliaries_authentification.auxilliaries_authentification import (
    AuxilliariesAuthentification,
)

from .forms import (
    InscriptionForm,
    ConnexionForm,
    SearchForm,
    InitializePasswordForm,
    LinkResetPasswordForm,
    ResetPasswordForm,
)

# Create your views here.
from django.http import HttpResponse


def activation_compte(request):
    """Active un compte"""
    # Vérification connexion utilisateur
    user = AuxilliariesUser().get_user(request)
    if user:
        # Utilisateur connecté
        mail = request.GET["mail"]
        if user.adresse_mail == mail:
            # Le mail de l'utilisateur correspond au mail du compte recu
            if user.cle_dactivation_de_compte == request.GET["key_activation"]:
                user.statut_activation_compte = True
                user.cle_dactivation_de_compte = None
                user.save()
                return redirect("../../user/home/")
            else:
                # La clé d'activation recu ne correspond pas à celle qui est stockée
                raise Http404()
        else:
            # Le mail de l'utilisateur ne correspond pas au mail du compte recu
            raise Http404()
    else:
        # Utilisateur non connecté
        return redirect("../../authentification/connexion/")


def index(request):
    """Index."""
    if "authentification/" in request.build_absolute_uri():
        return redirect("connexion/")
    else:
        return redirect("authentification/connexion/")


def connexion(request):
    """Connecte un utilisateur à partir du formulaire de l'application"""
    try:  # Utilisateur connecté
        request.session["user_id"]
        return redirect("../../user/home/")
    except Exception as e:  # Utilisateur non connecté
        try:  # Traitement du formulaire de connexion
            request.POST["email"]
            connexion_form = ConnexionForm(request.POST)
            if connexion_form.is_valid():  # Formulaire valide
                users_in_database = Utilisateurs.objects.filter(
                    adresse_mail=request.POST["email"]
                )
                return AuxilliariesAuthentification().make_connexion(
                    users_in_database, request
                )
            else:
                if not connexion_form.is_valid():  # Formulaire pas valide
                    context = {
                        "connexion_form": ConnexionForm(),
                        "search_form": SearchForm(),
                        "form_errors": connexion_form.errors.items(),
                    }
                    return render(request, "connexion.html", context)
        except Exception as e:
            # Demande du formulaire de connexion
            connexion_form = ConnexionForm()
            search_form = SearchForm()
            context = {"connexion_form": connexion_form, "search_form": search_form}
            return render(request, "connexion.html", context)


def google_connect(request):
    """Connecte un utilisateur à partir de son compte google"""
    # Vérification connexion utilisateur
    user = AuxilliariesUser().get_user(request)
    if user:
        # Utilisateur connecté
        return redirect("../../user/home/")
    else:
        # Utilisateur non connecté
        response_google_user = requests.get(
            "https://oauth2.googleapis.com/tokeninfo?id_token=" + request.GET["token"]
        )
        if response_google_user.status_code == 200:
            # Requete vers l'api de google reussie
            google_user = response_google_user.json()
            check_user = Utilisateurs.objects.filter(adresse_mail=google_user["email"])
            if len(check_user) == 0:
                # Aucun utilisateur dans l'application avec ce mail
                return HttpResponse("Aucun utilisateur n'existe avec ce compte google")
            else:
                # Au moins un utilisateur existe dans l'application
                user = check_user[0]
                request.session["user_id"] = user.id
                return HttpResponse("Connexion done")
        else:
            # Echec de la requete vers l'api de google
            raise Http404()


def inscription(request):
    """Inscris un utilisateur à partir du formulaire de l'application"""
    try:
        # Utilisateur connecté
        request.session["user_id"]
        return redirect("../../user/home/")
    except Exception as e:
        # Utilisateur non connecté
        try:
            # Envoie du formulaire d'inscription
            request.POST["name"]
            inscription_form = InscriptionForm(request.POST)
            return AuxilliariesAuthentification().check_form_make_inscription(
                inscription_form, request
            )
        except Exception as e:
            # Demande du formulaire d'inscription
            inscription_form = InscriptionForm()
            search_form = SearchForm()
            context = {"inscription_form": inscription_form, "search_form": search_form}
            return render(request, "inscription.html", context)


def envoie_activation_compte(request):
    """Envoie un lien d'activation de compte"""
    # Vérification connexion utilisateur
    user = AuxilliariesUser().get_user(request)
    if user:
        # Utilisateur connecté
        activation_key = "".join(
            [
                random.choice(
                    "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
                )
                for _ in range(24)
            ]
        )
        user.cle_dactivation_de_compte = activation_key
        user.save()
        sent_mail_statut = AuxilliariesAuthentification().send_mail(
            "activation_account", user
        )
        return redirect("../../user/home/")
    else:
        # Utilisateur non connecté
        raise Http404()


def envoie_lien_reinitialisation_password(request):
    """Envoie un lien de réinitialisation de mot de passe"""
    user = AuxilliariesUser().get_user(request)  # Vérification connexion utilisateur
    if user:  # Utilisateur connecté
        request.session["user_id"]
        return redirect("../../user/home/")
    else:  # Utilisateur non connecté
        if (
            request.method == "POST"
        ):  # Traitement de l'envoie de lien de réinitialisation de mot de passe
            mail = request.POST["email"]
            try:
                user = Utilisateurs.objects.get(adresse_mail=mail)
            except Exception as e:
                user = None
            if user:  # Un utilisateur avec l'email recu existe
                return AuxilliariesAuthentification().render_reinitialize_password(
                    user, request
                )
            else:  # Aucun utilisateur avec l'email recu existe
                return AuxilliariesAuthentification().render_no_user_found_reinitialize_password(
                    mail, request
                )
        else:  # Demande de la page d'envoie de lien de réinitialisation de mot de passe
            link_reset_form = LinkResetPasswordForm()
            search_form = SearchForm()
            context = {"link_reset_form": link_reset_form, "search_form": search_form}
            return render(
                request, "envoie_lien_reinitialisation_mot_de_passe.html", context
            )


def reinitialisation_mot_de_passe(request):
    """Réinitialise un mot de passe"""
    user = AuxilliariesUser().get_user(request)  # Vérification connexion utilisateur
    if user:  # Utilisateur connecté
        return redirect("../../user/home/")
    else:  # Utilisateur non conecté
        if request.method == "POST":  # Exécution de la réinitialisation de mot de passe
            return AuxilliariesAuthentification().check_valid_form_reinitialize_password(
                request
            )
        else:  # Demande de la page de réinitialisation de mot de passe
            mail = request.GET["mail"]
            user = get_object_or_404(Utilisateurs, adresse_mail=mail)
            if (
                user.cle_de_reinitialisation_de_mot_de_passe
                == request.GET["key_reinitialisation_password"]
            ):
                reset_form = ResetPasswordForm()
                search_form = SearchForm()
                context = {
                    "reset_form": reset_form,
                    "search_form": search_form,
                    "user": user,
                    "mail": mail,
                }
                return render(request, "reinitialisation_mot_de_passe.html", context)
            else:  # La clé de réinitialisation recue ne correspond pas à celle qui est stockée
                raise Http404()


def initialisation_mot_de_passe(request):
    """Crée un nouveau compte à partir du compte google de l'utilisateur"""
    user = AuxilliariesUser().get_user(request)  # Vérification connexion utilisateur
    if user:  # Utilisateur connecté
        return redirect("../../user/home/")
    else:  # Utilisateur non conecté
        if request.method == "POST":  # Traitement de la soummission du mot de passe
            return AuxilliariesAuthentification().check_valid_form_initialize_password(
                request
            )
        else:  # Demande du formulaire de l'initialisation du mot de passe
            initialize_form = InitializePasswordForm()
            search_form = SearchForm()
            context = {
                "initialize_form": initialize_form,
                "search_form": search_form,
                "mail": request.GET["mail"],
                "name": request.GET["name"],
            }
            return render(request, "initialisation_mot_de_passe.html", context)
