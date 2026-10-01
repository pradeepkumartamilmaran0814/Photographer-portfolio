from django.db import models
from django.utils.text import slugify
from django.utils import timezone


class Category(models.Model):
    TYPE_CHOICES = (
        ("project", "Project Category"),
        ("blog", "Blog Category"),
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    category_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="project")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="projects")
    tagline = models.CharField(max_length=300, blank=True)
    short_description = models.TextField(blank=True)
    client = models.CharField(max_length=150, blank=True, default="Studio Prism")
    year = models.CharField(max_length=20, default="2025")
    industry = models.CharField(max_length=100, blank=True, default="Tech")
    duration = models.CharField(max_length=50, blank=True, default="4 weeks")
    
    # Hero Cover Image
    cover_image = models.ImageField(upload_to="projects/", blank=True, null=True)
    cover_image_static = models.CharField(max_length=255, blank=True, help_text="Static hash or filename")
    
    # Case study sections (Matching project.pdf exactly)
    problem = models.TextField(blank=True)
    problem_image = models.ImageField(upload_to="projects/case_study/", blank=True, null=True)
    problem_image_static = models.CharField(max_length=255, blank=True)

    solution = models.TextField(blank=True)
    solution_image_1 = models.ImageField(upload_to="projects/case_study/", blank=True, null=True)
    solution_image_1_static = models.CharField(max_length=255, blank=True)
    solution_image_2 = models.ImageField(upload_to="projects/case_study/", blank=True, null=True)
    solution_image_2_static = models.CharField(max_length=255, blank=True)

    challenge = models.TextField(blank=True)

    summary = models.TextField(blank=True)
    summary_image_1 = models.ImageField(upload_to="projects/case_study/", blank=True, null=True)
    summary_image_1_static = models.CharField(max_length=255, blank=True)
    summary_image_2 = models.ImageField(upload_to="projects/case_study/", blank=True, null=True)
    summary_image_2_static = models.CharField(max_length=255, blank=True)

    live_link = models.URLField(blank=True)
    
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def cover_url(self):
        if self.cover_image:
            return self.cover_image.url
        if self.cover_image_static:
            return f"/framerusercontent.com/images/{self.cover_image_static}.jpg"
        return "/static/images/0WpkDjML9SeFblp0HONUfUfivIs.jpg"

    @property
    def problem_img_url(self):
        if self.problem_image:
            return self.problem_image.url
        if self.problem_image_static:
            return f"/framerusercontent.com/images/{self.problem_image_static}.jpg"
        return ""

    @property
    def solution_img_1_url(self):
        if self.solution_image_1:
            return self.solution_image_1.url
        if self.solution_image_1_static:
            return f"/framerusercontent.com/images/{self.solution_image_1_static}.jpg"
        return ""

    @property
    def solution_img_2_url(self):
        if self.solution_image_2:
            return self.solution_image_2.url
        if self.solution_image_2_static:
            return f"/framerusercontent.com/images/{self.solution_image_2_static}.jpg"
        return ""

    @property
    def summary_img_1_url(self):
        if self.summary_image_1:
            return self.summary_image_1.url
        if self.summary_image_1_static:
            return f"/framerusercontent.com/images/{self.summary_image_1_static}.jpg"
        return ""

    @property
    def summary_img_2_url(self):
        if self.summary_image_2:
            return self.summary_image_2.url
        if self.summary_image_2_static:
            return f"/framerusercontent.com/images/{self.summary_image_2_static}.jpg"
        return ""

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ImageField(upload_to="projects/gallery/", blank=True, null=True)
    image_static = models.CharField(max_length=255, blank=True)
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        if self.image_static:
            return f"/static/images/{self.image_static}"
        return ""

    def __str__(self):
        return f"{self.project.title} - Image #{self.id}"


class BlogPost(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=260, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="blog_posts")
    summary = models.TextField(blank=True)
    content = models.TextField()
    cover_image = models.ImageField(upload_to="blogs/", blank=True, null=True)
    cover_image_static = models.CharField(max_length=255, blank=True)
    author = models.CharField(max_length=100, default="DigiPorto")
    read_time = models.CharField(max_length=50, default="5 min read")
    published_date = models.DateField(default=timezone.now)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_date", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def cover_url(self):
        if self.cover_image:
            return self.cover_image.url
        if self.cover_image_static:
            return f"/static/images/{self.cover_image_static}"
        return "/static/images/0WpkDjML9SeFblp0HONUfUfivIs.jpg"

    def __str__(self):
        return self.title


class Service(models.Model):
    order_num = models.CharField(max_length=10, default="1.")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    hover_image = models.ImageField(upload_to="services/", blank=True, null=True, help_text="Hover image shown on floating card when hovering this service")
    hover_image_static = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "order_num"]

    @property
    def default_hover_url(self):
        defaults = {
            "1.": "/static/images/wOCTh6BhMTLrGPZ7C8doO3XdY.jpg",
            "2.": "/static/images/RPxWdsXRtMBhMcTCb414zGg2QY.jpg",
            "3.": "/static/images/Ov53jG8lAoAFuct0Li7vWgmOqQ.jpg",
            "4.": "/static/images/9HduiIXX5eSq1WREpvO4qCnKM.jpg",
        }
        num = (self.order_num or "").strip()
        if not num.endswith(".") and num.isdigit():
            num = num + "."
        return defaults.get(num, "/static/images/wOCTh6BhMTLrGPZ7C8doO3XdY.jpg")

    @property
    def hover_url(self):
        if self.hover_image:
            return self.hover_image.url
        if self.hover_image_static:
            return f"/static/images/{self.hover_image_static}"
        return self.default_hover_url

    def __str__(self):
        return f"{self.order_num} {self.title}"


class Experience(models.Model):
    role = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    period = models.CharField(max_length=100, default="2023 - Present")
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.role} at {self.company}"


class Skill(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default="Design")
    proficiency = models.PositiveIntegerField(default=90)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.name} ({self.proficiency}%)"


class Testimonial(models.Model):
    client_name = models.CharField(max_length=150)
    client_role = models.CharField(max_length=150, blank=True)
    client_company = models.CharField(max_length=150, blank=True)
    quote = models.TextField()
    client_avatar = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    client_avatar_static = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    @property
    def avatar_url(self):
        if self.client_avatar:
            return self.client_avatar.url
        if self.client_avatar_static:
            return f"/static/images/{self.client_avatar_static}"
        return ""

    def __str__(self):
        return f"{self.client_name} - {self.client_company}"


class FAQ(models.Model):
    order_num = models.CharField(max_length=10, default="1.")
    question = models.CharField(max_length=255)
    answer = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.order_num} {self.question}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Message from {self.name} ({self.email})"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-subscribed_at"]

    def __str__(self):
        return self.email


class SiteSettings(models.Model):
    site_title = models.CharField(max_length=100, default="Portavia")
    designer_name = models.CharField(max_length=100, default="Duncan Robert")
    tagline = models.CharField(max_length=200, default="DIGITAL DESIGNER")
    hero_role_1 = models.CharField(max_length=100, default="DIGITAL")
    hero_role_2 = models.CharField(max_length=100, default="DESIGNER")
    hero_headline = models.CharField(max_length=200, default="digital designer")
    hero_subheadline = models.TextField(
        default="I'm a US-based digital designer and Framer developer passionate about crafting meaningful and impactful digital experiences."
    )
    avatar_image = models.ImageField(upload_to="profile/", blank=True, null=True)
    avatar_image_static = models.CharField(max_length=255, blank=True)
    services_image = models.ImageField(upload_to="profile/", blank=True, null=True, help_text="Image shown at 'What I Can Do For You' / Services section")
    bio = models.TextField(
        default="Hi, I'm Duncan — a digital designer and Framer developer passionate about crafting meaningful and impactful digital experiences."
    )
    about_text = models.TextField(
        default="Hi, I'm Duncan — a digital designer and Framer developer passionate about crafting meaningful and impactful digital experiences."
    )
    about_headline = models.TextField(
        default="I'm a digital designer and Framer developer passionate about crafting meaningful, user-centered experiences."
    )
    about_subheadline = models.TextField(
        default="With a strong foundation in visual design and a deep understanding of interactive systems, I bring ideas to life through thoughtful design, smooth animations, and responsive layouts."
    )
    about_journey_subtitle = models.TextField(
        default="From curious creator to full-time designer, my path has been shaped by a passion for crafting purposeful, user-centered digital experiences—blending storytelling, structure, and design into every project."
    )
    about_image = models.ImageField(upload_to="profile/", blank=True, null=True, help_text="Portrait photo shown on About page")
    
    # Stats & Numbers
    stat_experience_num = models.CharField(max_length=20, default="6+")
    stat_experience_label = models.CharField(max_length=50, default="Years of Experience")
    stat_projects_num = models.CharField(max_length=20, default="50+")
    stat_projects_label = models.CharField(max_length=50, default="Completed Projects")
    stat_clients_num = models.CharField(max_length=20, default="30+")
    stat_clients_label = models.CharField(max_length=50, default="Clients on Worldwide")
    stat_satisfaction_num = models.CharField(max_length=20, default="99%")
    stat_satisfaction_label = models.CharField(max_length=50, default="Satisfaction Rate")
    stat_growth_num = models.CharField(max_length=20, default="200%")
    stat_growth_label = models.CharField(max_length=50, default="Growth")

    # Section Subtitles
    services_subtitle = models.TextField(
        default="As a digital designer, I am a visual storyteller, crafting experiences that connect deeply and spark creativity."
    )
    projects_subtitle = models.TextField(
        default="These selected projects reflect my passion for blending strategy with creativity — solving real problems through thoughtful design and impactful storytelling."
    )
    testimonials_subtitle = models.TextField(
        default="Here's what my clients have shared about their experiences working with me. Their trust and satisfaction motivate me to continue delivering designs that make an impact."
    )
    faq_subtitle = models.TextField(
        default="Here are answers to some of the most common questions I receive as a freelance designer. If you don't see your question here, feel free to reach out—I'm happy to help!"
    )
    blogs_subtitle = models.TextField(
        default="From design trends to creative processes, these articles offer insights to help you elevate your craft, solve challenges, and spark new ideas for your projects."
    )
    contact_title = models.CharField(max_length=150, default="LET'S WORK TOGETHER")
    contact_subtitle = models.TextField(
        default="Let's build something impactful together—whether it's your brand, your website, or your next big idea."
    )
    
    # Contact & Socials
    email = models.EmailField(default="designer@example.com")
    phone = models.CharField(max_length=50, default="+91 93614 80054")
    location = models.CharField(max_length=100, default="Saidapet , Chennai")
    availability_status = models.CharField(max_length=100, default="Available for work")
    behance_url = models.URLField(blank=True, default="https://behance.net")
    dribbble_url = models.URLField(blank=True, default="https://dribbble.com")
    twitter_url = models.URLField(blank=True, default="https://twitter.com")
    instagram_url = models.URLField(blank=True, default="https://instagram.com")
    linkedin_url = models.URLField(blank=True, default="https://linkedin.com")
    github_url = models.URLField(blank=True, default="https://github.com")
    resume_file = models.FileField(upload_to="profile/", blank=True, null=True)
    copyright_text = models.CharField(max_length=200, default="Copyright 2025. All Rights Reserved by oldshen")

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return f"{self.site_title} Settings ({self.designer_name})"

    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj

