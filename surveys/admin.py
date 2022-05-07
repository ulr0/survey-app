from django import forms
from django.contrib import admin
from nested_admin import NestedTabularInline, NestedStackedInline, NestedModelAdmin

from surveys.models import Survey, Question, Choice

class ChoiceInline(NestedTabularInline):
    model = Choice
    extra = 1
    min_num = 2

class QuestionInline(NestedStackedInline):
    model = Question
    extra = 1
    min_num = 1

    inlines = [ChoiceInline]

class SurveyAdmin(NestedModelAdmin):
    list_display = (
        'title',
        'created_at',
        'updated_at',
        'is_deleted'
    )

    fieldsets = (
        (None, {'fields' : ['title']}),
    )

    inlines = [QuestionInline]

admin.site.register(Survey, SurveyAdmin)