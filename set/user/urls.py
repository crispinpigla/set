

from django.conf.urls import url

from . import views # import views so we can use them in urls.

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

	#url('home/', views.index), # "/store" will call the method "index" in "views.py"
	url(r"^manage_contact/(?P<contact_id>[0-9]+)/$", views.manage_contact), # "/store" will call the method "index" in "views.py"
	url('contacts/', views.contacts), # "/store" will call the method "index" in "views.py"
	url('messages/', views.message), # "/store" will call the method "index" in "views.py"
	url(r"^messages_exchanges/(?P<user_id>[0-9]+)/$", views.messages_exchanges), # "/store" will call the method "index" in "views.py"
	url(r"^send_message/(?P<user_id>[0-9]+)/$", views.send_message), # "/store" will call the method "index" in "views.py"
	url(r"^updates_messages_user/(?P<user_id>[0-9]+)/$", views.updates_messages), # "/store" will call the method "index" in "views.py"
	url(r"^profil/(?P<user_id>[0-9]+)/$", views.profil), # "/store" will call the method "index" in "views.py"
	url('update_image_cover/', views.update_image_cover), # "/store" will call the method "index" in "views.py"
	url('update_profil_name/', views.update_profil_name), # "/store" will call the method "index" in "views.py"
	url('update_profil_mail/', views.update_profil_mail), # "/store" will call the method "index" in "views.py"
	url('suppression_compte/', views.suppression_compte), # "/store" will call the method "index" in "views.py"
	url('deconnexion/', views.deconnexion), # "/store" will call the method "index" in "views.py"
	

    url('home/', views.home), # "/store" will call the method "index" in "views.py"
    #url('', views.redirect_home), # "/store" will call the method "index" in "views.py"
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)