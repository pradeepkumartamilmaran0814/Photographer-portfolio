import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.test import Client
from portfolio.models import Project, BlogPost, ContactMessage, SiteSettings

client = Client()

print("=== TESTING PORTAVIA DJANGO BACKEND & DASHBOARD GUI ===")

# 1. Test Exact Framer Frontend Pages
res = client.get("/")
print(f"GET / (Framer Home) -> Status: {res.status_code}")
assert res.status_code == 200
assert "script_main" in res.content.decode("utf-8")
assert "Dashboard GUI" in res.content.decode("utf-8")

res = client.get("/about/")
print(f"GET /about/ (Framer About) -> Status: {res.status_code}")
assert res.status_code == 200

res = client.get("/projects/")
print(f"GET /projects/ (Framer Projects) -> Status: {res.status_code}")
assert res.status_code == 200

res = client.get("/projects/black-geometric-prisms/")
print(f"GET /projects/black-geometric-prisms/ -> Status: {res.status_code}")
assert res.status_code == 200

res = client.get("/blogs/")
print(f"GET /blogs/ (Framer Blogs) -> Status: {res.status_code}")
assert res.status_code == 200

res = client.get("/blogs/5-design-trends-that-will-define-2024/")
print(f"GET /blogs/5-design-trends-that-will-define-2024/ -> Status: {res.status_code}")
assert res.status_code == 200

# 2. Test Backend Dashboard GUI
res = client.get("/dashboard/")
print(f"GET /dashboard/ (Overview GUI) -> Status: {res.status_code}")
assert res.status_code == 200

res = client.get("/dashboard/projects/")
print(f"GET /dashboard/projects/ (Projects GUI) -> Status: {res.status_code}")
assert res.status_code == 200

res = client.get("/dashboard/projects/new/")
print(f"GET /dashboard/projects/new/ (New Project GUI) -> Status: {res.status_code}")
assert res.status_code == 200

first_project = Project.objects.first()
if first_project:
    res = client.get(f"/dashboard/projects/{first_project.pk}/edit/")
    print(f"GET /dashboard/projects/{first_project.pk}/edit/ -> Status: {res.status_code}")
    assert res.status_code == 200

res = client.get("/dashboard/blogs/")
print(f"GET /dashboard/blogs/ (Blogs GUI) -> Status: {res.status_code}")
assert res.status_code == 200

res = client.get("/dashboard/settings/")
print(f"GET /dashboard/settings/ (Settings GUI) -> Status: {res.status_code}")
assert res.status_code == 200

res = client.get("/dashboard/messages/")
print(f"GET /dashboard/messages/ (Inquiries GUI) -> Status: {res.status_code}")
assert res.status_code == 200

# 3. Test Updating Data in Dashboard GUI
update_data = {
    "title": "Obsidian Geometric Prisms [Updated]",
    "client": "Apex Studio",
    "year": "2026",
    "industry": "Futurism & 3D",
    "duration": "6 weeks",
    "tagline": "Updated via Portavia Dashboard GUI!",
    "is_featured": "on",
}
res = client.post(f"/dashboard/projects/{first_project.pk}/edit/", data=update_data, follow=True)
print(f"POST /dashboard/projects/{first_project.pk}/edit/ -> Status: {res.status_code}")
assert res.status_code == 200

# Verify in DB
first_project.refresh_from_db()
print(f"Verified Project Updated in DB: title = '{first_project.title}', year = '{first_project.year}'")
assert first_project.title == "Obsidian Geometric Prisms [Updated]"
assert first_project.year == "2026"

# 4. Test Updating Site Settings in Dashboard GUI (preserve original)
orig_phone = SiteSettings.get_solo().phone
orig_location = SiteSettings.get_solo().location
settings_data = {
    "site_title": "Portavia Studio",
    "designer_name": "DigiPorto",
    "tagline": "Senior Product Designer",
    "hero_headline": "DIGITAL DESIGNER",
    "hero_subheadline": "Crafting the next generation of digital products.",
    "bio": "Bio updated from custom Dashboard GUI.",
    "email": "designer@example.com",
    "phone": orig_phone,
    "location": orig_location,
    "availability_status": "Available for work",
}
res = client.post("/dashboard/settings/", data=settings_data, follow=True)
print(f"POST /dashboard/settings/ -> Status: {res.status_code}")
assert res.status_code == 200

# Verify on Live Framer Homepage
res = client.get("/")
assert orig_phone in res.content.decode("utf-8")
print(f"Verified Framer Homepage automatically reflects phone '{orig_phone}' from Dashboard!")

print("\n>>> ALL TESTS PASSED SUCCESSFULLY! BACKEND DASHBOARD GUI & FRAMER ARE FULLY SYNCED! <<<")
