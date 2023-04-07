from django.db import models
from users.models import User


class Project(models.Model):
    name = models.CharField(max_length=80, blank=False, null=False, verbose_name='Project Name')
    repo_link = models.URLField(null=True, blank=True, verbose_name="Repository Project's Link")
    users = models.ManyToManyField(User, verbose_name="Project's Allowed Users")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name="Updated at")
    is_deleted = models.BooleanField(default=False, verbose_name="Is deleted")

    def __str__(self):
        return f'{self.pk} - {self.name}'

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ("-created_at",)


class Todo(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="Project at")
    todo_text = models.TextField(null=False, blank=False, verbose_name='ToDo Text')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Created by User")
    is_active = models.BooleanField(default=True, verbose_name="Is active")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name="Updated at")
    is_deleted = models.BooleanField(default=False, verbose_name="Is deleted")

    def __str__(self):
        return f'{self.pk} - "{self.project}" - "{self.todo_text[:10]}..." - ' \
               f'{self.creator} - {self.updated_at}'

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    class Meta:
        verbose_name = "ToDo"
        verbose_name_plural = "ToDo List"
        ordering = ("-created_at",)
