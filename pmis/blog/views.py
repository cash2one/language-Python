# Create your views here.
from django.shortcuts import render, get_object_or_404
from blog.models import Posts

def index(request):
    latest = Posts.objects.order_by('-pubdate')[:5]
    return render(request, 'index.html', {'latest': latest})

def detail(request, posts_id):
    post = get_object_or_404(Posts, pk = posts_id)
    return render(request, 'detail.html', {'post':post})

