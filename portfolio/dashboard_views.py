import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.text import slugify

from .models import (
    Project,
    ProjectImage,
    BlogPost,
    Category,
    Service,
    Experience,
    Skill,
    Testimonial,
    FAQ,
    ContactMessage,
    SiteSettings,
)
from .forms import ContactForm


def dashboard_index(request):
    projects_count = Project.objects.count()
    blogs_count = BlogPost.objects.count()
    services_count = Service.objects.count()
    testimonials_count = Testimonial.objects.count()
    faqs_count = FAQ.objects.count()
    messages_count = ContactMessage.objects.count()
    unread_messages_count = ContactMessage.objects.filter(is_read=False).count()
    recent_projects = Project.objects.all()[:5]
    recent_messages = ContactMessage.objects.all()[:5]
    site_settings = SiteSettings.get_solo()

    context = {
        "page_title": "Dashboard Overview",
        "active_tab": "overview",
        "projects_count": projects_count,
        "blogs_count": blogs_count,
        "services_count": services_count,
        "testimonials_count": testimonials_count,
        "faqs_count": faqs_count,
        "messages_count": messages_count,
        "unread_messages_count": unread_messages_count,
        "recent_projects": recent_projects,
        "recent_messages": recent_messages,
        "site_settings": site_settings,
    }
    return render(request, "dashboard/index.html", context)


# ==========================================
# PROJECTS CRUD
# ==========================================

def dashboard_projects(request):
    projects = Project.objects.all()
    categories = Category.objects.filter(category_type="project")
    context = {
        "page_title": "Manage Projects",
        "active_tab": "projects",
        "projects": projects,
        "categories": categories,
    }
    return render(request, "dashboard/projects.html", context)


def dashboard_project_create(request):
    categories = Category.objects.filter(category_type="project")
    if request.method == "POST":
        title = request.POST.get("title")
        category_id = request.POST.get("category")
        category = Category.objects.filter(id=category_id).first() if category_id else None
        
        project = Project.objects.create(
            title=title,
            slug=slugify(title),
            category=category,
            tagline=request.POST.get("tagline", ""),
            client=request.POST.get("client", "Studio Client"),
            year=request.POST.get("year", "2025"),
            industry=request.POST.get("industry", "Design & Tech"),
            duration=request.POST.get("duration", "4 weeks"),
            problem=request.POST.get("problem", ""),
            solution=request.POST.get("solution", ""),
            challenge=request.POST.get("challenge", ""),
            summary=request.POST.get("summary", ""),
            is_featured="is_featured" in request.POST,
        )

        if "cover_image" in request.FILES:
            project.cover_image = request.FILES["cover_image"]
            project.save()

        messages.success(request, f"Project '{project.title}' created successfully!")
        return redirect("portfolio:dashboard_projects")

    context = {
        "page_title": "New Project",
        "active_tab": "projects",
        "categories": categories,
        "is_edit": False,
    }
    return render(request, "dashboard/project_form.html", context)


def dashboard_project_edit(request, identifier):
    if str(identifier).isdigit():
        project = Project.objects.filter(pk=identifier).first()
    else:
        project = Project.objects.filter(slug=identifier).first()

    if not project:
        messages.warning(request, f"Project '{identifier}' was not found. It may have been updated or re-seeded. Here is your active projects list.")
        return redirect("portfolio:dashboard_projects")

    categories = Category.objects.filter(category_type="project")

    if request.method == "POST":
        project.title = request.POST.get("title", project.title)
        category_id = request.POST.get("category")
        project.category = Category.objects.filter(id=category_id).first() if category_id else None
        project.tagline = request.POST.get("tagline", project.tagline)
        project.client = request.POST.get("client", project.client)
        project.year = request.POST.get("year", project.year)
        project.industry = request.POST.get("industry", project.industry)
        project.duration = request.POST.get("duration", project.duration)
        project.problem = request.POST.get("problem", project.problem)
        project.solution = request.POST.get("solution", project.solution)
        project.challenge = request.POST.get("challenge", project.challenge)
        project.summary = request.POST.get("summary", project.summary)
        project.is_featured = "is_featured" in request.POST

        if "cover_image" in request.FILES:
            project.cover_image = request.FILES["cover_image"]

        project.save()

        # Direct sync to Framer files without altering any animations
        try:
            from .framer_sync import sync_project_to_framer
            sync_project_to_framer(project)
        except Exception as e:
            print("Sync error:", e)

        messages.success(request, f"Project '{project.title}' updated successfully and synced with Framer!")
        return redirect("portfolio:dashboard_projects")

    context = {
        "page_title": f"Edit {project.title}",
        "active_tab": "projects",
        "project": project,
        "categories": categories,
        "is_edit": True,
    }
    return render(request, "dashboard/project_form.html", context)


@require_POST
def dashboard_project_delete(request, identifier):
    if str(identifier).isdigit():
        project = Project.objects.filter(pk=identifier).first()
    else:
        project = Project.objects.filter(slug=identifier).first()

    if project:
        title = project.title
        project.delete()
        messages.success(request, f"Project '{title}' was deleted.")
    else:
        messages.warning(request, "Project was not found.")
    return redirect("portfolio:dashboard_projects")



# ==========================================
# BLOGS CRUD
# ==========================================

def dashboard_blogs(request):
    blogs = BlogPost.objects.all()
    context = {
        "page_title": "Manage Blog Posts",
        "active_tab": "blogs",
        "blogs": blogs,
    }
    return render(request, "dashboard/blogs.html", context)


def dashboard_blog_create(request):
    categories = Category.objects.filter(category_type="blog")
    if request.method == "POST":
        title = request.POST.get("title")
        category_id = request.POST.get("category")
        category = Category.objects.filter(id=category_id).first() if category_id else None

        blog = BlogPost.objects.create(
            title=title,
            slug=slugify(title),
            category=category,
            author=request.POST.get("author", "DigiPorto"),
            read_time=request.POST.get("read_time", "5 min read"),
            summary=request.POST.get("summary", ""),
            content=request.POST.get("content", ""),
            is_published="is_published" in request.POST,
        )

        if "cover_image" in request.FILES:
            blog.cover_image = request.FILES["cover_image"]
            blog.save()

        messages.success(request, f"Blog post '{blog.title}' created successfully!")
        return redirect("portfolio:dashboard_blogs")

    context = {
        "page_title": "New Blog Post",
        "active_tab": "blogs",
        "categories": categories,
        "is_edit": False,
    }
    return render(request, "dashboard/blog_form.html", context)


def dashboard_blog_edit(request, identifier):
    if str(identifier).isdigit():
        blog = BlogPost.objects.filter(pk=identifier).first()
    else:
        blog = BlogPost.objects.filter(slug=identifier).first()

    if not blog:
        messages.warning(request, f"Article '{identifier}' was not found. Here is your active blog articles list.")
        return redirect("portfolio:dashboard_blogs")

    categories = Category.objects.filter(category_type="blog")

    if request.method == "POST":
        blog.title = request.POST.get("title", blog.title)
        category_id = request.POST.get("category")
        blog.category = Category.objects.filter(id=category_id).first() if category_id else None
        blog.author = request.POST.get("author", blog.author)
        blog.read_time = request.POST.get("read_time", blog.read_time)
        blog.summary = request.POST.get("summary", blog.summary)
        blog.content = request.POST.get("content", blog.content)
        blog.is_published = "is_published" in request.POST

        if "cover_image" in request.FILES:
            blog.cover_image = request.FILES["cover_image"]

        blog.save()
        messages.success(request, f"Blog post '{blog.title}' updated successfully!")
        return redirect("portfolio:dashboard_blogs")

    context = {
        "page_title": f"Edit {blog.title}",
        "active_tab": "blogs",
        "blog": blog,
        "categories": categories,
        "is_edit": True,
    }
    return render(request, "dashboard/blog_form.html", context)


@require_POST
def dashboard_blog_delete(request, identifier):
    if str(identifier).isdigit():
        blog = BlogPost.objects.filter(pk=identifier).first()
    else:
        blog = BlogPost.objects.filter(slug=identifier).first()

    if blog:
        title = blog.title
        blog.delete()
        messages.success(request, f"Blog article '{title}' was deleted.")
    else:
        messages.warning(request, "Article was not found.")
    return redirect("portfolio:dashboard_blogs")



# ==========================================
# ==========================================
# SERVICES CRUD
# ==========================================

def dashboard_services(request):
    site_settings = SiteSettings.get_solo()
    if request.method == "POST" and "update_section_header" in request.POST:
        sub = request.POST.get("services_subtitle", "")
        if sub:
            site_settings.services_subtitle = sub
        if "services_image" in request.FILES:
            site_settings.services_image = request.FILES["services_image"]
        site_settings.save()
        messages.success(request, "Services section subtitle & showcase photo updated successfully!")
        return redirect("portfolio:dashboard_services")

    services = Service.objects.all()
    context = {
        "page_title": "Services & Offerings",
        "active_tab": "services",
        "services": services,
        "site_settings": site_settings,
    }
    return render(request, "dashboard/services.html", context)


def dashboard_service_create(request):
    if request.method == "POST":
        order_num = request.POST.get("order_num", "1.")
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        is_active = "is_active" in request.POST
        order = int(request.POST.get("order", 0) or 0)

        service = Service.objects.create(
            order_num=order_num,
            title=title,
            description=description,
            is_active=is_active,
            order=order,
        )
        messages.success(request, f"Service '{service.title}' created successfully!")
        return redirect("portfolio:dashboard_services")

    context = {
        "page_title": "Add New Service",
        "active_tab": "services",
        "is_edit": False,
    }
    return render(request, "dashboard/service_form.html", context)


def dashboard_service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        service.order_num = request.POST.get("order_num", service.order_num)
        service.title = request.POST.get("title", service.title)
        service.description = request.POST.get("description", service.description)
        service.is_active = "is_active" in request.POST
        service.order = int(request.POST.get("order", service.order) or 0)
        service.save()
        messages.success(request, f"Service '{service.title}' updated successfully!")
        return redirect("portfolio:dashboard_services")

    context = {
        "page_title": f"Edit Service - {service.title}",
        "active_tab": "services",
        "service": service,
        "is_edit": True,
    }
    return render(request, "dashboard/service_form.html", context)


@require_POST
def dashboard_service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    title = service.title
    service.delete()
    messages.success(request, f"Service '{title}' was deleted from UI.")
    return redirect("portfolio:dashboard_services")


# ==========================================
# TESTIMONIALS CRUD
# ==========================================

def dashboard_testimonials(request):
    testimonials = Testimonial.objects.all()
    context = {
        "page_title": "Manage Testimonials",
        "active_tab": "testimonials",
        "testimonials": testimonials,
    }
    return render(request, "dashboard/testimonials.html", context)


def dashboard_testimonial_create(request):
    if request.method == "POST":
        client_name = request.POST.get("client_name", "")
        client_role = request.POST.get("client_role", "")
        client_company = request.POST.get("client_company", "")
        quote = request.POST.get("quote", "")
        is_active = "is_active" in request.POST
        order = int(request.POST.get("order", 0) or 0)

        t = Testimonial.objects.create(
            client_name=client_name,
            client_role=client_role,
            client_company=client_company,
            quote=quote,
            is_active=is_active,
            order=order,
        )
        if "client_avatar" in request.FILES:
            t.client_avatar = request.FILES["client_avatar"]
            t.save()

        messages.success(request, f"Testimonial from '{t.client_name}' created successfully!")
        return redirect("portfolio:dashboard_testimonials")

    context = {
        "page_title": "Add New Testimonial",
        "active_tab": "testimonials",
        "is_edit": False,
    }
    return render(request, "dashboard/testimonial_form.html", context)


def dashboard_testimonial_edit(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == "POST":
        testimonial.client_name = request.POST.get("client_name", testimonial.client_name)
        testimonial.client_role = request.POST.get("client_role", testimonial.client_role)
        testimonial.client_company = request.POST.get("client_company", testimonial.client_company)
        testimonial.quote = request.POST.get("quote", testimonial.quote)
        testimonial.is_active = "is_active" in request.POST
        testimonial.order = int(request.POST.get("order", testimonial.order) or 0)

        if "client_avatar" in request.FILES:
            testimonial.client_avatar = request.FILES["client_avatar"]

        testimonial.save()
        messages.success(request, f"Testimonial for '{testimonial.client_name}' updated successfully!")
        return redirect("portfolio:dashboard_testimonials")

    context = {
        "page_title": f"Edit Testimonial - {testimonial.client_name}",
        "active_tab": "testimonials",
        "testimonial": testimonial,
        "is_edit": True,
    }
    return render(request, "dashboard/testimonial_form.html", context)


@require_POST
def dashboard_testimonial_delete(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    name = testimonial.client_name
    testimonial.delete()
    messages.success(request, f"Testimonial by '{name}' was deleted from UI.")
    return redirect("portfolio:dashboard_testimonials")


# ==========================================
# FAQS CRUD
# ==========================================

def dashboard_faqs(request):
    faqs = FAQ.objects.all()
    context = {
        "page_title": "Manage FAQs",
        "active_tab": "faqs",
        "faqs": faqs,
    }
    return render(request, "dashboard/faqs.html", context)


def dashboard_faq_create(request):
    if request.method == "POST":
        order_num = request.POST.get("order_num", "1.")
        question = request.POST.get("question", "")
        answer = request.POST.get("answer", "")
        is_active = "is_active" in request.POST
        order = int(request.POST.get("order", 0) or 0)

        faq = FAQ.objects.create(
            order_num=order_num,
            question=question,
            answer=answer,
            is_active=is_active,
            order=order,
        )
        messages.success(request, f"FAQ '{faq.question}' created successfully!")
        return redirect("portfolio:dashboard_faqs")

    context = {
        "page_title": "Add New FAQ",
        "active_tab": "faqs",
        "is_edit": False,
    }
    return render(request, "dashboard/faq_form.html", context)


def dashboard_faq_edit(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    if request.method == "POST":
        faq.order_num = request.POST.get("order_num", faq.order_num)
        faq.question = request.POST.get("question", faq.question)
        faq.answer = request.POST.get("answer", faq.answer)
        faq.is_active = "is_active" in request.POST
        faq.order = int(request.POST.get("order", faq.order) or 0)
        faq.save()
        messages.success(request, f"FAQ '{faq.question}' updated successfully!")
        return redirect("portfolio:dashboard_faqs")

    context = {
        "page_title": f"Edit FAQ",
        "active_tab": "faqs",
        "faq": faq,
        "is_edit": True,
    }
    return render(request, "dashboard/faq_form.html", context)


@require_POST
def dashboard_faq_delete(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    q = faq.question
    faq.delete()
    messages.success(request, f"FAQ '{q}' was deleted from UI.")
    return redirect("portfolio:dashboard_faqs")


# ==========================================
# SETTINGS & INQUIRIES
# ==========================================

def dashboard_settings(request):
    settings_obj = SiteSettings.get_solo()

    if request.method == "POST":
        settings_obj.site_title = request.POST.get("site_title", settings_obj.site_title)
        settings_obj.designer_name = request.POST.get("designer_name", settings_obj.designer_name)
        settings_obj.tagline = request.POST.get("tagline", settings_obj.tagline)
        settings_obj.hero_role_1 = request.POST.get("hero_role_1", settings_obj.hero_role_1)
        settings_obj.hero_role_2 = request.POST.get("hero_role_2", settings_obj.hero_role_2)
        settings_obj.hero_headline = request.POST.get("hero_headline", settings_obj.hero_headline)
        settings_obj.hero_subheadline = request.POST.get("hero_subheadline", settings_obj.hero_subheadline)
        settings_obj.about_text = request.POST.get("about_text", settings_obj.about_text)
        settings_obj.bio = request.POST.get("bio", settings_obj.bio)

        # Stats
        settings_obj.stat_experience_num = request.POST.get("stat_experience_num", settings_obj.stat_experience_num)
        settings_obj.stat_experience_label = request.POST.get("stat_experience_label", settings_obj.stat_experience_label)
        settings_obj.stat_projects_num = request.POST.get("stat_projects_num", settings_obj.stat_projects_num)
        settings_obj.stat_projects_label = request.POST.get("stat_projects_label", settings_obj.stat_projects_label)
        settings_obj.stat_clients_num = request.POST.get("stat_clients_num", settings_obj.stat_clients_num)
        settings_obj.stat_clients_label = request.POST.get("stat_clients_label", settings_obj.stat_clients_label)
        settings_obj.stat_satisfaction_num = request.POST.get("stat_satisfaction_num", settings_obj.stat_satisfaction_num)
        settings_obj.stat_growth_num = request.POST.get("stat_growth_num", settings_obj.stat_growth_num)

        # Subtitles
        settings_obj.services_subtitle = request.POST.get("services_subtitle", settings_obj.services_subtitle)
        settings_obj.projects_subtitle = request.POST.get("projects_subtitle", settings_obj.projects_subtitle)
        settings_obj.testimonials_subtitle = request.POST.get("testimonials_subtitle", settings_obj.testimonials_subtitle)
        settings_obj.faq_subtitle = request.POST.get("faq_subtitle", settings_obj.faq_subtitle)
        settings_obj.blogs_subtitle = request.POST.get("blogs_subtitle", settings_obj.blogs_subtitle)
        settings_obj.contact_title = request.POST.get("contact_title", settings_obj.contact_title)
        settings_obj.contact_subtitle = request.POST.get("contact_subtitle", settings_obj.contact_subtitle)

        # Contact & Socials
        settings_obj.email = request.POST.get("email", settings_obj.email)
        settings_obj.phone = request.POST.get("phone", settings_obj.phone)
        settings_obj.location = request.POST.get("location", settings_obj.location)
        settings_obj.availability_status = request.POST.get("availability_status", settings_obj.availability_status)
        settings_obj.behance_url = request.POST.get("behance_url", "")
        settings_obj.dribbble_url = request.POST.get("dribbble_url", "")
        settings_obj.twitter_url = request.POST.get("twitter_url", "")
        settings_obj.instagram_url = request.POST.get("instagram_url", "")
        settings_obj.linkedin_url = request.POST.get("linkedin_url", "")
        settings_obj.github_url = request.POST.get("github_url", "")
        settings_obj.copyright_text = request.POST.get("copyright_text", settings_obj.copyright_text)

        if "avatar_image" in request.FILES:
            settings_obj.avatar_image = request.FILES["avatar_image"]

        if "services_image" in request.FILES:
            settings_obj.services_image = request.FILES["services_image"]

        if "resume_file" in request.FILES:
            settings_obj.resume_file = request.FILES["resume_file"]

        settings_obj.save()

        # Direct sync to Framer files without altering any animations
        try:
            from .framer_sync import sync_site_settings_to_framer
            sync_site_settings_to_framer(settings_obj)
        except Exception as e:
            print("Sync error:", e)

        messages.success(request, "Site settings updated successfully and synced with Framer frontend!")
        return redirect("portfolio:dashboard_settings")

    context = {
        "page_title": "Site & Profile Settings",
        "active_tab": "settings",
        "settings": settings_obj,
    }
    return render(request, "dashboard/settings.html", context)


def dashboard_messages(request):
    contact_messages = ContactMessage.objects.all()
    context = {
        "page_title": "Client Inquiries",
        "active_tab": "messages",
        "contact_messages": contact_messages,
    }
    return render(request, "dashboard/messages.html", context)


@require_POST
def dashboard_message_toggle_read(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.is_read = not msg.is_read
    msg.save()
    status_str = "read" if msg.is_read else "unread"
    messages.success(request, f"Marked message as {status_str}.")
    return redirect("portfolio:dashboard_messages")


@require_POST
def dashboard_message_delete(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.delete()
    messages.success(request, "Message deleted.")
    return redirect("portfolio:dashboard_messages")
