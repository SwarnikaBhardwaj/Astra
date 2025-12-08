from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import UserProfile, Hub, Post, Comment, MentorshipRequest, Skill, Badge
import random


class Command(BaseCommand):
    help = 'Seeds database with sample data for Astra'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Seeding database...')

        # Create skills
        skills_data = [
            ('Python', 'technical'), ('JavaScript', 'technical'), ('Data Science', 'technical'),
            ('Public Speaking', 'leadership'), ('Project Management', 'leadership'),
            ('Graphic Design', 'creative'), ('Writing', 'creative'), ('Video Editing', 'creative'),
            ('Marketing', 'business'), ('Fundraising', 'business'), ('Legal Research', 'advocacy'),
            ('Community Organizing', 'advocacy'), ('Mentorship', 'leadership'),
        ]

        skills = []
        for name, category in skills_data:
            skill, _ = Skill.objects.get_or_create(name=name, defaults={'category': category})
            skills.append(skill)

        self.stdout.write(f'✅ Created {len(skills)} skills')

        # Create badges
        badges_data = [
            ('Caregiver', 'Recognized for balancing caregiving responsibilities', '👶'),
            ('Community Organizer', 'Active in community advocacy and organizing', '🤝'),
            ('Mentor', 'Dedicated to helping others grow', '🌟'),
            ('First-Gen Professional', 'Breaking barriers in their field', '🚀'),
            ('Career Changer', 'Successfully pivoted careers', '🔄'),
        ]

        badges = []
        for name, desc, icon in badges_data:
            badge, _ = Badge.objects.get_or_create(name=name, defaults={'description': desc, 'icon': icon})
            badges.append(badge)

        self.stdout.write(f'✅ Created {len(badges)} badges')

        # Create required test users
        test_users = [
            {'username': 'mohitg2', 'password': 'graingerlibrary', 'is_staff': True,
             'first_name': 'Mohit', 'last_name': 'Gupta'},
            {'username': 'infoadmins', 'password': 'uiucinfo', 'is_staff': False,
             'first_name': 'Info', 'last_name': 'Admin'},
        ]

        for user_data in test_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'email': f"{user_data['username']}@example.com",
                    'is_staff': user_data['is_staff'],
                }
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
                # Create profile
                UserProfile.objects.get_or_create(user=user)

        # Create sample users
        sample_users = [
            ('sarah_mentor', 'Sarah', 'Chen', True),
            ('alex_learner', 'Alex', 'Rodriguez', False),
            ('jamie_advocate', 'Jamie', 'Williams', True),
            ('priya_dev', 'Priya', 'Patel', True),
            ('emma_designer', 'Emma', 'Johnson', False),
            ('lisa_founder', 'Lisa', 'Martinez', True),
            ('maya_writer', 'Maya', 'Thompson', False),
            ('nina_scientist', 'Nina', 'Kumar', True),
        ]

        users = []
        for username, first, last, is_mentor in sample_users:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first,
                    'last_name': last,
                    'email': f'{username}@example.com',
                }
            )
            if created:
                user.set_password('demo1234')
                user.save()

            # Create profile
            profile, _ = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'bio': f'Passionate about learning and growth. {first} is here to connect and share knowledge.',
                    'location': random.choice(
                        ['New York, NY', 'San Francisco, CA', 'Chicago, IL', 'Austin, TX', 'Remote']),
                    'is_mentor': is_mentor,
                    'reputation_score': random.randint(50, 500),
                }
            )

            # Add random skills (2-4)
            profile.skills.set(random.sample(skills, random.randint(2, 4)))

            # Add random badge (50% chance)
            if random.random() > 0.5:
                profile.equity_badges.add(random.choice(badges))

            users.append(user)

        self.stdout.write(f'✅ Created {len(users)} sample users')

        # Create hubs
        hubs_data = [
            ('STEM Careers', '💻', 'For women in science, technology, engineering, and mathematics'),
            ('Entrepreneurship', '🚀', 'Start, scale, and succeed in your own venture'),
            ('Health & Wellness', '💪', 'Physical and mental health support and advice'),
            ('Legal Rights', '⚖️', 'Know your rights and navigate legal systems'),
            ('Caregiving', '👶', 'Support for caregivers and work-life balance'),
            ('Creative Arts', '🎨', 'Express yourself through art, writing, and design'),
            ('Leadership', '⭐', 'Develop leadership skills and advance your career'),
        ]

        hubs = []
        for name, icon, desc in hubs_data:
            hub, _ = Hub.objects.get_or_create(
                name=name,
                defaults={'icon': icon, 'description': desc}
            )
            # Add random members
            hub.members.set(random.sample(users, random.randint(3, 8)))
            hubs.append(hub)

        self.stdout.write(f'✅ Created {len(hubs)} hubs')

        # Create posts
        post_templates = [
            ('question', 'How do I negotiate salary as a first-time employee?',
             'I just got my first job offer and I\'m nervous about negotiating. Any tips on how to approach this conversation?'),
            ('tutorial', 'Step-by-step guide to building your first portfolio website',
             'Here\'s how I built my portfolio from scratch using free tools. Step 1: Choose a platform (GitHub Pages is free). Step 2: Pick a template...'),
            ('story', 'My journey from teacher to software engineer',
             'Three years ago, I was teaching high school. Today, I\'m a full-time developer. Here\'s what I learned along the way...'),
            ('resource', 'Free online courses for data science beginners',
             'I\'ve compiled a list of the best free resources to start learning data science: 1) Python basics on Codecademy...'),
            ('playbook', 'Complete guide to applying for scholarships',
             'Step 1: Research opportunities early. Step 2: Gather all required documents. Step 3: Write compelling essays...'),
            ('question', 'Best practices for work-life balance with young children?',
             'I\'m struggling to manage my career and motherhood. How do you all do it?'),
            ('tutorial', 'Creating effective LinkedIn profiles that get noticed',
             'Your LinkedIn is your digital first impression. Here\'s how to optimize every section...'),
            ('story', 'How I started my nonprofit with zero funding',
             'Everyone said I needed investors. I proved them wrong. Here\'s the bootstrapping story...'),
            ('resource', 'Mental health resources for women entrepreneurs',
             'Running a business is stressful. Here are therapists, apps, and communities that helped me stay grounded...'),
            ('question', 'Should I pivot my career at 35?',
             'I\'m in finance but dream of being a designer. Is it too late to change careers?'),
        ]

        posts = []
        for post_type, title, content in post_templates:
            for _ in range(3):  # Create 3 variations of each
                post = Post.objects.create(
                    author=random.choice(users),
                    hub=random.choice(hubs),
                    title=title,
                    content=content,
                    post_type=post_type,
                    helpful_count=random.randint(0, 50),
                    is_anonymous=random.random() < 0.1,  # 10% anonymous
                )
                posts.append(post)

        self.stdout.write(f'✅ Created {len(posts)} posts')

        # Create comments
        comment_templates = [
            'This is so helpful, thank you!',
            'I had the same question - following!',
            'Have you tried talking to a career coach? That helped me.',
            'Great resource list. Bookmarking this!',
            'I went through this exact situation. Happy to chat if you want to DM.',
            'Check out XYZ resource - it was a game changer for me.',
            'This is exactly what I needed to hear today.',
        ]

        comments_created = 0
        for post in random.sample(posts, min(50, len(posts))):  # Add comments to 50 random posts
            num_comments = random.randint(1, 5)
            for _ in range(num_comments):
                Comment.objects.create(
                    post=post,
                    author=random.choice(users),
                    content=random.choice(comment_templates),
                    helpful_count=random.randint(0, 20),
                    is_accepted_answer=(random.random() < 0.2 and post.post_type == 'question'),
                )
                comments_created += 1

        self.stdout.write(f'✅ Created {comments_created} comments')

        # Create mentorship requests
        mentors = [u for u in users if u.profile.is_mentor]
        mentees = [u for u in users if not u.profile.is_mentor]

        requests_created = 0
        for mentee in mentees[:5]:  # First 5 non-mentors send requests
            for _ in range(random.randint(1, 2)):
                MentorshipRequest.objects.create(
                    mentee=mentee,
                    mentor=random.choice(mentors),
                    topic=random.choice(['Career transition', 'Technical skills', 'Leadership', 'Work-life balance']),
                    message='Hi! I would love to learn from your experience. Would you be open to a monthly call?',
                    status=random.choice(['pending', 'accepted', 'declined', 'completed']),
                )
                requests_created += 1

        self.stdout.write(f'✅ Created {requests_created} mentorship requests')

        self.stdout.write(self.style.SUCCESS('\n🎉 Database seeded successfully!'))
        self.stdout.write(f'📊 Total: {User.objects.count()} users, {Hub.objects.count()} hubs, '
                          f'{Post.objects.count()} posts, {Comment.objects.count()} comments')