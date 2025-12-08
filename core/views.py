from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import Hub, Post, Comment, UserProfile, MentorshipRequest, HelpfulVote, Skill
from .forms import SignUpForm, UserProfileForm, PostForm, CommentForm, MentorshipRequestForm
from django.contrib.auth.models import User
import json

@login_required
def home(request):
    """Landing page with recent posts"""
    if request.user.is_authenticated:
        # Show personalized feed for logged-in users
        joined_hubs = request.user.joined_hubs.all()
        if joined_hubs.exists():
            posts = Post.objects.filter(hub__in=joined_hubs).select_related('author', 'hub')[:20]
        else:
            posts = Post.objects.all().select_related('author', 'hub')[:20]
    else:
        # Show featured posts for anonymous users
        posts = Post.objects.all().select_related('author', 'hub')[:10]

    hubs = Hub.objects.annotate(member_count=Count('members'))[:6]

    context = {
        'posts': posts,
        'hubs': hubs,
    }
    return render(request, 'core/home.html', context)

@login_required
def about(request):
    """About page"""
    return render(request, 'core/about.html')


def signup(request):
    """User registration"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(
                user=user,
                bio=form.cleaned_data.get('bio', '')
            )
            login(request, user)
            messages.success(request, f'Welcome to Astra, {user.first_name}!')
            return redirect('core:home')
    else:
        form = SignUpForm()

    return render(request, 'core/signup.html', {'form': form})


def login_view(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('core:home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'core/login.html')


def logout_view(request):
    """User logout"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('core:login')

@login_required
def hub_list(request):
    """List all hubs"""
    hubs = Hub.objects.annotate(
        member_count=Count('members'),
        post_count=Count('posts')
    ).order_by('-member_count')

    return render(request, 'core/hub_list.html', {'hubs': hubs})

@login_required
def hub_detail(request, slug):
    """Hub detail with posts"""
    hub = get_object_or_404(Hub, slug=slug)
    posts = hub.posts.all().select_related('author', 'hub')

    # Check if user is a member
    is_member = request.user.is_authenticated and hub.members.filter(id=request.user.id).exists()

    context = {
        'hub': hub,
        'posts': posts,
        'is_member': is_member,
    }
    return render(request, 'core/hub_detail.html', context)


@login_required
def join_hub(request, slug):
    """Join or leave a hub"""
    hub = get_object_or_404(Hub, slug=slug)

    if hub.members.filter(id=request.user.id).exists():
        hub.members.remove(request.user)
        messages.info(request, f'You left {hub.name}')
    else:
        hub.members.add(request.user)
        messages.success(request, f'You joined {hub.name}!')

    return redirect('core:hub_detail', slug=slug)


def post_detail(request, pk):
    """Post detail with comments"""
    post = get_object_or_404(Post.objects.select_related('author', 'hub'), pk=pk)
    comments = post.comments.all().select_related('author')

    # Check if user has voted
    user_voted = False
    if request.user.is_authenticated:
        user_voted = HelpfulVote.objects.filter(user=request.user, post=post).exists()

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added!')
            return redirect('core:post_detail', pk=pk)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'user_voted': user_voted,
    }
    return render(request, 'core/post_detail.html', context)


@login_required
def post_create(request):
    """Create a new post"""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('core:post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'core/post_form.html', {'form': form, 'title': 'Create Post'})


@login_required
def post_edit(request, pk):
    """Edit existing post"""
    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated!')
            return redirect('core:post_detail', pk=pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'core/post_form.html', {'form': form, 'title': 'Edit Post', 'post': post})


@login_required
def post_delete(request, pk):
    """Delete post"""
    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted.')
        return redirect('core:home')

    return render(request, 'core/post_confirm_delete.html', {'post': post})


@login_required
def vote_helpful(request, pk):
    """Vote post as helpful"""
    post = get_object_or_404(Post, pk=pk)

    vote, created = HelpfulVote.objects.get_or_create(user=request.user, post=post)

    if created:
        post.helpful_count += 1
        post.save()
        messages.success(request, 'Marked as helpful!')
    else:
        vote.delete()
        post.helpful_count -= 1
        post.save()
        messages.info(request, 'Vote removed.')

    return redirect('core:post_detail', pk=pk)


@login_required
def add_comment(request, post_pk):
    """Add comment to post"""
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added!')

    return redirect('core:post_detail', pk=post_pk)


def profile_view(request, username):
    """View user profile"""
    from django.contrib.auth.models import User
    user = get_object_or_404(User, username=username)
    profile = user.profile
    posts = user.posts.all()[:10]

    context = {
        'profile_user': user,
        'profile': profile,
        'posts': posts,
    }
    return render(request, 'core/profile_view.html', context)


@login_required
def profile_edit(request, username):
    """Edit own profile"""
    if request.user.username != username:
        messages.error(request, 'You can only edit your own profile.')
        return redirect('core:profile_view', username=username)

    profile = request.user.profile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('core:profile_view', username=username)
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'core/profile_edit.html', {'form': form})


def mentor_list(request):
    """List all mentors"""
    mentors = UserProfile.objects.filter(is_mentor=True).select_related('user')
    return render(request, 'core/mentor_list.html', {'mentors': mentors})


@login_required
def request_mentorship(request, username):
    """Request mentorship from a mentor"""
    from django.contrib.auth.models import User
    mentor = get_object_or_404(User, username=username)

    if not mentor.profile.is_mentor:
        messages.error(request, 'This user is not a mentor.')
        return redirect('core:profile_view', username=username)

    if request.method == 'POST':
        form = MentorshipRequestForm(request.POST)
        if form.is_valid():
            mentorship_request = form.save(commit=False)
            mentorship_request.mentee = request.user
            mentorship_request.mentor = mentor
            mentorship_request.save()
            messages.success(request, f'Mentorship request sent to {mentor.get_full_name()}!')
            return redirect('core:profile_view', username=username)
    else:
        form = MentorshipRequestForm()

    return render(request, 'core/request_mentorship.html', {'form': form, 'mentor': mentor})


@login_required
def mentorship_dashboard(request):
    """View mentorship requests (sent and received)"""
    sent_requests = MentorshipRequest.objects.filter(mentee=request.user).select_related('mentor')
    received_requests = MentorshipRequest.objects.filter(mentor=request.user).select_related('mentee')

    context = {
        'sent_requests': sent_requests,
        'received_requests': received_requests,
    }
    return render(request, 'core/mentorship_dashboard.html', context)


@login_required
def update_mentorship_status(request, pk):
    """Accept/decline mentorship request"""
    mentorship_request = get_object_or_404(MentorshipRequest, pk=pk, mentor=request.user)

    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['accepted', 'declined']:
            mentorship_request.status = status
            mentorship_request.save()
            messages.success(request, f'Request {status}!')

    return redirect('core:mentorship_dashboard')


@staff_member_required
def analytics_dashboard(request):
    """Analytics dashboard for staff (with Vega-Lite charts)"""

    # Get hub stats for chart
    hubs = Hub.objects.annotate(
        member_count=Count('members'),
        post_count=Count('posts')
    ).values('name', 'icon', 'member_count', 'post_count')

    # Get skills distribution
    skills = Skill.objects.annotate(
        user_count=Count('users')
    ).filter(user_count__gt=0).order_by('-user_count')[:10]

    # Prepare data for Vega-Lite
    hub_data = [
        {'hub': h['name'], 'posts': h['post_count'], 'members': h['member_count']}
        for h in hubs
    ]

    skill_data = [
        {'skill': s.name, 'users': s.user_count}
        for s in skills
    ]

    # Mentorship stats
    mentorship_stats = {
        'pending': MentorshipRequest.objects.filter(status='pending').count(),
        'accepted': MentorshipRequest.objects.filter(status='accepted').count(),
        'declined': MentorshipRequest.objects.filter(status='declined').count(),
        'completed': MentorshipRequest.objects.filter(status='completed').count(),
    }

    context = {
        'hub_data': json.dumps(hub_data),
        'skill_data': json.dumps(skill_data),
        'mentorship_stats': mentorship_stats,
        'total_users': User.objects.count(),
        'total_posts': Post.objects.count(),
        'total_comments': Comment.objects.count(),
        'total_hubs': Hub.objects.count(),
    }

    return render(request, 'core/analytics_dashboard.html', context)


import csv
from django.http import HttpResponse


@login_required
def export_portfolio(request, username):
    """Export user's portfolio as CSV"""
    if request.user.username != username and not request.user.is_staff:
        messages.error(request, 'You can only export your own portfolio.')
        return redirect('core:home')

    from django.contrib.auth.models import User
    user = get_object_or_404(User, username=username)

    # Create the HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{username}_portfolio.csv"'

    writer = csv.writer(response)
    writer.writerow(['Type', 'Title', 'Hub', 'Date', 'Helpful Count', 'Comments'])

    # Add posts
    for post in user.posts.all():
        writer.writerow([
            post.get_post_type_display(),
            post.title,
            post.hub.name,
            post.created_at.strftime('%Y-%m-%d'),
            post.helpful_count,
            post.comment_count()
        ])

    return response