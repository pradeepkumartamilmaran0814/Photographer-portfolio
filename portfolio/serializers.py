from rest_framework import serializers
from .models import (
    Category,
    Project,
    ProjectImage,
    BlogPost,
    Service,
    Experience,
    Skill,
    Testimonial,
    ContactMessage,
    NewsletterSubscriber,
    SiteSettings,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "category_type"]


class ProjectImageSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField()

    class Meta:
        model = ProjectImage
        fields = ["id", "image_url", "caption", "order"]


class ProjectSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    cover_url = serializers.ReadOnlyField()
    gallery_images = ProjectImageSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "slug",
            "category",
            "category_name",
            "tagline",
            "short_description",
            "client",
            "year",
            "industry",
            "duration",
            "cover_url",
            "problem",
            "solution",
            "challenge",
            "summary",
            "live_link",
            "is_featured",
            "order",
            "gallery_images",
            "created_at",
        ]


class BlogPostSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    cover_url = serializers.ReadOnlyField()

    class Meta:
        model = BlogPost
        fields = [
            "id",
            "title",
            "slug",
            "category",
            "category_name",
            "summary",
            "content",
            "cover_url",
            "author",
            "read_time",
            "published_date",
            "is_featured",
            "created_at",
        ]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "order_num", "title", "description", "order"]


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ["id", "name", "email", "subject", "message", "created_at"]
        read_only_fields = ["id", "created_at"]


class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ["id", "email", "subscribed_at"]
        read_only_fields = ["id", "subscribed_at"]


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = "__all__"
