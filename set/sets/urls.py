

from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static

from . import views # import views so we can use them in urls.


urlpatterns = [
    #url('set/', views.sets), # "/store" will call the method "index" in "views.py"
    url("search/", views.search), # "/store" will call the method "index" in "views.py"
    url(r"^set/(?P<set_id>[0-9]+)/$", views.sets),
    url(r"^event/(?P<event_id>[0-9]+)/$", views.evenements), # "/store" will call the method "index" in "views.py"
    url("update_cover/", views.update_cover), # "/store" will call the method "index" in "views.py"
    url(r"^make_post_set/(?P<set_id>[0-9]+)/$", views.make_post_set), # "/store" will call the method "index" in "views.py"
    url(r"^make_post_event/(?P<event_id>[0-9]+)/$", views.make_post_event), # "/store" will call the method "index" in "views.py"
    url(r"^manage_like_post_set/(?P<post_id>[0-9]+)/$", views.manage_like_post_set), # "/store" will call the method "index" in "views.py"
    url(r"^manage_like_post_event/(?P<post_id>[0-9]+)/$", views.manage_like_post_event), # "/store" will call the method "index" in "views.py"
    #url('', views.home), # "/store" will call the method "index" in "views.py"
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

