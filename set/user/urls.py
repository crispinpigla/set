

from django.conf.urls import url

from . import views # import views so we can use them in urls.

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

	#url('home/', views.index),
	url(r"^manage_contact/(?P<contact_id>\w+)/$", views.manage_contact),
	url('contacts/', views.contacts),
	url('messages/', views.message),
	url(r"^messages_exchanges/(?P<user_id>\w+)/$", views.messages_exchanges),
	url(r"^send_message/(?P<user_id>\w+)/$", views.send_message),
	url(r"^updates_messages_user/(?P<user_id>\w+)/$", views.updates_messages),
	url(r"^profil/(?P<user_id>\w+)/$", views.profil),
	url('update_image_cover/', views.update_image_cover),
	url('update_profil_name/', views.update_profil_name),
	url('update_profil_mail/', views.update_profil_mail),
	url('suppression_compte/', views.suppression_compte),
	url('deconnexion/', views.deconnexion), 
	

    url('home/', views.home), 
    #url('', views.redirect_home), 
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)