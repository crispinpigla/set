from django.db import models

# Create your models here.

from sorl.thumbnail import get_thumbnail
from django.utils.html import format_html


from user.models import Utilisateurs


class Sets(models.Model):
	""""""
	nom = models.CharField(max_length=200)
	image_couverture = models.FileField(upload_to="")
	type0 = models.CharField(max_length=200)
	description = models.CharField(max_length=200)
	date = models.DateTimeField(auto_now=True, null=True)
	statut_fermeture_admin = models.BooleanField(default=False)




class Evenements(models.Model):
	""""""
	set0 = models.ForeignKey(Sets, on_delete=models.CASCADE)
	administrateur = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE, null=True)
	nom = models.CharField(max_length=200)
	description = models.CharField(max_length=200)
	date = models.DateTimeField(auto_now=True, null=True)
	statut_fermeture_admin = models.BooleanField(default=False)





class SetUtilisateurs(models.Model):
	""""""
	set0 = models.ForeignKey(Sets, on_delete=models.CASCADE)
	utilisateur = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE)
	statut = models.CharField(max_length=200)
	date = models.DateTimeField(auto_now=True, null=True)




class PublicationSet(models.Model):
	""""""
	set0 = models.ForeignKey(Sets, on_delete=models.CASCADE)
	auteur = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE)
	contenu_text = models.CharField(max_length=200)
	media1 = models.FileField(upload_to='')
	media2 = models.FileField(upload_to='')
	date = models.DateTimeField(auto_now=True, null=True)
	control_admin = models.BooleanField(default=False)
	masquage_admin = models.BooleanField(default=False)

	@property
	def view_media1(self):
		if self.media1:
			_thumbnail = get_thumbnail(self.media1, '300x300', upscale=False, crop=False, quality=100)
			return format_html('<img src="../../sets{}" width="{}" height="{}">'.format( _thumbnail.url, _thumbnail.width, _thumbnail.height))
		return ""

	@property
	def view_media2(self):
		if self.media2:
			_thumbnail = get_thumbnail(self.media2, '300x300', upscale=False, crop=False, quality=100)
			return format_html('<img src="../../sets{}" width="{}" height="{}">'.format( _thumbnail.url, _thumbnail.width, _thumbnail.height))
		return ""

	@property
	def view_detail_media1(self):
		if self.media1:
			_thumbnail = get_thumbnail(self.media1, '300x300', upscale=False, crop=False, quality=100)
			return format_html('<img src="../../../../../sets{}" width="{}" height="{}">'.format( _thumbnail.url, _thumbnail.width, _thumbnail.height))
		return ""

	@property
	def view_detail_media2(self):
		if self.media2:
			_thumbnail = get_thumbnail(self.media2, '300x300', upscale=False, crop=False, quality=100)
			return format_html('<img src="../../../../../sets{}" width="{}" height="{}">'.format( _thumbnail.url, _thumbnail.width, _thumbnail.height))


class JaimePublicationSet(models.Model):
	""""""
	publication_set = models.ForeignKey(PublicationSet, on_delete=models.CASCADE)
	jaimeur = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE, null=True)
	date = models.DateTimeField(auto_now=True, null=True)
		


class PublicationEvenement(models.Model):
	""""""
	evenement = models.ForeignKey(Evenements, on_delete=models.CASCADE)
	auteur = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE)
	contenu_text = models.CharField(max_length=200)
	media1 = models.FileField(upload_to='')
	media2 = models.FileField(upload_to='')
	date = models.DateTimeField(auto_now=True, null=True)
	control_admin = models.BooleanField(default=False)
	masquage_admin = models.BooleanField(default=False)

	@property
	def view_media1(self):
		if self.media1:
			_thumbnail = get_thumbnail(self.media1, '300x300', upscale=False, crop=False, quality=100)
			return format_html('<img src="../../sets{}" width="{}" height="{}">'.format( _thumbnail.url, _thumbnail.width, _thumbnail.height))
		return ""

	@property
	def view_media2(self):
		if self.media2:
			_thumbnail = get_thumbnail(self.media2, '300x300', upscale=False, crop=False, quality=100)
			return format_html('<img src="../../sets{}" width="{}" height="{}">'.format( _thumbnail.url, _thumbnail.width, _thumbnail.height))
		return ""

	@property
	def view_detail_media1(self):
		if self.media1:
			_thumbnail = get_thumbnail(self.media1, '300x300', upscale=False, crop=False, quality=100)
			return format_html('<img src="../../../../../sets{}" width="{}" height="{}">'.format( _thumbnail.url, _thumbnail.width, _thumbnail.height))
		return ""

	@property
	def view_detail_media2(self):
		if self.media2:
			_thumbnail = get_thumbnail(self.media2, '300x300', upscale=False, crop=False, quality=100)
			return format_html('<img src="../../../../../sets{}" width="{}" height="{}">'.format( _thumbnail.url, _thumbnail.width, _thumbnail.height))



class JaimePublicationEvenement(models.Model):
	""""""
	publication_evenement = models.ForeignKey(PublicationEvenement, on_delete=models.CASCADE)
	jaimeur = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE, null=True)
	date = models.DateTimeField(auto_now=True, null=True)
