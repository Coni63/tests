from django.db import models
from orderable.models import Orderable

class A(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey('C', on_delete=models.CASCADE)
    bs = models.ManyToManyField('B', through='AtoB')

    def __str__(self):
        return f"{self.name} ({self.category})"


class B(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
class C(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category

# class AtoB(models.Model):
class AtoB(Orderable):
    a = models.ForeignKey(A, on_delete=models.CASCADE)
    b = models.ForeignKey(B, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        unique_together = ('a', 'b')
        ordering = ['sort_order']


class Status(models.Model):
    message_id = models.CharField(max_length=10, blank=True)
    documentum_id = models.CharField(max_length=100, blank=True)
    publication_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, blank=True)
    status_message = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(blank=True)
    message = models.JSONField(blank=True)