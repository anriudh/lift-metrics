from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


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
    return render(request, 'workouts/dashboard.html')
