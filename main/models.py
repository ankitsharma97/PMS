from django.db import models
from django.contrib.auth.models import User
# Create your models here.
 
 
class Role(models.Model):
    name = models.CharField( max_length=50)
    
    def __str__(self):
        return self.name
    
    
class Assigned_Role(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    
    def __str__(self):
        return f" {self.name}: {self.role}"
    
    
class Problem(models.Model):
    day = models.IntegerField()
    problem_name = models.CharField(max_length=255)
    problem_link = models.URLField(max_length=500)
    difficulty = models.CharField(max_length=50)
    topic = models.CharField(max_length=100)
    subtopic = models.CharField(max_length=100)
    final_youtube_link = models.URLField(max_length=500, blank=True, null=True)
    record_by = models.CharField(max_length=100)
    hint_writer = models.ForeignKey(Assigned_Role, on_delete=models.CASCADE, related_name='hint_written_problems')
    deadline = models.DateField()
    small_hint = models.TextField(blank=True, null=True,default='')
    big_hint = models.TextField(blank=True, null=True,default='')
    reviewer = models.ForeignKey(Assigned_Role, on_delete=models.CASCADE, related_name='reviewed_problems')
    reviewed = models.BooleanField(default=False)
    reviewer_deadline = models.DateField()
    remark_for_small_hint = models.TextField(blank=True, null=True,default=None)
    remark_for_big_hint = models.TextField(blank=True, null=True,default=None)

    def __str__(self):
        return f"Day {self.day}: {self.problem_name} ({self.difficulty})"