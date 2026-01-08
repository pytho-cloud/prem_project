from django.shortcuts import render 
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from .models import Property, Lead ,ContactMessage 
import json
from  .filters import generate_key
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.http import FileResponse, HttpResponseBadRequest
from .utils import *
from .models import Property ,FeatureListing, Review, Appoinment


from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404
from .models import (
    Property,
    BannerModel,
    FeatureListing,
    Slogan,
    Review,
    AboutModel,
    PropertyCountModel,
    Appoinment,
)

def home(request):

    # -------------------------------------------------
    # 🔹 BROCHURE DOWNLOAD (GET request)
    # -------------------------------------------------
    download_id = request.GET.get("download_id")
    if download_id:
        prop = get_object_or_404(Property, id=download_id)

        if not prop.brochure:
            raise Http404("Brochure not found")

        try:
            response = FileResponse(
                open(prop.brochure.path, "rb"),
                content_type="application/pdf"
            )
            response["Content-Disposition"] = (
                f'attachment; filename="{prop.name}_brochure.pdf"'
            )
            return response
        except:
            raise Http404("Could not open brochure file")

    # -------------------------------------------------
    # 🔹 POST REQUEST HANDLING
    # -------------------------------------------------
    if request.method == "POST":

        # ---------- Review Form ----------
        if "comment" in request.POST:
            name = request.POST.get("name")
            comment = request.POST.get("comment")
            image = request.FILES.get("image") or "review_images/user.jpg"

            if comment:
                Review.objects.create(
                    name=name,
                    comment=comment,
                    image=image,
                    is_active=False
                )
            return redirect("home")

        # ---------- General Appointment ----------
        elif "ph_number" in request.POST and "property_name" not in request.POST:
            name = request.POST.get("name")
            ph_number = request.POST.get("ph_number")
            message = request.POST.get("message")

            if name and ph_number:
                Appoinment.objects.create(
                    name=name,
                    ph_number=ph_number,
                    message=message
                )
            return redirect("home")

        # ---------- Property Enquiry ----------
        elif "property_name" in request.POST:
            name = request.POST.get("name")
            ph_number = request.POST.get("ph_number")
            message = request.POST.get("message")
            property_name = request.POST.get("property_name")

            if name and ph_number:
                Appoinment.objects.create(
                    name=name,
                    ph_number=ph_number,
                    message=f"Property Enquiry: {property_name}\n{message or ''}"
                )
            return redirect("home")

    # -------------------------------------------------
    # 🔹 NORMAL PAGE DATA
    # -------------------------------------------------
    context = {
        "properties": Property.objects.all()[:6],
        "banners": BannerModel.objects.filter(is_active=True),
        "featured": FeatureListing.objects.filter(is_active=True).select_related("property"),
        "slogan": Slogan.objects.filter(is_active=True).first(),
        "about_items": AboutModel.objects.filter(is_active=True),
        "counters": PropertyCountModel.objects.filter(is_active=True),
        "reviews": Review.objects.filter(is_active=True),
    }

    return render(request, "home.html", context)


# 📞 Lead Form
@csrf_exempt
def save_lead(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            name = data.get("name")
            phone = data.get("phone")

            if not name or not phone:
                return JsonResponse({"error": "Please fill in all fields."}, status=400)

            Lead.objects.create(name=name, phone=phone)
            return JsonResponse({"message": "Thank you! We'll contact you soon."}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)




# def contact(request):

#     print("this is contact page with working condition ")

#     return render(request,'contact.html')

# ℹ️ About Page
def about(request):
    return render(request, "about.html")



def properties(request):
    properties = Property.objects.all()

    print("this is my sessions" , request.session.get('name'))

    q = request.GET.get('q')
    bhk = request.GET.get('bhk')
    sq_ft = request.GET.get('sq_ft')

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # --- Filtering ---
    if q:
        properties = properties.filter(
            Q(name__icontains=q) | Q(location__icontains=q)
        )

    if sq_ft:
        properties = properties.filter(
            Q(sq_ft__icontains = sq_ft)
        )
    if bhk:
        if bhk == '4':  # 4+ BHK case
            properties = properties.filter(bhk_type__gte=4)
        else:
            print(bhk,"this is my bhk")
            value = str(bhk) + "BHK"
            print(value,"this is my data",value)
            properties = properties.filter(bhk_type=value)
            print("this is my property" , properties)

    if min_price:
        properties = properties.filter(price__gte=min_price)

    if max_price:
        properties = properties.filter(price__lte=max_price)

    # --- Pagination ---
    paginator = Paginator(properties, 6)  # Show 6 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "properties": page_obj,
        "page_obj": page_obj,
    }
    print(context,"this is my data ")

    return render(request, "properties.html", context)

        

def single_product_view(request):
    id = request.GET.get('id')
    if not id:
        return redirect('properties')

    property_obj = get_object_or_404(Property, id=id)

    # 👇 Fetch all gallery images for this property
    gallery_images = property_obj.images.all()

    return render(
        request,
        'single_product.html',
        {
            'property': property_obj,
            'gallery_images': gallery_images
        }
    )






def submit_contact(request):
    if request.method == "POST":
        name = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        property_id = request.POST.get("property_id")
        page = request.POST.get("page")  # ✅ get 'page' from hidden input or form data

        # Save lead (assuming generate_key and Lead model exist)
        token = generate_key(len(email))
        Lead.objects.create(name=name, email=email, phone=phone, token=token)

        # ✅ Save session info
        request.session['name'] = name
        request.session['email'] = email
        request.session['phone'] = phone
        request.session['form_filled'] = True
        request.session.modified = True

        messages.success(request, "Thank you! You can now download brochures directly.")

        # ✅ Redirect based on page value
  
    # If not POST, just go to properties
    return redirect('properties')




def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        contact = request.POST.get('phone', '').strip()

        subject = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()

        # Save to DB (optional)
        ContactMessage.objects.create(
            name=name,
            email=email,
            contact=contact,
            subject=subject,
            message=message_text
            
        ).save()

        # Instead of staying on the same page, redirect to WhatsApp chat
        # whatsapp_message = f"Hi Nesto, I just sent you a message from the website. My name is {name}."
        # whatsapp_url = f"https://wa.me/919167208204?text={whatsapp_message.replace(' ', '%20')}"
        # return redirect(whatsapp_url)

    return redirect("/")





def getBanner(request):

    banner = Property.objects.order_by('-id')[:3]



def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        property_id = request.POST.get("property_id")
        page = request.POST.get("page")

        # ✅ Store user data in session
        request.session['name'] = username
        request.session['email'] = email
        request.session['phone'] = phone
        request.session.modified = True

        # ✅ Corrected redirect logic
        if page == 'home':
            return redirect('/')   # ✅ must use return
        else:
            return redirect('properties')  # ✅ only happens if page != home

    # GET request → render form
    return render(request, 'form.html')





def download_brochure(request):
  
    property_id = request.GET.get("id")
    print("Received brochure download ID:", property_id)

    if not property_id:
        return HttpResponseBadRequest("Missing id")

    try:
        prop = Property.objects.get(id=property_id)
    except Property.DoesNotExist:
        return HttpResponseBadRequest("Invalid property id")

    # brochure file should be prop.brochure (FileField)
    brochure = prop.brochure  

    if not brochure:
        return HttpResponseBadRequest("No brochure found for this property")

    # call your lead function (optional)
    addLeads(request, property_id)

    # correct file response
    return FileResponse(
        brochure.open("rb"),
        as_attachment=True,
        filename=brochure.name.split("/")[-1]   # correct filename
    )
    
    

# def appointment_view(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         ph_number = request.POST.get("ph_number")
#         message = request.POST.get("message")

#         Appoinment.objects.create(
#             name=name,
#             ph_number=ph_number,
#             message=message
#         )

#         return redirect("appoinment")  # reload page after submit

#     return render(request, "home.html")