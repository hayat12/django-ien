from django.conf import settings
from django.conf.urls import static
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('users/register/', views.CreateUserView.as_view(), name="register"),
    path('account/user', views.UpdateUser.as_view(), name="register"),
    path('account/upload-profile/<int:id>', views.uploadUserProfile, name="upload-profile"),
    path('account/user/<int:id>', views.CurrentUser.as_view()),
    path('user-details', views.UserDetail.as_view()),
    path('event', views.Events.as_view()),
    path('events', views.EventList.as_view()),
    path('event/<int:id>', views.Events.as_view()),
    path('search', views.SearchList.as_view()), 
    path('test-img', views.ImageBase64.as_view()),
    path('get-ticket/<int:id>', views.getTicket.as_view()),
    path('adgenda', views.CreateAdgena.as_view()),
    path('adgenda/<int:id>', views.AdgendaAPI.as_view()),
    path('connections', views.Connections.as_view())
]
