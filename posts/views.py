from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .models import Post
from .forms import PostForm

# Create your views here.
# INDEX
def list(request):
    # posts = Post.objects.order_by('-pk')     # 게시글이 없을 때 없다고 표시하고 싶을 때는 이렇게 데이터 받아옴
    posts = get_list_or_404(Post.objects.order_by('-pk'))
    context = {
        'posts': posts,
    }
    return render(request, 'posts/list.html', context)
    
# CREATE
def create(request):
    if request.method == "POST":
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post_form.save()
            return redirect('posts:list')
    else:
        post_form = PostForm()
    context = {
        'post_form' : post_form, 
    }
    return render(request, 'posts/form.html', context)
    
# UPDATE
def update(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.save()
            return redirect('posts:list')
    else:
        post_form = PostForm(instance=post)    # 위의 인스턴스 값 받아옴
    context = {
        'post_form' : post_form,
    }
    return render(request, 'posts/form.html', context)
    
# DELETE
def delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        post.delete()
    return redirect('posts:list')