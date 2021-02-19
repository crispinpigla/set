from django.db import models

# Create your models here.

from user.models import Utilisateurs


class Sets(models.Model):
	""""""
	nom = models.CharField(max_length=200)
	image_couverture = models.FileField(upload_to="upload")
	type0 = models.CharField(max_length=200)
	description = models.CharField(max_length=200)
	date = models.DateTimeField(auto_now=True, null=True)




class Evenements(models.Model):
	""""""
	set0 = models.ForeignKey(Sets, on_delete=models.CASCADE)
	administrateur = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE, null=True)
	nom = models.CharField(max_length=200)
	description = models.CharField(max_length=200)
	date = models.DateTimeField(auto_now=True, null=True)





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


class JaimePublicationEvenement(models.Model):
	""""""
	publication_evenement = models.ForeignKey(PublicationEvenement, on_delete=models.CASCADE)
	jaimeur = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE, null=True)
	date = models.DateTimeField(auto_now=True, null=True)