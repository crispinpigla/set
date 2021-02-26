

from django.conf.urls import url

from django.urls import path


from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    #url('set/', views.sets),
    url('creation_set/', views.creation_set),
    url(r"^creation_evenement/(?P<set_id>\w+)/$", views.creation_evenement),
    url("search/", views.search),
    url(r"^set/(?P<set_id>\w+)/$", views.sets),
    url(r"^event/(?P<event_id>\w+)/$", views.evenements),
    url("update_cover/", views.update_cover),
    url("update_description_set/", views.update_description_set), 
    url(r"^make_post_set/(?P<set_id>\w+)/$", views.make_post_set),
    url(r"^make_post_event/(?P<event_id>\w+)/$", views.make_post_event),
    url(r"^manage_like_post_set/(?P<post_id>\w+)/$", views.manage_like_post_set),
    url(r"^manage_like_post_event/(?P<post_id>\w+)/$", views.manage_like_post_event),
    url(r"^delete_add_user_set/(?P<set_id>\w+)/(?P<user_delete_add_id>\w+)/$", views.delete_add_user_set),
    url(r"^manage_enter_user_set/(?P<set_id>\w+)/$", views.manage_enter_user_set),
    url(r"^exit_set/(?P<set_id>\w+)/$", views.exit_set),
    
    path("", views.redirect_home),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

