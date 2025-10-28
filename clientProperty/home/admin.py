from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Property, Lead, Project, ContactMessage

# Property Admin
@admin.register(Property)
class PropertyAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('project_name','name', 'location', 'price', 'bhk_type')
    search_fields = ('name', 'location')
    list_filter = ('bhk_type', 'location', 'price')  

# Lead Admin
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

    # ✅ Add all useful filters
    list_filter = (
        'created_at',
        'project_name',
        'location',
        'bhk_type',
    )

    ordering = ('-created_at',)

# Project Admin
@admin.register(Project)
class ProjectAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('project_name', 'city', 'propert_bhk')
    search_fields = ('project_name', 'city')
    list_filter = ('city', 'propert_bhk') 

# ContactMessage Admin
@admin.register(ContactMessage)
class ContactMessageAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('created_at',)  
