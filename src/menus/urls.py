from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$',views.ItemCreateView.as_view(), name='create'),
    #url(r'^(?P<pk>\d+)/edit/$',views.ItemUpdateView.as_view(), name='edit'),
    url(r'^(?P<pk>\d+)/$',views.ItemUpdateView.as_view(), name='detail'),
    url(r'^$',views.ItemListView.as_view(), name='list'),
]
