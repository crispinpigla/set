""""""
from django.shortcuts import get_object_or_404

from ..models import Utilisateurs, Message


class AuxilliariesUser():

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
