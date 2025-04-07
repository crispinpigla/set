

from django.urls import re_path

from . import views # import views so we can use them in urls.

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    #re_path('home/', views.index),
    re_path(r"^manage_contact/(?P<contact_id>\w+)/$", views.manage_contact),
    re_path('contacts/', views.contacts),
    re_path('messages/', views.message),
    re_path(r"^messages_exchanges/(?P<user_id>\w+)/$", views.messages_exchanges),
    re_path(r"^send_message/(?P<user_id>\w+)/$", views.send_message),
    re_path(r"^updates_messages_user/(?P<user_id>\w+)/$", views.updates_messages),
    re_path(r"^profil/(?P<user_id>\w+)/$", views.profil),
    re_path('update_image_cover/', views.update_image_cover),
    re_path('update_profil_name/', views.update_profil_name),
    re_path('update_profil_mail/', views.update_profil_mail),
    re_path('suppression_compte/', views.suppression_compte),
    re_path('deconnexion/', views.deconnexion),


    re_path('home/', views.home),
    #re_path('', views.redirect_home),
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
