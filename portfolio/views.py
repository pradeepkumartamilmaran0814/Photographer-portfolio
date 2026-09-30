from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from rest_framework import generics, status
from rest_framework.response import Response

from .models import (
    Category,
    Project,
    BlogPost,
    Service,
    Experience,
    Skill,
    Testimonial,
    ContactMessage,
    NewsletterSubscriber,
    SiteSettings,
)
from .forms import ContactForm, NewsletterForm
from .serializers import (
    ProjectSerializer,
    BlogPostSerializer,
    CategorySerializer,
    ContactMessageSerializer,
    NewsletterSubscriberSerializer,
    SiteSettingsSerializer,
)


# ==========================================
# TEMPLATE VIEWS (FULL-STACK FRONTEND)
# ==========================================

def home_view(request):
    featured_projects = Project.objects.filter(is_featured=True)[:6]
    all_projects = Project.objects.all()[:8]
    services = Service.objects.filter(is_active=True)
    featured_blogs = BlogPost.objects.filter(is_published=True)[:2]
    testimonials = Testimonial.objects.filter(is_active=True)[:3]
    categories = Category.objects.filter(category_type="project")
    contact_form = ContactForm()
    newsletter_form = NewsletterForm()

    context = {
        "page_title": "Home",
        "featured_projects": featured_projects,
        "all_projects": all_projects,
        "services": services,
        "featured_blogs": featured_blogs,
        "testimonials": testimonials,
        "categories": categories,
        "contact_form": contact_form,
        "newsletter_form": newsletter_form,
    }
    return render(request, "portfolio/index.html", context)


def about_view(request):
    experiences = Experience.objects.all()
    skills = Skill.objects.all()
    testimonials = Testimonial.objects.filter(is_active=True)
    services = Service.objects.filter(is_active=True)
    contact_form = ContactForm()

    context = {
        "page_title": "About",
        "experiences": experiences,
        "skills": skills,
        "testimonials": testimonials,
        "services": services,
        "contact_form": contact_form,
    }
    return render(request, "portfolio/about.html", context)


def projects_list_view(request):
    category_slug = request.GET.get("category")
    projects = Project.objects.all()
    categories = Category.objects.filter(category_type="project")
    active_category = None

    if category_slug and category_slug != "all":
        try:
            active_category = Category.objects.get(slug=category_slug)
            projects = projects.filter(category=active_category)
        except Category.DoesNotExist:
            active_category = None

    context = {
        "page_title": "Projects",
        "projects": projects,
        "categories": categories,
        "active_category": active_category,
        "active_slug": category_slug or "all",
    }
    return render(request, "portfolio/projects.html", context)


def project_detail_view(request, slug):
    project = get_object_or_404(Project, slug=slug)
    related_projects = Project.objects.exclude(id=project.id)[:4]
    contact_form = ContactForm()

    context = {
        "page_title": project.title,
        "project": project,
        "related_projects": related_projects,
        "contact_form": contact_form,
    }
    return render(request, "portfolio/project_detail.html", context)


def blogs_list_view(request):
    category_slug = request.GET.get("category")
    blogs = BlogPost.objects.filter(is_published=True)
    categories = Category.objects.filter(category_type="blog")
    active_category = None

    if category_slug and category_slug != "all":
        try:
            active_category = Category.objects.get(slug=category_slug)
            blogs = blogs.filter(category=active_category)
        except Category.DoesNotExist:
            active_category = None

    newsletter_form = NewsletterForm()

    context = {
        "page_title": "Blogs",
        "blogs": blogs,
        "categories": categories,
        "active_category": active_category,
        "active_slug": category_slug or "all",
        "newsletter_form": newsletter_form,
    }
    return render(request, "portfolio/blogs.html", context)



def blog_detail_view(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug, is_published=True)
    related_blogs = BlogPost.objects.filter(is_published=True).exclude(id=blog.id)[:3]
    newsletter_form = NewsletterForm()

    # Split content into paragraphs for clean typography
    paragraphs = [p.strip() for p in blog.content.split("\n\n") if p.strip()]

    context = {
        "page_title": blog.title,
        "blog": blog,
        "paragraphs": paragraphs,
        "related_blogs": related_blogs,
        "newsletter_form": newsletter_form,
    }
    return render(request, "portfolio/blog_detail.html", context)


@require_POST
def contact_submit_view(request):
    form = ContactForm(request.POST)
    is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest" or request.content_type == "application/json"

    if form.is_valid():
        msg = form.save()
        success_msg = "Thank you! Your message has been sent successfully. I will get back to you shortly."
        if is_ajax:
            return JsonResponse({"status": "success", "message": success_msg, "id": msg.id})
        messages.success(request, success_msg)
        return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        err_msg = "Please check the form fields and try again."
        if is_ajax:
            return JsonResponse({"status": "error", "message": err_msg, "errors": form.errors}, status=400)
        messages.error(request, err_msg)
        return redirect(request.META.get("HTTP_REFERER", "/"))


@require_POST
def newsletter_subscribe_view(request):
    form = NewsletterForm(request.POST)
    is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest" or request.content_type == "application/json"

    if form.is_valid():
        email = form.cleaned_data["email"]
        sub, created = NewsletterSubscriber.objects.get_or_create(email=email)
        success_msg = "You are now subscribed to the newsletter!" if created else "You are already subscribed!"
        if is_ajax:
            return JsonResponse({"status": "success", "message": success_msg})
        messages.success(request, success_msg)
        return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        err_msg = "Please provide a valid email address."
        if is_ajax:
            return JsonResponse({"status": "error", "message": err_msg, "errors": form.errors}, status=400)
        messages.error(request, err_msg)
        return redirect(request.META.get("HTTP_REFERER", "/"))


# ==========================================
# REST API VIEWS (FOR EXTERNAL / HEADLESS APPS)
# ==========================================

class ProjectListAPI(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get("category")
        featured = self.request.query_params.get("featured")
        if category:
            qs = qs.filter(category__slug=category)
        if featured is not None:
            qs = qs.filter(is_featured=(featured.lower() == "true"))
        return qs


class ProjectDetailAPI(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = "slug"


class BlogListAPI(generics.ListCreateAPIView):
    queryset = BlogPost.objects.filter(is_published=True)
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category__slug=category)
        return qs


class BlogDetailAPI(generics.RetrieveAPIView):
    queryset = BlogPost.objects.filter(is_published=True)
    serializer_class = BlogPostSerializer
    lookup_field = "slug"


class ContactSubmitAPI(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer


class NewsletterSubscribeAPI(generics.CreateAPIView):
    queryset = NewsletterSubscriber.objects.all()
    serializer_class = NewsletterSubscriberSerializer


class SiteSettingsAPI(generics.RetrieveAPIView):
    serializer_class = SiteSettingsSerializer

    def get_object(self):
        return SiteSettings.get_solo()
