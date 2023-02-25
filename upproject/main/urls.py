from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('change/', views.ChangeView.as_view(), name='change'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', views.PasswordsChangeView.as_view() , name='password_change'),
    path('profile/', views.ProfileView.as_view(), name = 'profile'),
    path('posts/', views.PostList.as_view(), name='post_list'),
    path('posts/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('create/', views.PostCreationView.as_view(), name='post_creation'),
    path('myposts/', views.MyPostList.as_view(), name='my_post_list'),
    path('myposts/edit/<slug:slug>', views.PostEditView.as_view(), name='my_post_edit'),
]   

