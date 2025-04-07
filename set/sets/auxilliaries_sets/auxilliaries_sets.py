""""""
from django.shortcuts import render, get_object_or_404, redirect

from user.auxilliaries_user.auxilliaries_user import AuxilliariesUser

from user.models import Utilisateurs

from ..models import (
    Sets,
    SetUtilisateurs,
    PublicationSet,
    JaimePublicationSet,
    Evenements,
    PublicationEvenement,
    JaimePublicationEvenement,
)


from sets.forms import (
    CreateSetForm,
    CreateEventForm,
    SearchForm,
    CreateEventForm,
    SetDescriptionSetForm,
    PublicationSetForm,
    SetCoverImageForm,
    PublicationEventForm,
    SetDescriptionSetEvent,
)

from django.http import Http404, HttpResponse

from user.models import Contact


class AuxilliariesSets:
    """docstring for AuxilliariesSets"""

    def __init__(self):
        """"""
        pass

    def get_int_parameter(self, parameter):
        """"""
        try:
            out = int(parameter)
        except Exception as e:
            out = None
        return out

    def set_in_application(self, set_id):
        """"""

        try:
            out = get_object_or_404(Sets, id=set_id)
        except Exception as e:
            out = None
        return out

    def post_set_in_application(self, post_id):
        """"""

        try:
            out = get_object_or_404(PublicationSet, id=post_id)
        except Exception as e:
            out = None
        return out

    def post_event_in_application(self, post_id):
        """"""
        try:
            out = get_object_or_404(PublicationEvenement, id=post_id)
        except Exception as e:
            out = None
        return out

    def event_in_application(self, event_id):
        """"""

        try:
            out = get_object_or_404(Evenements, id=event_id)
        except Exception as e:
            out = None
        return out

    def get_user_set(self, user, set0):
        """"""
        try:
            out = SetUtilisateurs.objects.get(set0=set0, utilisateur=user)
        except Exception as e:
            out = None
        return out

    def get_section_set(self, request):
        """"""
        try:
            out = request.GET["section"]
        except Exception as e:
            out = "publications"
        return out

    def publications_likeurs_context(self, publications, request, for_who):
        """"""
        publications_likeurs = []
        if for_who == "sets":
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
        elif for_who == "events":
            for publication in publications:
                publications_likeurs.append(
                    [
                        publication,
                        JaimePublicationEvenement.objects.filter(
                            publication_evenement_id=publication.id
                        ),
                        JaimePublicationEvenement.objects.filter(
                            publication_evenement_id=publication.id,
                            jaimeur_id=request.session["user_id"],
                        ),
                    ]
                )
        return publications_likeurs

    def render_set_user_set(
        self, request, section_set, set_id, context, statut_user_in_set
    ):
        """"""
        if section_set == "publications":
            # Récupération des publications
            publications = PublicationSet.objects.filter(set0_id=set_id).order_by(
                "-date"
            )
            context["publications_likeurs"] = self.publications_likeurs_context(
                publications, request, "sets"
            )
            if statut_user_in_set == "attente_validation":
                return render(
                    request, "section_publications_users_wait_set.html", context
                )
            else:
                return render(request, "section_publications_set.html", context)

        elif section_set == "evenements":
            # Récupération des évènements
            events = Evenements.objects.filter(set0_id=set_id)
            context["events"] = events
            if statut_user_in_set == "attente_validation":
                return render(request, "section_evenements_set_out_set.html", context)
            else:
                return render(request, "section_evenements_set.html", context)
        elif section_set == "personnes":
            # Récupération des utilisateurs
            users_set = SetUtilisateurs.objects.filter(set0_id=set_id)
            users_set_list = [user_set.utilisateur for user_set in users_set]
            users_set_dictionnary = {
                user_set.utilisateur: user_set for user_set in users_set
            }
            # Récupération des contacts
            contacts = Contact.objects.filter(
                contact_owner_id=request.session["user_id"]
            )
            contacts_list = [contact.contact for contact in contacts]
            context["users_set"] = users_set
            context["users_set_list"] = users_set_list
            context["contacts"] = contacts
            context["contacts_list"] = contacts_list
            return render(request, "section_personnes_set.html", context)

    def render_set_user_no_set(self, request, section_set, set_id, context):
        """"""
        if section_set == "publications":
            # Demande des publications
            return render(request, "section_no_access_publications_set.html", context)
        elif section_set == "evenements":
            # Récupération des évènements
            events = Evenements.objects.filter(set0_id=set_id)
            context["events"] = events
            return render(request, "section_evenements_set_out_set.html", context)
        elif section_set == "personnes":
            # Récupération des utilisateurs
            users_set = SetUtilisateurs.objects.filter(set0_id=set_id)
            users_set_list = [user_set.utilisateur for user_set in users_set]
            users_set_dictionnary = {
                user_set.utilisateur: user_set for user_set in users_set
            }
            # Récupération des contacts
            contacts = Contact.objects.filter(
                contact_owner_id=request.session["user_id"]
            )
            contacts_list = [contact.contact for contact in contacts]
            context["users_set"] = users_set
            context["users_set_list"] = users_set_list
            context["contacts"] = contacts
            context["contacts_list"] = contacts_list
            return render(request, "section_personnes_set.html", context)

    def render_set_user_no_registred(self, request, section_set, set_id, context):
        """"""
        if section_set == "publications":
            # Demande des publications
            return render(request, "section_no_access_publications_set.html", context)
        elif section_set == "evenements":
            # Récupération des évènements
            events = Evenements.objects.filter(set0_id=set_id)
            context["events"] = events
            return render(request, "section_evenements_set_out_set.html", context)
        elif section_set == "personnes":
            # Récupération des utilisateurs
            users_set = SetUtilisateurs.objects.filter(set0_id=set_id)
            users_set_list = [user_set.utilisateur for user_set in users_set]
            users_set_dictionnary = {
                user_set.utilisateur: user_set for user_set in users_set
            }
            context["users_set"] = users_set
            context["users_set_list"] = users_set_list
            context["contacts"] = []
            context["contacts_list"] = []
            return render(request, "section_personnes_set.html", context)

    def form_is_not_empty(self, request):
        """"""
        contenu_text = request.POST["publication_text"]
        media1 = request.FILES.get("file_1", "")
        media2 = request.FILES.get("file_2", "")
        if contenu_text == "" and media1 == "" and media2 == "":
            # Le formulaire est vide
            out = False
        else:
            # Le formulaire n'est pas vide
            out = True
        return out

    def create_set(self, request, user, search_form):
        """"""
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
            set_user = SetUtilisateurs.objects.create(
                set0=set0, utilisateur=user, statut="administrateur"
            )
            return redirect("../../sets/set/" + str(set0.id) + "/")
        else:
            # formulaire pas valide
            context = {"create_set_form": create_set_form, "search_form": search_form}
            context["errors"] = create_set_form.errors.items()
            return render(request, "creation_set.html", context)

    def get_create_set_page(self, request, search_form, user):
        """"""
        create_set_form = CreateSetForm()
        context = {
            "create_set_form": create_set_form,
            "search_form": search_form,
            "user": user,
        }
        return render(request, "creation_set.html", context)

    def create_event(self, request, set0, user, search_form):
        """"""
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
            context = {
                "create_event_form": create_event_form,
                "search_form": search_form,
                "set": set0,
            }
            context["errors"] = create_event_form.errors.items()
            return render(request, "creation_evenement.html", context)

    def get_create_event_page(self, request, set0, user):
        """"""
        create_event_form = CreateEventForm()
        search_form = SearchForm()
        context = {
            "create_event_form": create_event_form,
            "search_form": search_form,
            "set": set0,
            "user": user,
        }
        return render(request, "creation_evenement.html", context)

    def create_event_user_set(self, request, user_set, set0, user):
        """"""
        # L'utilisateur appartient au set
        statut_user_in_set = user_set.statut
        if (statut_user_in_set == "administrateur") or (
            statut_user_in_set == "dans_set"
        ):
            # L'utilisateur n'est pas en attente
            search_form = SearchForm()
            if request.method == "POST":
                # Creation d'un évènement
                return self.create_event(request, set0, user, search_form)
            else:
                # Page de création d'un évènement
                return self.get_create_event_page(request, set0, user)
        elif statut_user_in_set == "attente_validation":
            # L'utilisateur est en attente
            return redirect("../../sets/set/" + str(set0.id) + "/")
        else:
            # Autre statut dans le set
            raise Http404()

    def create_event_if_set_opened(self, context, request, set0, user, set0_id):
        """"""
        if set0.statut_fermeture_admin:
            # Le set est fermé
            return render(request, "set_ferme.html", context)
        else:
            # le set n'est pas fermé
            user_set = AuxilliariesSets().get_user_set(user, set0_id)
            if user_set:
                # L'utilisateur appartient au set
                return self.create_event_user_set(request, user_set, set0, user)
            else:
                # L'utilisateur n'appartient pas au set
                return redirect("../../sets/set/" + str(set0.id) + "/")

    def context_set(self, statut_user_in_set, context):
        """"""
        if statut_user_in_set == "administrateur":
            # L'utilisateur est administrateur du set
            context["image_cover_form"] = SetCoverImageForm()
            context["set_description_form"] = SetDescriptionSetForm()
            context["new_post_form"] = PublicationSetForm()
            context["administrator_status"] = True
        elif statut_user_in_set == "dans_set":
            # L'utilisateur est simple membre du set
            context["new_post_form"] = PublicationSetForm()
            context["administrator_status"] = False
        elif statut_user_in_set == "attente_validation":
            # L'utilisateur est sur la liste d'attente du set
            context["administrator_status"] = False
        return context

    def render_set(
        self, connexion_user_status, context, request, user, set0, section_set, set0_id
    ):
        """"""
        context["set"] = set0
        if set0.statut_fermeture_admin:  # Le set est fermé
            return render(request, "set_ferme.html", context)
        else:
            # Le set n'est pas fermé
            if connexion_user_status == "connected_user":
                user_set = AuxilliariesSets().get_user_set(
                    user, set0
                )  # Vérification appartenance set utilisateur
                if user_set:  #   statut de l'utilisateur dans le set
                    statut_user_in_set = user_set.statut
                    context = AuxilliariesSets().context_set(
                        statut_user_in_set, context
                    )
                    return AuxilliariesSets().render_set_user_set(
                        request, section_set, set0_id, context, statut_user_in_set
                    )
                else:  # l'utilisateur n'appartient pas au set
                    return AuxilliariesSets().render_set_user_no_set(
                        request, section_set, set0_id, context
                    )
            elif connexion_user_status == "unconnected_user":  # unconnected user
                return AuxilliariesSets().render_set_user_no_registred(
                    request, section_set, set0_id, context
                )

    def render_set_connected_user(self, context, user, request, section_set, set0_id):
        """"""
        context["user"] = user
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            return AuxilliariesUser().redirect_unactivate_locked_user(
                user, "../../../user/home/"
            )
        else:
            # le compte est activé et n'est pas bloqué
            set0 = AuxilliariesSets().set_in_application(set0_id)
            if set0:
                # Le set existe dans l'application
                return AuxilliariesSets().render_set(
                    "connected_user", context, request, user, set0, section_set, set0_id
                )
            else:
                # Aucun set avec cet id dans l'application
                raise Http404()

    def render_set_unconnected_user(self, set0_id, context, request, user, section_set):
        """"""
        #  Vérification si l'identifiant du set correspond à un set dans l'application
        set0 = get_object_or_404(Sets, id=set0_id)
        if set0:
            #   Le set existe dans l'application
            return AuxilliariesSets().render_set(
                "unconnected_user", context, request, user, set0, section_set, set0_id
            )
        else:
            # Aucun set avec cet id dans l'application
            raise Http404()

    def render_event(self, connection_status, context, user, event_id, request):
        """"""
        context["user"] = user
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            return AuxilliariesUser().redirect_unactivate_locked_user(
                user, "../../../user/home/"
            )
        else:
            # le compte est activé et n'est pas bloqué
            # Vérification si l'identifiant de l'évènement correspond à un évènement dans l'application
            return self.render_event_activate_unlocked_unconnected(
                connection_status, event_id, context, request, user
            )

    def render_event_activate_unlocked_unconnected(
        self, connection_status, event_id, context, request, user
    ):
        """"""
        event0 = AuxilliariesSets().event_in_application(event_id)
        context["event"] = event0
        if event0:  # L'évènement existe dans l'application
            if event0.statut_fermeture_admin:  # L'évènement est fermé
                return render(request, "evenement_ferme.html", context)
            else:  # l'évènement n'est pas fermé
                return self.check_set_closed_render_event(
                    event0, context, request, connection_status, user, event_id
                )
        else:  # Aucun Evènement avec cet id dans l'application
            raise Http404()

    def check_set_closed_render_event(
        self, event0, context, request, connection_status, user, event_id
    ):
        """"""
        set0 = event0.set0
        context["set"] = set0
        if set0.statut_fermeture_admin:  # Le set ou l'évènement sont fermés
            return render(request, "evenement_ferme.html", context)
        else:
            # Le set et l'évènement ne sont pas fermés
            return self.render_event_set_and_event_unlocked(
                connection_status, user, set0, context, event_id, request, event0
            )

    def render_event_set_and_event_unlocked(
        self, connection_status, user, set0, context, event_id, request, event0
    ):
        """"""
        if connection_status == "connected_user":
            user_set = AuxilliariesSets().get_user_set(
                user, set0.id
            )  # Vérification appartenance set utilisateur
            context["user_set"] = user_set
            if user_set:  #   L'utilisateur appartient au set
                publications = PublicationEvenement.objects.filter(
                    evenement_id=event_id
                )
                context["publications_likeurs"] = self.publications_likeurs_context(
                    publications, request, "events"
                )
                statut_user_in_set = user_set.statut
                if (
                    statut_user_in_set == "attente_validation"
                ):  # L'utilisateur est en attente de validation du set
                    return render(request, "evenement_await_enter_set.html", context)
                else:  # L'utilisateur est membre entier du set
                    return self.render_event_user_set(context, user, event0, request)
            else:  # l'utilisateur n'appartient pas au set
                return render(request, "evenement_no_access_event.html", context)
        elif connection_status == "unconnected_user":
            return render(request, "evenement_no_access_event.html", context)

    def render_event_user_set(self, context, user, event0, request):
        """"""
        # L'utilisateur est membre entier du set
        new_post_form = PublicationEventForm()
        context["new_post_form"] = new_post_form
        if user == event0.administrateur:
            # L'utilisateur est administrateur de l'évènement
            event_description_form = SetDescriptionSetEvent()
            context["event_description_form"] = event_description_form
            return render(request, "evenement_administrator_event.html", context)
        else:
            # L'utilisateur n'est pas administrateur de l'évènement
            return render(request, "evenement_no_administrator_event.html", context)

    def render_search(self, section, request, context):
        """"""
        if section == "personnes":
            contenus = Utilisateurs.objects.filter(nom=request.GET["search_input"])
            try:
                owner = Utilisateurs.objects.get(id=request.session["user_id"])
                contacts = Contact.objects.filter(
                    contact_owner_id=request.session["user_id"]
                )
                users_in_contact = [contact.contact for contact in contacts]
                context["is_connected"] = True
            except Exception as e:
                users_in_contact = []
                owner = None
            context["users_in_contact"] = users_in_contact
            context["owner"] = owner
        elif section == "evenements":
            contenus = Evenements.objects.filter(nom=request.GET["search_input"])
        elif section == "sets":
            contenus = Sets.objects.filter(nom=request.GET["search_input"])
        context["contenus"] = contenus
        return render(request, "search.html", context)

    def update_set(self, part_of_set, set0, context, user, set0_id, request):
        """"""
        if set0.statut_fermeture_admin:  # Le set est fermé
            return redirect("../../sets/set/" + str(set0.id) + "/")
        else:  # le set n'est pas fermé
            context["set"] = set0
            user_set = AuxilliariesSets().get_user_set(
                user, set0_id
            )  # 		Vérification appartenance set utilisateur
            if user_set:
                return self.update_set_user_set(user_set, request, part_of_set, set0)
            else:  # l'utilisateur n'appartient pas au set
                return redirect("../../user/home/")

    def update_set_user_set(self, user_set, request, part_of_set, set0):
        """"""
        statut_user_in_set = user_set.statut  #   statut de l'utilisateur dans le set
        if (
            statut_user_in_set == "administrateur"
        ):  # L'utilisateur est administrateur du set
            if part_of_set == "cover":
                form = SetCoverImageForm(request.POST, request.FILES)
            elif part_of_set == "description":
                form = SetDescriptionSetForm(request.POST)
            if form.is_valid():  # formulaire valide
                if part_of_set == "cover":
                    set0.image_couverture = request.FILES["file"]
                    set0.save()
                elif part_of_set == "description":
                    set0.description = request.POST["description"]
                    set0.save()
                return redirect("../../sets/set/" + str(set0.id) + "/")
            else:  # formulaire invalide
                raise Http404()
        elif (
            statut_user_in_set == "attente_validation"
            or statut_user_in_set == "dans_set"
        ):  # L'utilisateur n'est pas administrateur du set
            return redirect("../../sets/set/" + str(set0.id) + "/")

    def make_post(self, entity, set0_id, request, set_id, event_id):
        """"""
        if entity == "set":
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
        elif entity == "event":
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

    def make_post_set(self, set0, user, set0_id, request, set_id):
        """"""
        if set0.statut_fermeture_admin:  # Le set est fermé
            return redirect("../../sets/set/" + str(set0.id) + "/")
        else:  #    le set n'est pas fermé
            user_set = self.get_user_set(
                user, set0_id
            )  #    Vérification appartenance set utilisateur
            if user_set:  #   statut de l'utilisateur dans le set
                statut_user_in_set = user_set.statut
                if (
                    statut_user_in_set == "administrateur"
                    or statut_user_in_set == "dans_set"
                ):  # L'utilisateur est administrateur ou simple membre du set
                    post_form = PublicationSetForm(request.POST, request.FILES)
                    if post_form.is_valid():  # Formulaire valide
                        if self.form_is_not_empty(request):
                            return self.make_post("set", set0_id, request, set_id, None)
                        else:
                            raise Http404()
                    else:
                        raise Http404()
                elif (
                    statut_user_in_set == "attente_validation"
                ):  # L'utilisateur est sur la liste d'attente du set
                    raise Http404()
            else:  # l'utilisateur n'appartient pas au set
                raise Http404()

    def make_post_event(self, event0, context, user, event_id, request):
        """"""
        if event0.statut_fermeture_admin:  # L'évènement est fermé
            return redirect("../../../sets/event/" + str(event0.id) + "/")
        else:  # l'évènement n'est pas fermé
            set0 = event0.set0
            context["set"] = set0
            if set0.statut_fermeture_admin:  # Le set est fermé
                return redirect("../../../sets/event/" + str(event0.id) + "/")
            else:  # le set n'est pas fermé
                user_set = self.get_user_set(
                    user, set0.id
                )  #   Vérification appartenance set utilisateur
                context["user_set"] = user_set
                if user_set:  #   L'utilisateur appartient au set
                    return self.make_post_event_user_set(user_set, request, event_id)
                else:  # l'utilisateur n'appartient pas au set
                    raise Http404()

    def make_post_event_user_set(self, user_set, request, event_id):
        """"""
        statut_user_in_set = user_set.statut
        if (
            statut_user_in_set == "attente_validation"
        ):  # L'utilisateur est en attente de validation du set
            raise Http404()
        else:  # L'utilisateur est membre entier du set
            post_form = PublicationEventForm(request.POST, request.FILES)
            if post_form.is_valid():  # Formulaire valide
                if self.form_is_not_empty(request):  # Formulaire non vide
                    return self.make_post("event", None, request, None, event_id)
                else:  # Formulaire vide
                    raise Http404()
            else:  # Formulaire invalide
                raise Http404()

    def manage_like_post(self, entity, post_id, request, user, post0):
        """"""
        if entity == "set":
            check = JaimePublicationSet.objects.filter(
                publication_set_id=post_id, jaimeur_id=request.session["user_id"]
            )
            if len(check) == 0:
                like = JaimePublicationSet.objects.create(
                    publication_set=post0, jaimeur=user
                )
                return HttpResponse("like_make")
            else:
                check[0].delete()
                return HttpResponse("unlike_make")
        elif entity == "event":
            check = JaimePublicationEvenement.objects.filter(
                publication_evenement_id=post_id, jaimeur_id=request.session["user_id"]
            )
            if len(check) == 0:
                like = JaimePublicationEvenement.objects.create(
                    publication_evenement=post0, jaimeur=user
                )
                return HttpResponse("like_make")
            else:
                check[0].delete()
                return HttpResponse("unlike_make")

    def http_like_post_set(self, set0, user, post_id, post0, request):
        """"""
        if set0.statut_fermeture_admin:  # Le set est fermé
            return redirect("../../sets/set/" + str(set0.id) + "/")
        else:  # le set n'est pas fermé
            user_set = AuxilliariesSets().get_user_set(
                user, set0.id
            )  #   Vérification appartenance set utilisateur
            if user_set:  #   statut de l'utilisateur dans le set
                statut_user_in_set = user_set.statut
                if (
                    statut_user_in_set == "attente_validation"
                ):  # L'utilisateur est en attente de validation du set
                    return HttpResponse("validate_enter_set_first")
                else:  # L'utilisateur est membre entier du set
                    return AuxilliariesSets().manage_like_post(
                        "set", post_id, request, user, post0
                    )
            else:  # l'utilisateur n'appartient pas au set
                raise Http404()

    def http_like_post_event(self, event0, user, request, post_id, post0):
        """"""
        if event0.statut_fermeture_admin:  # L'évènement est fermé
            return HttpResponse("event_locked")
        else:  # l'évènement n'est pas fermé
            set0 = event0.set0
            if set0.statut_fermeture_admin:  # Le set est fermé
                return HttpResponse("set_locked")
            else:  # le set n'est pas fermé
                user_set = AuxilliariesSets().get_user_set(
                    user, set0.id
                )  #   Vérification appartenance set utilisateur
                if user_set:  #   L'utilisateur appartient au set
                    statut_user_in_set = (
                        user_set.statut
                    )  #   statut de l'utilisateur dans le set
                    if (
                        statut_user_in_set == "attente_validation"
                    ):  # L'utilisateur est en attente de validation du set
                        return HttpResponse("validate_enter_set_first")
                    else:  # L'utilisateur est membre entier du set
                        return AuxilliariesSets().manage_like_post(
                            "event", post_id, request, user, post0
                        )
                else:  # l'utilisateur n'appartient pas au set
                    raise Http404()

    def make_delete_add_user_set(self, set0, user, set0_id, user_to_delete_add):
        """"""
        if set0.statut_fermeture_admin:  # Le set est fermé
            return redirect("../../../../sets/set/" + str(set0.id) + "/")
        else:  # le set n'est pas fermé
            user_set = AuxilliariesSets().get_user_set(
                user, set0_id
            )  #   Vérification appartenance set utilisateur
            if user_set:  #   statut de l'utilisateur dans le set
                statut_user_in_set = user_set.statut
                if (
                    statut_user_in_set == "administrateur"
                ):  # L'utilisateur est administrateur du set
                    return self.make_delete_add_user_set_administrator(
                        user_to_delete_add, set0_id, set0
                    )
                else:  # L'utilisateur n'est pas administrateur du set
                    raise Http404()
            else:  # l'utilisateur n'appartient pas au set
                raise Http404()

    def make_delete_add_user_set_administrator(self, user_to_delete_add, set0_id, set0):
        """"""
        user_set_to_delete_add = AuxilliariesSets().get_user_set(
            user_to_delete_add, set0_id
        )
        if (
            user_set_to_delete_add
        ):  # l'utilisateur à supprimer ou ajouter est dans le set
            user_set_to_delete_add.delete()
            return HttpResponse("user_deleted")
        else:  # L'utilisateur à supprimer ou ajouter n'est pas dans le set
            user_set_to_delete_add = SetUtilisateurs.objects.create(
                set0=set0, utilisateur=user_to_delete_add, statut="attente_validation"
            )
            return HttpResponse("user_added")

    def manage_enter_user_set(self, set0, user, set0_id, request):
        """"""
        if set0.statut_fermeture_admin:  # Le set est fermé
            return redirect("../../sets/set/" + str(set0.id) + "/")
        else:  # le set n'est pas fermé
            user_set = AuxilliariesSets().get_user_set(
                user, set0_id
            )  #   Vérification appartenance set utilisateur
            if user_set:  # -)   statut de l'utilisateur dans le set
                statut_user_in_set = user_set.statut
                if (
                    statut_user_in_set == "attente_validation"
                ):  # L'utilisateur est en attente d'entrée dans le set
                    if (
                        request.GET["confirm_enter"] == "yes"
                    ):  # L'utilisateur confirme son entrée dans le set
                        user_set.statut = "dans_set"
                        user_set.save()
                        return HttpResponse("added_done")
                    elif (
                        request.GET["confirm_enter"] == "no"
                    ):  # L'utilisateur annule son entrée dans le set
                        user_set.delete()
                        return HttpResponse("delete_done")
                else:  # L'utilisateur n'est pas en attente d'entrée dans le set
                    raise Http404()
            else:  # l'utilisateur n'appartient pas au set
                raise Http404()

    def make_exit_set(self, set0, user, set0_id):
        """"""
        if set0.statut_fermeture_admin:  # Le set est fermé
            return redirect("../../sets/set/" + str(set0.id) + "/")
        else:  # le set n'est pas fermé
            user_set = AuxilliariesSets().get_user_set(
                user, set0_id
            )  #   Vérification appartenance set utilisateur
            if user_set:
                statut_user_in_set = (
                    user_set.statut
                )  # -)   statut de l'utilisateur dans le set
                return self.make_exit_set_user_in_set(
                    statut_user_in_set, user_set, set0
                )
            else:  # l'utilisateur n'appartient pas au set
                raise Http404()

    def make_exit_set_user_in_set(self, statut_user_in_set, user_set, set0):
        """"""
        if statut_user_in_set == "administrateur":  # L'utilisateur est administrateur
            user_set.delete()
            if (
                len(SetUtilisateurs.objects.filter(set0=set0)) == 0
            ):  # Aucun utilisateur dans le set après la suppression
                set0.delete()
                return HttpResponse("delete_done_and_set_delete_done")

            else:  # présense d'utilisateurs dans le set après la suppression
                next_admin = SetUtilisateurs.objects.filter(set0=set0).order_by("date")[
                    0
                ]
                next_admin.statut = "administrateur"
                next_admin.save()
                return HttpResponse("delete_done")
        else:  # L'utilisateur n'est pas administrateur
            user_set.delete()
            return HttpResponse("delete_done")

    def make_delete_set(self, set0, context, user):
        """"""
        if set0.statut_fermeture_admin:  # Le set est fermé
            return redirect("../../sets/set/" + str(set0.id) + "/")
        else:  # le set n'est pas fermé
            context["set"] = set0
            user_set = AuxilliariesSets().get_user_set(user, set0)
            context["user_set"] = user_set
            if user_set:  # L'utilisateur appartient au set
                if (
                    user_set.statut == "administrateur"
                ):  # L'utilisateur est administrateur du set
                    set0.delete()
                    return redirect("../../../user/home/")
                else:  # L'utilisateur n'est pas administrateur du set
                    raise Http404()
            else:  # L'utilisateur n'appartient pas au set
                raise Http404()

    def make_delete_event(self, context, event0, user):
        """"""
        if event0.statut_fermeture_admin:  # L'évènement est fermé
            return redirect("../../../sets/event/" + str(event0.id) + "/")
        else:  # l'évènement n'est pas fermé
            set0 = event0.set0
            if set0.statut_fermeture_admin:  # Le set est fermé
                return redirect("../../sets/set/" + str(set0.id) + "/")
            else:  # le set n'est pas fermé
                context["set"] = set0
                user_set = AuxilliariesSets().get_user_set(user, set0)
                context["user_set"] = user_set
                if user_set:  # L'utilisateur appartient au set
                    if (
                        event0.administrateur == user
                    ):  # L'utilisateur est administrateur de lévènement
                        event0.delete()
                        return redirect("../../set/" + str(set0.id) + "/")
                    else:  # L'utilisateur n'est pas administrateur de lévènement
                        raise Http404()
                else:  # L'utilisateur n'appartient pas au set
                    raise Http404()
