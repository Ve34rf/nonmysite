"""nonmysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from test_rest.views import admin as html
from test_rest.views import script as script
from test_rest.views import testo as testo
from test_rest.views import index as index
from test_rest.views import register_request as register
from test_rest.views import contact as contact
from test_rest.views import login_request as login
from test_rest.views import about as about
from test_rest.views import create as comm
from test_rest.views import comment as comi
from test_rest.views import likeView
from test_rest.views import HomeView, PostHomeView, AddPostView, UpdatePostView, DeletePostView 
from test_rest.views import UserEditView, PasswordChangeView
from test_rest.views import password_success as password_success
from test_rest.views import ShowProfilePageView
from test_rest.views import EditProfilePageView
from test_rest.views import CreateProfilePageView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('html/', html),
    path('index/', index),
    path('html/script.js/', script),
    path('', about, name="home"),
    path('testo/', testo),
    path('register/', register, name="reg"),
    path('login/', login, name="log"),
    path('conts/', contact, name="conts"),
    path('comments/', comm, name="com"),
    path('comms/', comi, name="comi"),
    path('about/', include('django.contrib.auth.urls')),
    path('posts/', HomeView.as_view(), name="posts"),
    path('posts/<int:pk>', PostHomeView.as_view(), name="post-detail"),
    path('add_post/', AddPostView.as_view(), name="add_post"),
    path('posts/edit/<int:pk>', UpdatePostView.as_view(), name="update_post"),
    path('posts/<int:pk>/remove', DeletePostView.as_view(), name="delete_post"),
    path('edit_profile/', UserEditView.as_view(), name="edit_profile"),
    path('password/',PasswordChangeView.as_view(template_name='change_password.html')),
    path('password_success/', password_success, name="password_success"),
    path('like/<int:pk>', likeView, name="like_post"),
    path('<int:pk>/profile/', ShowProfilePageView.as_view(), name="show_profile_page"),
    path('<int:pk>/edit_profile_page/', EditProfilePageView.as_view(), name="edit_profile_page"),
    path('create_profile_page/', CreateProfilePageView.as_view(), name="create_profile_page"),


]

if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)