from django.shortcuts import render

from django.shortcuts import redirect

from user.models import Utilisateurs

from .forms import InscriptionForm, ConnexionForm, SearchForm, InitializePasswordForm, LinkResetPasswordForm, ResetPasswordForm


# Create your views here.
from django.http import HttpResponse

def index(request):
	""""""
	if  'authentification/' in request.build_absolute_uri():
		return redirect("connexion/")
	else:
		return redirect("authentification/connexion/")


def connexion(request):
	""""""

	try:
		# Utilisateur connecté
		request.session["user_id"]
		return redirect("../../user/")
	except Exception as e:
		# Utilisateur non connecté
		try  :
			# Envoie du formulaire de connexion
			request.POST['csrfmiddlewaretoken']
			connexion_form = ConnexionForm(request.POST)
			if connexion_form.is_valid() :
				users_in_database = Utilisateurs.objects.filter(adresse_mail=request.POST['email'])
				if len(users_in_database) == 0 :
					return HttpResponse('Aucun utilisateur ne possède un compte avec cette adresse mail')
				else:
					if users_in_database[0].mot_de_passe == request.POST['password'] :
						# adresse et mot de passe correct
						request.session["user_id"] = users_in_database[0].id
						return redirect("../../user/")
					else:
						return HttpResponse('Mot de passe incorrect')
			else:
				if not connexion_form.is_valid() :
					# Formulaire pas valide
					connexion_form.errors.items()
					return HttpResponse('Formulaire pas valide')
				
				
		except Exception as e:
			# Demande du formulaire de connexion
			connexion_form = ConnexionForm()
			search_form = SearchForm()
			context = { "connexion_form" : connexion_form, "search_form":search_form}
			#request.session["user_id"] = 1
			return render(request, "connexion.html", context)



	


def inscription(request):
	""""""

	try:
		# Utilisateur connecté
		request.session["user_id"]
		return redirect("../../user/")
	except Exception as e:
		# Utilisateur non connecté
		try  :
			# Envoie du formulaire d'inscription
			request.POST['csrfmiddlewaretoken']
			inscription_form = InscriptionForm(request.POST)
			if inscription_form.is_valid() and (request.POST['password'] == request.POST['confirmation_password'] ) :
				users_in_database = Utilisateurs.objects.filter(adresse_mail=request.POST['email'])
				if len(users_in_database) == 0 :
					user = Utilisateurs.objects.create(
	                nom=request.POST['name'],
	                adresse_mail=request.POST['email'],
	                mot_de_passe=request.POST['password'],
	            	)
					request.session["user_id"] = user.id
					return redirect("../../user/")
				else:
					return HttpResponse('Un compte possédant cette adresse mail existe déjà')
			else:
				if not inscription_form.is_valid() :
					# Formulaire pas valide
					inscription_form.errors.items()
					return HttpResponse('Formulaire pas valide')
				elif request.POST['password'] != request.POST['confirmation_password'] :
					# Mot de passe différent de la confirmation
					return HttpResponse('Mot de passe différent de la confirmation')


		except Exception as e:
			# Demande du formulaire d'inscription
			inscription_form = InscriptionForm()
			search_form = SearchForm()
			context = { "inscription_form" : inscription_form, "search_form":search_form}
			return render(request, "inscription.html", context)

def envoie_lien_reinitialisation_password(request):
	""""""
	print('uuuuuuuuuuuuuuuuuuuuuu')
	try:
		# Utilisateur connecté
		request.session["user_id"]
		return redirect("../../user/")
	except Exception as e:
		# Utilisateur non connecté
		print('oooooooooooooooooooooooooo')
		link_reset_form = LinkResetPasswordForm()
		search_form = SearchForm()
		context = { "link_reset_form" : link_reset_form, "search_form":search_form}
		return render(request, "envoie_lien_reinitialisation_mot_de_passe.html", context)


def reinitialisation_mot_de_passe(request):
	""""""
	try:
		# Utilisateur connecté
		request.session["user_id"]
		return redirect("../../user/")
	except Exception as e:
		# Utilisateur non connecté
		reset_form = ResetPasswordForm()
		search_form = SearchForm()
		context = { "reset_form" : reset_form, "search_form":search_form}
		return render(request, "reinitialisation_mot_de_passe.html", context)


def initialisation_mot_de_passe(request):
	""""""
	try:
		# Utilisateur connecté
		request.session["user_id"]
		return redirect("../../user/")
	except Exception as e:
		# Utilisateur non connecté
		initialize_form = InitializePasswordForm()
		search_form = SearchForm()
		context = { "initialize_form" : initialize_form, "search_form":search_form}
		return render(request, "initialisation_mot_de_passe.html", context)


