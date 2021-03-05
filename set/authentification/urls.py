

from django.conf.urls import url

from . import views # import views so we can use them in urls.


urlpatterns = [

    url('inscription/', views.inscription),
    url('initialisation_mot_de_passe/', views.initialisation_mot_de_passe),
    url('connexion/', views.connexion),
    url('google_connect/', views.google_connect),
    url('envoie_lien_reinitialisation_password/', views.envoie_lien_reinitialisation_password),
    url('reinitialisation_password/', views.reinitialisation_mot_de_passe),
    url('envoie_activation_compte/', views.envoie_activation_compte),
    url('activation_compte/', views.activation_compte),
    url('', views.index),

]