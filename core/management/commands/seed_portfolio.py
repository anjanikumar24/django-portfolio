from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import (
    AboutSection,
    BlogCategory,
    BlogPost,
    Certification,
    CodingProfile,
    Education,
    Experience,
    HeroSection,
    NavigationLink,
    PolicyPage,
    Project,
    ProjectCategory,
    Service,
    SiteConfiguration,
    Skill,
    SkillCategory,
    SocialLink,
    Statistic,
    Tag,
    Testimonial,
    TimelineItem,
)


class Command(BaseCommand):
    help = "Create editable professional placeholder content for the portfolio."

    def handle(self, *args, **options):
        site, _ = SiteConfiguration.objects.get_or_create(
            pk=1,
            defaults={
                "site_name": "Aarav Sharma",
                "footer_description": "Full stack engineer focused on reliable products, clean interfaces, and measurable business outcomes.",
                "copyright_text": "Copyright 2026 Aarav Sharma. All rights reserved.",
                "email": "hello@example.com",
                "phone": "+91 98765 43210",
                "address": "Bengaluru, India",
                "meta_title": "Aarav Sharma - Full Stack Software Engineer",
                "meta_description": "Premium Django portfolio for a full stack software engineer.",
            },
        )
        self.stdout.write(f"Configured site: {site.site_name}")

        nav_items = [
            ("Home", "/"),
            ("About", "/about/"),
            ("Skills", "/skills/"),
            ("Projects", "/projects/"),
            ("Experience", "/experience/"),
            ("Blog", "/blog/"),
            ("Contact", "/contact/"),
        ]
        for order, (label, url) in enumerate(nav_items):
            NavigationLink.objects.get_or_create(label=label, defaults={"url": url, "display_order": order})

        socials = [
            ("GitHub", "bi bi-github", "https://github.com/"),
            ("LinkedIn", "bi bi-linkedin", "https://www.linkedin.com/"),
            ("LeetCode", "bi bi-code-slash", "https://leetcode.com/"),
        ]
        for order, (name, icon, url) in enumerate(socials):
            SocialLink.objects.get_or_create(name=name, defaults={"icon_class": icon, "url": url, "display_order": order})

        HeroSection.objects.get_or_create(
            pk=1,
            defaults={
                "name": "Aarav Sharma",
                "professional_title": "Full Stack Software Engineer",
                "typing_text": "Django Developer|Backend Engineer|Product-Minded Builder",
                "short_description": "I design and ship secure, scalable web applications with thoughtful user experiences and dependable engineering foundations.",
                "github_link": "https://github.com/",
                "linkedin_link": "https://www.linkedin.com/",
                "leetcode_link": "https://leetcode.com/",
                "email": "hello@example.com",
                "phone": "+91 98765 43210",
                "location": "Bengaluru, India",
            },
        )

        AboutSection.objects.get_or_create(
            pk=1,
            defaults={
                "biography": "I am a full stack developer who enjoys turning ambiguous product ideas into polished, maintainable web applications.",
                "career_objective": "My goal is to build high-impact software with clean architecture, strong fundamentals, and interfaces people enjoy using.",
                "introduction": "I work across Django, relational databases, Bootstrap, and vanilla JavaScript.",
                "personal_details": "Open to internships, full-time engineering roles, and selective freelance projects.",
                "experience_summary": "2+ Years",
                "projects_completed": 18,
                "coding_journey": "Started with Python fundamentals, moved into Django, and now focus on production-quality full stack systems.",
            },
        )

        categories = {
            "Programming Languages": [("Python", 92), ("JavaScript", 84), ("SQL", 86)],
            "Backend": [("Django", 92), ("Django ORM", 90), ("Authentication", 82)],
            "Frontend": [("HTML5", 94), ("CSS3", 88), ("Bootstrap 5", 90)],
            "Database": [("SQLite", 86), ("PostgreSQL", 78)],
            "Tools": [("Git", 88), ("Docker Basics", 70)],
            "Currently Learning": [("System Design", 68), ("Cloud Deployment", 72)],
        }
        for order, (category_name, skills) in enumerate(categories.items()):
            category, _ = SkillCategory.objects.get_or_create(name=category_name, defaults={"display_order": order})
            for skill_order, (skill_name, percentage) in enumerate(skills):
                Skill.objects.get_or_create(
                    category=category,
                    name=skill_name,
                    defaults={"percentage": percentage, "display_order": skill_order},
                )

        for label, value, suffix, order in [
            ("Projects", 18, "+", 0),
            ("Technologies", 24, "+", 1),
            ("Certifications", 7, "+", 2),
            ("Coding Problems", 450, "+", 3),
        ]:
            Statistic.objects.get_or_create(label=label, defaults={"value": value, "suffix": suffix, "display_order": order})

        Service.objects.get_or_create(
            title="Full Stack Web Development",
            defaults={"icon_class": "bi bi-window-stack", "description": "End-to-end Django applications with polished Bootstrap interfaces."},
        )
        Service.objects.get_or_create(
            title="Backend Architecture",
            defaults={"icon_class": "bi bi-diagram-3", "description": "Clean models, secure forms, admin workflows, and maintainable business logic."},
        )
        Service.objects.get_or_create(
            title="Portfolio and Product UI",
            defaults={"icon_class": "bi bi-palette", "description": "Responsive, premium interfaces that feel modern without sacrificing clarity."},
        )

        Education.objects.get_or_create(
            degree="Bachelor of Technology",
            defaults={
                "college": "Sample Institute of Technology",
                "branch": "Computer Science and Engineering",
                "university": "Sample Technical University",
                "cgpa": "8.8 CGPA",
                "passing_year": "2026",
                "description": "Focused on software engineering, databases, algorithms, and web technologies.",
            },
        )
        Experience.objects.get_or_create(
            company="Product Studio Labs",
            position="Software Engineering Intern",
            defaults={
                "duration": "Jan 2026 - Jun 2026",
                "technologies": "Python, Django, Bootstrap, SQLite",
                "description": "Built internal tools and production features for business teams.",
                "responsibilities": "Implemented admin workflows\nOptimized database queries\nImproved frontend responsiveness",
            },
        )

        project_category, _ = ProjectCategory.objects.get_or_create(name="Web Applications")
        Project.objects.get_or_create(
            title="InsightFlow Analytics Dashboard",
            defaults={
                "category": project_category,
                "short_description": "A Django dashboard for tracking operational metrics with clean admin-managed content.",
                "full_description": "InsightFlow demonstrates secure forms, reusable templates, dynamic charts, and structured content managed entirely from the backend.",
                "features": "Dynamic admin content\nResponsive dashboard layout\nSearchable data views\nSEO-friendly pages",
                "technologies_used": "Django, Bootstrap 5, Vanilla JavaScript, SQLite",
                "project_status": "completed",
                "is_featured": True,
            },
        )

        Certification.objects.get_or_create(
            certificate_name="Django Web Development",
            defaults={"organization": "Sample Academy", "issue_date": timezone.now().date()},
        )
        CodingProfile.objects.get_or_create(platform="GitHub", defaults={"icon_class": "bi bi-github", "profile_url": "https://github.com/", "username": "developer"})
        TimelineItem.objects.get_or_create(
            title="Started Full Stack Development",
            defaults={"timeline_type": "learning", "period": "2024", "description": "Built a strong Python and web fundamentals base."},
        )
        Testimonial.objects.get_or_create(
            name="Sample Client",
            defaults={"position": "Product Manager", "company": "Tech Co", "review": "Delivered a clean, reliable portfolio with excellent attention to detail.", "rating": 5},
        )

        blog_category, _ = BlogCategory.objects.get_or_create(name="Engineering")
        tag, _ = Tag.objects.get_or_create(name="Django")
        post, _ = BlogPost.objects.get_or_create(
            title="How I Build Reliable Django Projects",
            defaults={
                "category": blog_category,
                "excerpt": "A practical look at models, admin workflows, templates, forms, and deployment-minded structure.",
                "content": "Reliable Django projects start with clear models, focused views, reusable templates, and disciplined admin configuration.",
                "published_at": timezone.now(),
                "is_featured": True,
            },
        )
        post.tags.add(tag)

        PolicyPage.objects.get_or_create(
            page_type="privacy",
            defaults={"title": "Privacy Policy", "content": "This website stores contact form submissions for follow-up communication only."},
        )
        PolicyPage.objects.get_or_create(
            page_type="terms",
            defaults={"title": "Terms & Conditions", "content": "The content on this portfolio is provided for professional review and communication."},
        )

        self.stdout.write(self.style.SUCCESS("Portfolio placeholder content created. Edit every item from Django admin."))
