from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Post, Group, User
from .forms import PostForm
from .utils import get_page_context

POSTS_ON_LIST: int = 10


def index(request):
    context = get_page_context(Post.objects.all().order_by('-pub_date'),
                               request
                               )
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:POSTS_ON_LIST]
    context = {
        'group': group,
        'posts': posts,
    }
    context.update(get_page_context(Post.objects.all().order_by('-pub_date'),
                   request)
                   )
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    context = {
        'author': author,
    }
    context.update(get_page_context(Post.objects.all().filter(author=author),
                   request)
                   )
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None)
        context = {'form': form, 'is_edit': False, }
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', request.user.username)
        context = {'form': form, 'is_edit': False, }
        return render(request, 'posts/create_post.html', context)
    form = PostForm()
    context = {'form': form, 'is_edit': False, }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect("posts:profile", post_id=post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect("posts: post_detail", post_id)
    else:
        context = {'form': form, 'is_edit': True, 'post': post}
        return render(request, 'posts/create_post.html', context)
