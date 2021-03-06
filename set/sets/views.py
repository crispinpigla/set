from django.shortcuts import render, get_object_or_404

from django.template.loader import render_to_string

# Create your views here.
from django.http import HttpResponse, Http404
from django.shortcuts import redirect

from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail import send_mail, EmailMessage
import smtplib

from user.auxilliaries_user.auxilliaries_user import AuxilliariesUser
from .auxilliaries_sets.auxilliaries_sets import AuxilliariesSets

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

    # Vérification connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)

    if user:
        # Utilisateur connecté
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            if not user.statut_activation_compte:
                # Le compte n'est pas activé
                return redirect('../../user/home/')
            elif user.statut_blocage_admin :
                # Le compte a été bloqué
                return redirect('../../user/home/')
        else:
            # le compte est activé et n'est pas bloqué
            search_form = SearchForm()
            if request.method == 'POST':
                # Creation de set
                create_set_form = CreateSetForm(request.POST, request.FILES)
                if create_set_form.is_valid():
                    # formulaire valide
                    set0 = Sets.objects.create(
                        nom=request.POST["name"],
                        image_couverture=request.FILES["file"],
                        type0=request.POST["type_set"],
                        description=request.POST["description"],
                    )
                    set_user = SetUtilisateurs.objects.create(set0=set0, utilisateur=user, statut="administrateur")
                    return redirect("../../sets/set/" + str(set0.id) + "/")
                else:
                    # formulaire pas valide
                    context = {"create_set_form": create_set_form, "search_form": search_form}
                    context['errors'] = create_set_form.errors.items()
                    return render(request, "creation_set.html", context)
            else:
                # Demande de page de création de set
                create_set_form = CreateSetForm()
                context = {"create_set_form": create_set_form, "search_form": search_form, 'user':user}
                return render(request, "creation_set.html", context)
    else:
        # Utilisateur non connecté
        return redirect("../../authentification/connexion/" )



def creation_evenement(request, set_id):
    """"""


    # Vérification connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)
    auxilliary_set = AuxilliariesSets()
    set0_id = auxilliary_set.get_int_parameter(set_id)
    set0 = None
    user_set = None
    statut_user_in_set = None
    search_form = SearchForm()
    context = {"search_form": search_form,"set": set0,"user":user,}

    if user:
        # Utilisateur connecté
        context['user'] = user


        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            if not user.statut_activation_compte:
                # Le compte n'est pas activé
                return redirect('../../../user/home/')
            elif user.statut_blocage_admin :
                # Le compte a été bloqué
                return redirect('../../../user/home/')
        else:
            # le compte est activé et n'est pas bloqué
            set0 = auxilliary_set.set_in_application(set0_id)
            if set0 :
                # Le set existe
                if set0.statut_fermeture_admin :
                    # Le set est fermé
                    return render(request, "set_ferme.html", context)
                else:
                    # le set n'est pas fermé
                    # Le set existe dans l'application
                    user_set = auxilliary_set.get_user_set(user, set0_id)
                    if user_set:
                        # L'utilisateur appartient au set
                        statut_user_in_set = user_set.statut
                        if statut_user_in_set == 'administrateur' or statut_user_in_set == 'dans_set' :
                            # L'utilisateur n'est pas en attente
                            search_form = SearchForm()
                            if request.method == 'POST':
                                # Creation d'un évènement
                                create_event_form = CreateEventForm(request.POST)
                                if create_event_form.is_valid():
                                    event = Evenements.objects.create(
                                        set0=set0,
                                        administrateur=user,
                                        nom=request.POST["name"],
                                        description=request.POST["description"],
                                    )
                                    return redirect("../../../sets/event/" + str(event.id) + "/")
                                else:
                                    # formulaire pas valide
                                    context = {"create_event_form": create_event_form,"search_form": search_form,"set": set0,}
                                    context['errors'] = create_event_form.errors.items()
                                    return render(request, "creation_evenement.html", context)
                            else:
                                # Page de création d'un évènement
                                create_event_form = CreateEventForm()
                                search_form = SearchForm()
                                context = {"create_event_form": create_event_form,"search_form": search_form,"set": set0, 'user':user }
                                return render(request, "creation_evenement.html", context)
                        elif statut_user_in_set == 'attente_validation':
                            # L'utilisateur est en attente
                            return redirect("../../sets/set/" + str(set0.id) + "/")
                        else:
                            # Autre statut dans le set
                            raise Http404()
                    else:
                        # L'utilisateur n'appartient pas au set
                        return redirect("../../sets/set/" + str(set0.id) + "/")
            else:
                # Le set n'existe pas dans l'application
                raise Http404()
    else:
        # Utilisateur non connecté
        return redirect("../../authentification/connexion/" )







def sets(request, set_id):
    """"""
    auxilliary_user = AuxilliariesUser()
    auxilliary_set = AuxilliariesSets()
    set0_id = auxilliary_set.get_int_parameter(set_id)
    section_set = auxilliary_set.get_section_set(request)
    set0 = None
    user_set = None
    statut_user_in_set = None
    user = auxilliary_user.get_user(request)

    search_form = SearchForm()
    context = {
        "search_form": search_form,
        "set": set0,
        "section_set": section_set,
        "user":user,
    }

    # -)   Vérification inscription utilisateur
    if user :
        # Utilisateur connecté
        context['user'] = user
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            if not user.statut_activation_compte:
                # Le compte n'est pas activé
                return redirect('../../../user/home/')
            elif user.statut_blocage_admin :
                # Le compte a été bloqué
                return redirect('../../../user/home/')
        else:
            # le compte est activé et n'est pas bloqué
            #    Vérification si l'identifiant du set correspond à un set dans l'application
            set0 = auxilliary_set.set_in_application(set0_id) #get_object_or_404(Sets, id=set_id)
            if set0 :
                # Le set existe dans l'application
                context['set'] = set0

                if set0.statut_fermeture_admin :
                    # Le set est fermé
                    return render(request, "set_ferme.html", context)
                else:
                    # Le set n'est pas fermé
                    # Vérification appartenance set utilisateur
                    user_set = auxilliary_set.get_user_set(user, set0)
                    if user_set:
                        # -)   statut de l'utilisateur dans le set
                        statut_user_in_set = user_set.statut
                        if statut_user_in_set == 'administrateur':
                            # L'utilisateur est administrateur du set
                            image_cover_form = SetCoverImageForm()
                            set_description_form = SetDescriptionSetForm()
                            new_post_form = PublicationSetForm()
                            context['image_cover_form'] = image_cover_form
                            context['set_description_form'] = set_description_form
                            context['new_post_form'] = new_post_form
                            context['administrator_status'] = True
                        elif statut_user_in_set == 'dans_set' :
                            # L'utilisateur est simple membre du set
                            new_post_form = PublicationSetForm()
                            context['new_post_form'] = new_post_form
                            context['administrator_status'] = False
                        elif statut_user_in_set == 'attente_validation' :
                            # L'utilisateur est sur la liste d'attente du set
                            context['administrator_status'] = False
                        return auxilliary_set.render_set_user_set(request, section_set, set0_id, context, statut_user_in_set)
                    else:
                        # l'utilisateur n'appartient pas au set
                        return auxilliary_set.render_set_user_no_set(request, section_set, set0_id, context)
            else:
                # Aucun set avec cet id dans l'application
                raise Http404()
    else:
        #      Utilisateur non-inscrit
        # -)   Vérification si l'identifiant du set correspond à un set dans l'application
        set0 = get_object_or_404(Sets, id=set0_id)
        if set0 :
            #   Le set existe dans l'application
            context['set'] = set0

            if set0.statut_fermeture_admin :
                # Le set est fermé
                return render(request, "set_ferme.html", context)
            else:
                # Le set n'est pas fermé
                return auxilliary_set.render_set_user_no_registred(request, section_set, set0_id, context)
        else:
            # Aucun set avec cet id dans l'application
            raise Http404()



def evenements(request, event_id):
    """"""

    # evenement

    auxilliary_user = AuxilliariesUser()
    auxilliary_set = AuxilliariesSets()
    event_id = auxilliary_set.get_int_parameter(event_id)
    set0 = None
    event0 = None
    user_set = None
    statut_user_in_set = None
    user = auxilliary_user.get_user(request)

    search_form = SearchForm()
    context = {
        "search_form": search_form,
        "set": set0,
        "user":user,
    }

    # -)   Vérification inscription utilisateur
    if user :
        context['user'] = user
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            if not user.statut_activation_compte:
                # Le compte n'est pas activé
                return redirect('../../../user/home/')
            elif user.statut_blocage_admin :
                # Le compte a été bloqué
                return redirect('../../../user/home/')
        else:
            # le compte est activé et n'est pas bloqué
            # Vérification si l'identifiant de l'évènement correspond à un évènement dans l'application
            event0 = auxilliary_set.event_in_application(event_id)
            context['event'] = event0
            if event0 :
                # L'évènement existe dans l'application
                if event0.statut_fermeture_admin :
                    # L'évènement est fermé
                    return render(request, "evenement_ferme.html", context)
                else:
                    # l'évènement n'est pas fermé
                    set0 = event0.set0
                    context['set'] = set0
                    if set0.statut_fermeture_admin :
                        # Le set ou l'évènement sont fermés
                        return render(request, "evenement_ferme.html", context)
                    else:
                        # Le set et l'évènement ne sont pas fermés
                        # Vérification appartenance set utilisateur
                        user_set = auxilliary_set.get_user_set(user, set0.id)
                        context['user_set'] = user_set
                        if user_set:
                            #   L'utilisateur appartient au set
                            publications = PublicationEvenement.objects.filter(evenement_id=event_id)
                            publications_likeurs = []
                            for publication in publications:
                                publications_likeurs.append([publication, JaimePublicationEvenement.objects.filter(publication_evenement_id=publication.id), JaimePublicationEvenement.objects.filter(publication_evenement_id=publication.id, jaimeur_id=request.session["user_id"])])
                            context['publications_likeurs'] = publications_likeurs
                            statut_user_in_set = user_set.statut
                            if statut_user_in_set == 'attente_validation':
                                # L'utilisateur est en attente de validation du set
                                return render(request, "evenement_await_enter_set.html", context)
                            else:
                                # L'utilisateur est membre entier du set
                                new_post_form = PublicationEventForm()
                                context['new_post_form'] = new_post_form
                                if user == event0.administrateur :
                                    # L'utilisateur est administrateur de l'évènement
                                    event_description_form = SetDescriptionSetEvent()
                                    context['event_description_form'] = event_description_form
                                    return render(request, "evenement_administrator_event.html", context)
                                else:
                                    # L'utilisateur n'est pas administrateur de l'évènement
                                    return render(request, "evenement_no_administrator_event.html", context)
                        else:
                            # l'utilisateur n'appartient pas au set
                            return render(request, "evenement_no_access_event.html", context)
            else:
                # Aucun Evènement avec cet id dans l'application
                raise Http404()
    else:
        #      Utilisateur non-inscrit
        # -)   Vérification si l'identifiant du set correspond à un évènement dans l'application
        event0 = auxilliary_set.event_in_application(event_id)
        context['event'] = event0
        if event0 :
            #   L'évènement existe dans l'application
            if event0.statut_fermeture_admin :
                # L'évènement est fermé
                return redirect("../../../sets/event/" + str(event0.id) + "/")
            else:
                # l'évènement n'est pas fermé
                set0 = event0.set0
                context['set'] = set0
                if set0.statut_fermeture_admin or event0.statut_fermeture_admin :
                    # Le set ou l'évènement sont fermés
                    return render(request, "evenement_ferme.html", context)
                else:
                    # Le set et l'évènement ne sont pas fermés
                    return render(request, "evenement_no_access_event.html", context)
        else:
            # Aucun Evènement avec set id dans l'application
            raise Http404()




def search(request):
    """"""

    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)

    context = { "recherche":request.GET["search_input"] }
    search_form = SearchForm()
    context['search_form'] = search_form

    # section de la recherche
    try:
        section = request.GET["section"]
    except Exception as e:
        section = "sets"
    context['section'] = section

    context['user'] = user

    if user:
        # utilisateur connecté
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            if not user.statut_activation_compte:
                # Le compte n'est pas activé
                return redirect('../../../user/home/')
            elif user.statut_blocage_admin :
                # Le compte a été bloqué
                return redirect('../../../user/home/')
        else:
            # le compte est activé et n'est pas bloqué
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
    else:
        # Utilisateur non connecté
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

    auxilliary_user = AuxilliariesUser()
    auxilliary_set = AuxilliariesSets()
    set0_id = auxilliary_set.get_int_parameter(request.GET["set_id"])

    set0 = None
    user_set = None
    statut_user_in_set = None
    user = auxilliary_user.get_user(request)

    context = { "set": set0, "user":user, }

    # -)   Vérification inscription utilisateur
    if user :
        context['user'] = user
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            if not user.statut_activation_compte:
                # Le compte n'est pas activé
                return redirect('../../../user/home/')
            elif user.statut_blocage_admin :
                # Le compte a été bloqué
                return redirect('../../../user/home/')
        else:
            # le compte est activé et n'est pas bloqué
            # -)    Vérification si l'identifiant du set correspond à un set dans l'application
            set0 = auxilliary_set.set_in_application(set0_id) 
            if set0 :
                if set0.statut_fermeture_admin :
                    # Le set est fermé
                    return redirect("../../sets/set/" + str(set0.id) + "/")
                else:
                    # le set n'est pas fermé
                    context['set'] = set0
                    # -)   Vérification appartenance set utilisateur
                    user_set = auxilliary_set.get_user_set(user, set0_id)
                    if user_set:
                        # -)   statut de l'utilisateur dans le set
                        statut_user_in_set = user_set.statut
                        if statut_user_in_set == 'administrateur':
                            # L'utilisateur est administrateur du set
                            form = SetCoverImageForm(request.POST, request.FILES)
                            if form.is_valid():
                                # formulaire valide
                                set0.image_couverture = request.FILES["file"]
                                set0.save()
                                return redirect("../../sets/set/" + str(set0.id) + "/")
                            else:
                                # formulaire invalide
                                raise Http404()
                        elif statut_user_in_set == 'attente_validation' or statut_user_in_set == 'dans_set':
                            # L'utilisateur n'est pas administrateur du set
                            return redirect("../../sets/set/" + str(set0.id) + "/")
                    else:
                        # l'utilisateur n'appartient pas au set
                        return redirect("../../user/home/")
            else:
                # Aucun set avec cet id dans l'application
                raise Http404()
    else:
        #      Utilisateur non-inscrit
        return redirect("../../authentification/connexion/")



def update_description_set(request):
    """"""
    auxilliary_user = AuxilliariesUser()
    auxilliary_set = AuxilliariesSets()
    set0_id = auxilliary_set.get_int_parameter(request.GET["set_id"])

    set0 = None
    user_set = None
    statut_user_in_set = None
    user = auxilliary_user.get_user(request)

    context = { "set": set0, "user":user, }

    # -)   Vérification inscription utilisateur
    if user :
        context['user'] = user
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            if not user.statut_activation_compte:
                # Le compte n'est pas activé
                return redirect('../../user/home/')
            elif user.statut_blocage_admin :
                # Le compte a été bloqué
                return redirect('../../user/home/')
        else:
            # le compte est activé et n'est pas bloqué
            # -)    Vérification si l'identifiant du set correspond à un set dans l'application
            set0 = auxilliary_set.set_in_application(set0_id) 
            if set0 :
                # Le set existe


                if set0.statut_fermeture_admin :
                    # Le set est fermé
                    return redirect("../../sets/set/" + str(set0.id) + "/")
                else:
                    # le set n'est pas fermé
                    context['set'] = set0
                    # -)   Vérification appartenance set utilisateur
                    user_set = auxilliary_set.get_user_set(user, set0_id)
                    if user_set:
                        # -)   statut de l'utilisateur dans le set
                        statut_user_in_set = user_set.statut
                        if statut_user_in_set == 'administrateur':
                            # L'utilisateur est administrateur du set
                            form = SetDescriptionSetForm(request.POST)
                            if form.is_valid():
                                # formulaire valide
                                set0.description = request.POST["description"]
                                set0.save()
                                return redirect("../../sets/set/" + str(set0.id) + "/")
                            else:
                                # formulaire invalide
                                raise Http404()
                        elif statut_user_in_set == 'attente_validation' or statut_user_in_set == 'dans_set':
                            # L'utilisateur n'est pas administrateur du set
                            return redirect("../../sets/set/" + str(set0.id) + "/")
                    else:
                        # l'utilisateur n'appartient pas au set
                        return redirect("../../user/home/")
            else:
                # Aucun set avec set id dans l'application
                raise Http404()
    else:
        #      Utilisateur non-inscrit
        return redirect("../../authentification/connexion/")


def make_post_set(request, set_id):
    """"""

    auxilliary_user = AuxilliariesUser()
    auxilliary_set = AuxilliariesSets()
    set0_id = auxilliary_set.get_int_parameter(set_id)
    section_set = auxilliary_set.get_section_set(request)
    set0 = None
    user_set = None
    statut_user_in_set = None
    user = auxilliary_user.get_user(request)

    # -)   Vérification inscription utilisateur
    if user :
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            if not user.statut_activation_compte:
                # Le compte n'est pas activé
                return redirect('../../../user/home/')
            elif user.statut_blocage_admin :
                # Le compte a été bloqué
                return redirect('../../../user/home/')
        else:
            # le compte est activé et n'est pas bloqué
            # -)    Vérification si l'identifiant du set correspond à un set dans l'application
            set0 = auxilliary_set.set_in_application(set0_id) #get_object_or_404(Sets, id=set_id)
            if set0 :
                # Le set existe


                if set0.statut_fermeture_admin :
                    # Le set est fermé
                    return redirect("../../sets/set/" + str(set0.id) + "/")
                else:
                    # le set n'est pas fermé
                    # -)   Vérification appartenance set utilisateur
                    user_set = auxilliary_set.get_user_set(user, set0_id)
                    if user_set:
                        # -)   statut de l'utilisateur dans le set
                        statut_user_in_set = user_set.statut
                        if statut_user_in_set == 'administrateur' or statut_user_in_set == 'dans_set' :
                            # L'utilisateur est administrateur ou simple membre du set
                            post_form = PublicationSetForm(request.POST, request.FILES)
                            if post_form.is_valid():
                                # Formulaire valide
                                if auxilliary_set.form_is_not_empty(request):
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
                                    raise Http404()
                            else:
                                raise Http404()
                        elif statut_user_in_set == 'attente_validation' :
                            # L'utilisateur est sur la liste d'attente du set
                            raise Http404()
                    else:
                        # l'utilisateur n'appartient pas au set
                        raise Http404()
            else:
                # Aucun set avec cet id dans l'application
                raise Http404()
    else:
        #      Utilisateur non-inscrit
        raise Http404()




def make_post_event(request, event_id):
    """"""

    auxilliary_user = AuxilliariesUser()
    auxilliary_set = AuxilliariesSets()
    event_id = auxilliary_set.get_int_parameter(event_id)
    set0 = None
    event0 = None
    user_set = None
    statut_user_in_set = None
    user = auxilliary_user.get_user(request)

    search_form = SearchForm()
    context = {
        "search_form": search_form,
        "set": set0,
        "user":user,
    }

    # -)   Vérification inscription utilisateur
    if user :
        context['user'] = user
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            if not user.statut_activation_compte:
                # Le compte n'est pas activé
                return redirect('../../../user/home/')
            elif user.statut_blocage_admin :
                # Le compte a été bloqué
                return redirect('../../../user/home/')
        else:
            # le compte est activé et n'est pas bloqué
            # -)    Vérification si l'identifiant de l'évènement correspond à un évènement dans l'application
            event0 = auxilliary_set.event_in_application(event_id)
            context['event'] = event0
            if event0 :
                # L'évènement existe dans l'application
                if event0.statut_fermeture_admin :
                    # L'évènement est fermé
                    return redirect("../../../sets/event/" + str(event0.id) + "/")
                else:
                    # l'évènement n'est pas fermé
                    set0 = event0.set0
                    context['set'] = set0

                    if set0.statut_fermeture_admin :
                        # Le set est fermé
                        return redirect("../../../sets/event/" + str(event0.id) + "/")
                    else:
                        # le set n'est pas fermé
                        # -)   Vérification appartenance set utilisateur
                        user_set = auxilliary_set.get_user_set(user, set0.id)
                        context['user_set'] = user_set
                        if user_set:
                            #   L'utilisateur appartient au set
                            statut_user_in_set = user_set.statut
                            if statut_user_in_set == 'attente_validation':
                                # L'utilisateur est en attente de validation du set
                                raise Http404()
                            else:
                                # L'utilisateur est membre entier du set
                                post_form = PublicationEventForm(request.POST, request.FILES)
                                if post_form.is_valid():
                                    # Formulaire valide
                                    if auxilliary_set.form_is_not_empty(request):
                                        # Formulaire non vide
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
                                        # Formulaire vide
                                        raise Http404()
                                else:
                                    # Formulaire invalide
                                    raise Http404()
                        else:
                            # l'utilisateur n'appartient pas au set
                            raise Http404()
            else:
                # Aucun Evènement avec cet id dans l'application
                raise Http404()
    else:
        #      Utilisateur non-inscrit
        raise Http404()





def manage_like_post_set(request, post_id):
    """"""

    auxilliary_user = AuxilliariesUser()
    auxilliary_set = AuxilliariesSets()
    post0_id = auxilliary_set.get_int_parameter(post_id)
    post0 = None
    set0 = None
    user_set = None
    statut_user_in_set = None
    user = auxilliary_user.get_user(request)

    # -)   Vérification inscription utilisateur
    if user :
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            if not user.statut_activation_compte:
                # Le compte n'est pas activé
                return redirect('../../../user/home/')
            elif user.statut_blocage_admin :
                # Le compte a été bloqué
                return redirect('../../../user/home/')
        else:
            # le compte est activé et n'est pas bloqué
            # -)    Vérification si l'identifiant du set correspond à un post dans l'application
            post0 = auxilliary_set.post_set_in_application(post0_id)
            if post0:
                set0 = post0.set0
                if set0 :
                    # Le set existe

                    if set0.statut_fermeture_admin :
                        # Le set est fermé
                        return redirect("../../sets/set/" + str(set0.id) + "/")
                    else:
                        # le set n'est pas fermé
                        # -)   Vérification appartenance set utilisateur
                        user_set = auxilliary_set.get_user_set(user, set0.id)
                        if user_set:
                            # -)   statut de l'utilisateur dans le set
                            statut_user_in_set = user_set.statut
                            if statut_user_in_set == 'attente_validation':
                                # L'utilisateur est en attente de validation du set
                                return HttpResponse("validate_enter_set_first")
                            else:
                                # L'utilisateur est membre entier du set
                                check = JaimePublicationSet.objects.filter(publication_set_id=post_id, jaimeur_id=request.session["user_id"])
                                if len(check) == 0 :
                                    like = JaimePublicationSet.objects.create(
                                        publication_set=post0,
                                        jaimeur=user,
                                    )
                                    return HttpResponse("like_make")
                                else:
                                    check[0].delete()
                                    return HttpResponse("unlike_make")
                        else:
                            # l'utilisateur n'appartient pas au set
                            raise Http404()
                else:
                    # Aucun set avec cet id dans l'application
                    raise Http404()
            else:
                # Aucune publication avec cet id
                raise Http404()
    else:
        #      Utilisateur non-inscrit
        raise Http404()





def manage_like_post_event(request, post_id):
    """"""

    auxilliary_user = AuxilliariesUser()
    auxilliary_set = AuxilliariesSets()
    post0_id = auxilliary_set.get_int_parameter(post_id)
    post0 = None
    set0 = None
    event0 = None
    user_set = None
    statut_user_in_set = None
    user = auxilliary_user.get_user(request)

    # -)   Vérification inscription utilisateur
    if user :
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            if not user.statut_activation_compte:
                # Le compte n'est pas activé
                return redirect('../../../user/home/')
            elif user.statut_blocage_admin :
                # Le compte a été bloqué
                return redirect('../../../user/home/')
        else:
            # le compte est activé et n'est pas bloqué
            # -)    Vérification si l'identifiant de l'évènement correspond à un évènement dans l'application
            post0 = auxilliary_set.post_event_in_application(post0_id)
            if post0:
                event0 = post0.evenement
                if event0 :
                    # L'évènement existe dans l'application

                    if event0.statut_fermeture_admin :
                        # L'évènement est fermé
                        return redirect("../../../sets/event/" + str(event0.id) + "/")
                    else:
                        # l'évènement n'est pas fermé
                        set0 = event0.set0
                        if set0.statut_fermeture_admin :
                            # Le set est fermé
                            return redirect("../../../sets/event/" + str(event0.id) + "/")
                        else:
                            # le set n'est pas fermé
                            # -)   Vérification appartenance set utilisateur
                            user_set = auxilliary_set.get_user_set(user, set0.id)
                            if user_set:
                                #   L'utilisateur appartient au set
                                # -)   statut de l'utilisateur dans le set
                                statut_user_in_set = user_set.statut
                                if statut_user_in_set == 'attente_validation':
                                    # L'utilisateur est en attente de validation du set
                                    return HttpResponse("validate_enter_set_first")
                                else:
                                    # L'utilisateur est membre entier du set
                                    check = JaimePublicationEvenement.objects.filter(publication_evenement_id=post_id, jaimeur_id=request.session["user_id"])
                                    if len(check) == 0 :
                                        like = JaimePublicationEvenement.objects.create(
                                            publication_evenement=post0,
                                            jaimeur=user,
                                        )
                                        return HttpResponse("like_make")
                                    else:
                                        check[0].delete()
                                        return HttpResponse("unlike_make")
                            else:
                                # l'utilisateur n'appartient pas au set
                                raise Http404()
                else:
                    # Aucun Evènement avec cet id dans l'application
                    raise Http404()
            else:
                # Aucune publication avec cet id
                raise Http404()
    else:
        #      Utilisateur non-inscrit
        raise Http404()



def delete_add_user_set(request, set_id, user_delete_add_id):
    """"""

    auxilliary_user = AuxilliariesUser()
    auxilliary_set = AuxilliariesSets()
    set0_id = auxilliary_set.get_int_parameter(set_id)
    user_to_delete_add_id = auxilliary_set.get_int_parameter(user_delete_add_id)
    set0 = None
    user_set = None
    user_to_delete_add = None
    statut_user_in_set = None
    user = auxilliary_user.get_user(request)

    # -)   Vérification inscription utilisateur
    if user :
        # l'utilisateur existe
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            if not user.statut_activation_compte:
                # Le compte n'est pas activé
                return redirect('../../../../user/home/')
            elif user.statut_blocage_admin :
                # Le compte a été bloqué
                return redirect('../../../../user/home/')
        else:
            # le compte est activé et n'est pas bloqué
            # -)    Vérification si l'identifiant du set correspond à un set dans l'application
            set0 = auxilliary_set.set_in_application(set0_id)
            user_to_delete_add = auxilliary_user.user_in_application(user_to_delete_add_id)
            if set0 and user_to_delete_add :
                # Le set et l'utilisateur à ajouter/supprimer existent
                if set0.statut_fermeture_admin :
                    # Le set est fermé
                    return redirect("../../../../sets/set/" + str(set0.id) + "/")
                else:
                    # le set n'est pas fermé
                    # -)   Vérification appartenance set utilisateur
                    user_set = auxilliary_set.get_user_set(user, set0_id)
                    if user_set:
                        # -)   statut de l'utilisateur dans le set
                        statut_user_in_set = user_set.statut
                        if statut_user_in_set == 'administrateur':
                            # L'utilisateur est administrateur du set
                            user_set_to_delete_add = auxilliary_set.get_user_set(user_to_delete_add, set0_id)
                            if user_set_to_delete_add :
                                # l'utilisateur à supprimer ou ajouter est dans le set
                                user_set_to_delete_add.delete()
                                return HttpResponse("user_deleted")
                            else:
                                # L'utilisateur à supprimer ou ajouter n'est pas dans le set
                                user_set_to_delete_add = SetUtilisateurs.objects.create(set0=set0, utilisateur=user_to_delete_add, statut='attente_validation')
                                return HttpResponse("user_added")
                        else:
                            # L'utilisateur n'est pas administrateur du set
                            raise Http404()
                    else:
                        # l'utilisateur n'appartient pas au set
                        raise Http404()
            else:
                # Aucun set avec cet id dans l'application ou aucun utilisateur dans l'application avec l'id recu
                raise Http404()
    else:
        #      Utilisateur non-inscrit
        raise Http404()




def manage_enter_user_set(request, set_id):
    """"""
    auxilliary_user = AuxilliariesUser()
    auxilliary_set = AuxilliariesSets()
    set0_id = auxilliary_set.get_int_parameter(set_id)
    set0 = None
    user_set = None
    statut_user_in_set = None
    user = auxilliary_user.get_user(request)

    # -)   Vérification inscription utilisateur
    if user :
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            if not user.statut_activation_compte:
                # Le compte n'est pas activé
                return redirect('../../../user/home/')
            elif user.statut_blocage_admin :
                # Le compte a été bloqué
                return redirect('../../../user/home/')
        else:
            # le compte est activé et n'est pas bloqué
            # -)    Vérification si l'identifiant du set correspond à un set dans l'application
            set0 = auxilliary_set.set_in_application(set0_id)
            if set0 :
                #Le set existe
                if set0.statut_fermeture_admin :
                    # Le set est fermé
                    return redirect("../../sets/set/" + str(set0.id) + "/")
                else:
                    # le set n'est pas fermé
                    # -)   Vérification appartenance set utilisateur
                    user_set = auxilliary_set.get_user_set(user, set0_id)
                    if user_set:
                        # -)   statut de l'utilisateur dans le set
                        statut_user_in_set = user_set.statut
                        if statut_user_in_set == 'attente_validation':
                            # L'utilisateur est en attente d'entrée dans le set
                            if request.GET['confirm_enter'] == 'yes':
                                # L'utilisateur confirme son entrée dans le set
                                user_set.statut = 'dans_set'
                                user_set.save()
                                return HttpResponse('added_done')
                            elif request.GET['confirm_enter'] == 'no':
                                # L'utilisateur annule son entrée dans le set
                                user_set.delete()
                                return HttpResponse('delete_done')
                        else:
                            # L'utilisateur n'est pas en attente d'entrée dans le set
                            raise Http404()
                    else:
                        # l'utilisateur n'appartient pas au set
                        raise Http404()
            else:
                # Aucun set avec cet id dans l'application ou aucun utilisateur dans l'application avec l'id recu
                raise Http404()
    else:
        #      Utilisateur non-inscrit
        raise Http404()





def exit_set(request, set_id):
    """"""

    auxilliary_user = AuxilliariesUser()
    auxilliary_set = AuxilliariesSets()
    set0_id = auxilliary_set.get_int_parameter(set_id)
    set0 = None
    user_set = None
    statut_user_in_set = None
    user = auxilliary_user.get_user(request)

    # -)   Vérification inscription utilisateur
    if user :
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            if not user.statut_activation_compte:
                # Le compte n'est pas activé
                return redirect('../../../user/home/')
            elif user.statut_blocage_admin :
                # Le compte a été bloqué
                return redirect('../../../user/home/')
        else:
            # le compte est activé et n'est pas bloqué
            # -)    Vérification si l'identifiant du set correspond à un set dans l'application
            set0 = auxilliary_set.set_in_application(set0_id)
            if set0 :
                # Le set existe
                if set0.statut_fermeture_admin :
                    # Le set est fermé
                    return redirect("../../sets/set/" + str(set0.id) + "/")
                else:
                    # le set n'est pas fermé
                    # -)   Vérification appartenance set utilisateur
                    user_set = auxilliary_set.get_user_set(user, set0_id)
                    if user_set:
                        # -)   statut de l'utilisateur dans le set
                        statut_user_in_set = user_set.statut
                        if statut_user_in_set == 'administrateur':
                            # L'utilisateur est administrateur
                            user_set.delete()
                            if len(SetUtilisateurs.objects.filter(set0=set0)) == 0 :
                                # Aucun utilisateur dans le set après la suppression
                                set0.delete()
                                return HttpResponse('delete_done_and_set_delete_done')
                            else:
                                # présense d'utilisateurs dans le set après la suppression
                                next_admin = SetUtilisateurs.objects.filter(set0=set0).order_by('date')[0]
                                next_admin.statut = 'administrateur'
                                next_admin.save()
                                return HttpResponse('delete_done')
                        else:
                            # L'utilisateur n'est pas administrateur
                            user_set.delete()
                            return HttpResponse('delete_done')
                    else:
                        # l'utilisateur n'appartient pas au set
                        raise Http404()
            else:
                # Aucun set avec cet id dans l'application ou aucun utilisateur dans l'application avec l'id recu
                raise Http404()
    else:
        #      Utilisateur non-inscrit
        raise Http404()






def delete_set(request, set_id):
    """"""
    
    auxilliary_user = AuxilliariesUser()
    auxilliary_set = AuxilliariesSets()
    set0 = None
    user_set = None
    statut_user_in_set = None
    user = auxilliary_user.get_user(request)

    search_form = SearchForm()
    context = {
        "search_form": search_form,
        "set": set0,
        "user":user,
    }

    if user:
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            if not user.statut_activation_compte:
                # Le compte n'est pas activé
                return redirect('../../../user/home/')
            elif user.statut_blocage_admin :
                # Le compte a été bloqué
                return redirect('../../../user/home/')
        else:
            # le compte est activé et n'est pas bloqué
            # l'utilisateur est connecté
            context['user'] = user
            set0 = auxilliary_set.set_in_application(set_id)
            if set0:
                # Le set existe
                if set0.statut_fermeture_admin :
                    # Le set est fermé
                    return redirect("../../sets/set/" + str(set0.id) + "/")
                else:
                    # le set n'est pas fermé
                    context['set'] = set0
                    user_set = auxilliary_set.get_user_set(user, set0)
                    context['user_set'] = user_set
                    if user_set:
                        # L'utilisateur appartient au set
                        if user_set.statut == 'administrateur' :
                            # L'utilisateur est administrateur du set
                            set0.delete()
                            return redirect('../../../user/home/' )
                        else:
                            # L'utilisateur n'est pas administrateur du set
                            raise Http404()
                    else:
                        # L'utilisateur n'appartient pas au set
                        raise Http404()
            else:
                #L'évènement n'existe pas dans l'application
                raise Http404()
    else:
        # L'utilisateur n'est pas connecté
        raise Http404()


def delete_event(request, event_id):
    """"""


    auxilliary_user = AuxilliariesUser()
    auxilliary_set = AuxilliariesSets()
    set0 = None
    event0 = None
    user_set = None
    statut_user_in_set = None
    user = auxilliary_user.get_user(request)

    search_form = SearchForm()
    context = {
        "search_form": search_form,
        "set": set0,
        "user":user,
    }

    if user:
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            if not user.statut_activation_compte:
                # Le compte n'est pas activé
                return redirect('../../../user/home/')
            elif user.statut_blocage_admin :
                # Le compte a été bloqué
                return redirect('../../../user/home/')
        else:
            # le compte est activé et n'est pas bloqué
            # l'utilisateur est connecté
            context['user'] = user
            event0 = auxilliary_set.event_in_application(event_id)
            context['event'] = event0
            if event0:
                # L'évènement existe
                if event0.statut_fermeture_admin :
                    # L'évènement est fermé
                    return redirect("../../../sets/event/" + str(event0.id) + "/")
                else:
                    # l'évènement n'est pas fermé
                    set0 = event0.set0
                    if set0.statut_fermeture_admin :
                        # Le set est fermé
                        return redirect("../../sets/set/" + str(set0.id) + "/")
                    else:
                        # le set n'est pas fermé
                        context['set'] = set0
                        user_set = auxilliary_set.get_user_set(user, set0)
                        context['user_set'] = user_set
                        if user_set:
                            # L'utilisateur appartient au set
                            if event0.administrateur == user :
                                # L'utilisateur est administrateur du set
                                event0.delete()
                                return redirect('../../set/' + str(set0.id) + '/' )
                            else:
                                # L'utilisateur n'est pas administrateur du set
                                raise Http404()
                        else:
                            # L'utilisateur n'appartient pas au set
                            raise Http404()
            else:
                #L'évènement n'existe pas dans l'application
                raise Http404()
    else:
        # L'utilisateur n'est pas connecté
        raise Http404()







def redirect_home(self):
    """"""
    return redirect("../../../user/home/")