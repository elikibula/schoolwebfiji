from django.shortcuts import render,  redirect, get_object_or_404
from .models import News, Category
from django.contrib.auth.decorators import login_required
from .forms import NewsForm



@login_required
def news_list(request):
    # Main news list
    news_posts = News.objects.all().order_by('-date_posted')
    
    # Recent news (last 5 posts)
    recent_news = News.objects.all().order_by('-date_posted')[:5]
    
    # All categories
    categories = Category.objects.all()
    
    context = {
        'news_posts': news_posts,
        'recent_news': recent_news,
        'categories': categories,
    }
    return render(request, 'news/news.html', context)

@login_required
def news_detail(request, slug):
    # Get the main news item
    news = get_object_or_404(News, slug=slug)
    
    # Get recent news (exclude current news item)
    recent_news = News.objects.exclude(pk=news.pk).order_by('-date_posted')[:5]
    
    # Get all categories
    categories = Category.objects.all()
    
    context = {
        'news': news,
        'recent_news': recent_news,
        'categories': categories,
    }
    return render(request, 'news/news_detail.html', context)

@login_required
def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return redirect('news:news_detail', slug=news.slug)
    else:
        form = NewsForm()
    return render(request, 'news/create_news.html', {'form': form})

@login_required
def update_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    form = NewsForm(request.POST or None, request.FILES or None, instance=news)
    if form.is_valid():
        form.save()
        messages.success(request, "News updated successfully.")
        return redirect('news:news_list')
    return render(request, 'news/news_form.html', {'form': form})

@login_required
def delete_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        news.delete()
        messages.success(request, "News deleted successfully.")
        return redirect('news:news_list')
    return render(request, 'news/delete_news.html', {'news': news})

@login_required
def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    news_posts = News.objects.filter(category=category).order_by('-date_posted')
    
    context = {
        'category': category,
        'news_posts': news_posts,
        'recent_news': News.objects.exclude(category=category).order_by('-date_posted')[:5],
        'categories': Category.objects.all(),
    }
    return render(request, 'news/category.html', context)

    