from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from django.utils.html import format_html
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

@admin.register(Slogan)
class SloganAdmin(admin.ModelAdmin):
    list_display = ("text", "created_at","is_active","is_banner_slogen","is_banner_sub_slogen")
    
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")



@admin.register(AboutModel)
class AboutModelAdmin(admin.ModelAdmin):
    list_display = ('heading', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('heading',)


@admin.register(PropertyCountModel)
class AboutModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'counts')
    list_filter = ('is_active',)
    search_fields = ('name',)



@admin.register(Appoinment)
class AppoinmentModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'ph_number','message')
    list_filter = ('name',)
    search_fields = ('name',)
    
    
@admin.register(WhyChooseUs)
class WhyChooseUsAdmin(admin.ModelAdmin):
    list_display = ('icon_preview', 'title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    ordering = ('order',)
    search_fields = ('title',)

    def icon_preview(self, obj):
        if obj.icon_class:
            return format_html(
                '<i class="{}" style="font-size:20px;color:#007bff;"></i>',
                obj.icon_class
            )
        return "-"
    icon_preview.short_description = "Icon"
