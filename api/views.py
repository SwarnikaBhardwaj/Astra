from django.http import JsonResponse
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from core.models import Hub, Post, Comment, UserProfile, MentorshipRequest, Skill, User
from datetime import datetime, timedelta


def hubs_json(request):
    """Return all hubs with stats as JSON"""
    hubs = Hub.objects.annotate(
        member_count=Count('members'),
        post_count=Count('posts')
    ).values('id', 'name', 'slug', 'icon', 'description', 'member_count', 'post_count')

    return JsonResponse({
        'hubs': list(hubs),
        'total': len(hubs)
    })


def posts_json(request, hub_slug):
    """Return posts for a specific hub as JSON"""
    try:
        hub = Hub.objects.get(slug=hub_slug)
        posts = hub.posts.select_related('author').values(
            'id', 'title', 'content', 'post_type',
            'helpful_count', 'created_at',
            'author__username', 'author__first_name', 'author__last_name'
        )

        return JsonResponse({
            'hub': hub.name,
            'posts': list(posts),
            'total': len(posts)
        })
    except Hub.DoesNotExist:
        return JsonResponse({'error': 'Hub not found'}, status=404)


def platform_stats(request):
    """Overall platform statistics for analytics dashboard"""
    stats = {
        'total_users': User.objects.count(),
        'total_posts': Post.objects.count(),
        'total_comments': Comment.objects.count(),
        'total_hubs': Hub.objects.count(),
        'total_mentors': UserProfile.objects.filter(is_mentor=True).count(),
        'total_mentorship_requests': MentorshipRequest.objects.count(),
        'pending_requests': MentorshipRequest.objects.filter(status='pending').count(),
        'accepted_requests': MentorshipRequest.objects.filter(status='accepted').count(),
    }

    # Hub stats
    hub_stats = Hub.objects.annotate(
        member_count=Count('members'),
        post_count=Count('posts')
    ).values('name', 'icon', 'member_count', 'post_count')

    stats['hub_breakdown'] = list(hub_stats)

    # Post type distribution
    post_types = Post.objects.values('post_type').annotate(
        count=Count('id')
    ).order_by('-count')

    stats['post_types'] = list(post_types)

    return JsonResponse(stats)


def growth_stats(request):
    """User and post growth over time (last 30 days)"""
    thirty_days_ago = datetime.now() - timedelta(days=30)

    # Users by date
    users_by_date = User.objects.filter(
        date_joined__gte=thirty_days_ago
    ).annotate(
        date=TruncDate('date_joined')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')

    # Posts by date
    posts_by_date = Post.objects.filter(
        created_at__gte=thirty_days_ago
    ).annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')

    return JsonResponse({
        'users': [
            {'date': str(item['date']), 'count': item['count']}
            for item in users_by_date
        ],
        'posts': [
            {'date': str(item['date']), 'count': item['count']}
            for item in posts_by_date
        ]
    })


def skills_distribution(request):
    """Most common skills across the platform"""
    skills = Skill.objects.annotate(
        user_count=Count('users')
    ).filter(user_count__gt=0).order_by('-user_count')[:10]

    data = [
        {'skill': skill.name, 'count': skill.user_count}
        for skill in skills
    ]

    return JsonResponse({'skills': data})
