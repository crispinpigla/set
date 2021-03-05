import random, string

import requests
import json

import os

import google
from google.oauth2 import id_token
from google.auth.transport import requests as grequests

from django.shortcuts import render

from django.shortcuts import get_object_or_404

from django.template.loader import render_to_string

from django.core.mail import send_mail, EmailMessage

from django.shortcuts import redirect

from django.http import HttpResponse, Http404

from user.models import Utilisateurs

from user.auxilliaries_user.auxilliaries_user import AuxilliariesUser
from .auxilliaries_authentification.auxilliaries_authentification import AuxilliariesAuthentification

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
    """"""

    # Vérification connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)

    if user:
        # Utilisateur connecté
        mail = request.GET['mail']
        if user.adresse_mail == mail:
            # Le mail de l'utilisateur correspond au mail du compte recu
            if user.cle_dactivation_de_compte == request.GET['key_activation']  :
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
    """"""
    if "authentification/" in request.build_absolute_uri():
        return redirect("connexion/")
    else:
        return redirect("authentification/connexion/")




def connexion(request):
    """"""

    try:
        # Utilisateur connecté
        request.session["user_id"]
        return redirect("../../user/home/")
    except Exception as e:
        # Utilisateur non connecté
        try:
            # Envoie du formulaire de connexion
            request.POST["email"]
            connexion_form = ConnexionForm(request.POST)
            if connexion_form.is_valid():
                # Formulaire valide
            	users_in_database = Utilisateurs.objects.filter(adresse_mail=request.POST["email"])
            	if len(users_in_database) == 0:
                    # L'email recu ne correspond à aucun utilisateur de l'application
                    connexion_form = ConnexionForm()
                    search_form = SearchForm()
                    context = {"connexion_form": connexion_form, "search_form": search_form, 'no_mail_in_application_error':True }
                    return render(request, "connexion.html", context)
            	else:
                    # Il existe au moins un utilisateur dans l'application
                    if users_in_database[0].mot_de_passe == request.POST["password"]:
                    	# adresse et mot de passe correct
                    	request.session["user_id"] = users_in_database[0].id
                    	return redirect("../../user/home/")
                    else:
                        # Mot de passe incorrect
                        connexion_form = ConnexionForm()
                        search_form = SearchForm()
                        context = {"connexion_form": connexion_form, "search_form": search_form, 'password_error':True }
                        return render(request, "connexion.html", context)
            else:
                if not connexion_form.is_valid():
                    # Formulaire pas valide
                    context = {"connexion_form": ConnexionForm(), "search_form": SearchForm(), 'form_errors':connexion_form.errors.items() }
                    return render(request, "connexion.html", context)

        except Exception as e:
            # Demande du formulaire de connexion
            connexion_form = ConnexionForm()
            search_form = SearchForm()
            context = {"connexion_form": connexion_form, "search_form": search_form}
            # request.session["user_id"] = 1
            return render(request, "connexion.html", context)








def google_connect(request):
    """"""

    # Vérification connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)

    if user:
        # Utilisateur connecté
        return redirect("../../user/home/")
    else:
        # Utilisateur non connecté
        response_google_user = requests.get('https://oauth2.googleapis.com/tokeninfo?id_token=' + request.GET['token'] )
        if response_google_user.status_code == 200:
            # Requete vers l'api de google reussie
            google_user = response_google_user.json()
            check_user = Utilisateurs.objects.filter(adresse_mail=google_user['email'])
            if len(check_user) == 0 :
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
    """"""

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
            if inscription_form.is_valid() and (request.POST["password"] == request.POST["confirmation_password"]):
            	users_in_database = Utilisateurs.objects.filter(adresse_mail=request.POST["email"])
            	if len(users_in_database) == 0:
                    activation_key = "".join([random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(24)])
                    user = Utilisateurs.objects.create(nom=request.POST["name"], adresse_mail=request.POST["email"], mot_de_passe=request.POST["password"], cle_dactivation_de_compte=activation_key)
                    # Envoie de mail
                    if os.environ.get("ENV") == "PRODUCTION":
                        host = 'http://34.105.144.166'
                    else:
                        host = 'http://localhost:8000'
                    html_message = render_to_string('activation_compte.html', {'user': user, 'host':host})
                    msg = EmailMessage(subject='Activation du compte', body=html_message, from_email='', bcc=[user.adresse_mail])
                    msg.content_subtype = "html"
                    msg.send()
                    # Création de la session
                    request.session["user_id"] = user.id
                    return redirect("../../user/home/")
            	else:
                    inscription_form = InscriptionForm()
                    search_form = SearchForm()
                    context = {"inscription_form": inscription_form, "search_form": search_form, "already_mail_error":True}
                    return render(request, "inscription.html", context)
            else:
                if not inscription_form.is_valid():
                # Formulaire pas valide
                    context = {"inscription_form": InscriptionForm(), "search_form": SearchForm(), "inscription_form_error":inscription_form.errors.items()}
                    return render(request, "inscription.html", context)
                elif request.POST["password"] != request.POST["confirmation_password"]:
                    inscription_form = InscriptionForm()
                    search_form = SearchForm()
                    context = {"inscription_form": inscription_form, "search_form": search_form, "no_match_password_error":True}
                    return render(request, "inscription.html", context)

        except Exception as e:
            # Demande du formulaire d'inscription
            inscription_form = InscriptionForm()
            search_form = SearchForm()
            context = {"inscription_form": inscription_form, "search_form": search_form}
            return render(request, "inscription.html", context)




def envoie_activation_compte(request):
    """"""

    # Vérification connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)

    if user:
        # Utilisateur connecté
        activation_key = "".join([random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(24)])
        user.cle_dactivation_de_compte = activation_key
        user.save()

        if os.environ.get("ENV") == "PRODUCTION":
            host = 'http://34.105.144.166'
        else:
            host = 'http://localhost:8000'
        html_message = render_to_string('activation_compte.html', {'user': user, 'host':host})
        msg = EmailMessage(subject='Activation du compte', body=html_message, from_email='', bcc=[user.adresse_mail])
        msg.content_subtype = "html"
        msg.send()
        return redirect('../../user/home/')
    else:
        # Utilisateur non connecté
        raise Http404()




def envoie_lien_reinitialisation_password(request):
    """"""

    # Vérification connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)
    if user:
        # Utilisateur connecté
        request.session["user_id"]
        return redirect("../../user/home/")
    else:
        # Utilisateur non connecté
        if request.method == 'POST':
            # Traitement de l'envoie de lien de réinitialisation de mot de passe
            mail = request.POST['email']
            try:
                user = Utilisateurs.objects.get(adresse_mail=mail)
            except Exception as e:
                user = None

            if user  :
                # Un utilisateur avec l'email recu existe
                reinitialisation_password_key = "".join([random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(24)])
                user.cle_de_reinitialisation_de_mot_de_passe = reinitialisation_password_key
                user.save()

                if os.environ.get("ENV") == "PRODUCTION":
                    host = 'http://34.105.144.166'
                else:
                    host = 'http://localhost:8000'
                html_message = render_to_string('mail_reinitialisation_mot_de_passe.html', {'user': user, 'host':host})
                msg = EmailMessage(subject='Réinitialisation du mot de passe', body=html_message, from_email='', bcc=[user.adresse_mail])
                msg.content_subtype = "html"
                sent_mail_statut = msg.send()
                link_reset_form = LinkResetPasswordForm()
                search_form = SearchForm()
                context = {"link_reset_form": link_reset_form, "search_form": search_form, "send_mail":sent_mail_statut, "user":user }
                return render(request, "envoie_lien_reinitialisation_mot_de_passe.html", context)
            else:
                # Aucun utilisateur avec l'email recu existe
                # Demande de la page d'envoie de lien de réinitialisation de mot de passe
                link_reset_form = LinkResetPasswordForm()
                search_form = SearchForm()
                context = {"link_reset_form": link_reset_form, "search_form": search_form, "no_user_with_mail_error":True, 'mail':mail }
                return render(request, "envoie_lien_reinitialisation_mot_de_passe.html", context)
        else:
            # Demande de la page d'envoie de lien de réinitialisation de mot de passe
            link_reset_form = LinkResetPasswordForm()
            search_form = SearchForm()
            context = {"link_reset_form": link_reset_form, "search_form": search_form}
            return render(request, "envoie_lien_reinitialisation_mot_de_passe.html", context)






def reinitialisation_mot_de_passe(request):
    """"""

    # Vérification connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)

    if user:
        # Utilisateur connecté
        return redirect("../../user/home/")
    else:
        # Utilisateur non conecté
        if request.method == 'POST':
            ###################
            # Exécution de la réinitialisation de mot de passe
            reset_password_form = ResetPasswordForm(request.POST)
            search_form = SearchForm()
            if reset_password_form.is_valid():
                # formulaire valide
                mail = request.POST["email"]
                user = get_object_or_404(Utilisateurs, adresse_mail=mail)
                reset_form = ResetPasswordForm()
                if (request.POST["password"] == request.POST["confirmation_password"]) and ( user.cle_de_reinitialisation_de_mot_de_passe == request.POST["reset_key"] ) :
                    # Mot de passe et confirmation identiques et bonne clé
                    user.mot_de_passe = request.POST["password"]
                    user.cle_de_reinitialisation_de_mot_de_passe = None
                    user.save()
                    context = { "reset_password_form": reset_password_form, "search_form": search_form, 'user':user , 'state_reinitialisation':True , 'user':user, 'reset_form':reset_form }
                    return render(request, "reinitialisation_mot_de_passe.html", context)
                else:
                    #
                    if user.cle_de_reinitialisation_de_mot_de_passe != request.POST["reset_key"] :
                        # Mauvaise clé
                        raise Http404()
                    else:
                        # Mot de passe et confirmation non-identique
                        context = { "reset_password_form": reset_password_form, "search_form": search_form, 'user':user , 'password_different_to_confirmation':True , 'user':user, 'reset_form':reset_form }
                        return render(request, "reinitialisation_mot_de_passe.html", context)
            else:
                # formulaire pas valide
                context = {"reset_password_form": reset_password_form, "search_form": search_form}
                context['errors'] = reset_password_form.errors.items()
                return render(request, "reinitialisation_mot_de_passe.html", context)
            ###################
        else:
            # Demande de la page de réinitialisation de mot de passe
            mail = request.GET['mail']
            user = get_object_or_404(Utilisateurs, adresse_mail=mail)
            if user.cle_de_reinitialisation_de_mot_de_passe == request.GET['key_reinitialisation_password']  :
                reset_form = ResetPasswordForm()
                search_form = SearchForm()
                context = { "reset_form": reset_form, "search_form": search_form, 'user':user, "mail":mail }
                return render(request, "reinitialisation_mot_de_passe.html", context)
            else:
                # La clé de réinitialisation recue ne correspond pas à celle qui est stockée
                raise Http404()







def initialisation_mot_de_passe(request):
    """"""

    # Vérification connexion utilisateur
    auxilliary_user = AuxilliariesUser()
    user = auxilliary_user.get_user(request)

    if user:
        # Utilisateur connecté
        return redirect("../../user/home/")
    else:
        # Utilisateur non conecté
        if request.method == 'POST':
            # Traitement de la soummission du mot de passe
            ##############################
            initialize_form = InitializePasswordForm(request.POST)
            if initialize_form.is_valid() and (request.POST["password"] == request.POST["confirmation_password"]):
                users_in_database = Utilisateurs.objects.filter(adresse_mail=request.POST["email"])
                if len(users_in_database) == 0:
                    # Aucun utilisateur avec le mail recu
                    activation_key = "".join([random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(24)])
                    user = Utilisateurs.objects.create(nom=request.POST["name"], adresse_mail=request.POST["email"], mot_de_passe=request.POST["password"], cle_dactivation_de_compte=activation_key)
                    # Envoie de mail
                    if os.environ.get("ENV") == "PRODUCTION":
                        host = 'http://34.105.144.166'
                    else:
                        host = 'http://localhost:8000'
                    html_message = render_to_string('activation_compte.html', {'user': user, 'host':host})
                    msg = EmailMessage(subject='Activation du compte', body=html_message, from_email='', bcc=[user.adresse_mail])
                    msg.content_subtype = "html"
                    msg.send()
                    # Création de la session
                    request.session["user_id"] = user.id
                    return redirect("../../user/home/")
                else:
                    # Le mail recu appartient déjà à un autre utilisateur
                    initialize_form = InitializePasswordForm()
                    search_form = SearchForm()
                    context = {"initialize_form": initialize_form, "search_form": search_form, 'mail':request.POST['email'], 'name':request.POST['name'], "already_mail_error":True }
                    return render(request, "initialisation_mot_de_passe.html", context)
            else:
                if not initialize_form.is_valid():
                # Formulaire pas valide
                    context = {"initialize_form":InitializePasswordForm(), "search_form": SearchForm(), "initialize_password_form_error":initialize_form.errors.items(), 'mail':request.POST['email'], 'name':request.POST['name']}
                    context['initialize_form_errors'] = initialize_form.errors.items()
                    return render(request, "initialisation_mot_de_passe.html", context)
                elif request.POST["password"] != request.POST["confirmation_password"]:
                    context = {"initialize_form":InitializePasswordForm(), "search_form": SearchForm(), "no_match_password_error":True, 'mail':request.POST['email'], 'name':request.POST['name']}
                    return render(request, "initialisation_mot_de_passe.html", context)
            ##############################
        else:
            # Demande du formulaire de l'initialisation du mot de passe
            initialize_form = InitializePasswordForm()
            search_form = SearchForm()
            context = {"initialize_form": initialize_form, "search_form": search_form, 'mail':request.GET['mail'], 'name':request.GET['name'] }
            return render(request, "initialisation_mot_de_passe.html", context)

