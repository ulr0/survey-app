from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET, require_POST

from surveys.models import Survey, Question

@require_GET
def get_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    questions = Question.objects.prefetch_related('choice_set').filter(survey_id=survey.id)

    return render(request, 'templates/surveys/survey.html', {
        'survey' : survey,
        'questions' : questions
    })

@require_POST
def create_respondent_answers(request, survey_id):
    print(1)
    return render(request, 'templates/surveys/submitted.html')