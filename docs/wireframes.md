# Astra - UI/UX Planning & Wireframes

## Project Vision
Astra is a safe social platform for women to learn, connect, and rise together. 
Design inspired by Indian goddesses - powerful, divine, yet welcoming.

## Color Palette
- Dark Azure
- Golden Orange (specks of it to symbolise the colour of astra)
- White

## User Flows

### 1. New User Journey
```
Landing → Signup → Auto-login → Home Feed → Browse Hubs → Join Hub → Create Post
```

### 2. Returning User Journey
```
Login → Home Feed (personalized) → comment on posts → request mentorship → export portfolio
```

### 3. Mentor Journey
```
Login → Mentorship Dashboard → Review Requests → Accept/Decline → Engage with Mentees
```

### 4. Staff Admin Journey
```
Login → Analytics Dashboard → View Charts → Monitor Platform Health → Admin Panel
```

## Page Layouts

### Login/Signup Pages
- Centered card design
- Dark background with gold accents
- Clean form fields with validation
- "Join Us" CTA prominently displayed

### Home Feed
- Left: Main content area with posts
- Right: Sidebar with hub directory and user stats
- Top: Navigation bar with user menu
- Posts display: Hub badge, title, excerpt, author, helpful count

### Hub Detail
- Header: Hub icon, name, description, member/post count
- Join/Leave button (gold accent)
- Posts list with filtering options
- "Create Post" button for members

### Post Detail
- Full post content with formatting
- Author information (respects anonymity settings)
- "Mark as Helpful" button with count
- Comments section with nested replies
- Edit/Delete for post author

### Profile Page
- Left sidebar: Avatar, bio, stats, skills, badges
- Main area: Recent posts grid
- Action buttons: Edit Profile, Export Portfolio CSV
- "Request Mentorship" for mentor profiles

### Analytics Dashboard (Staff Only)
- 4 stat cards: Users, Posts, Comments, Hubs
- Interactive Vega-Lite charts (3 charts)
- Matplotlib trend chart
- API endpoints reference table

## Design Principles

1. **Royal & Serious:** No playful animations, professional fonts
2  **Gold Accents:** Borders, icons, highlights for emphasis
3 **Accessibility:** High contrast, readable fonts, clear navigation
4 **Mobile Responsive:** Bootstrap grid system ensures mobile compatibility

## Screenshots
See `/docs/screenshots/` folder for actual implementation.
```
