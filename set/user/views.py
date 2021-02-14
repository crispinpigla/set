from django.shortcuts import render

from .forms import SearchForm, CreateSetForm, CreateEventForm

from .models import Utilisateurs
from sets.models import Sets, SetUtilisateurs, Evenements

from django.shortcuts import redirect

# Create your views here.
from django.http import HttpResponse









def home(request):
	""""""

	try  :
		# Utilisateur connecté
		request.session["user_id"]
		search_form = SearchForm()
		context = { "search_form":search_form }
		return render(request, "acceuil.html", context)

	except Exception as e:
		# Utilisateur non connecté
		return redirect("../authentification/connexion/")


def creation_set(request):
	""""""

	try  :
		# Utilisateur connecté
		request.session["user_id"]
		try  :
			# Reception du formulaire de creation de set
			request.POST['csrfmiddlewaretoken']
			create_set_form = CreateSetForm(request.POST, request.FILES)
			if create_set_form.is_valid() :
				user = Utilisateurs.objects.get(pk=request.session["user_id"])
				set0 = Sets.objects.create(
                nom=request.POST['name'],
                image_couverture=request.FILES['file'],
                type0=request.POST['type_set'],
                description=request.POST['description'],
            	)
				set_user = SetUtilisateurs.objects.create(
                set0=set0,
                utilisateur=user,
                statut='administrateur',
            	)
				return redirect("../../sets/set/" + str(set0.id) + '/')
			else:
				if not create_set_form.is_valid() :
					# Formulaire pas valide
					create_set_form.errors.items()
					print(create_set_form.errors.items())
					return HttpResponse('Formulaire pas valide')
		except Exception as e:
			# Demande du formulaire de creation de set
			create_set_form = CreateSetForm()
			search_form = SearchForm()
			context = { "create_set_form" : create_set_form, "search_form":search_form}
			#request.session["user_id"] = 1
			return render(request, "creation_set.html", context)

		search_form = SearchForm()
		create_set_form = CreateSetForm()
		context = { "search_form":search_form, "create_set_form" : create_set_form }
		return render(request, "creation_set.html", context)

	except Exception as e:
		# Utilisateur non connecté
		return redirect("../../authentification/connexion/")
    



def creation_evenement(request, set_id):
	""""""

	set0 = Sets.objects.filter(id=set_id)
	set0 = set0[0]

	try  :
		# Utilisateur connecté
		request.session["user_id"]
		try  :
			# Reception du formulaire de creation de set
			request.POST['csrfmiddlewaretoken']
			create_event_form = CreateEventForm(request.POST)
			if create_event_form.is_valid() :
				user = Utilisateurs.objects.get(pk=request.session["user_id"])
				event = Evenements.objects.create(
				set0=set0,
                nom=request.POST['name'],
                description=request.POST['description'],
            	)
				return redirect("../../sets/evenement/" + str(event.id) + '/')
			else:
				if not create_event_form.is_valid() :
					# Formulaire pas valide
					create_event_form.errors.items()
					print(create_event_form.errors.items())
					return HttpResponse('Formulaire pas valide')
		except Exception as e:
			# Demande du formulaire de creation de set
			create_event_form = CreateEventForm()
			search_form = SearchForm()
			context = { "create_event_form" : create_event_form, "search_form":search_form, "set":set0 }
			return render(request, "creation_evenement.html", context)





		#search_form = SearchForm()
		#context = { "search_form":search_form }
		#return render(request, "creation_evenement.html", context)

	except Exception as e:
		# Utilisateur non connecté
		return redirect("../../authentification/connexion/")





def contact(request):
	""""""

	try  :
		# Utilisateur connecté
		request.session["user_id"]
		context = {}
		return render(request, "contact.html", context)
	except Exception as e:
		# Utilisateur non connecté
		return redirect("../../authentification/connexion/")




def message(request):
	""""""

	try  :
		# Utilisateur connecté
		del request.session["user_id"]
		return redirect("../../")
	except Exception as e:
		# Utilisateur non connecté
		return redirect("../../authentification/connexion/")
    




    



def deconnexion(request):
	""""""

	try  :
		# Utilisateur connecté
		del request.session["user_id"]
		return redirect("../../")
	except Exception as e:
		# Utilisateur non connecté
		return redirect("../../authentification/connexion/")
    