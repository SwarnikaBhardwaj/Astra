# Astra - For women, by women 

A Django web application that empowers women through knowledge sharing, mentorship, and community building. Meant to be a safe space for them to share experiences, stories, advice and support each other in a world that doesn't support them.

## What is this?

Astra is basically a platform where women can:
- Share knowledge through posts (tutorials, stories, resources, questions)
- Join topic-based communities called "hubs" (STEM, entrepreneurship, health, etc.)
- Find and connect with mentors
- Build their portfolio and track their contributions

The whole design is a royal blue and gold theme - meant to feel powerful and welcoming at the same time. Also inspired by the Indian 'astra' or weapon indicating there's a warrior inside every woman. 

## Live Links

Deployed Site: https://astra-ubml.onrender.com

## Test It Out

You can log in with these accounts:

**Staff account** (can see everything including analytics):
- Username: mohitg2
- Password: graingerlibrary

**Regular user account**:
- Username: infoadmins
- Password: uiucinfo

**Other sample accounts** (password is demo1234 for all):
- sarah_mentor (she's a mentor in STEM)
- alex_learner (regular user)
- priya_dev (another mentor)

## Main Features

### Community Hubs
There are 7 different hubs you can join for now - STEM, Entrepreneurship, Health, Legal Rights, Caregiving, Creative Arts, and Leadership. Each one has its own posts and community.

### Posts and Comments
You can create different types of posts (questions, tutorials, stories, resources). Other users can comment, and you can mark posts as "helpful" which increases the author's reputation.

### Mentorship System
If you're a mentor people can send you mentorship requests. You can accept or decline them. There's a whole dashboard to manage this.

### User Profiles
Every user has a profile showing their bio, skills, badges, and all their posts. You can also download your portfolio as a CSV file.

### Analytics Dashboard
If you're staff there's an analytics page with interactive charts showing platform stats - things like posts per hub, top skills, mentorship request statuses, etc.

### Privacy Options
You can post anonymously if you want and there are different visibility settings for your profile.

## Tech Stack

- Django 5.0 (Python web framework)
- Bootstrap 5 (for the UI)
- Vega-Lite (for interactive charts)
- Matplotlib (for additional charts)
- SQLite database (can switch to PostgreSQL easily)

## Running It Locally

If you want to run this on your own computer:

1. Clone it
```bash
clone repository
cd Astra
```

2. Make a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install stuff
```bash
pip install -r requirements.txt
```

4. Set up the database
```bash
python manage.py migrate
```

5. Load sample data
```bash
python manage.py seed_data
```

6. Run it
```bash
python manage.py runserver
```

Then go to http://127.0.0.1:8000

## What I Built (Requirements Met)

### Required Stuff (Table 1 - 15 points)
- Set up the whole Django project with proper structure
- Made wireframes and documented the UI design
- Created 7 database models with relationships
- Built 20+ views and templates
- Implemented user authentication (login, signup, logout)
- Deployed it to a live server

### Add-On Features (Table 2 - did 7 out of required 5)
- Complex database queries with aggregations
- Custom CSS styling with Bootstrap
- Interactive Vega-Lite charts
- Full CRUD operations (create, read, update, delete)
- JSON API endpoints for future mobile app
- CSV export functionality
- Public user registration system

### Bonus Stuff
- Matplotlib chart showing post trends
- Complete mentorship matching system
- Voting system for helpful content
- Anonymous posting
- Skills and badges system


## Project Structure
```
astra-women-platform/
├── Astra/              # Django project settings
├── core/               # Main app with all the features
│   ├── models.py      # Database models
│   ├── views.py       # Page logic
│   ├── forms.py       # Forms for user input
│   ├── templates/     # HTML templates
│   └── static/        # CSS and other static files
├── api/                # JSON API endpoints
├── docs/               # Documentation and screenshots
├── manage.py          # Django management script
└── README.md          # This file
```

## Documentation

- Wireframes and design docs: `docs/wireframes.md`
- Full feature list: `docs/topics_summary.pdf`
- Project reflection: `docs/final.txt`
- Screenshots: `docs/screenshots/`

## Design Philosophy

The whole look is meant to be royal and powerful but still welcoming with deep blue and gold accents. Inspired by Indian goddesses and mandala art. No unnecessary animations or playful stuff - kept it serious and professional.

Used proper fonts (Crimson Text for headings, Montserrat for body text) and made sure everything has good contrast for accessibility.

## Future Ideas

If I keep working on this:
- Add real-time notifications
- Email alerts for mentorship stuff
- Search functionality
- Integration with external APIs
- Mobile app using the JSON endpoints
- Video upload for tutorial posts
- Two-factor authentication

## Contact

Swarnika Bhardwaj
sb113@illinois.edu

---

Built as a capstone project. December 2025.

#Fuelscrolling