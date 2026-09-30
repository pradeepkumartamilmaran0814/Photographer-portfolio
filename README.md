# Portavia Portfolio - Django Backend & Dynamic Frontend

This project transforms the static Framer portfolio (`portavia.framer.website`) into a dynamic, production-ready **Python Django** full-stack web application with complete **Django Admin CMS** support and **REST API** endpoints.

---

## 🚀 Quick Start

The Django server is already running at:
- **Exact Framer Live Frontend**: [http://localhost:8000/](http://localhost:8000/)
- **Visual Backend Dashboard GUI**: [http://localhost:8000/dashboard/](http://localhost:8000/dashboard/)
- **Django Low-Level Admin**: [http://localhost:8000/admin/](http://localhost:8000/admin/)
  - **Username**: `admin`
  - **Password**: `admin123`

---

## 🎨 Backend Dashboard GUI Features (`/dashboard/`)

A dedicated, modern visual control panel designed to update your Framer site without writing code:
- **📊 Overview**: Quick metrics for projects, blogs, inquiries, and designer availability status.
- **📁 Projects Manager (`/dashboard/projects/`)**:
  - Add, edit, or delete projects with live image previews and upload support.
  - Case study breakdowns (Problem, Solution, Challenge, Summary, Client, Year, Duration).
- **📝 Blog Articles Manager (`/dashboard/blogs/`)**:
  - Add, edit, and publish articles with cover image upload and formatted content.
- **⚙️ Site & Profile Settings (`/dashboard/settings/`)**:
  - Update designer name, headlines, bio, email, phone, location, social links, and downloadable resume.
- **💬 Client Inquiries (`/dashboard/messages/`)**:
  - View contact form messages submitted by visitors, mark as read/unread, or delete.


---

## 🛠 Features Implemented

1. **Full-Stack Dynamic Views & Templates**:
   - `GET /` — Home page with Hero, Services, Featured Projects, About Preview, Endorsements, and Latest Articles.
   - `GET /about/` — Biography, Work Experience Timeline, Skills & Competencies with animated progress bars, and Testimonials.
   - `GET /projects/` — Complete portfolio archive with **dynamic category filtering** (UI/UX, Graphic Design, Web Design, Branding).
   - `GET /projects/<slug>/` — In-depth Case Study page with Client, Year, Duration, Problem Statement, Design Solution, Challenges, Impact Summary, Gallery Images, and Recommended Case Studies.
   - `GET /blogs/` — Design Insights & Articles archive with category filtering.
   - `GET /blogs/<slug>/` — Full blog article page with formatted typography, author/date metadata, newsletter box, and related articles.

2. **Interactive Database-Backed Forms**:
   - **Contact Form** (`POST /contact/submit/`): Submits client project inquiries via AJAX with real-time toast feedback and saves directly into the database (`ContactMessage` model).
   - **Newsletter Form** (`POST /newsletter/subscribe/`): Allows users to subscribe to monthly design updates and stores subscriber emails (`NewsletterSubscriber` model).

3. **REST API Endpoints**:
   - `GET /api/projects/` & `GET /api/projects/<slug>/`
   - `GET /api/blogs/` & `GET /api/blogs/<slug>/`
   - `POST /api/contact/` (AJAX/External API contact submissions)
   - `POST /api/newsletter/` (Newsletter subscriptions)
   - `GET /api/settings/` (Site configuration and designer profile)

4. **Django Admin Panel (`/admin/`)**:
   - Manage Projects, Blog Posts, Services, Experiences, Skills, Testimonials, Inquiries, and Site Settings.
   - Image upload support with automatic fallbacks for bundled static images.

---

## 📁 Project Architecture

```
d:\ASAP\design-port\
├── manage.py                          # Django management script
├── db.sqlite3                         # SQLite database with seeded data
├── core/                              # Project root settings & URL routing
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── portfolio/                         # Portfolio application
│   ├── models.py                      # Data models (Project, BlogPost, Service, etc.)
│   ├── views.py                       # Template views & REST API endpoints
│   ├── admin.py                       # Custom Django Admin configuration
│   ├── serializers.py                 # DRF serializers
│   ├── forms.py                       # Contact & Newsletter forms
│   ├── context_processors.py          # Global site settings processor
│   └── management/commands/           # Data seeder command (`seed_portfolio`)
├── templates/                         # HTML templates
│   ├── base.html                      # Glassmorphic header, footer, contact section
│   └── portfolio/
│       ├── index.html                 # Home page
│       ├── about.html                 # About page
│       ├── projects.html              # Projects catalog
│       ├── project_detail.html        # Case study detail
│       ├── blogs.html                 # Blog archive
│       └── blog_detail.html           # Blog post detail
├── static/                            # Static assets
│   ├── css/portavia-theme.css         # Clean theme styling matching Framer design
│   ├── js/main.js                     # AJAX form handling & mobile navigation
│   └── images/                        # All 92 bundled assets from Framer export
└── media/                             # User-uploaded files from Django admin
```

---

## 💻 Manual Commands

- **Run Dev Server**:
  ```bash
  python manage.py runserver
  ```
- **Re-seed Initial Data**:
  ```bash
  python manage.py seed_portfolio
  ```
- **Run Backend Tests**:
  ```bash
  python test_backend.py
  ```
