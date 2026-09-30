from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category,
    Project,
    ProjectImage,
    BlogPost,
    Service,
    Experience,
    Skill,
    Testimonial,
    FAQ,
    ContactMessage,
    NewsletterSubscriber,
    SiteSettings,
)


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 2
    fields = ("image", "image_static", "caption", "order")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category_type", "slug")
    list_filter = ("category_type",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("cover_preview", "title", "category", "year", "client", "is_featured", "order")
    list_display_links = ("title",)
    list_filter = ("category", "is_featured", "year")
    search_fields = ("title", "client", "problem", "solution")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_featured", "order")
    inlines = [ProjectImageInline]

    def cover_preview(self, obj):
        url = obj.cover_url
        if url:
            return format_html('<img src="{}" style="width: 50px; height: 35px; object-fit: cover; border-radius: 4px;" />', url)
        return "-"
    cover_preview.short_description = "Cover"


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("cover_preview", "title", "category", "published_date", "author", "is_published", "is_featured")
    list_display_links = ("title",)
    list_filter = ("category", "is_published", "is_featured", "published_date")
    search_fields = ("title", "summary", "content")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_published", "is_featured")

    def cover_preview(self, obj):
        url = obj.cover_url
        if url:
            return format_html('<img src="{}" style="width: 50px; height: 35px; object-fit: cover; border-radius: 4px;" />', url)
        return "-"
    cover_preview.short_description = "Cover"


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("order_num", "title", "is_active", "order")
    list_editable = ("is_active", "order")
    search_fields = ("title", "description")


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "company", "period", "order")
    list_editable = ("order",)
    search_fields = ("role", "company")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "proficiency", "order")
    list_editable = ("proficiency", "order")
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("client_name", "client_role", "client_company", "is_active", "order")
    list_editable = ("is_active", "order")
    search_fields = ("client_name", "client_company", "quote")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("order_num", "question", "is_active", "order")
    list_editable = ("is_active", "order")
    search_fields = ("question", "answer")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    list_editable = ("is_read",)
    readonly_fields = ("created_at",)


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "subscribed_at", "is_active")
    list_filter = ("is_active", "subscribed_at")
    search_fields = ("email",)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Site & Profile", {
            "fields": ("site_title", "designer_name", "tagline", "hero_headline", "hero_subheadline", "bio", "resume_file")
        }),
        ("Contact & Location", {
            "fields": ("email", "phone", "location", "availability_status")
        }),
        ("Social Links", {
            "fields": ("dribbble_url", "twitter_url", "instagram_url", "linkedin_url", "github_url")
        }),
    )

    def has_add_permission(self, request):
        # Only allow 1 instance of settings
        return not SiteSettings.objects.exists()
