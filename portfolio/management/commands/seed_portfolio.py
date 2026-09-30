import os
import json
from datetime import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from portfolio.models import (
    Category,
    Project,
    ProjectImage,
    BlogPost,
    Service,
    Experience,
    Skill,
    Testimonial,
    SiteSettings,
)


class Command(BaseCommand):
    help = "Seed database with initial portfolio data from Framer site"

    def handle(self, *args, **options):
        self.stdout.write("Starting portfolio database seeding...")

        # 1. Create superuser if not exists
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@portavia.local", "admin123")
            self.stdout.write(self.style.SUCCESS("Created superuser: admin / admin123"))

        # 2. Site Settings
        settings, _ = SiteSettings.objects.get_or_create(id=1)
        settings.site_title = "Portavia"
        settings.designer_name = "DigiPorto"
        settings.tagline = "Digital Designer & Visual Creator"
        settings.hero_headline = "digital designer"
        settings.hero_subheadline = "Crafting high-impact digital experiences, modern brands, and intuitive user interfaces."
        settings.bio = (
            "I'm a multidisciplinary digital designer and visual artist specializing in UI/UX design, "
            "web design, 3D composition, and brand identity rollout. Over the past 6+ years, I have worked "
            "with innovative startups and industry leaders to create compelling, user-centered digital products."
        )
        settings.email = "designer@example.com"
        settings.phone = "+1 (555) 123-4567"
        settings.location = "San Francisco, CA"
        settings.availability_status = "Available for freelance projects & design roles"
        settings.dribbble_url = "https://dribbble.com"
        settings.twitter_url = "https://x.com"
        settings.instagram_url = "https://instagram.com"
        settings.linkedin_url = "https://linkedin.com"
        settings.github_url = "https://github.com"
        settings.save()
        self.stdout.write(self.style.SUCCESS("Saved Site Settings"))

        # 3. Services
        services_data = [
            ("1.", "ui/ux design", "Transforming user insights into high-converting, visually breathtaking web and mobile applications with intuitive information architecture."),
            ("2.", "Graphic Design", "Designing impactful visual assets, poster designs, editorial layouts, and advertising collateral that captivates audiences."),
            ("3.", "Web Design", "Building responsive, modern, and accessible websites tailored to your brand goals, prioritizing performance and user delight."),
            ("4.", "Branding", "Crafting comprehensive visual identities from logo systems and color theory to typography rules and complete brand rollout guides."),
        ]
        Service.objects.all().delete()
        for idx, (num, title, desc) in enumerate(services_data):
            Service.objects.create(
                order_num=num,
                title=title,
                description=desc,
                order=idx + 1,
                is_active=True
            )
        self.stdout.write(self.style.SUCCESS(f"Created {len(services_data)} Services"))

        # 4. Experiences
        experiences_data = [
            ("Lead Product Designer", "Studio Aurora", "2023 - Present", "Directing UI/UX strategy and design systems across client design sprints."),
            ("Senior UI/UX Designer", "InnovateTech Labs", "2021 - 2023", "Spearheaded web platform overhaul and design component library for 500k+ active users."),
            ("Brand & Visual Designer", "Prism Creative Co.", "2019 - 2021", "Created cross-platform brand guidelines, campaign visuals, and promotional assets."),
        ]
        Experience.objects.all().delete()
        for idx, (role, comp, per, desc) in enumerate(experiences_data):
            Experience.objects.create(
                role=role,
                company=comp,
                period=per,
                description=desc,
                order=idx + 1
            )
        self.stdout.write(self.style.SUCCESS(f"Created {len(experiences_data)} Experiences"))

        # 5. Skills
        skills_data = [
            ("UI / UX Design", "Design", 95),
            ("Figma & Design Systems", "Design", 98),
            ("Framer & Webflow", "Tools", 92),
            ("3D & Motion Graphics", "Design", 88),
            ("Typography & Layout", "Design", 94),
            ("HTML5 / CSS3 / Vanilla JS", "Development", 85),
            ("Brand Strategy", "Strategy", 90),
        ]
        Skill.objects.all().delete()
        for idx, (name, cat, prof) in enumerate(skills_data):
            Skill.objects.create(
                name=name,
                category=cat,
                proficiency=prof,
                order=idx + 1
            )
        self.stdout.write(self.style.SUCCESS(f"Created {len(skills_data)} Skills"))

        # 6. Testimonials
        testimonials_data = [
            ("Marcus Vance", "Product VP", "InnovateTech", "Working with DigiPorto transformed our digital presence. The attention to typography, motion, and user experience is world-class.", "1jsryiRhbB5SoLHzyceqqF9tpo.jpg"),
            ("Elena Rostova", "Founder", "Intenza Boutique", "The brand rollout exceeded every expectation. Our conversion rates jumped by 40% immediately following launch.", "KhZnIlAtOozB2Axd5yg9ALd7A.jpg"),
            ("Liam Henderson", "Design Director", "Studio Prism", "An exceptional creative partner. Seamless blend of aesthetic elegance and functional engineering.", "FigaBMy3WrTNL79MFKifsXxXE.jpg"),
        ]
        Testimonial.objects.all().delete()
        for idx, (cname, crole, ccomp, quote, avatar) in enumerate(testimonials_data):
            Testimonial.objects.create(
                client_name=cname,
                client_role=crole,
                client_company=ccomp,
                quote=quote,
                client_avatar_static=avatar,
                order=idx + 1,
                is_active=True
            )
        self.stdout.write(self.style.SUCCESS(f"Created {len(testimonials_data)} Testimonials"))

        # 7. Projects from extracted_projects.json
        projects_file = os.path.join(r"d:\ASAP\design-port", "extracted_projects.json")
        project_cat_map = {
            "black-geometric-prisms": "Branding",
            "innovatetech-identity-rollout": "Branding",
            "coral-spiral-abstract": "Graphic Design",
            "pantone-very-peri-poster-design": "Graphic Design",
            "summer-vibes-festival-campaign": "Graphic Design",
            "intenza-brand-boutique-e-gift-card-design": "UI / UX Design",
            "shopease-redesign-sprint": "UI / UX Design",
            "vistahaven-stunning-real-estate-template": "Web Design",
        }

        if os.path.exists(projects_file):
            with open(projects_file, "r", encoding="utf-8") as f:
                projects_list = json.load(f)
            
            for idx, pdata in enumerate(projects_list):
                slug = pdata.get("slug", "") or f"project-{idx+1}"
                cat_name = project_cat_map.get(slug, pdata.get("category", "UI / UX Design"))
                category, _ = Category.objects.get_or_create(
                    slug=slugify(cat_name),
                    defaults={"name": cat_name, "category_type": "project"}
                )
                
                project, _ = Project.objects.update_or_create(
                    slug=slug,
                    defaults={
                        "title": pdata.get("title") or "Project",
                        "category": category,
                        "tagline": pdata.get("tagline") or "",
                        "short_description": pdata.get("tagline") or "",
                        "client": pdata.get("client") or "Studio Client",
                        "year": pdata.get("year") or "2025",
                        "industry": pdata.get("industry") or "Tech & Design",
                        "duration": pdata.get("duration") or "4 weeks",
                        "cover_image_static": pdata.get("cover_image_static") or "",
                        "problem": pdata.get("problem") or "",
                        "solution": pdata.get("solution") or "",
                        "challenge": pdata.get("challenge") or "",
                        "summary": pdata.get("summary") or "",
                        "is_featured": True,
                        "order": idx + 1,
                    }
                )
                
                # Add gallery images if empty
                if not project.gallery_images.exists():
                    for g_idx, g_img in enumerate(pdata.get("gallery_images", [])):
                        ProjectImage.objects.create(
                            project=project,
                            image_static=g_img,
                            order=g_idx + 1
                        )
            
            self.stdout.write(self.style.SUCCESS(f"Synced {len(projects_list)} Projects with stable IDs"))

        # 8. Blogs from extracted_blogs.json
        blogs_file = os.path.join(r"d:\ASAP\design-port", "extracted_blogs.json")
        blog_cat_map = {
            "5-design-trends-that-will-define-2024": "Insights",
            "mastering-ui-ux-design-key-principles-for-success": "Insights",
            "the-role-of-color-psychology-in-branding": "Design",
            "the-power-of-typography-in-web-design": "Design",
            "how-to-streamline-your-design-workflow": "Tutorials",
            "balancing-creativity-and-functionality-in-design": "Tutorials",
        }

        if os.path.exists(blogs_file):
            with open(blogs_file, "r", encoding="utf-8") as f:
                blogs_list = json.load(f)
            
            for idx, bdata in enumerate(blogs_list):
                slug = bdata.get("slug", "") or f"article-{idx+1}"
                cat_name = blog_cat_map.get(slug, bdata.get("category", "Insights"))
                category, _ = Category.objects.get_or_create(
                    slug=slugify(cat_name),
                    defaults={"name": cat_name, "category_type": "blog"}
                )

                pub_date_str = bdata.get("published_date", "")
                try:
                    pub_date = datetime.strptime(pub_date_str, "%b %d, %Y").date()
                except Exception:
                    pub_date = datetime.now().date()

                BlogPost.objects.update_or_create(
                    slug=slug,
                    defaults={
                        "title": bdata.get("title") or "Article",
                        "category": category,
                        "summary": bdata.get("summary") or "",
                        "content": bdata.get("content") or "",
                        "cover_image_static": bdata.get("cover_image_static") or "",
                        "author": "DigiPorto",
                        "read_time": "5 min read",
                        "published_date": pub_date,
                        "is_featured": (idx < 2),
                        "is_published": True,
                    }
                )
            self.stdout.write(self.style.SUCCESS(f"Synced {len(blogs_list)} Blog Posts with stable IDs"))


        self.stdout.write(self.style.SUCCESS("Portfolio database seeding completed successfully!"))
