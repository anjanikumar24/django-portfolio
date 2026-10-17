from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import BlogPost, Project


class StaticViewSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return [
            "core:home",
            "core:about",
            "core:skills",
            "core:projects",
            "core:experience",
            "core:education",
            "core:certifications",
            "core:achievements",
            "core:services",
            "core:gallery",
            "core:blog",
            "core:contact",
        ]

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Project.objects.filter(is_active=True)


class BlogPostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return BlogPost.objects.filter(is_active=True)
