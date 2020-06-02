from django.urls import path, include
from talentsWeb.views import user, talent
user_patterns = [
    path('login', user.login),
    path('register', user.register),
    path('myInfo', user.myInfo),
    path('logout', user.logout),
    path('update', user.update)
]


talent_patterns = [
    path('fetch/<category>', talent.fetch_by_cate),
    path('fetch/', talent.fetch_by_cate),
    path('search/<category>', talent.search),
    path('search/', talent.search),
    path('group/orgn', talent.group_by_orgn),
    path('group/doma', talent.group_by_doma),
    path('top10/sort_by/<sort_field>', talent.top10),
    path('download_with_article', talent.download_with_article)
]

api_patterns = [
    path('user/', include(user_patterns)),
    path('talent/', include(talent_patterns))

]

urlpatterns = [
    path('api/', include(api_patterns))
]
