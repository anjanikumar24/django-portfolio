from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib import messages

from .forms import ContactForm

from .forms import ContactForm
from .models import (
    AboutSection,
    Achievement,
    BlogCategory,
    BlogPost,
    Certification,
    CodingProfile,
    Education,
    Experience,
    GalleryImage,
    HeroSection,
    PolicyPage,
    Project,
    ProjectCategory,
    Service,
    SkillCategory,
    Statistic,
    Testimonial,
    TimelineItem,
)


def active(model):
    return model.objects.filter(is_active=True)


def home(request):
    context = {
        "hero": active(HeroSection).first(),
        "about": active(AboutSection).first(),
        "skill_categories": active(SkillCategory).prefetch_related("skills"),
        "featured_projects": active(Project).filter(is_featured=True)[:6],
        "services": active(Service)[:6],
        "statistics": active(Statistic),
        "testimonials": active(Testimonial)[:6],
        "recent_posts": active(BlogPost).order_by("-published_at", "-created_at")[:3],
        "contact_form": ContactForm(),
    }
    return render(request, "core/home.html", context)


def about(request):
    return render(
        request,
        "core/about.html",
        {
            "about": active(AboutSection).first(),
            "statistics": active(Statistic),
            "timelines": active(TimelineItem),
            "coding_profiles": active(CodingProfile),
        },
    )


def skills(request):
    return render(request, "core/skills.html", {"skill_categories": active(SkillCategory).prefetch_related("skills")})


def projects(request):
    query = request.GET.get("q", "")
    category_slug = request.GET.get("category", "")
    items = active(Project).select_related("category")
    if query:
        items = items.filter(Q(title__icontains=query) | Q(short_description__icontains=query) | Q(technologies_used__icontains=query))
    if category_slug:
        items = items.filter(category__slug=category_slug)
    paginator = Paginator(items, 9)
    return render(
        request,
        "core/projects.html",
        {
            "projects": paginator.get_page(request.GET.get("page")),
            "categories": active(ProjectCategory),
            "query": query,
            "category_slug": category_slug,
        },
    )


def project_detail(request, slug):
    project = get_object_or_404(active(Project).select_related("category").prefetch_related("screenshots"), slug=slug)
    related = active(Project).filter(category=project.category).exclude(pk=project.pk)[:3]
    return render(request, "core/project_detail.html", {"project": project, "related_projects": related})


def experience(request):
    return render(request, "core/experience.html", {"experiences": active(Experience), "timelines": active(TimelineItem).filter(timeline_type="career")})


def education(request):
    return render(request, "core/education.html", {"educations": active(Education), "timelines": active(TimelineItem).filter(timeline_type="education")})


def certifications(request):
    return render(request, "core/certifications.html", {"certifications": active(Certification)})


def achievements(request):
    return render(request, "core/achievements.html", {"achievements": active(Achievement)})


def services(request):
    return render(request, "core/services.html", {"services": active(Service)})


def gallery(request):
    return render(request, "core/gallery.html", {"images": active(GalleryImage)})


def blog(request):
    query = request.GET.get("q", "")
    category_slug = request.GET.get("category", "")
    posts = active(BlogPost).select_related("category").prefetch_related("tags").order_by("-published_at", "-created_at")
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(excerpt__icontains=query) | Q(content__icontains=query))
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    paginator = Paginator(posts, 6)
    return render(
        request,
        "core/blog.html",
        {
            "posts": paginator.get_page(request.GET.get("page")),
            "categories": active(BlogCategory),
            "query": query,
            "category_slug": category_slug,
        },
    )


def blog_detail(request, slug):
    post = get_object_or_404(active(BlogPost).select_related("category").prefetch_related("tags"), slug=slug)
    related = active(BlogPost).filter(category=post.category).exclude(pk=post.pk)[:3]
    recent = active(BlogPost).exclude(pk=post.pk).order_by("-published_at", "-created_at")[:5]
    return render(request, "core/blog_detail.html", {"post": post, "related_posts": related, "recent_posts": recent})


# def contact(request):
#     form = ContactForm(request.POST or None)
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         messages.success(request, "Your message has been saved successfully.")
#         return redirect("core:contact")
#     return render(request, "core/contact.html", {"contact_form": form})
def contact(request):
    form = ContactForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        contact_message = form.save()

        subject = f"Portfolio Contact: {contact_message.subject}"

        email_body = f"""
New message received from your portfolio contact form.

Name: {contact_message.name}
Email: {contact_message.email}
Phone: {contact_message.phone or 'Not provided'}
Subject: {contact_message.subject}

Message:
{contact_message.message}

Received at: {contact_message.created_at}
"""

        try:
            email = EmailMessage(
                subject=subject,
                body=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACT_RECEIVER_EMAIL],
                reply_to=[contact_message.email],
            )

            email.send(fail_silently=False)

            messages.success(
                request,
                "Your message has been sent successfully!"
            )

        except Exception:
            messages.warning(
                request,
                "Your message was saved, but email delivery failed."
            )

        return redirect("core:contact")

    return render(
        request,
        "core/contact.html",
        {"contact_form": form}
    )



def policy_page(request, page_type):
    page = get_object_or_404(active(PolicyPage), page_type=page_type)
    return render(request, "core/policy.html", {"page": page})
