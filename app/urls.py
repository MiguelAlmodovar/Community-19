from django.urls import path, re_path
from app import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name ='login_view'),
    path('register/', views.register, name = 'register'),
    path('logout/',views.logoutUser, name ='logout'),
    path('account/', views.accountSettings, name="account"),
    path('posts/', views.posts, name = "posts" ),
    path('upvote/<str:pk>/', views.upvote, name = "upvote"),
    path('downvote/<str:pk>/', views.downvote, name = "downvote"),
    path('createa/',views.createa, name = 'createa'),
    path('announcements/', views.announcements, name = "announcements"),
    path('announcement/<str:pk>/',views.announcement, name = 'announcement'),
    path('post/<str:pk>/', views.post, name = 'post'),
    path('adminpanel/', views.adminpanel, name = 'adminpanel'),
    path('delete/<str:pk>/', views.deletepost, name = 'deletepost'),
    path('deleteown/<str:pk>/', views.deleteownpost, name = 'deleteownpost'),
    path('review/<str:pk>/', views.reviewpost, name = 'reviewpost'),
    path('report/<str:pk>/', views.report, name = 'report'),
    path('deletea/<str:pk>/', views.deletea, name = 'deletea'),
    path('deleteowna/<str:pk>/', views.deleteowna, name = 'deleteowna'),
    path('reviewa/<str:pk>/', views.reviewa, name = 'reviewa'),
    path('deleteuser/<str:pk>/', views.deleteuser, name = 'deleteuser'),
    path('users/', views.users, name = 'users'),
    path('reset-password/',auth_views.PasswordResetView.as_view(template_name = "app/password_reset.html"),name = 'reset_password'),
    path('reset-password-sent/',auth_views.PasswordResetDoneView.as_view(template_name = "app/password_reset_sent.html"), name = 'password_reset_done'),
    path('reset-password/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = "app/password_reset_form.html"), name = 'password_reset_confirm'),
    path('reset-password-complete/',auth_views.PasswordResetCompleteView.as_view(template_name = "app/password_reset_done.html"), name = 'password_reset_complete'),
]