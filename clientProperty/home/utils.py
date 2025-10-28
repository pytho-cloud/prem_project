from .models import *




def addLeads(request, id):

    property = Property.objects.get(id=id)

    name = request.session['name']
    phone = request.session['phone']
    email = request.session['email']
    print("add leads" ,name)
    property_name = property.name
    project_name = property.project_name
    location = property.location
    bhk_type = property.bhk_type
    price = property.price

    create_leads = Lead.objects.create(
        name=name,
        phone=phone,
        email=email,
        project_name=project_name,
        property_name=property_name,
        location=location,
        price=price
    )

    create_leads.save()

    return property.name  ,property.brochure