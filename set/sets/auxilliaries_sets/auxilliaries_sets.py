""""""
from django.shortcuts import render, get_object_or_404


from ..models import Sets, SetUtilisateurs, PublicationSet, JaimePublicationSet, Evenements, PublicationEvenement

from user.models import Contact



class AuxilliariesSets():
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

	def render_set_user_set(self,request, section_set, set_id, context, statut_user_in_set):
		""""""
		if section_set == 'publications' :
			# Récupération des publications
			publications = PublicationSet.objects.filter(set0_id=set_id)
			publications_likeurs = []
			for publication in publications:
				publications_likeurs.append([publication, JaimePublicationSet.objects.filter(publication_set_id=publication.id), JaimePublicationSet.objects.filter(publication_set_id=publication.id, jaimeur_id=request.session["user_id"])])
			context['publications_likeurs'] = publications_likeurs
			if statut_user_in_set == 'attente_validation' :
				return render(request, "section_publications_users_wait_set.html", context)
			else:
				return render(request, "section_publications_set.html", context)

		elif section_set == 'evenements' :
			# Récupération des évènements
			events = Evenements.objects.filter(set0_id=set_id)
			context['events'] = events
			if statut_user_in_set == 'attente_validation' :
				return render(request, "section_evenements_set_out_set.html", context)
			else:
				return render(request, "section_evenements_set.html", context)
		elif section_set == 'personnes' :
        	# Récupération des utilisateurs
			users_set = SetUtilisateurs.objects.filter(set0_id=set_id)
			users_set_list = [ user_set.utilisateur for user_set in users_set ]
			users_set_dictionnary = { user_set.utilisateur:user_set for user_set in users_set }
			# Récupération des contacts
			contacts = Contact.objects.filter(contact_owner_id=request.session["user_id"])
			contacts_list = [ contact.contact for contact in contacts ]
			context['users_set'] = users_set
			context['users_set_list'] = users_set_list
			context['contacts'] = contacts
			context['contacts_list'] = contacts_list
			return render(request, "section_personnes_set.html", context)

	def render_set_user_no_set(self,request, section_set, set_id, context):
		""""""
		if section_set == 'publications' :
			# Demande des publications
			return render(request, "section_no_access_publications_set.html", context)
		elif section_set == 'evenements' :
			# Récupération des évènements
			events = Evenements.objects.filter(set0_id=set_id)
			context['events'] = events
			return render(request, "section_evenements_set_out_set.html", context)
		elif section_set == 'personnes' :
        	# Récupération des utilisateurs
			users_set = SetUtilisateurs.objects.filter(set0_id=set_id)
			users_set_list = [ user_set.utilisateur for user_set in users_set ]
			users_set_dictionnary = { user_set.utilisateur:user_set for user_set in users_set }
			# Récupération des contacts
			contacts = Contact.objects.filter(contact_owner_id=request.session["user_id"])
			contacts_list = [ contact.contact for contact in contacts ]
			context['users_set'] = users_set
			context['users_set_list'] = users_set_list
			context['contacts'] = contacts
			context['contacts_list'] = contacts_list
			return render(request, "section_personnes_set.html", context)

	def render_set_user_no_registred(self,request, section_set, set_id, context):
		""""""
		if section_set == 'publications' :
			# Demande des publications
			return render(request, "section_no_access_publications_set.html", context)
		elif section_set == 'evenements' :
			# Récupération des évènements
			events = Evenements.objects.filter(set0_id=set_id)
			context['events'] = events
			return render(request, "section_evenements_set_out_set.html", context)
		elif section_set == 'personnes' :
        	# Récupération des utilisateurs
			users_set = SetUtilisateurs.objects.filter(set0_id=set_id)
			users_set_list = [ user_set.utilisateur for user_set in users_set ]
			users_set_dictionnary = { user_set.utilisateur:user_set for user_set in users_set }
			context['users_set'] = users_set
			context['users_set_list'] = users_set_list
			context['contacts'] = []
			context['contacts_list'] = []
			return render(request, "section_personnes_set.html", context)

	def form_is_not_empty(self, request):
		""""""
		contenu_text = request.POST["publication_text"]
		media1 = request.FILES.get("file_1", "")
		media2 = request.FILES.get("file_2", "")
		if contenu_text == '' and media1 == '' and media2 == '' :
			# Le formulaire est vide
			out = False
		else:
			# Le formulaire n'est pas vide
			out = True
		return out
