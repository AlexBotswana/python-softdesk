from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, viewsets, status # Ctrl + Shift + P -> Type and select 'Python: Select Interpreter' and enter into your projects virtual environment
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Project, Contributor, Issue, Comment
from .serializers import UsersSerializer, ProjectsSerializer, ContributorsSerializer, IssuesSerializer, CommentsSerializer
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

# User = get_user_model()

class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        password = validated_data.get('password')
        hashed_password = make_password(password)
        serializer.save(password=hashed_password)
        user = serializer.instance
        Token.objects.get_or_create(user=user)

'''
class SignInView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(SignInView, self).post(request, *args, **kwargs)
        token = response.data.get('token', None)

        if token:
            user = User.objects.get(pk=response.data.get('user_id'))
            serializer = UsersSerializer(user)
            return Response({'token': token, 'user': serializer.data})
        
        return response
'''

class ProjectsCreate(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'id'

class ProjectDetail(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectsSerializer
    lookup_field = 'id'

class IssueDetail(generics.RetrieveAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssuesSerializer
    lookup_field  = 'id'

class CommentDetail(generics.RetrieveAPIView):
    queryset  = Comment.objects.all()
    serializer_class = CommentsSerializer
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
        author_id = self.kwargs.get("author_user_id")
        projects = Comment.objects.filter(author_user_id=author_id)
        return projects

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CommentsSerializer(queryset, many=True)
        return Response({"Comments": serializer.data})

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # delete token 
            refresh_token = request.data.get("refresh_token")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "No refresh token provided."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)