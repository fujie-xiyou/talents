from django.urls import path, include
from talentsWeb.views import user
user_patterns = [
    path('login', user.login),
    path('register', user.register),
    path('myInfo', user.myInfo)
]

api_patterns = [
    path('user/', include(user_patterns)),

]

urlpatterns = [
    path('api/', include(api_patterns))
]
