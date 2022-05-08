from collections import defaultdict

from django.contrib import admin
from django.utils.html import format_html
from nested_admin import NestedTabularInline, NestedStackedInline, NestedModelAdmin
from django.shortcuts import get_object_or_404, render

from surveys.models import Survey, Question, Choice, Respondent, Answer

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
        'update'
    ]
    list_display_links = [
        'update'
    ]
    list_per_page = 15

    search_fields = ['title', 'question__title']

    inlines = [QuestionInline]

    def title_to_detail(self, obj):
        return format_html(f"<a href='http://127.0.0.1:8000/admin/surveys/survey/{obj.id}'>{obj.title}</a>")

    def number_of_questions(self, obj):
        return Question.objects.filter(survey_id=obj.id).count()

    def number_of_respondents(self, obj):
        return Respondent.objects.filter(survey_id=obj.id).count()
    
    def update(self, obj):
        return 'update'

    def get_urls(self):
        from django.urls import path
        urls = super(SurveyAdmin, self).get_urls()
        url = [
            path('<int:survey_id>', self.admin_site.admin_view(self.get_survey_detail))
        ]
        return url + urls
    
    def get_survey_detail(self, request, survey_id):
        survey = get_object_or_404(Survey, id=survey_id)
        questions = Question.objects.prefetch_related('choice_set').filter(survey_id=survey_id)
        number_of_respondents = Respondent.objects.filter(survey_id=survey_id).count()
        answers = Answer.objects.select_related('respondent').filter(respondent__survey_id=survey_id)
        
        choice_count = defaultdict(int)
        for answer in answers:
            choice_count[answer.choice_id] += 1

        return render(request, "templates/admin/survey_detail.html", {
            'survey' : survey,
            'questions' : questions,
            'number_of_respondents' : number_of_respondents,
            'choice_count' : choice_count
        })

admin.site.register(Survey, SurveyAdmin)