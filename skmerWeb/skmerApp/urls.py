from django.urls import path
from django.urls import include
from . import  views


urlpatterns = [
    path('', views.home, name='skmerHome'),
    path('signup/', views.signup, name='skmerSignup'),
    path("logout", views.logout_request, name="logout"),
    path('skmerUser/<slug:skmerUserId>/resources/',views.resources,name='skmerResources'),
    path('skmerUser/<slug:skmerUserId>/about/', views.about, name='skmerAbout'),
]
