from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect

from .models import Sets, SetUtilisateurs, PublicationSet, JaimePublicationSet, Evenements, PublicationEvenement, JaimePublicationEvenement
from user.models import Utilisateurs

from .forms import (
    SearchForm,
    SetCoverImageForm,
    SetDescriptionSetForm,
    PublicationSetForm, SetDescriptionSetEvent, PublicationEventForm
)


def sets(request, set_id):
    """"""

    set0 = Sets.objects.filter(id=set_id)


    # Récupération des publications
    publications = PublicationSet.objects.filter(set0_id=set_id)
    publications_likeurs = []
    for publication in publications:
        publications_likeurs.append([publication, JaimePublicationSet.objects.filter(publication_set_id=publication.id), JaimePublicationSet.objects.filter(publication_set_id=publication.id, jaimeur_id=request.session["user_id"])])


    if len(set0) != 0:
        set0 = set0[0]

        # Récupération des évènements
        events = Evenements.objects.filter(set0_id=set0.id)

        # Récupération des utilisateurs
        users_set = SetUtilisateurs.objects.filter(set0_id=set0.id)

        # statut set de l'utilisateur dans le set
        administrator_status = False
        for user_set in users_set:
            if user_set.utilisateur_id == request.session["user_id"]:
                user_intermedaire_table = SetUtilisateurs.objects.get(
                    utilisateur_id=request.session["user_id"], set0_id=set0.id
                )
                if user_intermedaire_table.statut == "administrateur":
                    administrator_status = True

        # section du set
        try:
            section = request.GET["section"]
        except Exception as e:
            section = "publications"

        search_form = SearchForm()
        image_cover_form = SetCoverImageForm()
        set_description_form = SetDescriptionSetForm()
        new_post_form = PublicationSetForm()
        context = {
            "search_form": search_form,
            "image_cover_form": image_cover_form,
            "set_description_form": set_description_form,
            "new_post_form": new_post_form,
            "set": set0,
            "administrator_status": administrator_status,
            "section": section,
            "publications_likeurs": publications_likeurs,
            "users_set": users_set,
            "events":events,
        }
        return render(request, "set.html", context)
    else:
        return HttpResponse("Aucun set avec cet id")


def evenements(request, event_id):
    """"""

    # evenement
    event = Evenements.objects.filter(id=event_id)

    if len(event) != 0:

        event = event[0]

        # publications de l'évènement
        publications = PublicationEvenement.objects.filter(evenement_id=event_id)
        publications_likeurs = []
        for publication in publications:
            publications_likeurs.append([publication, JaimePublicationEvenement.objects.filter(publication_evenement_id=publication.id), JaimePublicationEvenement.objects.filter(publication_evenement_id=publication.id, jaimeur_id=request.session["user_id"])])

        # set
        set0 = event.set0

        # Récupération des utilisateurs
        users_set = SetUtilisateurs.objects.filter(set0_id=set0.id)

        # statut évènement de l'utilisateur dans le set
        administrator_status = False
        for user_set in users_set:
            if user_set.utilisateur_id == request.session["user_id"]:
                user_intermedaire_table = SetUtilisateurs.objects.get(
                    utilisateur_id=request.session["user_id"], set0_id=set0.id
                )
                if user_intermedaire_table.statut == "administrateur":
                    administrator_status = True

        search_form = SearchForm()
        event_description_form = SetDescriptionSetEvent()
        new_post_form = PublicationEventForm()
        context = {
            "search_form": search_form,
            "event_description_form": event_description_form,
            "new_post_form": new_post_form,
            "set": set0,
            "administrator_status": administrator_status,
            "publications_likeurs": publications_likeurs,
            "users_set": users_set,
            "event":event,
        }
        return render(request, "evenement.html", context)



def search(request):
    """"""

    #print(request.GET["search_input"])

    search_form = SearchForm()

    # section du set
    try:
        section = request.GET["section"]
    except Exception as e:
        section = "sets"

    if section == "personnes":
        contenus = Utilisateurs.objects.filter(nom=request.GET["search_input"])
    elif section == "evenements":
        contenus = Evenements.objects.filter(nom=request.GET["search_input"])
    elif section == "sets":
        contenus = Sets.objects.filter(nom=request.GET["search_input"])

    print(contenus)

    context = { "search_form": search_form, "section":section, "contenus":contenus, "recherche":request.GET["search_input"] }
    return render(request, "search.html", context)




def update_cover(request):
    """"""

    print(request.GET["set_id"])

    form = SetCoverImageForm(request.POST, request.FILES)
    print(form)
    if form.is_valid():
        set0 = Sets.objects.get(id=request.GET["set_id"])
        set0.image_couverture = request.FILES["file"]
        set0.save()
        print("ok")
        return redirect("../../sets/set/" + str(set0.id) + "/")
    else:
        return HttpResponse("Formulaire invalide")


def make_post_set(request, set_id):
    """"""

    post_form = PublicationSetForm(request.POST, request.FILES)
    if post_form.is_valid():
        set0 = Sets.objects.get(id=set_id)
        user = Utilisateurs.objects.get(id=request.session["user_id"])
        post = PublicationSet.objects.create(
            set0=set0,
            auteur=user,
            contenu_text=request.POST["publication_text"],
            media1=request.FILES.get("file_1", ""),
            media2=request.FILES.get("file_2", ""),
        )
        return redirect("../../set/" + str(set0.id) + "/")
    else:
        return HttpResponse("Formulaire invalide")



def make_post_event(request, event_id):
    """"""

    post_form = PublicationEventForm(request.POST, request.FILES)
    if post_form.is_valid():
        event = Evenements.objects.get(id=event_id)
        user = Utilisateurs.objects.get(id=request.session["user_id"])
        post = PublicationEvenement.objects.create(
            evenement=event,
            auteur=user,
            contenu_text=request.POST["publication_text"],
            media1=request.FILES.get("file_1", ""),
            media2=request.FILES.get("file_2", ""),
        )
        return redirect("../../event/" + str(event.id) + "/")
    else:
        return HttpResponse("Formulaire invalide")



def manage_like_post_set(request, post_id):
    """"""

    user = Utilisateurs.objects.get(id=request.session["user_id"])
    publication_set = PublicationSet.objects.get(id=post_id)
    check = JaimePublicationSet.objects.filter(publication_set_id=post_id, jaimeur_id=request.session["user_id"])
    if len(check) == 0 :
        like = JaimePublicationSet.objects.create(
            publication_set=publication_set,
            jaimeur=user,
        )
        return HttpResponse("like_make")
    else:
        check[0].delete()
        return HttpResponse("unlike_make")




def manage_like_post_event(request, post_id):
    """"""

    user = Utilisateurs.objects.get(id=request.session["user_id"])
    publication_event = PublicationEvenement.objects.get(id=post_id)
    print(publication_event)
    check = JaimePublicationEvenement.objects.filter(publication_evenement_id=post_id, jaimeur_id=request.session["user_id"])
    if len(check) == 0 :
        like = JaimePublicationEvenement.objects.create(
            publication_evenement=publication_event,
            jaimeur=user,
        )
        return HttpResponse("like_make")
    else:
        check[0].delete()
        return HttpResponse("unlike_make")