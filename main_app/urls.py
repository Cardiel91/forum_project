
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),

    path('register', views.register),

    path('login', views.login),

    path('bright_ideas', views.idea),

    path('logout', views.logout),

    path('message', views.message_post),
    
    path('delete/<int:user_id>', views.delete_message),

    path('comment_post/<int:wall_message_id>', views.comment_post),

    path('users/<int:user_id>', views.user_page),

    path('liked_ideas/<int:user_id>', views.liked_ideas),

    



]