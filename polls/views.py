from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Question, Choice
from django.http import HttpResponseRedirect
from django.urls import reverse
def home(request):
    return redirect(reverse('polls:choose_mode'))

def index(request):
    latest_questions = Question.objects.order_by('-pub_date')[:5]
    return render(request, 'polls/index.html', {'questions': latest_questions})

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.", 
    })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

import random
from django.views.decorators.csrf import csrf_exempt

@login_required
def choose_mode(request):
    return render(request, 'polls/choose_mode.html')

@login_required
def exam_view(request):
    questions = list(Question.objects.filter(mode='EXAM'))
    random.shuffle(questions)
    return render(request, 'polls/exam.html', {'questions': questions})
 
@login_required
def exam_submit(request):
    if request.method == 'POST':
        score = 0
        total = 0
        for key, value in request.POST.items():
            if key.startswith('question_'):
                try:
                    choice = Choice.objects.get(pk=int(value))
                    if choice.is_correct:
                        score += 1
                    total += 1
                except (ValueError, Choice.DoesNotExist):
                    continue
        percent = round((score / total) * 100) if total > 0 else 0
        return render(request, 'polls/exam_result.html', {
            'score': score,
            'total': total,
            'percent': percent
        })
    return redirect('polls:exam')

@login_required
def survey_view(request):
    questions = Question.objects.filter(mode='SURVEY')
    return render(request, 'polls/survey.html', {'questions': questions})

@login_required
def survey_submit(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('question_'):
                try:
                    choice = Choice.objects.get(pk=value)
                    choice.votes += 1
                    choice.save()
                except Choice.DoesNotExist:
                    continue
        questions = Question.objects.filter(mode='SURVEY')
        return render(request, 'polls/survey_result.html', {'questions': questions})
    return redirect('polls:survey')

