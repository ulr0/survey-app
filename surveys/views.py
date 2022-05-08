from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction

from surveys.models import Respondent, Survey, Question, Answer
from surveys.exceptions import CheckboxNotChecked

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
    survey = get_object_or_404(Survey, id=survey_id)
    
    try:
        questions = Question.objects.filter(survey_id=survey_id)
        phone_number = request.POST.get('phone_number')
        
        with transaction.atomic():
            respondent = Respondent.objects.create(survey_id=survey_id, phone_number=phone_number)

            for question in questions:
                if question.choice_type != 'checkbox':
                    choice = request.POST.get('question_' + str(question.id))
                    Answer.objects.create(
                        respondent_id=respondent.id, 
                        question_id=question.id, 
                        choice_id=int(choice))
                
                else:
                    choices = request.POST.getlist('question_' + str(question.id))

                    if not choices:
                        raise CheckboxNotChecked(f"{question.title} 문항의 답을 선택해주세요.")

                    bulk_answer_list = [Answer(
                        respondent_id=respondent.id,
                        question_id=question.id,
                        choice_id=int(choice)) for choice in choices]
                    Answer.objects.bulk_create(bulk_answer_list)

        return render(request, 'templates/surveys/submit.html')
    
    except CheckboxNotChecked as e:
        messages.error(request, e)
        return redirect('surveys:get_survey', survey_id=survey.id)

    except:
        messages.error(request, '설문 제출에 실패하였습니다. 다시 제출해주세요.')
        return redirect('surveys:get_survey', survey_id=survey.id)