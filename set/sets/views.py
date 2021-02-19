from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect

from .models import Sets, SetUtilisateurs, PublicationSet, JaimePublicationSet, Evenements, PublicationEvenement, JaimePublicationEvenement
from user.models import Utilisateurs, Contact

from .forms import (
    CreateSetForm,
    CreateEventForm,
    SearchForm,
    SetCoverImageForm,
    SetDescriptionSetForm,
    PublicationSetForm, SetDescriptionSetEvent, PublicationEventForm
)




def creation_set(request):
    """"""

    try:
        # Utilisateur connecté
        request.session["user_id"]
        try:
            # Reception du formulaire de creation de set
            request.POST["csrfmiddlewaretoken"]
            create_set_form = CreateSetForm(request.POST, request.FILES)
            if create_set_form.is_valid():
                user = Utilisateurs.objects.get(pk=request.session["user_id"])
                set0 = Sets.objects.create(
                    nom=request.POST["name"],
                    image_couverture=request.FILES["file"],
                    type0=request.POST["type_set"],
                    description=request.POST["description"],
                )
                set_user = SetUtilisateurs.objects.create(
                    set0=set0, utilisateur=user, statut="administrateur"
                )
                return redirect("../../sets/set/" + str(set0.id) + "/")
            else:
                if not create_set_form.is_valid():
                    # Formulaire pas valide
                    create_set_form.errors.items()
                    print(create_set_form.errors.items())
                    return HttpResponse("Formulaire pas valide")
        except Exception as e:
            # Demande du formulaire de creation de set
            create_set_form = CreateSetForm()
            search_form = SearchForm()
            context = {"create_set_form": create_set_form, "search_form": search_form}
            # request.session["user_id"] = 1
            return render(request, "creation_set.html", context)

        search_form = SearchForm()
        create_set_form = CreateSetForm()
        context = {"search_form": search_form, "create_set_form": create_set_form}
        return render(request, "creation_set.html", context)

    except Exception as e:
        # Utilisateur non connecté
        return redirect("../../authentification/connexion/")


def creation_evenement(request, set_id):
    """"""

    set0 = Sets.objects.filter(id=set_id)
    set0 = set0[0]

    try:
        # Utilisateur connecté
        request.session["user_id"]
        try:
            # Reception du formulaire de creation de set
            request.POST["csrfmiddlewaretoken"]
            create_event_form = CreateEventForm(request.POST)
            if create_event_form.is_valid():
                user = Utilisateurs.objects.get(pk=request.session["user_id"])
                event = Evenements.objects.create(
                    set0=set0,
                    nom=request.POST["name"],
                    description=request.POST["description"],
                )
                return redirect("../../sets/evenement/" + str(event.id) + "/")
            else:
                if not create_event_form.is_valid():
                    # Formulaire pas valide
                    create_event_form.errors.items()
                    print(create_event_form.errors.items())
                    return HttpResponse("Formulaire pas valide")
        except Exception as e:
            # Demande du formulaire de creation de set
            create_event_form = CreateEventForm()
            search_form = SearchForm()
            context = {
                "create_event_form": create_event_form,
                "search_form": search_form,
                "set": set0,
            }
            return render(request, "creation_evenement.html", context)

        # search_form = SearchForm()
        # context = { "search_form":search_form }
        # return render(request, "creation_evenement.html", context)

    except Exception as e:
        # Utilisateur non connecté
        return redirect("../../authentification/connexion/")









def sets(request, set_id):
    """"""

    try:
        request.session["user_id"]
        user = Utilisateurs.objects.get(id=request.session["user_id"])

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
            users_set_list = [ user_set.utilisateur for user_set in users_set ]
            users_set_dictionnary = { user_set.utilisateur:user_set for user_set in users_set }
            print(users_set_dictionnary)

            # Récupération des contacts
            contacts = Contact.objects.filter(contact_owner_id=request.session["user_id"])
            contacts_list = [ contact.contact for contact in contacts ]

            # statut set de l'utilisateur dans le set
            administrator_status = False
            if ( user in users_set_dictionnary ):
                print(' le  ---- ', users_set_dictionnary[user].statut)
                if users_set_dictionnary[user].statut == "administrateur":
                    administrator_status = True
                    print('est administrateur')


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
                "users_set_list":users_set_list,
                "events":events,
                "contacts":contacts,
                "contacts_list":contacts_list,
                "user":user,
            }
            return render(request, "set.html", context)
        else:
            return HttpResponse("Aucun set avec cet id")

    except Exception as e:
        return HttpResponse('Utilisateur non connecté')



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

    context = { "recherche":request.GET["search_input"] }

    search_form = SearchForm()
    context['search_form'] = search_form

    # section du set
    try:
        section = request.GET["section"]
    except Exception as e:
        section = "sets"
    context['section'] = section

    try:
        request.session["user_id"]
        user = Utilisateurs.objects.get(id=request.session["user_id"])
    except Exception as e:
        user = False
        
    context['user'] = user

    if section == "personnes":
        contenus = Utilisateurs.objects.filter(nom=request.GET["search_input"])
        try:
            owner = Utilisateurs.objects.get(id=request.session["user_id"])
            contacts = Contact.objects.filter(contact_owner_id=request.session["user_id"])
            users_in_contact = [ contact.contact for contact in contacts ]
            context['is_connected'] = True
        except Exception as e:
            users_in_contact = []
            owner = None
        context['users_in_contact'] = users_in_contact
        context['owner'] = owner
    elif section == "evenements":
        contenus = Evenements.objects.filter(nom=request.GET["search_input"])
    elif section == "sets":
        contenus = Sets.objects.filter(nom=request.GET["search_input"])
    context['contenus'] = contenus


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
    print(0)
    user = Utilisateurs.objects.get(id=request.session["user_id"])
    publication_set = PublicationSet.objects.get(id=post_id)
    print(1)
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


def delete_add_user_set(request, set_id, user_delete_add_id):
    """"""

    try:
        confirm_enter = request.GET['confirm_enter']
        set_user  = SetUtilisateurs.objects.get(set0_id=set_id, utilisateur_id=user_delete_add_id)
        set0 = Sets.objects.get(id=set_id)
        if confirm_enter == 'yes':
            set_user.statut = 'dans_set'
            set_user.save()
            #return render(request, "sortie_set.html", { "user_set":set_user, 'set':set0 })
            return HttpResponse('confirmation_done')

        elif confirm_enter == 'no':
            print(0)
            set_user.delete()
            set_users_admin  = SetUtilisateurs.objects.filter(set0_id=set_id, statut='administrateur')
            if len(set_users_admin) == 0:
                print(1)
                # Aucun administrateur dans le set après la sortie de l'utilisateur
                set_users  = SetUtilisateurs.objects.filter(set0_id=set_id).order_by("date")
                if len(set_users) == 0 :
                    # Aucun utilisateur dans le set
                    set0.delete()
                    #set_envent = Evenements.objects.filter(set0_id=set_id)
                    #set_posts = PublicationSet.objects.filter(set0_id=set_id)

                    print(2)
                    return HttpResponse("delete_user_and_set_done")
                else:
                    # Au moins un utilisateur dans le set
                    print(3)
                    set_users[0].statut = 'administrateur'
                    set_users[0].save()
                    return HttpResponse('delete_done')
            else:
                return HttpResponse('delete_done')

    except Exception as e:
        check  = SetUtilisateurs.objects.filter(set0_id=set_id, utilisateur_id=user_delete_add_id)
        if len(check) == 0 :
            # Aucun utilisateur de cet id n'appartient au set de cet id
            user_delete_add = Utilisateurs.objects.filter(id=user_delete_add_id)
            set0 = Sets.objects.filter(id=set_id)
            if  len(user_delete_add) == 0 or len(set0) == 0 :
                # Aucun utilisateur n'existe avec l'id utilisateur recue ou aucun set n'existe avec l'id de set recu
                return HttpResponse("parametre(s) invalide(s)")
            else:
                SetUtilisateurs.objects.create(set0=set0[0], utilisateur=user_delete_add[0], statut='attente_validation')
                return render(request, "delete_user_set.html", {})
        else:
            check[0].delete()
            return render(request, "add_user_set.html", {})

        return HttpResponse("here")
