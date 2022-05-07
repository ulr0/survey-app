from django.contrib import admin
from django.utils.html import format_html
from nested_admin import NestedTabularInline, NestedStackedInline, NestedModelAdmin

from surveys.models import Survey, Question, Choice, Respondent

class ChoiceInline(NestedTabularInline):
    model = Choice
    extra = 1
    min_num = 2

class QuestionInline(NestedStackedInline):
    model = Question
    extra = 1
    min_num = 1

    inlines = [ChoiceInline]

@admin.display(description=("Column title"))
class SurveyAdmin(NestedModelAdmin):
    list_display = [
        'title_to_detail',
        'number_of_questions',
        'number_of_respondents',
        'created_at',
        'updated_at',
        'is_deleted',
        'update'
    ]
    list_display_links = [
        'update'
    ]
    list_per_page = 15

    fieldsets = (
        (None, {'fields' : ['title']}),
    )

    inlines = [QuestionInline]

    def title_to_detail(self, obj):
        return format_html(f"<a href='http://127.0.0.1:8000/admin/surveys/{obj.id}'>{obj.title}</a>")

    def number_of_questions(self, obj):
        return Question.objects.filter(survey_id=obj.id).count()

    def number_of_respondents(self, obj):
        return Respondent.objects.filter(survey_id=obj.id).count()
    
    def update(self, obj):
        return 'update'

admin.site.register(Survey, SurveyAdmin)