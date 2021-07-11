"""uiassignment URL Configuration

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
from django.contrib import admin
from django.urls import path
from user.views import users_view, user_view, search_user_view, token_view

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("users/", users_view),
    path("user/<str:acct>/", user_view),
    path("search/user/<str:fullname>/", search_user_view),
    path("token/<str:acct>/", token_view),
]

"""
GET user/<str:acct>
POST 
DELETE
PUT
"""
