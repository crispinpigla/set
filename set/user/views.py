import json
import copy

from django.shortcuts import render

from django.db.models import Q

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
from django.http import HttpResponse


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

    search_form = SearchForm()
    try:
        # Utilisateur connecté
        request.session["user_id"]
        user = Utilisateurs.objects.get(id=request.session["user_id"])
        contacts = Contact.objects.filter(contact_owner_id=request.session["user_id"])
        contenus = [contact.contact for contact in contacts]
        print(contenus)
        context = {"contenus": contenus, "search_form": search_form, "user":user}
        return render(request, "contact.html", context)
    except Exception as e:
        # Utilisateur non connecté
        return redirect("../../authentification/connexion/")


def message(request):
    """"""
    search_form = SearchForm()
    try:
        # Utilisateur connecté
        request.session["user_id"]
        user = Utilisateurs.objects.get(id=request.session["user_id"])
        messages0 = Message.objects.filter(
            Q(which_from=request.session["user_id"])
            | Q(which_to=request.session["user_id"])
        ).order_by("-date")
        users_messages = []

        # rangement des messages par autre utilisateur du message
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

        print("Le user message : ", users_messages)
        context = {"search_form": search_form, "messages": users_messages, "user": user}
        return render(request, "message.html", context)
    except Exception as e:
        # Utilisateur non connecté
        return redirect("../../authentification/connexion/")


def messages_exchanges(request, user_id):
    """"""
    search_form = SearchForm()
    message_form = MessageForm()
    try:
        # Utilisateur connecté
        request.session["user_id"]
        if int(user_id) == request.session["user_id"]:
            return redirect("../../authentification/connexion/")
        else:
            user = Utilisateurs.objects.get(id=request.session["user_id"])
            user_to = Utilisateurs.objects.get(id=user_id)
            messages = Message.objects.filter(
                (Q(which_from=request.session["user_id"]) & Q(which_to=user_id))
                | (Q(which_from=user_id) & Q(which_to=request.session["user_id"]))
            ).order_by("date")
            print(messages)
            context = {
                "search_form": search_form,
                "message_form": message_form,
                "messages": messages,
                "user_to": user_to,
                "user": user,
            }
            return render(request, "message_exchange.html", context)
    except Exception as e:
        # Utilisateur non connecté
        return redirect("../../authentification/connexion/")


def updates_messages(request, user_id):
    """Mises à jour des messages d'une discussion"""

    try:
        # Utilisateur connecté
        request.session["user_id"]
        if int(user_id) == request.session["user_id"]:
            return HttpResponse("l'expéditeur est le destinataire")
        else:
            user = Utilisateurs.objects.get(id=request.session["user_id"])
            user_to = Utilisateurs.objects.get(id=user_id)
            last_message = Message.objects.filter(id=request.GET["last_message_id"])
            if len(last_message) == 0:
                messages = Message.objects.filter(
                    (
                        (Q(which_from=request.session["user_id"]) & Q(which_to=user_id))
                        | (
                            Q(which_from=user_id)
                            & Q(which_to=request.session["user_id"])
                        )
                    )
                ).order_by("date")
            else:
                last_message = last_message[0]
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
                print(messages)
            context = {"messages": messages, "user": user}
            return render(request, "un_message.html", context)
    except Exception as e:
        # Utilisateur non connecté
        return redirect("../../authentification/connexion/")


def send_message(request, user_id):
    """"""

    try:
        # Utilisateur connecté
        request.session["user_id"]
        sender = Utilisateurs.objects.get(id=request.session["user_id"])
        receiver = Utilisateurs.objects.get(id=user_id)
        message_text = request.GET["message_text"]
        last_message_id = request.GET["last_message_id"]
        message = Message.objects.create(
            which_from=sender, which_to=receiver, contenu_text=message_text
        )
        print(message)
        context = {}
        reponse = (
            "le message text : "
            + message_text
            + " Le last message id"
            + str(last_message_id)
        )
        return HttpResponse(reponse)
        # return render(request, "message_exchange.html", context)
    except Exception as e:
        # Utilisateur non connecté
        return redirect("../../authentification/connexion/")


def deconnexion(request):
    """"""

    try:
        # Utilisateur connecté
        del request.session["user_id"]
        return redirect("../../")
    except Exception as e:
        # Utilisateur non connecté
        return redirect("../../authentification/connexion/")


def manage_contact(request, contact_id):
    """"""

    user = Utilisateurs.objects.get(id=request.session["user_id"])
    contact = Utilisateurs.objects.filter(id=contact_id)
    if len(contact) == 0:
        return HttpResponse("aucun contact avec cet id")
    else:
        contact = contact[0]
        check = Contact.objects.filter(contact_owner_id=user.id, contact_id=contact.id)
        if len(check) == 0:
            print("not in contacts")
            new_contact = Contact.objects.create(contact_owner=user, contact=contact)
            contacts = Contact.objects.filter(
                contact_owner_id=request.session["user_id"]
            )
            users_in_contact = [contact.contact for contact in contacts]
            print(contacts)
        else:
            print("in contacts")
            check[0].delete()
            contacts = Contact.objects.filter(
                contact_owner_id=request.session["user_id"]
            )
            users_in_contact = [contact.contact for contact in contacts]
            print(contacts)
        context = {"contenu": contact, "users_in_contact": users_in_contact}
        return render(request, "delete_add_contact.html", context)







def profil(request, user_id):
    """"""

    user = Utilisateurs.objects.get(id=request.session["user_id"]) 
    user_profil = Utilisateurs.objects.filter(id=user_id)
    context = { "user": user }

    if len(user_profil) == 0 :
        pass
    else:
        user_profil = user_profil[0]
        context['user_profil'] = user_profil

    print(user_profil)

    


    image_cover_form = ProfilImageForm()
    search_form = SearchForm()
    context['image_cover_form'] = image_cover_form
    context['search_form'] = search_form

    print(0)


    # section du set
    try:
        section_profil = request.GET["section_profil"]
    except Exception as e:
        section_profil = "sets"

    print(section_profil)
    print(context)
    print(1)

    context['section_profil'] = section_profil

    if section_profil == 'sets':
        sets_user_profil = SetUtilisateurs.objects.filter(utilisateur=user_profil)
        context['sets_user_profil'] = sets_user_profil
    elif section_profil == 'coordonees':
        set_name_form = SetNameForm()
        set_mail_form = SetMailForm()
        context['set_name_form'] = set_name_form
        context['set_mail_form'] = set_mail_form

    print(2)
    print(context)

    return render(request, "profil.html", context)



def update_image_cover(request):
    """"""

    try:
        # Utilisateur connecté
        request.session["user_id"]
        form = ProfilImageForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            user = Utilisateurs.objects.get(id=request.session["user_id"])
            user.image_profil = request.FILES["file"]
            user.save()
            print("ok")
            return redirect("../../user/profil/" + str(request.session["user_id"]) + "/?section_profil=coordonees" )
            #return HttpResponse('done')
        else:
            return HttpResponse('formulaire invalide')
        # return render(request, "message_exchange.html", context)
    except Exception as e:
        # Utilisateur non connecté
        return redirect("../../authentification/connexion/")



def update_profil_name(request):
    """"""

    try:
        # Utilisateur connecté
        request.session["user_id"]
        form = SetNameForm(request.POST)
        print(form)
        if form.is_valid():
            user = Utilisateurs.objects.get(id=request.session["user_id"])
            user.nom = request.POST["name"]
            user.save()
            print("ok")
            return redirect("../../user/profil/" + str(request.session["user_id"]) + "/?section_profil=coordonees" )
            #return HttpResponse('done')
        else:
            return HttpResponse('formulaire invalide')
        # return render(request, "message_exchange.html", context)
    except Exception as e:
        # Utilisateur non connecté
        return redirect("../../authentification/connexion/")

def update_profil_mail(request):
    """"""

    try:
        # Utilisateur connecté
        request.session["user_id"]
        form = SetMailForm(request.POST)
        print(form)
        if form.is_valid():
            user = Utilisateurs.objects.get(id=request.session["user_id"])
            user.adresse_mail = request.POST["mail"]
            user.save()
            print("ok")
            return redirect("../../user/profil/" + str(request.session["user_id"]) + "/?section_profil=coordonees" )
            #return HttpResponse('done')
        else:
            return HttpResponse('formulaire invalide')
        # return render(request, "message_exchange.html", context)
    except Exception as e:
        # Utilisateur non connecté
        return redirect("../../authentification/connexion/")




def suppression_compte(request):
    """"""

    try:
        # Utilisateur connecté
        request.session["user_id"]
        user = Utilisateurs.objects.get(id=request.session["user_id"])
        del request.session["user_id"]
        #return HttpResponse('done')
        user.delete()
        return redirect("../../authentification/connexion/")
    except Exception as e:
        # Utilisateur non connecté
        return redirect("../../authentification/connexion/")






def redirect_home(request):
    """"""

    return redirect("../../authentification/connexion/")
