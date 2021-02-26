import json
import copy

from django.shortcuts import render, get_object_or_404

from django.db.models import Q

from .auxilliaries_user.auxilliaries_user import AuxilliariesUser

from .forms import SearchForm, MessageForm, ProfilImageForm, SetNameForm, SetMailForm

from .models import Utilisateurs, Contact, Message
from sets.models import (
    Sets,
    SetUtilisateurs,
    Evenements,
    PublicationSet,
    JaimePublicationSet,
)

from django.shortcuts import redirect

# Create your views here.
from django.http import HttpResponse, Http404


def home(request):
    """"""

    try:
        # Utilisateur connecté
        request.session["user_id"]
        user = Utilisateurs.objects.get(pk=request.session["user_id"])
        sets_user = SetUtilisateurs.objects.filter(utilisateur=user)
        publications = []

        for set_user in sets_user:
            publications0 = PublicationSet.objects.filter(set0=set_user.set0)
            for publication in publications0:
                publications.append(publication)

        publications = publications[:10]
        publications_likeurs = []
        for publication in publications:
            publications_likeurs.append(
                [
                    publication,
                    JaimePublicationSet.objects.filter(
                        publication_set_id=publication.id
                    ),
                    JaimePublicationSet.objects.filter(
                        publication_set_id=publication.id,
                        jaimeur_id=request.session["user_id"],
                    ),
                ]
            )

        search_form = SearchForm()
        context = {
            "search_form": search_form,
            "user": user,
            "publications_likeurs": publications_likeurs,
        }
        return render(request, "acceuil.html", context)

    except Exception as e:
        # Utilisateur non connecté
        return redirect("../authentification/connexion/")



def contacts(request):
    """"""

    # Vérification de la connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)

    if user:
        # Utilisateur connecté
        search_form = SearchForm()
        contacts = Contact.objects.filter(contact_owner_id=request.session["user_id"])
        contenus = [contact.contact for contact in contacts]
        users_in_contact = list(contenus)
        context = {"contenus": contenus, "users_in_contact":users_in_contact, "search_form": search_form, "user":user}
        return render(request, "contact.html", context)
    else:
        # Utilisateur non connecté
        raise Http404()


def message(request):
    """"""

    # Vérification de la connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)

    if user:
        # Utilisateur connecté
        search_form = SearchForm()
        request.session["user_id"]
        user = Utilisateurs.objects.get(id=request.session["user_id"])
        messages0 = Message.objects.filter(
            Q(which_from=request.session["user_id"])
            | Q(which_to=request.session["user_id"])
        ).order_by("-date")
        users_messages = []

        # rangement des messages par auteur du message
        for message in messages0:
            if message.which_from.id == request.session["user_id"]:
                users_messages.append({"other": message.which_to, "message": message})
            elif message.which_to.id == request.session["user_id"]:
                users_messages.append({"other": message.which_from, "message": message})

        # rangement des messages selon qu'ils soient derniers dans la discussion ou non
        users_already_messages = []
        for user_messages in users_messages:
            if user_messages["other"] in users_already_messages:
                user_messages["last_message"] = False
            elif user_messages["other"] not in users_already_messages:
                user_messages["last_message"] = True
                users_already_messages.append(user_messages["other"])
        context = {"search_form": search_form, "messages": users_messages, "user": user}
        return render(request, "message.html", context)
    else:
        # Utilisateur non connecté
        raise Http404()



def messages_exchanges(request, user_id):
    """"""

    # Vérification de la connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)
    correspondant = auxilliary_user.user_in_application(user_id)

    if user:
        # Utilisateur connecté
        if correspondant:
            # Le correspondant est un utilisateur existant dans l'application
            if correspondant != user:
                # Le correspondant est différent de l'utilisateur
                search_form = SearchForm()
                message_form = MessageForm()
                messages = Message.objects.filter(
                    (Q(which_from=request.session["user_id"]) & Q(which_to=user_id))
                    | (Q(which_from=user_id) & Q(which_to=request.session["user_id"]))
                ).order_by("date")
                context = {
                    "search_form": search_form,
                    "message_form": message_form,
                    "messages": messages,
                    "user_to": correspondant,
                    "user": user,
                }
                return render(request, "message_exchange.html", context)
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
        if correspondant:
            # Le correspondant est un utilisateur existant dans l'application
            if correspondant != user:
                # Le correspondant est différent de l'utilisateur
                last_message = auxilliary_user.message_in_application(request.GET["last_message_id"])
                if last_message:
                    # Un dernier message n'existe pas avec l'id recu
                    #last_message = last_message[0]
                    messages = Message.objects.filter(
                        (
                            (Q(which_from=request.session["user_id"]) & Q(which_to=user_id))
                            | (
                                Q(which_from=user_id)
                                & Q(which_to=request.session["user_id"])
                            )
                        )
                        & Q(date__gt=last_message.date)
                    ).order_by("date")
                else:
                    # Un dernier message existe avec l'id recu
                    messages = Message.objects.filter(
                        (
                            (Q(which_from=request.session["user_id"]) & Q(which_to=user_id))
                            | (
                                Q(which_from=user_id)
                                & Q(which_to=request.session["user_id"])
                            )
                        )
                    ).order_by("date")
                context = {"messages": messages, "user": user}
                return render(request, "un_message.html", context)
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
    """"""

    # Vérification de la connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)
    correspondant = auxilliary_user.user_in_application(user_id)

    if user:
        # Utilisateur connecté
        if correspondant:
            # Le correspondant est un utilisateur existant dans l'application
            if correspondant != user:
                # Le correspondant est différent de l'utilisateur
                message_text = request.GET["message_text"]
                message = Message.objects.create(
                    which_from=user, which_to=correspondant, contenu_text=message_text
                )
                return HttpResponse('send')
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
    """"""

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
    """"""

    # Vérification de la connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)
    contact = auxilliary_user.user_in_application(contact_id)

    if user:
        # Utilisateur connecté
        if contact:
            # Le contact est un utilisateur existant dans l'application
            check = Contact.objects.filter(contact_owner_id=user.id, contact_id=contact.id)
            if len(check) == 0:
                new_contact = Contact.objects.create(contact_owner=user, contact=contact)
                return HttpResponse("contact_added")
            else:
                check[0].delete()
                return HttpResponse("contact_deleted")
        else:
            # Le contact n'est pas un utilisateur existant de l'application
            raise Http404()
    else:
        # Utilisateur non connecté
        raise Http404()










def profil(request, user_id):
    """"""


    # Vérification de la connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)
    target = auxilliary_user.user_in_application(user_id)

    if user:
        # Utilisateur connecté
        context = { "user": user }
        if target:
            # La cible est un utilisateur existant dans l'application
            context['user_profil'] = target
            search_form = SearchForm()
            context['search_form'] = search_form
            # section du profil
            try:
                section_profil = request.GET["section_profil"]
            except Exception as e:
                section_profil = "sets"
            context['section_profil'] = section_profil

            if target != user:
                # La cible est différente de l'utilisateur
                if section_profil == 'sets':
                    sets_user_profil = SetUtilisateurs.objects.filter(utilisateur=target)
                    context['sets_user_profil'] = sets_user_profil
                elif section_profil == 'coordonees':
                    pass
                else:
                    raise Http404()
            else:
                # La cible est égal à l'utilisateur
                image_cover_form = ProfilImageForm()
                context['image_cover_form'] = image_cover_form
                if section_profil == 'sets':
                    sets_user_profil = SetUtilisateurs.objects.filter(utilisateur=target)
                    context['sets_user_profil'] = sets_user_profil
                elif section_profil == 'coordonees':
                    set_name_form = SetNameForm()
                    set_mail_form = SetMailForm()
                    context['set_name_form'] = set_name_form
                    context['set_mail_form'] = set_mail_form
                else:
                    raise Http404()
            return render(request, "profil.html", context)
        else:
            # La cible n'est pas un utilisateur existant de l'application
            raise Http404()
    else:
        # Utilisateur non connecté
        context = { }
        if target:
            # La cible est un utilisateur existant dans l'application
            context['user_profil'] = target
            search_form = SearchForm()
            context['search_form'] = search_form
            # section du profil
            try:
                section_profil = request.GET["section_profil"]
            except Exception as e:
                section_profil = "sets"
            context['section_profil'] = section_profil

            # La cible est différente de l'utilisateur
            if section_profil == 'sets':
                sets_user_profil = SetUtilisateurs.objects.filter(utilisateur=target)
                context['sets_user_profil'] = sets_user_profil
            elif section_profil == 'coordonees':
                pass
            else:
                raise Http404()

            return render(request, "profil.html", context)
        else:
            # La cible n'est pas un utilisateur existant de l'application
            raise Http404()





def update_image_cover(request):
    """"""

    # Vérification de la connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)

    if user:
        # Utilisateur connecté
        form = ProfilImageForm(request.POST, request.FILES)
        if form.is_valid():
            user = Utilisateurs.objects.get(id=request.session["user_id"])
            user.image_profil = request.FILES["file"]
            user.save()
            return redirect("../../user/profil/" + str(request.session["user_id"]) + "/?section_profil=coordonees" )
        else:
            # Formulaire invalide
            raise Http404()
    else:
        # Utilisateur non connecté
        raise Http404()



def update_profil_name(request):
    """"""

    # Vérification de la connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)

    if user:
        # Utilisateur connecté
        form = SetNameForm(request.POST)
        if form.is_valid():
            user.nom = request.POST["name"]
            user.save()
            return redirect("../../user/profil/" + str(request.session["user_id"]) + "/?section_profil=coordonees" )
        else:
            # Formulaire invalide
            raise Http404()
    else:
        # Utilisateur non connecté
        raise Http404()



def update_profil_mail(request):
    """"""

    # Vérification de la connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)

    if user:
        # Utilisateur connecté
        form = SetMailForm(request.POST)
        if form.is_valid():
            user.adresse_mail = request.POST["mail"]
            user.save()
            return redirect("../../user/profil/" + str(request.session["user_id"]) + "/?section_profil=coordonees" )
        else:
            # Formulaire invalide
            raise Http404()
    else:
        # Utilisateur non connecté
        raise Http404()



def suppression_compte(request):
    """"""

    # Vérification de la connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)

    if user:
        # Utilisateur connecté
        del request.session["user_id"]
        user.delete()
        return redirect("../../authentification/connexion/")
    else:
        # Utilisateur non connecté
        raise Http404()







def redirect_home(request):
    """"""

    return redirect("../../authentification/connexion/")
