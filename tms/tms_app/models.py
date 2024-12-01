from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

# Extend AbstractUser to include roles
class User(AbstractUser):
    ROLE_CHOICES = [
        ('PM', 'Project Manager'),
        ('TL', 'Team Leader'),
        ('TM', 'Team Member'),
    ]
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

# Project Model
class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_projects",
        limit_choices_to={'role': 'PM'}
    )
    team_lead = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="led_projects",
        limit_choices_to={'role': 'TL'}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Task Model
class Task(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks",
        limit_choices_to={'role': 'TM'}
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.status})"

# Team Assignment Model (Optional)
class TeamAssignment(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="team_assignments"
    )
    team_member = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="team_assignments",
        limit_choices_to={'role': 'TM'}
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.team_member.username} -> {self.project.name}"
