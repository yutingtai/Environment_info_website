from django.urls import path
from . import views

app_name = "display_info"
urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('refresh', views.refresh, name="refresh"),
    path('delete_all', views.delete_all, name="delete_all")
]
