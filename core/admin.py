from django.contrib import admin
from django.utils.html import format_html

from .models import (
    AboutSection,
    Achievement,
    BlogCategory,
    BlogPost,
    Certification,
    CodingProfile,
    ContactMessage,
    Education,
    Experience,
    GalleryImage,
    HeroSection,
    NavigationLink,
    PolicyPage,
    Project,
    ProjectCategory,
    ProjectScreenshot,
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


class ImagePreviewMixin:
    image_field = "image"

    @admin.display(description="Preview")
    def image_preview(self, obj):
        image = getattr(obj, self.image_field, None)
        if image:
            return format_html('<img src="{}" style="height:54px;border-radius:8px;object-fit:cover;" />', image.url)
        return "-"


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(ImagePreviewMixin, admin.ModelAdmin):
    image_field = "logo"
    list_display = ("site_name", "email", "phone", "is_active", "image_preview")
    fieldsets = (
        ("Branding", {"fields": ("site_name", "logo", "favicon", "is_active")}),
        ("Footer", {"fields": ("footer_description", "copyright_text", "email", "phone", "address")}),
        ("SEO", {"fields": ("meta_title", "meta_description", "og_image")}),
    )


@admin.register(NavigationLink)
class NavigationLinkAdmin(admin.ModelAdmin):
    list_display = ("label", "url", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    search_fields = ("label", "url")
    list_filter = ("is_active", "open_in_new_tab")


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    search_fields = ("name", "url")
    list_filter = ("is_active",)


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ("label", "value", "suffix", "display_order", "is_active")
    list_editable = ("value", "suffix", "display_order", "is_active")
    search_fields = ("label",)
    list_filter = ("is_active",)


@admin.register(HeroSection)
class HeroSectionAdmin(ImagePreviewMixin, admin.ModelAdmin):
    image_field = "professional_photo"
    list_display = ("name", "professional_title", "location", "is_active", "image_preview")
    search_fields = ("name", "professional_title", "location")
    list_filter = ("is_active",)
    fieldsets = (
        ("Main Content", {"fields": ("name", "professional_title", "typing_text", "short_description", "is_active")}),
        ("Media", {"fields": ("professional_photo", "cover_image", "resume_pdf")}),
        ("Buttons", {"fields": ("resume_button_text", "hire_me_button_text", "contact_button_text")}),
        ("Links", {"fields": ("github_link", "linkedin_link", "leetcode_link")}),
        ("Contact", {"fields": ("email", "phone", "location")}),
        ("SEO", {"fields": ("meta_title", "meta_description", "og_image")}),
    )


@admin.register(AboutSection)
class AboutSectionAdmin(ImagePreviewMixin, admin.ModelAdmin):
    image_field = "about_image"
    list_display = ("title", "experience_summary", "projects_completed", "is_active", "image_preview")
    search_fields = ("title", "biography", "career_objective")
    fieldsets = (
        ("Content", {"fields": ("title", "biography", "career_objective", "introduction", "personal_details")}),
        ("Metrics", {"fields": ("experience_summary", "projects_completed", "coding_journey")}),
        ("Media", {"fields": ("about_image", "resume_pdf", "resume_button_text")}),
        ("SEO", {"fields": ("meta_title", "meta_description", "og_image")}),
        ("Publishing", {"fields": ("is_active", "display_order")}),
    )


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    inlines = [SkillInline]
    list_display = ("name", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    search_fields = ("name",)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "percentage", "display_order", "is_active")
    list_editable = ("percentage", "display_order", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "category__name")


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("degree", "college", "university", "passing_year", "display_order", "is_active")
    list_filter = ("passing_year", "is_active")
    search_fields = ("college", "degree", "branch", "university", "school")


@admin.register(Experience)
class ExperienceAdmin(ImagePreviewMixin, admin.ModelAdmin):
    image_field = "logo"
    list_display = ("position", "company", "duration", "is_active", "image_preview")
    list_filter = ("is_active",)
    search_fields = ("company", "position", "technologies")


class ProjectScreenshotInline(admin.TabularInline):
    model = ProjectScreenshot
    extra = 1


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug", "display_order", "is_active")
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(ImagePreviewMixin, admin.ModelAdmin):
    image_field = "thumbnail"
    inlines = [ProjectScreenshotInline]
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "category", "project_status", "completion_date", "is_featured", "is_active", "image_preview")
    list_filter = ("category", "project_status", "is_featured", "is_active")
    search_fields = ("title", "short_description", "technologies_used")
    fieldsets = (
        ("Overview", {"fields": ("title", "slug", "category", "thumbnail", "short_description", "is_featured")}),
        ("Details", {"fields": ("full_description", "features", "technologies_used")}),
        ("Links and Status", {"fields": ("github_link", "live_demo_link", "project_status", "completion_date")}),
        ("SEO", {"fields": ("meta_title", "meta_description", "og_image")}),
        ("Publishing", {"fields": ("is_active", "display_order")}),
    )


@admin.register(Certification)
class CertificationAdmin(ImagePreviewMixin, admin.ModelAdmin):
    image_field = "certificate_image"
    list_display = ("certificate_name", "organization", "issue_date", "is_active", "image_preview")
    list_filter = ("organization", "issue_date", "is_active")
    search_fields = ("certificate_name", "organization")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    search_fields = ("title", "description")


@admin.register(Achievement)
class AchievementAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("achievement", "competition", "award", "is_active", "image_preview")
    list_filter = ("competition", "is_active")
    search_fields = ("achievement", "competition", "award")


@admin.register(CodingProfile)
class CodingProfileAdmin(admin.ModelAdmin):
    list_display = ("platform", "username", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    search_fields = ("platform", "username")


@admin.register(GalleryImage)
class GalleryImageAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("title", "display_order", "is_active", "image_preview")
    list_editable = ("display_order", "is_active")
    search_fields = ("title", "caption")


@admin.register(TimelineItem)
class TimelineItemAdmin(admin.ModelAdmin):
    list_display = ("title", "timeline_type", "period", "display_order", "is_active")
    list_filter = ("timeline_type", "is_active")
    search_fields = ("title", "period", "description")


@admin.register(Testimonial)
class TestimonialAdmin(ImagePreviewMixin, admin.ModelAdmin):
    image_field = "photo"
    list_display = ("name", "position", "company", "rating", "is_active", "image_preview")
    list_filter = ("rating", "is_active")
    search_fields = ("name", "position", "company", "review")


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug", "display_order", "is_active")
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug", "display_order", "is_active")
    search_fields = ("name",)


@admin.register(BlogPost)
class BlogPostAdmin(ImagePreviewMixin, admin.ModelAdmin):
    image_field = "featured_image"
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "category", "published_at", "is_featured", "is_active", "image_preview")
    list_filter = ("category", "tags", "is_featured", "is_active", "published_at")
    search_fields = ("title", "excerpt", "content")
    filter_horizontal = ("tags",)
    fieldsets = (
        ("Article", {"fields": ("title", "slug", "category", "tags", "featured_image", "excerpt", "content")}),
        ("Publishing", {"fields": ("published_at", "is_featured", "is_active", "display_order")}),
        ("SEO", {"fields": ("meta_title", "meta_description", "og_image")}),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "phone", "subject", "message")
    readonly_fields = ("name", "email", "phone", "subject", "message", "created_at")


@admin.register(PolicyPage)
class PolicyPageAdmin(admin.ModelAdmin):
    list_display = ("title", "page_type", "is_active")
    list_filter = ("page_type", "is_active")
    search_fields = ("title", "content")
    fieldsets = (
        ("Content", {"fields": ("page_type", "title", "content")}),
        ("SEO", {"fields": ("meta_title", "meta_description", "og_image")}),
        ("Publishing", {"fields": ("is_active", "display_order")}),
    )


admin.site.site_header = "Portfolio Administration"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Content Management"
