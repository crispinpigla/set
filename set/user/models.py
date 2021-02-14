from django.db import models

# Create your models here.








class Utilisateurs(models.Model):
	""""""

	nom = models.CharField(max_length=200, null=True)
	adresse_mail = models.CharField(max_length=200, null=True)
	mot_de_passe = models.CharField(max_length=200, null=True)
	image_profil = models.FileField(upload_to='', null=True)
	code_de_reinitialisation_de_mot_de_passe = models.CharField(max_length=200, null=True)


class Contact(models.Model):
	""""""
	contact_owner = models.ForeignKey(Utilisateurs, related_name="a", on_delete=models.CASCADE)
	contact = models.ForeignKey(Utilisateurs, related_name="b",  on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now=True, null=True)


class Message(models.Model):
	""""""
	which_from = models.ForeignKey(Utilisateurs, related_name="e",  on_delete=models.CASCADE)
	which_to = models.ForeignKey(Utilisateurs, related_name="f",  on_delete=models.CASCADE)
	contenu_text = models.CharField(max_length=200)
	date = models.DateTimeField(auto_now=True, null=True)


