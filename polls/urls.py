from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:question_id>/results/', views.results, name='results'),

    path('choose-mode/', views.choose_mode, name='choose_mode'),
    path('exam/', views.exam_view, name='exam'),
    path('exam/submit/', views.exam_submit, name='exam_submit'),
    path('survey/', views.survey_view, name='survey'),
    path('survey/submit/', views.survey_submit, name='survey_submit'),
]
