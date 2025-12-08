from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    # Authentication
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Hubs
    path('hubs/', views.hub_list, name='hub_list'),
    path('hub/<slug:slug>/', views.hub_detail, name='hub_detail'),
    path('hub/<slug:slug>/join/', views.join_hub, name='join_hub'),

    # Posts
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/vote/', views.vote_helpful, name='vote_helpful'),

    # Comments
    path('post/<int:post_pk>/comment/', views.add_comment, name='add_comment'),

    # Profiles
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    path('profile/<str:username>/edit/', views.profile_edit, name='profile_edit'),

    # Mentorship
    path('mentors/', views.mentor_list, name='mentor_list'),
    path('mentorship/request/<str:username>/', views.request_mentorship, name='request_mentorship'),
    path('mentorship/dashboard/', views.mentorship_dashboard, name='mentorship_dashboard'),
    path('mentorship/<int:pk>/update/', views.update_mentorship_status, name='update_mentorship_status'),
# Analytics
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('profile/<str:username>/export/', views.export_portfolio, name='export_portfolio'),
]