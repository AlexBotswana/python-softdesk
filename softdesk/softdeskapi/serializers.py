from rest_framework import serializers
from .models import User, Project, Contributor, Issue, Comment

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',
                  'first_name',
                  'last_name',
                  'email',
                  'can_be_contacted',
                  'can_data_be_shared',
        )

class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id',
                  'title',
                  'description',
                  'type',
                  'author_id',
        )

class ContributorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ('id',
                  'is_owner',
                  'project_id',
                  'user_id',
        )

class IssuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ('id',
                  'title',
                  'description',
                  'status',
                  'priority',
                  'tag',
                  'assigned_user_id',
                  'author_user_id',
                  'project_id',
        )

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id',
                  'description',
                  'author_id',
                  'issue_id',
        )