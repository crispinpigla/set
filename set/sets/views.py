"""  Vue de l'application sets  """


# Create your views here.
from django.http import Http404
from django.shortcuts import redirect

from user.auxilliaries_user.auxilliaries_user import AuxilliariesUser
from .auxilliaries_sets.auxilliaries_sets import AuxilliariesSets

from .forms import SearchForm


def creation_set(request):
    """Crée un nouveau set """
    # Vérification connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)
    if user:
        # Utilisateur connecté
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            return AuxilliariesUser().redirect_unactivate_locked_user(
                user, "../../user/home/"
            )
        else:
            # le compte est activé et n'est pas bloqué
            search_form = SearchForm()
            if request.method == "POST":
                # Creation de set
                return AuxilliariesSets().create_set(request, user, search_form)
            else:
                # Demande de page de création de set
                return AuxilliariesSets().get_create_set_page(
                    request, search_form, user
                )
    else:
        # Utilisateur non connecté
        return redirect("../../authentification/connexion/")


def creation_evenement(request, set_id):
    """Crée un nouvel évènement"""
    # Vérification connexion utilisateur
    user = AuxilliariesUser().get_user(request)
    set0_id = AuxilliariesSets().get_int_parameter(set_id)
    context = {"search_form": SearchForm(), "user": user}
    if user:
        # Utilisateur connecté
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
                # Le set existe
                return AuxilliariesSets().create_event_if_set_opened(
                    context, request, set0, user, set0_id
                )
            else:
                # Le set n'existe pas dans l'application
                raise Http404()
    else:
        # Utilisateur non connecté
        return redirect("../../authentification/connexion/")


def sets(request, set_id):
    """Gère l'affichage d'un set"""
    set0_id = AuxilliariesSets().get_int_parameter(set_id)
    section_set = AuxilliariesSets().get_section_set(request)
    user = AuxilliariesUser().get_user(request)
    context = {"search_form": SearchForm(), "section_set": section_set, "user": user}
    #   Vérification inscription utilisateur
    if user:
        # Utilisateur connecté
        return AuxilliariesSets().render_set_connected_user(
            context, user, request, section_set, set0_id
        )
    else:
        #      Utilisateur non-inscrit
        return AuxilliariesSets().render_set_unconnected_user(
            set0_id, context, request, user, section_set
        )


def evenements(request, event_id):
    """Gère l'affichage d'un évènement"""
    event_id = AuxilliariesSets().get_int_parameter(event_id)
    user = AuxilliariesUser().get_user(request)
    context = {"search_form": SearchForm(), "user": user}
    #   Vérification inscription utilisateur
    if user:  #       Utilisateur connecté
        return AuxilliariesSets().render_event(
            "connected_user", context, user, event_id, request
        )
    else:  #      Utilisateur non-inscrit
        return AuxilliariesSets().render_event_activate_unlocked_unconnected(
            "unconnected_user", event_id, context, request, user
        )


def search(request):
    """Gère les recherches"""
    user = AuxilliariesUser().get_user(request)
    context = {"recherche": request.GET["search_input"], "search_form": SearchForm()}
    section = AuxilliariesUser().get_sections_pages(
        request, "recherche"
    )  # section de la recherche
    context["section"] = section
    context["user"] = user
    if user:
        # utilisateur connecté
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            return AuxilliariesUser().redirect_unactivate_locked_user(
                user, "../../../user/home/"
            )
        else:
            # le compte est activé et n'est pas bloqué
            return AuxilliariesSets().render_search(section, request, context)
    else:
        # Utilisateur non connecté
        return AuxilliariesSets().render_search(section, request, context)


def update_cover(request):
    """Met à jour l'image de couverture d'un set"""
    auxilliary_set = AuxilliariesSets()
    set0_id = AuxilliariesSets().get_int_parameter(request.GET["set_id"])
    user = AuxilliariesUser().get_user(request)
    context = {"user": user}
    #   Vérification inscription utilisateur
    if user:
        context["user"] = user
        if not user.statut_activation_compte or user.statut_blocage_admin:
            # Le compte n'est pas activé ou a été bloqué
            return AuxilliariesUser().redirect_unactivate_locked_user(
                user, "../../user/home/"
            )
        else:
            #     le compte est activé et n'est pas bloqué
            #     Vérification si l'identifiant du set correspond à un set dans l'application
            set0 = AuxilliariesSets().set_in_application(set0_id)
            if set0:
                return AuxilliariesSets().update_set(
                    "cover", set0, context, user, set0_id, request
                )
            else:
                #   Aucun set avec cet id dans l'application
                raise Http404()
    else:
        #      Utilisateur non-inscrit
        return redirect("../../authentification/connexion/")


def update_description_set(request):
    """Met à jour la description d'un set"""
    set0_id = AuxilliariesSets().get_int_parameter(request.GET["set_id"])
    user = AuxilliariesUser().get_user(request)
    context = {"user": user}
    if user:  #   Vérification inscription utilisateur
        context["user"] = user
        if (
            not user.statut_activation_compte or user.statut_blocage_admin
        ):  # Le compte n'est pas activé ou a été bloqué
            return AuxilliariesUser().redirect_unactivate_locked_user(
                user, "../../user/home/"
            )
        else:
            # le compte est activé et n'est pas bloqué
            # -)    Vérification si l'identifiant du set correspond à un set dans l'application
            set0 = AuxilliariesSets().set_in_application(set0_id)
            if set0:
                # Le set existe
                return AuxilliariesSets().update_set(
                    "description", set0, context, user, set0_id, request
                )
            else:
                # Aucun set avec set id dans l'application
                raise Http404()
    else:
        #      Utilisateur non-inscrit
        return redirect("../../authentification/connexion/")


def make_post_set(request, set_id):
    """Crée une publication dans un set"""
    set0_id = AuxilliariesSets().get_int_parameter(set_id)
    section_set = AuxilliariesSets().get_section_set(request)
    user = AuxilliariesUser().get_user(request)
    if user:  #   Utilisateur connecté
        if (
            not user.statut_activation_compte or user.statut_blocage_admin
        ):  # Le compte n'est pas activé ou a été bloqué
            return AuxilliariesUser().redirect_unactivate_locked_user(
                user, "../../../user/home/"
            )
        else:  # le compte est activé et n'est pas bloqué
            set0 = AuxilliariesSets().set_in_application(
                set0_id
            )  #    Vérification si l'identifiant du set correspond à un set dans l'application
            if set0:  # Le set existe
                return AuxilliariesSets().make_post_set(
                    set0, user, set0_id, request, set_id
                )
            else:  # Aucun set avec cet id dans l'application
                raise Http404()
    else:  # Utilisateur non-inscrit
        raise Http404()


def make_post_event(request, event_id):
    """Crée une publication dans un évènement"""
    event_id = AuxilliariesSets().get_int_parameter(event_id)
    user = AuxilliariesUser().get_user(request)
    context = {"search_form": SearchForm(), "user": user}
    if user:  #   Vérification inscription utilisateur
        context["user"] = user
        if (
            not user.statut_activation_compte or user.statut_blocage_admin
        ):  # Le compte n'est pas activé ou a été bloqué
            return AuxilliariesUser().redirect_unactivate_locked_user(
                user, "../../../user/home/"
            )
        else:  # le compte est activé et n'est pas bloqué
            event0 = AuxilliariesSets().event_in_application(
                event_id
            )  #   Vérification si l'identifiant de l'évènement correspond à un évènement dans l'application
            context["event"] = event0
            if event0:  # L'évènement existe dans l'application
                return AuxilliariesSets().make_post_event(
                    event0, context, user, event_id, request
                )
            else:  # Aucun Evènement avec cet id dans l'application
                raise Http404()
    else:  #      Utilisateur non-inscrit
        raise Http404()


def manage_like_post_set(request, post_id):
    """Ajout et supprime un like d'une publication d'un set"""
    post0_id = AuxilliariesSets().get_int_parameter(post_id)
    user = AuxilliariesUser().get_user(request)
    if user:  #   Vérification inscription utilisateur
        if (
            not user.statut_activation_compte or user.statut_blocage_admin
        ):  # Le compte n'est pas activé ou a été bloqué
            return AuxilliariesUser().httpresponse_unactivate_locked_user(user)
        else:  # le compte est activé et n'est pas bloqué
            post0 = AuxilliariesSets().post_set_in_application(post0_id)
            if post0:
                set0 = post0.set0
                if set0:  # Le set existe
                    return AuxilliariesSets().http_like_post_set(
                        set0, user, post_id, post0, request
                    )
                else:  # Aucun set avec cet id dans l'application
                    raise Http404()
            else:  # Aucune publication avec cet id
                raise Http404()
    else:  #      Utilisateur non-inscrit
        raise Http404()


def manage_like_post_event(request, post_id):
    """Ajout et supprime un like d'une publication d'un évènement"""
    post0_id = AuxilliariesSets().get_int_parameter(post_id)
    user = AuxilliariesUser().get_user(request)
    if user:  #   Vérification inscription utilisateur
        if (
            not user.statut_activation_compte or user.statut_blocage_admin
        ):  # Le compte n'est pas activé ou a été bloqué
            return AuxilliariesUser().httpresponse_unactivate_locked_user(user)
        else:  # le compte est activé et n'est pas bloqué
            post0 = AuxilliariesSets().post_event_in_application(
                post0_id
            )  # Vérification si l'identifiant de l'évènement correspond à un évènement dans l'application
            if post0:
                event0 = post0.evenement
                if event0:  # L'évènement existe dans l'application
                    return AuxilliariesSets().http_like_post_event(
                        event0, user, request, post_id, post0
                    )
                else:  # Aucun Evènement avec cet id dans l'application
                    raise Http404()
            else:  # Aucune publication avec cet id
                raise Http404()
    else:  #      Utilisateur non-inscrit
        raise Http404()


def delete_add_user_set(request, set_id, user_delete_add_id):
    """Ajoute et supprime un utilisateur d'un set"""
    set0_id = AuxilliariesSets().get_int_parameter(set_id)
    user_to_delete_add_id = AuxilliariesSets().get_int_parameter(user_delete_add_id)
    user = AuxilliariesUser().get_user(request)
    if user:  # l'utilisateur existe
        if (
            not user.statut_activation_compte or user.statut_blocage_admin
        ):  # Le compte n'est pas activé ou a été bloqué
            return AuxilliariesUser().httpresponse_unactivate_locked_user(user)
        else:  # le compte est activé et n'est pas bloqué
            set0 = AuxilliariesSets().set_in_application(
                set0_id
            )  #    Vérification si l'identifiant du set correspond à un set dans l'application
            user_to_delete_add = AuxilliariesUser().user_in_application(
                user_to_delete_add_id
            )
            if (
                set0 and user_to_delete_add
            ):  # Le set et l'utilisateur à ajouter/supprimer existent
                return AuxilliariesSets().make_delete_add_user_set(
                    set0, user, set0_id, user_to_delete_add
                )
            else:  # Aucun set avec cet id dans l'application ou aucun utilisateur dans l'application avec l'id recu
                raise Http404()
    else:  #      Utilisateur non-inscrit
        raise Http404()


def manage_enter_user_set(request, set_id):
    """Gère la validation de l'entrée d'un utilisateur dans un set"""
    set0_id = AuxilliariesSets().get_int_parameter(set_id)
    user = AuxilliariesUser().get_user(request)
    if user:  # -)   Vérification inscription utilisateur
        if (
            not user.statut_activation_compte or user.statut_blocage_admin
        ):  # Le compte n'est pas activé ou a été bloqué
            return AuxilliariesUser().httpresponse_unactivate_locked_user(user)
        else:  # le compte est activé et n'est pas bloqué
            set0 = AuxilliariesSets().set_in_application(
                set0_id
            )  #    Vérification si l'identifiant du set correspond à un set dans l'application
            if set0:  # Le set existe
                return AuxilliariesSets().manage_enter_user_set(
                    set0, user, set0_id, request
                )
            else:  # Aucun set avec cet id dans l'application ou aucun utilisateur dans l'application avec l'id recu
                raise Http404()
    else:  #      Utilisateur non-inscrit
        raise Http404()


def exit_set(request, set_id):
    """Sort un utilisateur d'un set"""
    set0_id = AuxilliariesSets().get_int_parameter(set_id)
    user = AuxilliariesUser().get_user(request)
    if user:  #   Vérification inscription utilisateur
        if (
            not user.statut_activation_compte or user.statut_blocage_admin
        ):  # Le compte n'est pas activé ou a été bloqué
            return AuxilliariesUser().httpresponse_unactivate_locked_user(user)
        else:  # le compte est activé et n'est pas bloqué
            set0 = AuxilliariesSets().set_in_application(
                set0_id
            )  #    Vérification si l'identifiant du set correspond à un set dans l'application
            if set0:  # Le set existe
                return AuxilliariesSets().make_exit_set(set0, user, set0_id)
            else:  # Aucun set avec cet id dans l'application ou aucun utilisateur dans l'application avec l'id recu
                raise Http404()
    else:  #      Utilisateur non-inscrit
        raise Http404()


def delete_set(request, set_id):
    """Supprime un set"""
    user = AuxilliariesUser().get_user(request)
    search_form = SearchForm()
    context = {"search_form": search_form, "user": user}
    if user:  # l'utilisateur est connecté
        if (
            not user.statut_activation_compte or user.statut_blocage_admin
        ):  # Le compte n'est pas activé ou a été bloqué
            return AuxilliariesUser().redirect_unactivate_locked_user(
                user, "../../../user/home/"
            )
        else:  # le compte est activé et n'est pas bloqué
            context["user"] = user
            set0 = AuxilliariesSets().set_in_application(set_id)
            if set0:  # Le set existe
                return AuxilliariesSets().make_delete_set(set0, context, user)
            else:  # L'évènement n'existe pas dans l'application
                raise Http404()
    else:  # L'utilisateur n'est pas connecté
        raise Http404()


def delete_event(request, event_id):
    """Supprime un évènement"""
    user = AuxilliariesUser().get_user(request)
    search_form = SearchForm()
    context = {"search_form": search_form, "user": user}
    if user:  # l'utilisateur est connecté
        if (
            not user.statut_activation_compte or user.statut_blocage_admin
        ):  # Le compte n'est pas activé ou a été bloqué
            return AuxilliariesUser().redirect_unactivate_locked_user(
                user, "../../../user/home/"
            )
        else:  # le compte est activé et n'est pas bloqué
            context["user"] = user
            event0 = AuxilliariesSets().event_in_application(event_id)
            context["event"] = event0
            if event0:  # L'évènement existe
                return AuxilliariesSets().make_delete_event(context, event0, user)
            else:  # L'évènement n'existe pas dans l'application
                raise Http404()
    else:  # L'utilisateur n'est pas connecté
        raise Http404()


def redirect_home(self):
    """Redirige vers la page d'acceuil"""
    return redirect("../../../user/home/")
