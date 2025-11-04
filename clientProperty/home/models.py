from django.db import models
from multiselectfield import MultiSelectField  

class Property(models.Model):
    BHK_CHOICES = [
        ('1BHK', '1 BHK'),
        ('2BHK', '2 BHK'),
        ('3BHK', '3 BHK'),
        ('4BHK', '4 BHK'),
    ]

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="properties/", blank=True, null=True)
    location = models.CharField(max_length=255)
    price = models.IntegerField()
    short_description = models.TextField(blank=True)
    description = models.TextField(blank=True)
    bhk_type = models.CharField(null=True,blank=True,max_length=255)
    brochure = models.FileField(upload_to='property_brochures/', blank=True, null=True)
    partner_logo =  models.ImageField(upload_to="partners_logo/", blank=True, null=True)
    project_name =models.CharField(max_length=255,null=True,blank=True)
    floor_plane_image =  models.ImageField(upload_to="floor_plan/", blank=True, null=True)
    sq_ft = models.CharField(null=True,blank=True,max_length=255)
    phone_number =  models.CharField(max_length=20, null=True, blank=True)
    selling_status = models.CharField(  # ✅ New: Status field
        max_length=30,
        choices=[
            ('Ready to Move', 'Ready to Move'),
            ('Under Construction', 'Under Construction'),
            ('Sold Out', 'Sold Out')
        ],
        default='Ready to Move'
    )
    # most_recent = models.BooleanField(default=False)
    


    def __str__(self):
        return f"{self.name} - {self.location}"


class Lead(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email =models.EmailField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    token  = models.TextField(null=True,blank=True)
    project_name =models.CharField(max_length=255,null=True,blank=True)
    property_name = models.CharField(max_length=255,null=True)
    location = models.CharField(max_length=255,null=True)
    bhk_type = models.CharField(max_length=255,null=True)
    price = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"
    



class Project(models.Model):
    # Basic info
    project_name = models.CharField(max_length=255)
    project_description = models.TextField()
    # Location
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    # state = models.CharField(max_length=100)
    # zip_code = models.CharField(max_length=20)
    main_image = models.ImageField(upload_to='projects/')
    propert_bhk = models.CharField(max_length=255)


def __str__(self):
    return self.project_name






class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=20, null=True, blank=True)

    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"




class FeatureListing(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    featured_project_name = models.CharField(max_length=255, blank=True, null=True)
    featured_location = models.CharField(max_length=255, blank=True, null=True)
    featured_price = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.property:
            if not self.featured_project_name:
                self.featured_project_name = self.property.project_name
            if not self.featured_location:
                self.featured_location = self.property.location
            if not self.featured_price:
                self.featured_price = self.property.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.property.name} - Featured"







class BannerModel(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    subtitle = models.CharField(max_length=300, blank=True, null=True)
    banner_image = models.ImageField(upload_to="banner/slider/")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title if self.title else "Banner"
