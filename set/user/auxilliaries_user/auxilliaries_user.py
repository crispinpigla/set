""""""
from django.shortcuts import render, get_object_or_404, redirect

from django.db.models import Q

from ..models import Utilisateurs, Message, Contact

from sets.models import SetUtilisateurs, PublicationSet, JaimePublicationSet

# from sets.auxilliaries_sets.auxilliaries_sets import AuxilliariesSets

from user.forms import (
    SearchForm,
    MessageForm,
    ProfilImageForm,
    SetNameForm,
    SetMailForm,
)

from django.http import HttpResponse, Http404


class AuxilliariesUser:

    """docstring for AuxilliariesUser"""

    def __init__(self):
        """"""
        pass

    def get_user(self, request):
        """"""
        try:
            user = Utilisateurs.objects.get(id=request.session["user_id"])
        except Exception as e:
            user = None
        return user

    def user_in_application(self, user_id):
        """"""
        try:
            out = get_object_or_404(Utilisateurs, id=user_id)
        except Exception as e:
            out = None
        return out

    def message_in_application(self, message_id):
        """"""
        try:
            out = get_object_or_404(Message, id=message_id)
        except Exception as e:
            out = None
        return out

    def render_unactivate_or_locked_account(self, user, request):
        """"""
        if not user.statut_activation_compte:
            # Le compte n'est pas activé
            search_form = SearchForm()
            context = {"search_form": search_form, "user": user}
            return render(request, "compte_inactif.html", context)
        elif user.statut_blocage_admin:
            # Le compte a été bloqué
            search_form = SearchForm()
            context = {"search_form": search_form, "user": user}
            return render(request, "compte_ferme.html", context)

    def publications_likeurs_context(self, publications, request):
        """"""
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
        return publications_likeurs

    def render_home(self, user, request):
        """"""
        sets_user = SetUtilisateurs.objects.filter(utilisateur=user)
        publications = []
        for set_user in sets_user:
            publications0 = PublicationSet.objects.filter(set0=set_user.set0)
            for publication in publications0:
                publications.append(publication)
        publications = publications[:10]
        search_form = SearchForm()
        context = {
            "search_form": search_form,
            "user": user,
            "publications_likeurs": self.publications_likeurs_context(
                publications, request
            ),
        }
        return render(request, "acceuil.html", context)

    def redirect_unactivate_locked_user(self, user, link):
        """"""
        if not user.statut_activation_compte:
            # Le compte n'est pas activé
            return redirect(link)
        elif user.statut_blocage_admin:
            # Le compte a été bloqué
            return redirect(link)

    def httpresponse_unactivate_locked_user(self, user):
        """"""
        if not user.statut_activation_compte:
            # Le compte n'est pas activé
            return HttpResponse("account_unactivate")
        elif user.statut_blocage_admin:
            # Le compte a été bloqué
            return HttpResponse("account_locked")

    def get_lasts_messages_user(self, request):
        """"""
        messages0 = Message.objects.filter(
            Q(which_from=request.session["user_id"])
            | Q(which_to=request.session["user_id"])
        ).order_by("-date")
        # rangement des messages par auteur du message
        users_messages = []
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
        return users_messages

    def render_messages_exchanges(self, request, correspondant, user):
        """"""
        # Le correspondant est différent de l'utilisateur
        search_form = SearchForm()
        message_form = MessageForm()
        messages = Message.objects.filter(
            (Q(which_from=request.session["user_id"]) & Q(which_to=correspondant.id))
            | (Q(which_from=correspondant.id) & Q(which_to=request.session["user_id"]))
        ).order_by("date")
        context = {
            "search_form": search_form,
            "message_form": message_form,
            "messages": messages,
            "user_to": correspondant,
            "user": user,
        }
        return render(request, "message_exchange.html", context)

    def render_update_messages(self, request, correspondant, user):
        """"""
        last_message = self.message_in_application(request.GET["last_message_id"])
        if last_message:
            # Un dernier message existe avec l'id recu
            messages = Message.objects.filter(
                (
                    (
                        Q(which_from=request.session["user_id"])
                        & Q(which_to=correspondant.id)
                    )
                    | (
                        Q(which_from=correspondant.id)
                        & Q(which_to=request.session["user_id"])
                    )
                )
                & Q(date__gt=last_message.date)
            ).order_by("date")
        else:
            # Un dernier message n'existe pas avec l'id recu
            messages = Message.objects.filter(
                (
                    (
                        Q(which_from=request.session["user_id"])
                        & Q(which_to=correspondant.id)
                    )
                    | (
                        Q(which_from=correspondant.id)
                        & Q(which_to=request.session["user_id"])
                    )
                )
            ).order_by("date")
        context = {"messages": messages, "user": user}
        return render(request, "un_message.html", context)

    def http_send_message(self, request, correspondant, user):
        """"""
        message_text = request.GET["message_text"]
        message = Message.objects.create(
            which_from=user, which_to=correspondant, contenu_text=message_text
        )
        return HttpResponse("send")

    def check_delete_add_contact(self, user, contact):
        """"""
        check = Contact.objects.filter(contact_owner_id=user.id, contact_id=contact.id)
        if len(check) == 0:
            new_contact = Contact.objects.create(contact_owner=user, contact=contact)
            return HttpResponse("contact_added")
        else:
            check[0].delete()
            return HttpResponse("contact_deleted")

    def get_sections_pages(self, request, page):
        """"""
        if page == "profil":
            try:
                section_profil = request.GET["section_profil"]
            except Exception as e:
                section_profil = "sets"
            section = section_profil
        elif page == "recherche":
            try:
                section = request.GET["section"]
            except Exception as e:
                section = "sets"
        elif page == "set":
            pass
        return section

    def get_own_profil(self, request, context, section_profil, user):
        """"""
        image_cover_form = ProfilImageForm()
        context["image_cover_form"] = image_cover_form
        if section_profil == "sets":
            sets_user_profil = SetUtilisateurs.objects.filter(utilisateur=user)
            context["sets_user_profil"] = sets_user_profil
            return render(request, "profil.html", context)
        elif section_profil == "coordonees":
            set_name_form = SetNameForm()
            set_mail_form = SetMailForm()
            context["set_name_form"] = set_name_form
            context["set_mail_form"] = set_mail_form
            return render(request, "profil.html", context)
        else:
            raise Http404()

    def get_profil_else(self, context, target, section_profil, request):
        """"""
        if section_profil == "sets":
            sets_user_profil = SetUtilisateurs.objects.filter(utilisateur=target)
            context["sets_user_profil"] = sets_user_profil
            return render(request, "profil.html", context)
        elif section_profil == "coordonees":
            return render(request, "profil.html", context)
        else:
            raise Http404()

    def get_profil_connected_user(self, user, target, request):
        """"""
        context = {"user": user}
        if target:
            # La cible est un utilisateur existant dans l'application
            context["user_profil"] = target
            search_form = SearchForm()
            context["search_form"] = search_form
            # section du profil
            context["section_profil"] = self.get_sections_pages(request, "profil")
            if target != user:
                # La cible est différente de l'utilisateur
                return self.get_profil_else(
                    context, target, self.get_sections_pages(request, "profil"), request
                )
            else:
                # La cible est égal à l'utilisateur
                return self.get_own_profil(
                    request, context, self.get_sections_pages(request, "profil"), user
                )
        else:
            # La cible n'est pas un utilisateur existant de l'application
            raise Http404()

    def get_profil_unconnected_user(self, target, context, request):
        """"""
        context["user_profil"] = target
        search_form = SearchForm()
        context["search_form"] = search_form
        # section du profil
        context["section_profil"] = self.get_sections_pages(request, "profil")
        # La cible est différente de l'utilisateur
        return self.get_profil_else(
            context, target, self.get_sections_pages(request, "profil"), request
        )
