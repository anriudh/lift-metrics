from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Workout
from .forms import WorkoutForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    # Adding Bootstrap classes to form fields manually for consistency
    for field in form.fields.values():
        field.widget.attrs.update({'class': 'form-control bg-slate-700 border-slate-600 text-slate-100'})
        
    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard(request):
    recent_workouts = Workout.objects.filter(user=request.user).order_by('-date')[:5]
    context = {
        'recent_workouts': recent_workouts,
    }
    return render(request, 'workouts/dashboard.html', context)


@login_required
def workout_history(request):
    workouts = Workout.objects.filter(user=request.user).order_by('-date')
    return render(request, 'workouts/history.html', {'workouts': workouts})


@login_required
def log_workout(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            return redirect('dashboard')
    else:
        form = WorkoutForm()
        
    return render(request, 'workouts/log_workout.html', {'form': form})
