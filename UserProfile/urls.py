from django.urls import path

from . import views
app_name='UserProfile'

urlpatterns=[

    path('signin/',views.signin,name='signin'),
    path('',views.profile, name='profile'),
    path('<str:username>',views.friendprofile,name='friendprofile'),
    path('chat/<str:username>',views.chats,name='chats'),
    path('addfriend/',views.addfriend, name='addfriend'),
    path('',views.home, name='home'),
    path('photos/<str:username>',views.Photos,name='Photos'),
    path('notification/',views.note, name='note'),
    #path('comment/',views.comment, name='comment'),
    #path('signin/',views.logout,name='logout'),



]