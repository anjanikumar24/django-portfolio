from .models import NavigationLink, SiteConfiguration, SocialLink


def site_content(request):
    return {
        "site_config": SiteConfiguration.objects.filter(is_active=True).first(),
        "nav_links": NavigationLink.objects.filter(is_active=True),
        "social_links": SocialLink.objects.filter(is_active=True),
    }
