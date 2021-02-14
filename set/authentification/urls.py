

from django.conf.urls import url

from . import views # import views so we can use them in urls.


urlpatterns = [

    url('inscription/', views.inscription), # "/store" will call the method "index" in "views.py"
    url('initialisation_mot_de_passe/', views.initialisation_mot_de_passe), # "/store" will call the method "index" in "views.py"
    url('connexion/', views.connexion), # "/store" will call the method "index" in "views.py"
    url('envoie_lien_reinitialisation_password/', views.envoie_lien_reinitialisation_password), # "/store" will call the method "index" in "views.py"
    url('reinitialisation_password/', views.reinitialisation_mot_de_passe), # "/store" will call the method "index" in "views.py"
    url('', views.index), # "/store" will call the method "index" in "views.py"

]