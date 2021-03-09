"""   Vue de l'application user   """

from django.shortcuts import render

from .auxilliaries_user.auxilliaries_user import AuxilliariesUser

from .forms import SearchForm, ProfilImageForm, SetNameForm, SetMailForm

from .models import Utilisateurs, Contact

from django.shortcuts import redirect

# Create your views here.
from django.http import Http404


def home(request):
    """Acceuil d'un utilisateur connecté"""
    # Vérification de la connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)
    if user:
        # Utilisateur connecté
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            return auxilliary_user.render_unactivate_or_locked_account(user, request)
        else:
            # le compte est activé et n'est pas bloqué
            return auxilliary_user.render_home(user, request)
    else:
        # Utilisateur pas connecté
        return redirect("../authentification/connexion/")


def contacts(request):
    """Contacts d'un utilisateur"""
    # Vérification de la connexion utilisateur
    user = AuxilliariesUser().get_user(request)
    if user:
        # Utilisateur connecté
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            return AuxilliariesUser().redirect_unactivate_locked_user(user, "../home/")
        else:
            # le compte est activé et n'est pas bloqué
            search_form = SearchForm()
            contacts = Contact.objects.filter(
                contact_owner_id=request.session["user_id"]
            )
            contenus = [contact.contact for contact in contacts]
            users_in_contact = list(contenus)
            context = {
                "contenus": contenus,
                "users_in_contact": users_in_contact,
                "search_form": search_form,
                "user": user,
            }
            return render(request, "contact.html", context)
    else:
        # Utilisateur non connecté
        raise Http404()


def message(request):
    """Messages d'un utilisateur"""
    # Vérification de la connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)
    if user:
        # Utilisateur connecté
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            return AuxilliariesUser().redirect_unactivate_locked_user(user, "../home/")
        else:
            # le compte est activé et n'est pas bloqué
            search_form = SearchForm()
            request.session["user_id"]
            user = Utilisateurs.objects.get(id=request.session["user_id"])
            context = {
                "search_form": search_form,
                "messages": AuxilliariesUser().get_lasts_messages_user(request),
                "user": user,
            }
            return render(request, "message.html", context)
    else:
        # Utilisateur non connecté
        raise Http404()


def messages_exchanges(request, user_id):
    """Messages échangés d'une conversation"""
    # Vérification de la connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)
    correspondant = auxilliary_user.user_in_application(user_id)
    if user:
        # Utilisateur connecté
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            return AuxilliariesUser().redirect_unactivate_locked_user(
                user, "../../../user/home/"
            )
        else:
            # le compte est activé et n'est pas bloqué
            if correspondant:
                # Le correspondant est un utilisateur existant dans l'application
                if correspondant != user:
                    # Le correspondant est différent de l'utilisateur
                    return AuxilliariesUser().render_messages_exchanges(
                        request, correspondant, user
                    )
                else:
                    # Le correspondant est égal à l'utilisateur
                    raise Http404()
            else:
                # Le contact n'est pas un utilisateur existant de l'application
                raise Http404()
    else:
        # Utilisateur non connecté
        raise Http404()


def updates_messages(request, user_id):
    """Mises à jour des messages d'une discussion"""

    # Vérification de la connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)
    correspondant = auxilliary_user.user_in_application(user_id)

    if user:
        # Utilisateur connecté
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            return AuxilliariesUser().httpresponse_unactivate_locked_user(user)
        else:
            # le compte est activé et n'est pas bloqué
            if correspondant:
                # Le correspondant est un utilisateur existant dans l'application
                if correspondant != user:
                    # Le correspondant est différent de l'utilisateur
                    return AuxilliariesUser().render_update_messages(
                        request, correspondant, user
                    )
                else:
                    # Le correspondant est égal à l'utilisateur
                    raise Http404()
            else:
                # Le contact n'est pas un utilisateur existant de l'application
                raise Http404()
    else:
        # Utilisateur non connecté
        raise Http404()


def send_message(request, user_id):
    """Envoie d'un message"""
    # Vérification de la connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)
    correspondant = auxilliary_user.user_in_application(user_id)
    if user:
        # Utilisateur connecté
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            return AuxilliariesUser().httpresponse_unactivate_locked_user(user)
        else:
            # le compte est activé et n'est pas bloqué
            if correspondant:
                # Le correspondant est un utilisateur existant dans l'application
                if correspondant != user:
                    # Le correspondant est différent de l'utilisateur
                    return AuxilliariesUser().http_send_message(
                        request, correspondant, user
                    )
                else:
                    # Le correspondant est égal à l'utilisateur
                    raise Http404()
            else:
                # Le contact n'est pas un utilisateur existant de l'application
                raise Http404()
    else:
        # Utilisateur non connecté
        raise Http404()


def deconnexion(request):
    """Déconnecte un utilisateur"""
    # Vérification de la connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)
    if user:
        # Utilisateur connecté
        del request.session["user_id"]
        return redirect("../../")
    else:
        # Utilisateur non connecté
        raise Http404()


def manage_contact(request, contact_id):
    """Ajoute et supprime un contact"""
    # Vérification de la connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)
    contact = auxilliary_user.user_in_application(contact_id)
    if user:
        # Utilisateur connecté
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            return AuxilliariesUser().httpresponse_unactivate_locked_user(user)
        else:
            # le compte est activé et n'est pas bloqué
            if contact:
                # Le contact est un utilisateur existant dans l'application
                return AuxilliariesUser().check_delete_add_contact(user, contact)
            else:
                # Le contact n'est pas un utilisateur existant de l'application
                raise Http404()
    else:
        # Utilisateur non connecté
        raise Http404()


def profil(request, user_id):
    """Affiche le profil d'un utilisateur"""
    # Vérification de la connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)
    target = auxilliary_user.user_in_application(user_id)

    if user:
        # Utilisateur connecté
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            return AuxilliariesUser().redirect_unactivate_locked_user(
                user, "../../home/"
            )
        else:
            # le compte est activé et n'est pas bloqué
            return AuxilliariesUser().get_profil_connected_user(user, target, request)
    else:
        # Utilisateur non connecté
        context = {"user": user}
        if target:
            # La cible est un utilisateur existant dans l'application
            return AuxilliariesUser().get_profil_unconnected_user(
                target, context, request
            )
        else:
            # La cible n'est pas un utilisateur existant de l'application
            raise Http404()


def update_image_cover(request):
    """Met à jour l'image de profil d'un utilisateur"""
    # Vérification de la connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)
    if user:
        # Utilisateur connecté
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            return AuxilliariesUser().redirect_unactivate_locked_user(
                user, "../../home/"
            )
        else:
            # le compte est activé et n'est pas bloqué
            form = ProfilImageForm(request.POST, request.FILES)
            if form.is_valid():
                user = Utilisateurs.objects.get(id=request.session["user_id"])
                user.image_profil = request.FILES["file"]
                user.save()
                return redirect(
                    "../../user/profil/"
                    + str(request.session["user_id"])
                    + "/?section_profil=coordonees"
                )
            else:
                # Formulaire invalide
                raise Http404()
    else:
        # Utilisateur non connecté
        raise Http404()


def update_profil_name(request):
    """Met à jour le nom d'un utilisateur"""

    # Vérification de la connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)
    if user:
        # Utilisateur connecté
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            return AuxilliariesUser().redirect_unactivate_locked_user(
                user, "../../home/"
            )
        else:
            # le compte est activé et n'est pas bloqué
            form = SetNameForm(request.POST)
            if form.is_valid():
                user.nom = request.POST["name"]
                user.save()
                return redirect(
                    "../../user/profil/"
                    + str(request.session["user_id"])
                    + "/?section_profil=coordonees"
                )
            else:
                # Formulaire invalide
                raise Http404()
    else:
        # Utilisateur non connecté
        raise Http404()


def update_profil_mail(request):
    """Met à jour le mail d'un utilisateur"""
    # Vérification de la connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)

    if user:
        # Utilisateur connecté
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            return AuxilliariesUser().redirect_unactivate_locked_user(
                user, "../../home/"
            )
        else:
            # le compte est activé et n'est pas bloqué
            form = SetMailForm(request.POST)
            if form.is_valid():
                user.adresse_mail = request.POST["mail"]
                user.save()
                return redirect(
                    "../../user/profil/"
                    + str(request.session["user_id"])
                    + "/?section_profil=coordonees"
                )
            else:
                # Formulaire invalide
                raise Http404()
    else:
        # Utilisateur non connecté
        raise Http404()


def suppression_compte(request):
    """Supprime un compte"""
    # Vérification de la connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)
    if user:
        # Utilisateur connecté
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            return AuxilliariesUser().redirect_unactivate_locked_user(
                user, "../../home/"
            )
        else:
            # le compte est activé et n'est pas bloqué
            del request.session["user_id"]
            user.delete()
            return redirect("../../authentification/connexion/")
    else:
        # Utilisateur non connecté
        raise Http404()


def redirect_home(request):
    """"""
    return redirect("../../authentification/connexion/")
