from django.urls import path
from django.urls import include
from . import  views


urlpatterns = [
    path('<slug:skmerUserId>/viewqueries/', views.viewQueries, name='queryView'),
    path('<slug:skmerUserId>/viewqueries/delete/<slug:queryId>/', views.deleteQuery, name='queryDelete'),
    path('<slug:skmerUserId>/viewqueries/viewdistance/<slug:queryId>/', views.viewDistance, name='queryViewDistance')

]
