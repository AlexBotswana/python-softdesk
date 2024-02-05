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
        # extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
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
    
    def put(self, validated_data, pk):
        project = Project.objects.filter(id=pk)
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

class IssuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ('id',
                  'title',
                  'description',
                  #'status',
                  #'priority',
                  #'tag',
                  'assigned_user_id',
                  'project_id',
                  #'author_user_id',
        )
    def create(self, validated_data):
        issue = Issue.objects.create(**validated_data)
        return issue

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id',
                  'description',
                  #'author_user_id',
                  'issue_id',
        )
    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment
