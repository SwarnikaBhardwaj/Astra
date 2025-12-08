from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models import Count


class Skill(models.Model):
    """Skills that users can have (e.g., Python, Public Speaking, Fundraising)"""
    CATEGORY_CHOICES = [
        ('technical', 'Technical'),
        ('creative', 'Creative'),
        ('leadership', 'Leadership'),
        ('business', 'Business'),
        ('advocacy', 'Advocacy'),
    ]

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='technical')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Badge(models.Model):
    """Equity badges for non-traditional contributions"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Emoji or icon class")

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """Extended user profile with privacy and mentorship settings"""
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('pseudonymous', 'Pseudonymous'),
        ('trusted', 'Trusted Circle Only'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    visibility_mode = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')
    is_mentor = models.BooleanField(default=False)
    skills = models.ManyToManyField(Skill, blank=True, related_name='users')
    equity_badges = models.ManyToManyField(Badge, blank=True, related_name='users')
    reputation_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_display_name(self):
        """Return pseudonym if visibility is pseudonymous"""
        if self.visibility_mode == 'pseudonymous':
            return f"User{self.user.id}"
        return self.user.get_full_name() or self.user.username

    def post_count(self):
        return self.user.posts.count()

    def comment_count(self):
        return self.user.comments.count()


class Hub(models.Model):
    """Topic-based communities (e.g., STEM, Entrepreneurship, Health)"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='💡', help_text="Emoji for hub icon")
    created_at = models.DateTimeField(auto_now_add=True)
    moderators = models.ManyToManyField(UserProfile, blank=True, related_name='moderated_hubs')
    members = models.ManyToManyField(User, blank=True, related_name='joined_hubs')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def member_count(self):
        return self.members.count()

    def post_count(self):
        return self.posts.count()

    class Meta:
        ordering = ['-created_at']


class Post(models.Model):
    """User-generated content (questions, tutorials, stories, resources)"""
    POST_TYPE_CHOICES = [
        ('question', '❓ Question'),
        ('tutorial', '📚 Tutorial'),
        ('story', '💭 Story'),
        ('resource', '🔗 Resource'),
        ('playbook', '📖 Playbook'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default='question')
    video_url = models.URLField(blank=True, help_text="Optional YouTube/Vimeo link")
    is_anonymous = models.BooleanField(default=False)
    helpful_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_author_display(self):
        """Return 'Anonymous' if post is anonymous"""
        if self.is_anonymous:
            return "Anonymous"
        return self.author.profile.get_display_name()

    def comment_count(self):
        return self.comments.count()

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    """Comments on posts, with accepted answer functionality"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    is_accepted_answer = models.BooleanField(default=False)
    helpful_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

    class Meta:
        ordering = ['-is_accepted_answer', '-helpful_count', '-created_at']


class MentorshipRequest(models.Model):
    """Requests from mentees to mentors"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('completed', 'Completed'),
    ]

    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentee_requests')
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentor_requests')
    topic = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.mentee.username} → {self.mentor.username}: {self.topic}"

    class Meta:
        ordering = ['-created_at']


class HelpfulVote(models.Model):
    """Track who voted what as helpful (prevents duplicate votes)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['user', 'post'], ['user', 'comment']]
