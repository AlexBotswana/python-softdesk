"""
URL configuration for softdesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth.models import User
from softdeskapi.views import UserDetail, ProjectsViewSet, ProjectDetail, ContributorsViewSet, IssuesViewSet, CommentsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'projects', ProjectsViewSet, basename='projects')

router_contrib = DefaultRouter()
router_contrib.register(r'projects', ContributorsViewSet, basename='contributors')

router_issue = DefaultRouter()
router_issue.register(r'issues', IssuesViewSet, basename='issues')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('users/<int:id>/', UserDetail.as_view(), name='UserDetail'),
    path('projects/<int:id>/', ProjectDetail.as_view(), name='ProjectDetail'),
    path('projects/users/<int:author_id>/', include(router.urls)),
    path('projects/contributors/<int:project_id>/', include(router_contrib.urls)),
    path('projects/issues/users/<int:assigned_user_id>/', include(router_issue.urls)),
]
