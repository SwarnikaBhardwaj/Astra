from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # JSON endpoints for data
    path('hubs/', views.hubs_json, name='hubs_json'),
    path('posts/<slug:hub_slug>/', views.posts_json, name='posts_json'),
    path('stats/platform/', views.platform_stats, name='platform_stats'),
    path('stats/growth/', views.growth_stats, name='growth_stats'),
    path('stats/skills/', views.skills_distribution, name='skills_distribution'),
]