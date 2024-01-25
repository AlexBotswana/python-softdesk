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
from softdeskapi.views import (
                            SignUpView, 
                            # SignInView, 
                            ProjectsCreate, 
                            UserDetail, 
                            ProjectDetail, 
                            IssueDetail, 
                            CommentDetail, 
                            ProjectsViewSet,  
                            ContributorsViewSet, 
                            IssuesViewSet, 
                            CommentsViewSet,
                            LogoutView,
                            )
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

router_project = DefaultRouter()
router_project.register(r'projects', ProjectsViewSet, basename='projects')

router_contrib = DefaultRouter()
router_contrib.register(r'projects', ContributorsViewSet, basename='contributors')

router_issue = DefaultRouter()
router_issue.register(r'issues', IssuesViewSet, basename='issues')

router_comment = DefaultRouter()
router_comment.register(r'comments', CommentsViewSet, basename='comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('signup/', SignUpView.as_view(), name='signup'),
    # path('signin/', SignInView.as_view(), name='signin'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('projects/create/', ProjectsCreate.as_view(), name='ProjectCreate'),
    path('users/<int:id>/', UserDetail.as_view(), name='UserDetail'),
    path('projects/<int:id>/', ProjectDetail.as_view(), name='ProjectDetail'),
    path('issues/<int:id>/', IssueDetail.as_view(), name='IssueDetail'),
    path('comment/<int:id>/', CommentDetail.as_view(), name='CommentDetail'),
    path('users/<int:author_id>/', include(router_project.urls)),
    path('contributors/<int:project_id>/', include(router_contrib.urls)),
    path('users/<int:assigned_user_id>/', include(router_issue.urls)),
    path('users/<int:author_user_id>/', include(router_comment.urls)),
]
