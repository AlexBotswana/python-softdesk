from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, Project, Contributor, Issue, Comment

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id',
                  'first_name',
                  'last_name',
                  'email',
                  'username',
                  'password',
                  'birthdate',
                  'can_be_contacted',
                  'can_data_be_shared',
        )

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

class UsersUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id',
                  'first_name',
                  'last_name',
                  'email',
                  'birthdate',
                  'can_be_contacted',
                  'can_data_be_shared',
        )

    def update(self, validated_data, id_user):
        user = User.objects.filter(id=id_user)
        user.update(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
            birthdate = validated_data['birthdate'],
            can_be_contacted = validated_data['can_be_contacted'],
            can_data_be_shared = validated_data['can_data_be_shared'],
        )
        return user

class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id',
                  'title',
                  'description',
                  'type',
                  'author_id',
        )
    def create(self, validated_data):
        author = self.context['request'].user
        project = Project.objects.create(author=author, **validated_data)
        return project
    
    def update(self, validated_data, id_project):
        project = Project.objects.filter(id=id_project)
        project.update(
            title = validated_data['title'],
            description = validated_data['description'],
            type = validated_data['type'],
        )
        return project

class ContributorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ('id',
                  'user',
                  'project',
                  'is_owner',
        )
    def create(self, validated_data):
        contributor = Contributor.objects.create(**validated_data)
        return contributor

class IssuesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ('id',
                  'title',
                  'description',
                  'assigned_user_id',
                  'project_id',
        )

    def create(self, validated_data):
        issue = Issue.objects.create(**validated_data)
        return issue

class IssuesSerializer(serializers.ModelSerializer):
    status = serializers.CharField(required=False)
    priority = serializers.CharField(required=False)
    tag = serializers.CharField(required=False)

    class Meta:
        model = Issue
        fields = ('id',
                  'title',
                  'description',
                  'status',
                  'priority',
                  'tag',
                  'assigned_user_id',
                  'project_id',
        )

    def update(self, validated_data, id_issue):
        issue = Issue.objects.filter(id=id_issue)
        issue.update(
            title = validated_data.get('title'),
            description = validated_data['description'],
            status = validated_data.get('status'),
            priority = validated_data.get('priority'),
            tag = validated_data.get('tag'),
            assigned_user_id = validated_data['assigned_user_id'],
        )
        return issue

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id',
                  'description',
                  'issue_id',
        )

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment

