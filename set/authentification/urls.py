

from django.urls import re_path

from . import views # import views so we can use them in urls.


urlpatterns = [

    re_path('inscription/', views.inscription),
    re_path('initialisation_mot_de_passe/', views.initialisation_mot_de_passe),
    re_path('connexion/', views.connexion),
    re_path('google_connect/', views.google_connect),
    re_path('envoie_lien_reinitialisation_password/', views.envoie_lien_reinitialisation_password),
    re_path('reinitialisation_password/', views.reinitialisation_mot_de_passe),
    re_path('envoie_activation_compte/', views.envoie_activation_compte),
    re_path('activation_compte/', views.activation_compte),
    re_path('', views.index),

]
