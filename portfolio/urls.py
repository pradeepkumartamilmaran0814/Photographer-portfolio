from django.urls import path
from . import views
from . import framer_views
from . import dashboard_views

app_name = "portfolio"

urlpatterns = [
    # ==========================================
    # EXACT FRAMER FRONTEND (DYNAMICALLY SERVED)
    # ==========================================
    path("", framer_views.framer_home_view, name="framer_home"),
    path("about/", framer_views.framer_about_view, name="framer_about"),
    path("projects/", framer_views.framer_projects_view, name="framer_projects"),
    path("projects/<slug:slug>/", framer_views.framer_project_detail_view, name="framer_project_detail"),
    path("blogs/", framer_views.framer_blogs_view, name="framer_blogs"),
    path("blogs/<slug:slug>/", framer_views.framer_blog_detail_view, name="framer_blog_detail"),

    # Direct .html compatibility (for original Framer links)
    path("index.html", framer_views.framer_home_view),
    path("about.html", framer_views.framer_about_view),
    path("projects.html", framer_views.framer_projects_view),
    path("blogs.html", framer_views.framer_blogs_view),
    path("projects/<slug:slug>.html", framer_views.framer_project_detail_view),
    path("blogs/<slug:slug>.html", framer_views.framer_blog_detail_view),

    # ==========================================
    # BACKEND DASHBOARD GUI (PAGE-BY-PAGE EDITORS)
    # ==========================================
    path("dashboard/", dashboard_views.dashboard_index, name="dashboard_index"),
    path("dashboard/page/home/", dashboard_views.dashboard_page_home, name="dashboard_page_home"),
    path("dashboard/page/about/", dashboard_views.dashboard_page_about, name="dashboard_page_about"),
    path("dashboard/page/about/experiences/new/", dashboard_views.dashboard_experience_create, name="dashboard_experience_create"),
    path("dashboard/page/about/experiences/<int:pk>/edit/", dashboard_views.dashboard_experience_edit, name="dashboard_experience_edit"),
    path("dashboard/page/about/experiences/<int:pk>/delete/", dashboard_views.dashboard_experience_delete, name="dashboard_experience_delete"),

    path("dashboard/projects/", dashboard_views.dashboard_projects, name="dashboard_projects"),
    path("dashboard/projects/new/", dashboard_views.dashboard_project_create, name="dashboard_project_create"),
    path("dashboard/projects/<str:identifier>/edit/", dashboard_views.dashboard_project_edit, name="dashboard_project_edit"),
    path("dashboard/projects/<str:identifier>/delete/", dashboard_views.dashboard_project_delete, name="dashboard_project_delete"),
    
    path("dashboard/blogs/", dashboard_views.dashboard_blogs, name="dashboard_blogs"),
    path("dashboard/blogs/new/", dashboard_views.dashboard_blog_create, name="dashboard_blog_create"),
    path("dashboard/blogs/<str:identifier>/edit/", dashboard_views.dashboard_blog_edit, name="dashboard_blog_edit"),
    path("dashboard/blogs/<str:identifier>/delete/", dashboard_views.dashboard_blog_delete, name="dashboard_blog_delete"),

    path("dashboard/settings/", dashboard_views.dashboard_settings, name="dashboard_settings"),
    
    path("dashboard/services/", dashboard_views.dashboard_services, name="dashboard_services"),
    path("dashboard/services/new/", dashboard_views.dashboard_service_create, name="dashboard_service_create"),
    path("dashboard/services/<int:pk>/edit/", dashboard_views.dashboard_service_edit, name="dashboard_service_edit"),
    path("dashboard/services/<int:pk>/delete/", dashboard_views.dashboard_service_delete, name="dashboard_service_delete"),

    path("dashboard/testimonials/", dashboard_views.dashboard_testimonials, name="dashboard_testimonials"),
    path("dashboard/testimonials/new/", dashboard_views.dashboard_testimonial_create, name="dashboard_testimonial_create"),
    path("dashboard/testimonials/<int:pk>/edit/", dashboard_views.dashboard_testimonial_edit, name="dashboard_testimonial_edit"),
    path("dashboard/testimonials/<int:pk>/delete/", dashboard_views.dashboard_testimonial_delete, name="dashboard_testimonial_delete"),

    path("dashboard/faqs/", dashboard_views.dashboard_faqs, name="dashboard_faqs"),
    path("dashboard/faqs/new/", dashboard_views.dashboard_faq_create, name="dashboard_faq_create"),
    path("dashboard/faqs/<int:pk>/edit/", dashboard_views.dashboard_faq_edit, name="dashboard_faq_edit"),
    path("dashboard/faqs/<int:pk>/delete/", dashboard_views.dashboard_faq_delete, name="dashboard_faq_delete"),

    path("dashboard/messages/", dashboard_views.dashboard_messages, name="dashboard_messages"),
    path("dashboard/messages/<int:pk>/toggle/", dashboard_views.dashboard_message_toggle_read, name="dashboard_message_toggle_read"),
    path("dashboard/messages/<int:pk>/delete/", dashboard_views.dashboard_message_delete, name="dashboard_message_delete"),

    # Form Submissions
    path("contact/submit/", views.contact_submit_view, name="contact_submit"),
    path("newsletter/subscribe/", views.newsletter_subscribe_view, name="newsletter_subscribe"),

    # REST APIs
    path("api/projects/", views.ProjectListAPI.as_view(), name="api_projects"),
    path("api/projects/<slug:slug>/", views.ProjectDetailAPI.as_view(), name="api_project_detail"),
    path("api/blogs/", views.BlogListAPI.as_view(), name="api_blogs"),
    path("api/blogs/<slug:slug>/", views.BlogDetailAPI.as_view(), name="api_blog_detail"),
    path("api/contact/", views.ContactSubmitAPI.as_view(), name="api_contact"),
    path("api/newsletter/", views.NewsletterSubscribeAPI.as_view(), name="api_newsletter"),
    path("api/settings/", views.SiteSettingsAPI.as_view(), name="api_settings"),
]
