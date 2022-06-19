from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse

from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import User, Post, Profile
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 10)
    if request.GET.get("page") != None:
        try:
            posts = paginator.page(request.GET.get("page"))
        except:
            posts = paginator.page(1)
    else:
        posts = paginator.page(1)

    return render(request, 'network/index.html', {'posts': posts})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            users_profile = Profile.objects.create(user=user)
            users_profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def profile(request, username):      

    user = User.objects.get(username=username)
    users_profile = Profile.objects.get(user=request.user)
    profile = Profile.objects.get(user=user)
    posts = Post.objects.filter(user=user).order_by('-timestamp')
    paginator = Paginator(posts, 10)
    if request.GET.get("page") != None:
        try:
            posts = paginator.page(request.GET.get("page"))
        except:
            posts = paginator.page(1)
    else:
        posts = paginator.page(1)
    
    print(posts)
    #print(profile)
    print(users_profile)
    for i in users_profile.follower.all():
        print(i)
    context = {
        'posts': posts,
        "user": user,
        "profile": profile,
        'users_profile': users_profile
    }
    return render(request, 'network/profile.html', context)


@login_required
def following(request):
    following = Profile.objects.get(user=request.user).following.all()
    posts = Post.objects.filter(user__in=following).order_by('-timestamp')
    paginator = Paginator(posts, 10)
    if request.GET.get("page") != None:
        try:
            posts = paginator.page(request.GET.get("page"))
        except:
            posts = paginator.page(1)
    else:
        posts = paginator.page(1)
    return render(request, 'network/following.html', {'posts': posts})


@login_required
@csrf_exempt
def like(request):
    if request.method == "POST":
        post_id = request.POST.get('postid')
        print(post_id)
        is_liked = request.POST.get('is_liked')
        print(is_liked)
        try:
            post = Post.objects.get(id=post_id)
            if is_liked == 'no':
                post.like.add(request.user)
                is_liked = 'yes'
            elif is_liked == 'yes':
                post.like.remove(request.user)
                is_liked = 'no'
            post.save()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        except:
            return JsonResponse({'error': "Post not found", "status": 404})
            
    return JsonResponse({}, status=400)
    


@login_required
@csrf_exempt
def follow(request):
    if request.method == "POST":
        user = request.POST.get('user')
        action = request.POST.get('action')

        if action == 'Follow':
            try:
                # add user to current user's following list
                user = User.objects.get(username=user)
                profile = Profile.objects.get(user=request.user)
                profile.following.add(user)
                profile.save()

                # add current user to  user's follower list
                profile = Profile.objects.get(user=user)
                profile.follower.add(request.user)
                profile.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            except:
                return JsonResponse({}, status=404)
                
        else:
            try:
                # add user to current user's following list
                user = User.objects.get(username=user)
                profile = Profile.objects.get(user=request.user)
                profile.following.remove(user)
                profile.save()

                # add current user to  user's follower list
                profile = Profile.objects.get(user=user)
                profile.follower.remove(request.user)
                profile.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            except:
                return JsonResponse({}, status=404)
                

    return JsonResponse({}, status=400)
    



@login_required
@csrf_exempt
def edit_post(request):
    if request.method == "POST":
        post_id = request.POST.get('postid')
        new_post = request.POST.get('post')
        print(post_id)
        print(new_post)
        try:
            post = Post.objects.get(id=post_id)
            if post.user == request.user:
                post.post = new_post.strip()
                post.save()
                return redirect('index')
        except:
            return JsonResponse({}, status=404)

    return JsonResponse({}, status=400)
    


@login_required
@csrf_exempt
def addpost(request):
    if request.method == "POST":
        post = request.POST.get('add-text')
        if len(post) != 0:
            obj = Post()
            obj.post = post
            obj.user = request.user
            obj.save()
            context = {
                'status': 201,
                'post_id': obj.id,
                'username': request.user.username,
                'timestamp': obj.timestamp.strftime("%B %d, %Y, %I:%M %p"),
            }
            return redirect('index')
    return JsonResponse({}, status=400)
    

