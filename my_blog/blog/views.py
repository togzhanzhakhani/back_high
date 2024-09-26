from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Post, User, Tag
from .forms import PostForm, CommentForm, CustomUserCreationForm
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.core.cache import cache


def index(request):
    return HttpResponse("Hello, Blog!")

@cache_page(60)
def post_list(request):
    author_id = request.GET.get('author')
    tag_id = request.GET.get('tag')
    posts = Post.objects.select_related('author').prefetch_related('tags')
    if author_id:
        posts = posts.filter(author__id=author_id)
    if tag_id:
        posts = posts.filter(tags__id=tag_id)
    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    authors = User.objects.all()
    tags = Tag.objects.all()
    return render(request, 'blog/post_list.html', {'page_obj': page_obj, 'authors': authors, 'tags': tags, 'selected_author': author_id, 'selected_tag': tag_id})

def get_comment_count(post):
    cache_key = f'comment_count_{post.id}'
    count = cache.get(cache_key)
    if count is None:
        count = post.comments.count() 
        cache.set(cache_key, count, timeout=600)  
    return count

@cache_page(60)
def post_detail(request, pk):
    post = get_object_or_404(Post.objects.prefetch_related('comments'), pk=pk)
    comment_count = get_comment_count(post)
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                cache.delete(f'comment_count_{post.id}')
                return redirect('post_detail', pk=post.pk)
        else:
            return redirect('login')
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': post.comments.all(), 'form': form, 'comment_count': comment_count})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})
