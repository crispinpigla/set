


from django.urls import path, re_path


from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    #re_path('set/', views.sets),
    re_path('creation_set/', views.creation_set),
    re_path(r"^creation_evenement/(?P<set_id>\w+)/$", views.creation_evenement),
    re_path("search/", views.search),
    re_path(r"^set/(?P<set_id>\w+)/$", views.sets),
    re_path(r"^event/(?P<event_id>\w+)/$", views.evenements),
    re_path("update_cover/", views.update_cover),
    re_path("update_description_set/", views.update_description_set),
    re_path(r"^make_post_set/(?P<set_id>\w+)/$", views.make_post_set),
    re_path(r"^make_post_event/(?P<event_id>\w+)/$", views.make_post_event),
    re_path(r"^manage_like_post_set/(?P<post_id>\w+)/$", views.manage_like_post_set),
    re_path(r"^manage_like_post_event/(?P<post_id>\w+)/$", views.manage_like_post_event),
    re_path(r"^delete_add_user_set/(?P<set_id>\w+)/(?P<user_delete_add_id>\w+)/$", views.delete_add_user_set),
    re_path(r"^manage_enter_user_set/(?P<set_id>\w+)/$", views.manage_enter_user_set),
    re_path(r"^exit_set/(?P<set_id>\w+)/$", views.exit_set),

    re_path(r"^delete_set/(?P<set_id>\w+)/$", views.delete_set),
    re_path(r"^delete_event/(?P<event_id>\w+)/$", views.delete_event),

    
    path("", views.redirect_home),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

