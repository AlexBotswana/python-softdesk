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
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            )

        user.set_password(validated_data['password'])
        user.save()
        #user = serializer.instance
        #Token.objects.get_or_create(user=user)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # delete token 
            refresh_token = request.data["refresh_token"]
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "No refresh token provided."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

###################################################
# Create Projects, Contributors, Issues, Comments #
###################################################
        
class ProjectsCreate(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        project = Project.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            type=validated_data['type'],
            author_id=self.request.user.id
        )
        project.save()

class ContributorsCreate(generics.CreateAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user_id = self.request.data.get('user')
        project_id = self.request.data.get('project')
        is_owner = self.request.data.get('is_owner')

        # Contributor user et project doivent etre des instances de classe User et Project
        user_instance = User.objects.get(pk=user_id)
        project_instance = Project.objects.get(pk=project_id)

        serializer.save(user=user_instance, project=project_instance, is_owner=is_owner)

class IssuesCreate(generics.CreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssuesSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        title = self.request.data.get('title')
        description = self.request.data.get('description')
        assigned_user = self.request.data.get('assigned_user_id')
        project_id = self.request.data.get('project_id')
        author_user = self.request.user.id

        assigned_user_instance = User.objects.get(pk=assigned_user)
        author_user_instance = User.objects.get(pk=author_user)
        
        serializer.save(title=title,
                        description=description,
                        assigned_user_id=assigned_user_instance,
                        project_id=project_id,
                        author_user_id=author_user_instance,
                    )

class CommentsCreate(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        description = self.request.data.get('description')
        issue_id = self.request.data.get('issue_id')
        author_user = self.request.user.id

        issue_instance = Issue.objects.get(pk=issue_id)
        author_user_instance = User.objects.get(pk=author_user)
        
        serializer.save(description=description,
                        issue_id=issue_instance,
                        author_user_id=author_user_instance,
                    )

###################################################
# Update Projects, Issues, Comments #
###################################################

class ProjectUpdate(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectsSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    
    def perform_update(self, request, id_project):
        print('hello')
        """
        PUT Method for details project
        Return :
            - updated projects only by this author
        """
        """get_object_or_404(Project, id=id_project)
        author = Contributor.objects.filter(project=id_project, role="AUTHOR").first()
        print(author)
        print(self.request.user.id)
        if author.user.id == self.request.user.id:
            serializer = ProjectsSerializer(
                data=request.data)
            if serializer.is_valid():
                serializer.put(serializer.data, id_project)
                return Response(serializer.data)
            return Response("INPUT ERROR",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response("YOU ARE NOT THE AUTHOR OF THIS PROJECT !\
             Update Unauthorized",
                        status=status.HTTP_401_UNAUTHORIZED)"""
        
        """ project = get_object_or_404(Project, id=id_project)
        author = Project.objects.filter(project_id=project, role="author").first()
        print(author.user.id)
        print("hello")
        if author.user.id == self.request.user.id:
            serializer = ProjectsSerializer(project, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response("INPUT ERROR", status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response("YOU ARE NOT THE AUTHOR OF THIS PROJECT! Update Unauthorized", status=status.HTTP_401_UNAUTHORIZED)"""

"""class IssueUpdate(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = IssuesSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    
    def update_issue(self, request, id_issue):
        issue = get_object_or_404(Issue, id=id_issue)
        serializer = IssuesSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response("INPUT ERROR", status=status.HTTP_406_NOT_ACCEPTABLE)
"""      
############################################################
# View details of Projects, Contributors, Issues, Comments #
############################################################

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'id'

class ProjectDetail(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectsSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

class IssueDetail(generics.RetrieveAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssuesSerializer
    lookup_field  = 'id'

class CommentDetail(generics.RetrieveAPIView):
    queryset  = Comment.objects.all()
    serializer_class = CommentsSerializer
    lookup_field = 'id'

#########################################################
# View list of Projects, Contributors, Issues, Comments #
#########################################################

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
        # paramètre 'author' pour filtrer les projets par utilisateur
        author_id = self.kwargs.get("author_user_id")
        projects = Comment.objects.filter(author_user_id=author_id)
        return projects

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CommentsSerializer(queryset, many=True)
        return Response({"Comments": serializer.data})

###################################################
# Delete Projects, Contributors, Issues, Comments #
###################################################
    
