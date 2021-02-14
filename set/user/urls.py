

from django.conf.urls import url

from . import views # import views so we can use them in urls.


urlpatterns = [
    
	#url('home/', views.index), # "/store" will call the method "index" in "views.py"
	url('creation_set/', views.creation_set), # "/store" will call the method "index" in "views.py"
	url(r"^creation_evenement/(?P<event_id>[0-9]+)/$", views.creation_evenement), # "/store" will call the method "index" in "views.py"
	url('contacts/', views.contact), # "/store" will call the method "index" in "views.py"
	url('messages/', views.message), # "/store" will call the method "index" in "views.py"
	url('deconnexion/', views.deconnexion), # "/store" will call the method "index" in "views.py"

    url('', views.home), # "/store" will call the method "index" in "views.py"
]