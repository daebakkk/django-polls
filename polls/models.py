from django.db import models
from django.urls import reverse
# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    MODE_CHOICES = [
        ('EXAM', 'Exam'),
        ('SURVEY', 'Survey'),
    ]
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='SURVEY')

    def __str__(self):
        return self.question_text

    def get_absolute_url(self):
        return reverse('polls:detail', args=[str(self.id)])

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.choice_text
