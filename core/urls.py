from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("skills/", views.skills, name="skills"),
    path("projects/", views.projects, name="projects"),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),
    path("experience/", views.experience, name="experience"),
    path("education/", views.education, name="education"),
    path("certifications/", views.certifications, name="certifications"),
    path("achievements/", views.achievements, name="achievements"),
    path("services/", views.services, name="services"),
    path("gallery/", views.gallery, name="gallery"),
    path("blog/", views.blog, name="blog"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("contact/", views.contact, name="contact"),
    path("privacy-policy/", views.policy_page, {"page_type": "privacy"}, name="privacy"),
    path("terms-and-conditions/", views.policy_page, {"page_type": "terms"}, name="terms"),
]
