from django.urls import path, include
from talentsWeb.views import user, talent
user_patterns = [
    path('login', user.login),
    path('register', user.register),
    path('myInfo', user.myInfo),
    path('logout', user.logout)
]


talent_patterns = [
    path('fetch/<category>', talent.fetch_by_cate),
    path('fetch/', talent.fetch_by_cate),
    path('search/<category>', talent.search),
    path('search/', talent.search),
]

api_patterns = [
    path('user/', include(user_patterns)),
    path('talent/', include(talent_patterns))

]

urlpatterns = [
    path('api/', include(api_patterns))
]
