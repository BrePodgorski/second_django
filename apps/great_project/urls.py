from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout_view$', views.logout_view),
    url(r'^quotes$', views.quotes),
    url(r'^process_quotes$', views.process_quotes),
    url(r'^add_to_fav/(?P<my_quote_id>\d+)$', views.add_to_fav),
    url(r'^remove_from_fav/(?P<my_quote_id>\d+)$', views.remove_from_fav),
    url(r'^user/(?P<a_user_id>\d+)$', views.user),


    ]
