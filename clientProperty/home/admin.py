from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Property, Lead, Project, ContactMessage

# Property Admin
@admin.register(Property)
class PropertyAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'location', 'price', 'bhk_type')
    search_fields = ('name', 'location')
    list_filter = ('bhk_type', 'location', 'price')  

# Lead Admin
@admin.register(Lead)
class LeadAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at')
    search_fields = ('name', 'phone', 'email')
    list_filter = ('created_at',)  # Filter by date created

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
