from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets # Ctrl + Shift + P -> Type and select 'Python: Select Interpreter' and enter into your projects virtual environment
from rest_framework.response import Response
from .models import User, Project, Contributor, Issue, Comment
from .serializers import UsersSerializer, ProjectsSerializer, ContributorsSerializer, IssuesSerializer, CommentsSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'id'

class ProjectDetail(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectsSerializer
    lookup_field = 'id'

class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectsSerializer

    def get_object(self):
       obj = get_object_or_404(Project.objects.all(), author_id=self.kwargs["pk"])
       self.check_object_permissions(self.request, obj)
       return obj

    def get_queryset(self):
        # Utilisez le paramètre 'author' pour filtrer les projets par utilisateur
        author_id = self.kwargs.get("author_id")
        projects = Project.objects.filter(author__id=author_id)
        return projects

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProjectsSerializer(queryset, many=True)
        return Response({"projects": serializer.data})
    
    def retrieve(self, request, *args, **kwargs):
        project = self.get_object()
        serializer = ProjectsSerializer(project)
        return Response(serializer.data)

class ContributorsViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorsSerializer

    def get_object(self):
       obj = get_object_or_404(Contributor.objects.all(), project_id=self.kwargs["pk"])
       self.check_object_permissions(self.request, obj)
       return obj

    def get_queryset(self):
        # Utilisez le paramètre 'project' pour filtrer les projets par utilisateur
        project_id = self.kwargs.get("project_id")
        projects = Contributor.objects.filter(project__id=project_id)
        return projects

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ContributorsSerializer(queryset, many=True)
        return Response({"Contributors": serializer.data})

class IssuesViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssuesSerializer

    def get_object(self):
        obj = get_object_or_404(Issue.objects.all(), assigned_user_id=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        # Utilisez le paramètre 'assigned_user_id' pour filtrer les projets par utilisateur
        assigned_user = self.kwargs.get("assigned_user_id")
        issues = Issue.objects.filter(assigned_user_id=assigned_user)
        return issues

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = IssuesSerializer(queryset, many=True)
        return Response({"Issues": serializer.data})

class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer

    def get_object(self):
        obj = get_object_or_404(Comment.objects.all(), project_id=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        # Utilisez le paramètre 'author' pour filtrer les projets par utilisateur
        project_id = self.kwargs.get("project")
        projects = Comment.objects.filter(project=project_id)
        return projects

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CommentsSerializer(queryset, many=True)
        return Response({"Comments": serializer.data})

