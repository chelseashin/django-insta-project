from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q
# from itertools import chain
from .forms import PostForm, ImageForm, CommentForm
from .models import Post, Image, Comment

# Create your views here.
# INDEX
def list(request):
    # 1 - Q objects 방식으로 하는 것이 좋음.
    followings = request.user.followings.all()
    posts = Post.objects.filter(Q(user__in=followings) | Q(user=request.user.id)).order_by('-pk')
    
    # 2
    # followings = request.user.followings.all()
    # chain_followings = chain(follwings, [request.user])
    # posts = Post.objects.filter(Q(user__in=chain_followings).order_by('-pk')
    
    # posts = Post.objects.filter(user__in=request.user.followings.all()).order_by('-pk')    # 내가 팔로잉하고있는 모든 유저
    # posts = Post.objects.order_by('-pk')     # 기본. 게시글이 없을 때 없다고 표시하고 싶을 때는 이렇게 데이터 받아옴
    # posts = get_list_or_404(Post.objects.order_by('-pk'))
    
    comment_form = CommentForm()
    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'posts/list.html', context)
    
# CREATE
@login_required
def create(request):
    if request.method == "POST":
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)    # 게시글 내용 처리 끝
            post.user = request.user   # 유저와 함께 저장
            post.save()
            # 이미지가 여러개 돌기 때문에
            for image in request.FILES.getlist('file'):
                request.FILES['file'] = image
                image_form = ImageForm(files=request.FILES)
                if image_form.is_valid():
                    image = image_form.save(commit=False)
                    image.post = post
                    image.save()
            return redirect('posts:list')
    else:
        post_form = PostForm()
        image_form = ImageForm()
    context = {
        'post_form' : post_form, 
        'image_form' : image_form,
    }
    return render(request, 'posts/form.html', context)
    
# UPDATE
@login_required
def update(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    
    if post.user != request.user:
        return redirect('post:list')
    
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
@login_required
def delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    
    if post.user != request.user:
        return redirect('post:list')
    
    if request.method == 'POST':
        post.delete()
    return redirect('posts:list')
    
@login_required
@require_POST
def comment_create(request, post_pk):
    form = CommentForm(request.POST)
    if form.is_valid():
        # comment 를 바로 저장하지 않고 현재 user, post_pk 정보를 넣어서 저장
         comment = form.save(commit=False)    # 들어올 값 더 있음
         comment.user = request.user
         comment.post_id = post_pk
         comment.save()
    return redirect('posts:list')
    
@login_required
@require_POST
def comment_delete(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user != comment.user:
        return redirect('posts:list')
    comment.delete()
    return redirect('posts:list')
    
# 좋아요 구현
@login_required
def like(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    # 1
    # 이미 해당 유저가 like_users에 존재하면 해당 유저를 삭제
    # 이미 해당 유저가 like를 누른 상태면 좋아요 취소
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
    else:    # 없으면 추가(좋아요)
        post.like_users.add(request.user)
    return redirect('posts:list')
    
    # 2 
    # if post.like_users.filter(pk=user.pk).exists():
    #     post.like_users.remove(user)
    # else:
    #     post.like_users.add(request.user)
    # return redirect('posts:list')
    
# 모든 유저들의 글을 볼 수 있게 하기 위해
@login_required
def explore(request):
    posts = Post.objects.order_by('-pk')
    # posts = Post.objects.exclude(user=request.user).order_by('-pk')     # 나말고 모든 사람들의 글을 볼 수 있음
    comment_form = CommentForm()
    context = {
        'posts': posts, 
        'comment_form': comment_form,
    }
    return render(request, 'posts/explore.html', context)