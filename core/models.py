from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ["display_order", "-created_at"]


class SEOModel(models.Model):
    meta_title = models.CharField(max_length=180, blank=True)
    meta_description = models.TextField(blank=True)
    og_image = models.ImageField(upload_to="seo/", blank=True)

    class Meta:
        abstract = True


class SiteConfiguration(TimeStampedModel, SEOModel):
    site_name = models.CharField(max_length=120, default="Portfolio")
    logo = models.ImageField(upload_to="branding/", blank=True)
    favicon = models.ImageField(upload_to="branding/", blank=True)
    footer_description = models.TextField(blank=True)
    copyright_text = models.CharField(max_length=180, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    address = models.CharField(max_length=220, blank=True)

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def __str__(self):
        return self.site_name


class NavigationLink(TimeStampedModel):
    label = models.CharField(max_length=80)
    url = models.CharField(max_length=220)
    open_in_new_tab = models.BooleanField(default=False)

    def __str__(self):
        return self.label


class SocialLink(TimeStampedModel):
    name = models.CharField(max_length=80)
    icon_class = models.CharField(max_length=80, blank=True, help_text="Bootstrap Icon class")
    url = models.URLField()

    def __str__(self):
        return self.name


class HeroSection(TimeStampedModel, SEOModel):
    name = models.CharField(max_length=140)
    professional_title = models.CharField(max_length=180)
    typing_text = models.CharField(max_length=260)
    short_description = models.TextField()
    professional_photo = models.ImageField(upload_to="hero/", blank=True)
    cover_image = models.ImageField(upload_to="hero/", blank=True)
    resume_pdf = models.FileField(upload_to="resume/", blank=True)
    resume_button_text = models.CharField(max_length=60, default="Download Resume")
    hire_me_button_text = models.CharField(max_length=60, default="Hire Me")
    contact_button_text = models.CharField(max_length=60, default="Contact")
    github_link = models.URLField(blank=True)
    linkedin_link = models.URLField(blank=True)
    leetcode_link = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    location = models.CharField(max_length=160, blank=True)

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"

    def __str__(self):
        return self.name


class AboutSection(TimeStampedModel, SEOModel):
    title = models.CharField(max_length=120, default="About Me")
    about_image = models.ImageField(upload_to="about/", blank=True)
    biography = models.TextField()
    career_objective = models.TextField(blank=True)
    introduction = models.TextField(blank=True)
    personal_details = models.TextField(blank=True)
    experience_summary = models.CharField(max_length=120, blank=True)
    projects_completed = models.PositiveIntegerField(default=0)
    coding_journey = models.TextField(blank=True)
    resume_pdf = models.FileField(upload_to="resume/", blank=True)
    resume_button_text = models.CharField(max_length=60, default="Download Resume")

    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Section"

    def __str__(self):
        return self.title


class SkillCategory(TimeStampedModel):
    name = models.CharField(max_length=120)
    icon_class = models.CharField(max_length=80, blank=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name_plural = "Skill Categories"

    def __str__(self):
        return self.name


class Skill(TimeStampedModel):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=120)
    icon_class = models.CharField(max_length=80, blank=True)
    percentage = models.PositiveSmallIntegerField(default=80)

    def __str__(self):
        return self.name


class Education(TimeStampedModel):
    college = models.CharField(max_length=180, blank=True)
    degree = models.CharField(max_length=180)
    branch = models.CharField(max_length=180, blank=True)
    university = models.CharField(max_length=180, blank=True)
    school = models.CharField(max_length=180, blank=True)
    cgpa = models.CharField(max_length=40, blank=True)
    passing_year = models.CharField(max_length=20)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.degree


class Experience(TimeStampedModel):
    company = models.CharField(max_length=180)
    logo = models.ImageField(upload_to="experience/", blank=True)
    position = models.CharField(max_length=180)
    duration = models.CharField(max_length=120)
    technologies = models.CharField(max_length=260, blank=True)
    description = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)

    def __str__(self):
        return f"{self.position} at {self.company}"


class ProjectCategory(TimeStampedModel):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name_plural = "Project Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Project(TimeStampedModel, SEOModel):
    STATUS_CHOICES = [
        ("planned", "Planned"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("archived", "Archived"),
    ]
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True, blank=True)
    thumbnail = models.ImageField(upload_to="projects/thumbnails/", blank=True)
    short_description = models.TextField()
    full_description = models.TextField()
    features = models.TextField(blank=True)
    technologies_used = models.CharField(max_length=260)
    github_link = models.URLField(blank=True)
    live_demo_link = models.URLField(blank=True)
    project_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="completed")
    completion_date = models.DateField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:project_detail", kwargs={"slug": self.slug})

    def feature_list(self):
        return [item.strip() for item in self.features.splitlines() if item.strip()]

    def __str__(self):
        return self.title


class ProjectScreenshot(TimeStampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="screenshots")
    image = models.ImageField(upload_to="projects/screenshots/")
    caption = models.CharField(max_length=160, blank=True)

    def __str__(self):
        return self.caption or self.project.title


class Certification(TimeStampedModel):
    certificate_name = models.CharField(max_length=180)
    organization = models.CharField(max_length=180)
    issue_date = models.DateField(null=True, blank=True)
    certificate_image = models.ImageField(upload_to="certifications/", blank=True)
    certificate_url = models.URLField(blank=True)

    def __str__(self):
        return self.certificate_name


class Service(TimeStampedModel):
    icon_class = models.CharField(max_length=80, blank=True)
    title = models.CharField(max_length=140)
    description = models.TextField()

    def __str__(self):
        return self.title


class Achievement(TimeStampedModel):
    achievement = models.CharField(max_length=180)
    competition = models.CharField(max_length=180, blank=True)
    award = models.CharField(max_length=180, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="achievements/", blank=True)

    def __str__(self):
        return self.achievement


class CodingProfile(TimeStampedModel):
    platform = models.CharField(max_length=120)
    icon_class = models.CharField(max_length=80, blank=True)
    profile_url = models.URLField()
    username = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return self.platform


class Statistic(TimeStampedModel):
    label = models.CharField(max_length=120)
    value = models.PositiveIntegerField(default=0)
    suffix = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.label


class GalleryImage(TimeStampedModel):
    title = models.CharField(max_length=140)
    image = models.ImageField(upload_to="gallery/")
    caption = models.TextField(blank=True)

    def __str__(self):
        return self.title


class TimelineItem(TimeStampedModel):
    TIMELINE_TYPES = [
        ("learning", "Learning Journey"),
        ("career", "Career Timeline"),
        ("education", "Education Timeline"),
    ]
    timeline_type = models.CharField(max_length=20, choices=TIMELINE_TYPES)
    title = models.CharField(max_length=160)
    period = models.CharField(max_length=80)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Testimonial(TimeStampedModel):
    name = models.CharField(max_length=140)
    photo = models.ImageField(upload_to="testimonials/", blank=True)
    position = models.CharField(max_length=140, blank=True)
    company = models.CharField(max_length=140, blank=True)
    review = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)

    def __str__(self):
        return self.name


class BlogCategory(TimeStampedModel):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name_plural = "Blog Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(TimeStampedModel):
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class BlogPost(TimeStampedModel, SEOModel):
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True, blank=True)
    featured_image = models.ImageField(upload_to="blog/", blank=True)
    excerpt = models.TextField()
    content = models.TextField()
    published_at = models.DateTimeField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:blog_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=140)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    subject = models.CharField(max_length=180)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject}"


class PolicyPage(TimeStampedModel, SEOModel):
    PAGE_TYPES = [
        ("privacy", "Privacy Policy"),
        ("terms", "Terms & Conditions"),
    ]
    page_type = models.CharField(max_length=20, choices=PAGE_TYPES, unique=True)
    title = models.CharField(max_length=160)
    content = models.TextField()

    def __str__(self):
        return self.title
