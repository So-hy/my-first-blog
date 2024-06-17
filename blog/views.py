from django.http import JsonResponse
from django.shortcuts import render
from .models import Post
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from rest_framework import viewsets
from .serializers import PostSerializer
import json
from django.views.decorators.csrf import csrf_protect

class BlogImage(viewsets.ModelViewSet): 
    queryset = Post.objects.all() 
    serializer_class = PostSerializer
    
# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
   post = get_object_or_404(Post, pk=pk)
   return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request): 
    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


# def post_new(request):
#     if request.method == "POST":
#         form = PostForm(request.POST) 
#         if form.is_valid():
#             post = form.save(commit=False) 
#             post.author = request.user 
#             post.published_date = timezone.now() 
#             post.save()
#             return redirect('post_detail', pk=post.pk) 
#     else:
#         form = PostForm()
#     return render(request, 'blog/post_edit.html', {'form': form})

@csrf_protect
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return JsonResponse({'status': 'success', 'post_id': post.pk})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError:
            json_data = {}

        post_data = request.POST.dict()
        post_data.update(json_data)

        form = PostForm(post_data, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return JsonResponse({'status': 'success', 'post_id': post.pk})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def js_test(request):
    return render(request, 'blog/js_test.html',{})