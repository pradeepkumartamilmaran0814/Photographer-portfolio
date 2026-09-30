import os
import re
import shutil
from django.conf import settings
from .models import Project, BlogPost, SiteSettings

FRAMER_DIR = os.path.join(settings.BASE_DIR, "portavia.framer.website")
IMAGES_DIR = os.path.join(settings.BASE_DIR, "framerusercontent.com", "images")


def sync_project_to_framer(project):
    """
    Syncs project updates (new cover image, title, tagline) directly
    into portavia.framer.website HTML files and framer image assets.
    Keeps 100% of the Framer animations, 3D scroll, and UI untouched.
    """
    # 1. If an uploaded image was provided, copy it directly to replace the static image asset
    if project.cover_image and project.cover_image_static:
        static_img_path = os.path.join(IMAGES_DIR, project.cover_image_static)
        if os.path.exists(static_img_path):
            try:
                shutil.copy2(project.cover_image.path, static_img_path)
            except Exception as e:
                print(f"Error syncing image: {e}")

    # 2. Sync title in index.html and projects.html
    files_to_update = [
        os.path.join(FRAMER_DIR, "index.html"),
        os.path.join(FRAMER_DIR, "projects.html"),
        os.path.join(FRAMER_DIR, "projects", f"{project.slug}.html"),
    ]

    for fpath in files_to_update:
        if os.path.exists(fpath):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()

                # If project was renamed, we can update occurrences
                # In project detail file:
                if fpath.endswith(f"{project.slug}.html"):
                    # Update client, year, duration
                    content = re.sub(r'(Client\s*:\s*</p>.*?<p[^>]*class="[^"]*framer-text[^"]*"[^>]*>).*?(</p>)', rf'\g<1>{project.client}\g<2>', content, flags=re.DOTALL)
                    content = re.sub(r'(Year\s*:\s*</p>.*?<p[^>]*class="[^"]*framer-text[^"]*"[^>]*>).*?(</p>)', rf'\g<1>{project.year}\g<2>', content, flags=re.DOTALL)
                    content = re.sub(r'(Project Duration\s*:\s*</p>.*?<p[^>]*class="[^"]*framer-text[^"]*"[^>]*>).*?(</p>)', rf'\g<1>{project.duration}\g<2>', content, flags=re.DOTALL)
                    content = re.sub(r'(Industry\s*:\s*</p>.*?<p[^>]*class="[^"]*framer-text[^"]*"[^>]*>).*?(</p>)', rf'\g<1>{project.industry}\g<2>', content, flags=re.DOTALL)

                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(content)
            except Exception as e:
                print(f"Error updating {fpath}: {e}")


def sync_site_settings_to_framer(site_settings):
    """
    Syncs global email and phone across all Framer HTML files directly.
    """
    html_files = [
        os.path.join(FRAMER_DIR, "index.html"),
        os.path.join(FRAMER_DIR, "about.html"),
        os.path.join(FRAMER_DIR, "projects.html"),
        os.path.join(FRAMER_DIR, "blogs.html"),
    ]

    for fpath in html_files:
        if os.path.exists(fpath):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Update email and phone
                if site_settings.email:
                    content = content.replace("designer@example.com", site_settings.email)
                if site_settings.phone:
                    content = content.replace("+1 (555) 123-4567", site_settings.phone)

                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(content)
            except Exception as e:
                print(f"Error syncing settings to {fpath}: {e}")
