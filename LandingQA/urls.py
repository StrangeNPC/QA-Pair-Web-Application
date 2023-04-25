from django.urls import path 
from . import views 
from LandingQA.views import qa

urlpatterns = [ 
    path('', views.index, name='index'),
    path('qa', views.qa, name='qa'),
]