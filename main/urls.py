from django.urls import path
from . import views


urlpatterns = [
    path('DashBoard/',views.DashBoard,name='DashBoard'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('addQ/',views.AddQuestion,name='addQ'),
    path('editQ/<int:Pid>',views.EditQuestion,name='editQ'),
]
