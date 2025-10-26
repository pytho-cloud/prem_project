from django.db import models

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
    description = models.TextField(blank=True)
    bhk_type = models.CharField(max_length=10, choices=BHK_CHOICES, default='2BHK')
    brochure = models.FileField(upload_to='property_brochures/', blank=True, null=True)
    # most_recent = models.BooleanField(default=False)
    


    def __str__(self):
        return f"{self.name} - {self.location}"


class Lead(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email =models.EmailField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    token  = models.TextField(null=True,blank=True)

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




from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
