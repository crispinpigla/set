"""   """








class AuxilliariesAuthentification():
	"""docstring for AuxilliariesAuthentification"""
	def __init__(self):
		""""""
		pass

	def send_activation_mail(self, user):
		""""""
		mail = request.GET['mail']
		user = get_object_or_404(Utilisateurs, adresse_mail=mail)

		if user.cle_dactivation_de_compte == request.GET['key_activation']  :
			pass
		html_message = render_to_string('activation_compte.html', {'context': 'values'})
		mail = send_mail('Subject here', '', 'crispinpigla@yahoo.fr', ['crispinpigla@yahoo.fr'], fail_silently=False, html_message=html_message)
		