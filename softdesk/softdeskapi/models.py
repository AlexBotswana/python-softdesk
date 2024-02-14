from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

from django.db import models

class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500, unique=True)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token

class Project(models.Model):
    PROJECT_TYPES = (
        ('BE', 'Back-end'),
        ('FE', 'Front-end'),
        ('IOS', 'IOS'),
        ('ANDROID', 'Android'),
    )

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=1024, blank=True)
    type = models.CharField(max_length=32, choices=PROJECT_TYPES)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name='project_created_by'
        )
    created_time = models.DateTimeField(auto_now_add=True)
    project_user = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='softdesk_contributors',
    )

    def __str__(self):
        return self.title
    
class User(AbstractUser):
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=False)
    birthdate = models.DateField(default='2001-01-01')
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    user_project = models.ManyToManyField(
        Project,
        related_name='softdesk_contributors',
        )
    groups = models.ManyToManyField(
        Group,
        related_name='softdesk_users',
        )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='softdesk_users_permissions',
        )

class Contributor(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        )
    is_owner = models.BooleanField()
    created_time = models.DateTimeField(auto_now_add=True)

class Issue(models.Model):
    PRIORITY_CHOICES = (
        ('FAIBLE', 'Faible'),
        ('MOYENNE', 'Moyenne'),
        ('ELEVEE', 'Elevee'),
    )
    STATUS_CHOICES = (
        ('A FAIRE','A faire'),
        ('EN COURS','En cours'),
        ('TERMINE','Termine'),
    )
    TAG_CHOICES = (
        ('BUG','Bug'),
        ('AMELIORATION','Amelioration'),
        ('TACHE','Tache'),
    )

    title = models.CharField('Titre', max_length=128)
    description = models.TextField(
        'Description',
        max_length=1024,
        blank=True,
        )
    status = models.CharField(
        'Status',
        max_length=32,
        choices=STATUS_CHOICES,
        )
    priority = models.CharField(
        'Priorité',
        max_length=32,
        choices=PRIORITY_CHOICES,
        )
    tag = models.CharField(
        'Balise',
        max_length=32,
        choices=TAG_CHOICES,
        )
    created_time = models.DateTimeField(auto_now_add=True)

    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='issues',
        )

    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )

    assigned_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assigned',
        default=author_user_id,
        )

    def __str__(self):
        return self.title


class Comment(models.Model):
    description = models.TextField(
        'Description',
        max_length=1024,
        blank=True,
        )

    author_user_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )

    issue_id = models.ForeignKey(
        to=Issue,
        on_delete=models.CASCADE,
        related_name='comments',
        )

    created_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "Commentaire de {}".format(
            self.author_user_id.username,
            )
