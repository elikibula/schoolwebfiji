# home/views.py
from django.shortcuts import render, redirect
from news.models import News  # Import the News model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


def home(request):
    featured_news = News.objects.filter(is_featured=True).select_related('author', 'category').order_by('-date_posted')[:3]

    return render(request, 'home/index.html', {
        'featured_news': featured_news,
    })
    
def about_view(request):
    return render(request, 'home/about.html')


def students_view(request):
    return render(request, 'home/students.html')


@login_required
def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')  # Use your custom dashboard template


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard or any other page
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
