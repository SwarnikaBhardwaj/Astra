from django.contrib import admin
from .models import UserProfile, Hub, Post, Comment, MentorshipRequest, Skill, Badge, HelpfulVote


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'is_mentor', 'visibility_mode', 'reputation_score', 'created_at']
    list_filter = ['is_mentor', 'visibility_mode', 'created_at']
    search_fields = ['user__username', 'user__email', 'bio']
    filter_horizontal = ['skills', 'equity_badges']
    readonly_fields = ['created_at', 'reputation_score']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']
    search_fields = ['name']


@admin.register(Hub)
class HubAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'member_count', 'post_count', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    filter_horizontal = ['moderators', 'members']
    readonly_fields = ['created_at']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'hub', 'post_type', 'is_anonymous', 'helpful_count', 'created_at']
    list_filter = ['post_type', 'hub', 'is_anonymous', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['created_at', 'updated_at', 'helpful_count']
    date_hierarchy = 'created_at'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'is_accepted_answer', 'helpful_count', 'created_at']
    list_filter = ['is_accepted_answer', 'created_at']
    search_fields = ['content', 'author__username']
    readonly_fields = ['created_at', 'helpful_count']


@admin.register(MentorshipRequest)
class MentorshipRequestAdmin(admin.ModelAdmin):
    list_display = ['mentee', 'mentor', 'topic', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['mentee__username', 'mentor__username', 'topic']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(HelpfulVote)
class HelpfulVoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'comment', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username']