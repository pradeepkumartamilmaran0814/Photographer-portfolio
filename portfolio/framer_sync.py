import os
import re
import shutil
from django.conf import settings
from .models import Project, BlogPost, SiteSettings

FRAMER_DIR = os.path.join(settings.BASE_DIR, "portavia.framer.website")
IMAGES_DIR = os.path.join(settings.BASE_DIR, "framerusercontent.com", "images")


def _copy_to_static_asset(uploaded_file, static_hash):
    if not uploaded_file or not static_hash:
        return
    clean_hash = static_hash.replace('.jpg', '').replace('.jpeg', '').replace('.png', '').replace('.webp', '')
    if not os.path.exists(uploaded_file.path):
        return
    for ext in ['.jpg', '.jpeg']:
        target_path = os.path.join(IMAGES_DIR, f"{clean_hash}{ext}")
        try:
            shutil.copy2(uploaded_file.path, target_path)
        except Exception as e:
            print(f"Error copying {clean_hash}{ext}: {e}")


def sync_project_to_framer(project):
    """
    Syncs project updates (cover image, case study images, title, client, etc.)
    directly into portavia.framer.website HTML files and framer image assets.
    Keeps 100% of the Framer animations, 3D scroll, and UI untouched.
    """
    # 1. Sync all uploaded images into framerusercontent.com/images/
    _copy_to_static_asset(project.cover_image, project.cover_image_static)
    _copy_to_static_asset(project.problem_image, project.problem_image_static)
    _copy_to_static_asset(project.solution_image_1, project.solution_image_1_static)
    _copy_to_static_asset(project.solution_image_2, project.solution_image_2_static)
    _copy_to_static_asset(project.summary_image_1, project.summary_image_1_static)
    _copy_to_static_asset(project.summary_image_2, project.summary_image_2_static)

    # 2. Sync title and metadata in Framer HTML files directly
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

                # In project detail file:
                if fpath.endswith(f"{project.slug}.html"):
                    if project.client:
                        content = re.sub(r'(Client\s*:\s*</p>.*?<p[^>]*>).*?(</p>)', rf'\g<1>{project.client}\g<2>', content, flags=re.DOTALL)
                    if project.year:
                        content = re.sub(r'(Year\s*:\s*</p>.*?<p[^>]*>).*?(</p>)', rf'\g<1>{project.year}\g<2>', content, flags=re.DOTALL)
                    if project.duration:
                        content = re.sub(r'(Project Duration\s*:\s*</p>.*?<p[^>]*>).*?(</p>)', rf'\g<1>{project.duration}\g<2>', content, flags=re.DOTALL)
                    if project.industry:
                        content = re.sub(r'(Industry\s*:\s*</p>.*?<p[^>]*>).*?(</p>)', rf'\g<1>{project.industry}\g<2>', content, flags=re.DOTALL)
                    if project.problem:
                        content = re.sub(r'(Problem\s*:\s*</h3>.*?<p[^>]*>).*?(</p>)', rf'\g<1>{project.problem}\g<2>', content, flags=re.DOTALL)
                    if project.solution:
                        content = re.sub(r'(Solution\s*:\s*</h3>.*?<p[^>]*>).*?(</p>)', rf'\g<1>{project.solution}\g<2>', content, flags=re.DOTALL)
                    if project.challenge:
                        content = re.sub(r'(Challenge\s*:\s*</h3>.*?<p[^>]*>).*?(</p>)', rf'\g<1>{project.challenge}\g<2>', content, flags=re.DOTALL)
                    if project.summary:
                        content = re.sub(r'(Summary\s*:\s*</h3>.*?<p[^>]*>).*?(</p>)', rf'\g<1>{project.summary}\g<2>', content, flags=re.DOTALL)

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
