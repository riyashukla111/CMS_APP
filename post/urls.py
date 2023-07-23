from django.urls import path
from . import views

urlpatterns = [
    path('create_post/', views.create_post , name='post'),
    path('get_post/<int:id>', views.get_posts , name='post'),
    path('get_post/', views.get_posts , name='get_post'),
    path('update_post/<int:id>', views.update_post , name='update_post'),
    path('delete_post/<int:id>', views.delete_post , name='delete_post'),
    path('get_like/<int:post_id>', views.get_likes , name='get_like'),
    path('create_like/<int:post_id>', views.give_like , name='create_like'),
    path('delete_like/<int:post_id>', views.delete_like , name='delete_like'),


]