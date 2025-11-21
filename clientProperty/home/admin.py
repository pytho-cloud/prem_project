from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (
    Property, Lead, Project, ContactMessage,
    FeatureListing, BannerModel, PropertyImage
)

# -------------------------
# PROPERTY IMAGES INLINE
# -------------------------
class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3  # Show 3 blank upload fields by default
    fields = ('image',)
    readonly_fields = ()

# -------------------------
# PROPERTY ADMIN
# -------------------------
@admin.register(Property)
class PropertyAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('project_name', 'name', 'location', 'price', 'bhk_type')
    search_fields = ('name', 'location')
    list_filter = ('bhk_type', 'location', 'price')
    inlines = [PropertyImageInline]  # Attach inline images


# -------------------------
# PROPERTY IMAGE ADMIN (OPTIONAL)
# -------------------------
@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'image')
    search_fields = ('property__name',)


# -------------------------
# LEAD ADMIN
# -------------------------
@admin.register(Lead)
class LeadAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = (
        'name',
        'phone',
        'email',
        'project_name',
        'property_name',
        'location',
        'bhk_type',
        'price',
        'created_at',
    )
    search_fields = (
        'name',
        'phone',
        'email',
        'project_name',
        'property_name',
        'location',
        'bhk_type',
    )
    list_filter = ('created_at', 'project_name', 'location', 'bhk_type')
    ordering = ('-created_at',)


# -------------------------
# PROJECT ADMIN
# -------------------------
@admin.register(Project)
class ProjectAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('project_name', 'city', 'propert_bhk')
    search_fields = ('project_name', 'city')
    list_filter = ('city', 'propert_bhk')


# -------------------------
# CONTACT MESSAGE ADMIN
# -------------------------
@admin.register(ContactMessage)
class ContactMessageAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'email', 'contact', 'subject', 'created_at')
    search_fields = ('name', 'email', 'contact', 'subject')
    list_filter = ('created_at',)


# -------------------------
# FEATURE LISTING ADMIN
# -------------------------
@admin.register(FeatureListing)
class FeatureListingAdmin(ImportExportModelAdmin):
    list_display = (
        'property',
        'featured_project_name',
        'featured_location',
        'featured_price',
        'is_active'
    )
    list_filter = ('is_active',)


# -------------------------
# BANNER ADMIN
# -------------------------
@admin.register(BannerModel)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle", "banner_image", "is_active")
