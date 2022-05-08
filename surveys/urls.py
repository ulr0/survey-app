from django.urls import path

from surveys.views import get_survey, create_respondent_answers

app_name = 'surveys'

urlpatterns = [
    path('<int:survey_id>', get_survey, name='get_survey'),
    path('<int:survey_id>/submit', create_respondent_answers, name='create_respondent_answers'),
]