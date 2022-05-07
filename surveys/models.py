from tkinter import CASCADE
from django.db import models

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

class Survey(TimeStampModel):
    title = models.CharField(max_length=100)

    class Meta:
        db_table = 'surveys'

    def __str__(self):
        return f"{self.title}"

class Question(TimeStampModel):
    CHOICE_TYPE_CHOICES = (
        ('checkbox', 'checkbox'),
        ('radio', 'radio'),
        ('select', 'select')
    )
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    choice_type = models.CharField(max_length=10, choices=CHOICE_TYPE_CHOICES, default='radio')

    class Meta:
        db_table = 'questions'

    def __str__(self):
        return f"{self.title}"

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=50)

    class Meta:
        db_table = 'choices'
    
    def __str__(self):
        return f"{self.text}"

class Respondent(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=15)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'respondents'

class Answer(models.Model):
    respondent = models.ForeignKey(Respondent, on_delete=models.CASCADE) 
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'answers'