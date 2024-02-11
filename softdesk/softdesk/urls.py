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
                            LogoutView,
                            ProjectsCreate,
                            ContributorsCreate,
                            IssuesCreate,
                            CommentsCreate,
                            ProjectsUpdate,
                            IssuesUpdate,
                            ProjectsDelete,
                            ContributorsDelete,
                            IssuesDelete,
                            CommentsDelete,
                            UserDetail, 
                            ProjectDetail, 
                            IssueDetail, 
                            CommentDetail, 
                            ProjectsViewSet,  
                            ContributorsViewSet, 
                            IssuesViewSet, 
                            CommentsViewSet,
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
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # Create Projects, Contributors, Issues, Comments
    path('projects/create/', ProjectsCreate.as_view(), name='ProjectCreate'),
    path('contributors/create/', ContributorsCreate.as_view(), name='ContributorCreate'),
    path('issues/create/', IssuesCreate.as_view(), name='IssueCreate'),
    path('comments/create/', CommentsCreate.as_view(), name='CommentCreate'),
    # Update Projects, Contributors, Issues, Comments
    path('projects/update/<int:id>/', ProjectsUpdate.as_view(), name='ProjectUpdate'),
    path('issues/update/<int:id>/', IssuesUpdate.as_view(), name='IssueUpdate'),
    # Delete Projects, Contributors, Issues, Comments
    path('projects/delete/<int:pk>/', ProjectsDelete.as_view(), name='ProjectDelete'),
    path('contributors/delete/<int:pk>/', ContributorsDelete.as_view(), name='ContributorDelete'),
    path('issues/delete/<int:pk>/', IssuesDelete.as_view(), name='IssueDelete'),
    path('comments/delete/<int:pk>/', CommentsDelete.as_view(), name='CommentDelete'),
    # View details of Projects, Contributors, Issues, Comments
    path('users/<int:id>/', UserDetail.as_view(), name='UserDetail'),
    path('projects/<int:id>/', ProjectDetail.as_view(), name='ProjectDetail'),
    path('issues/<int:id>/', IssueDetail.as_view(), name='IssueDetail'),
    path('comment/<int:id>/', CommentDetail.as_view(), name='CommentDetail'),
    # View list of Projects, Contributors, Issues, Comments
    path('users/<int:author_id>/', include(router_project.urls)),
    path('contributors/<int:project_id>/', include(router_contrib.urls)),
    path('users/<int:assigned_user_id>/', include(router_issue.urls)),
    path('users/<int:author_user_id>/', include(router_comment.urls)),
]
