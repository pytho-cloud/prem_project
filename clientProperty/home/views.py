from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Property, Lead ,ContactMessage
import json
from  .filters import generate_key
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
# 🏠 Home Page with Filter
def home(request):
    # query = request.GET.get('query', '')
    # price_min = request.GET.get('price_min', '')
    # price_max = request.GET.get('price_max', '')
    # bhk = request.GET.get('bhk', '')

    # properties = Property.objects.all().order_by('-id')

    # # 🔍 Search
    # if query:
    #     properties = properties.filter(
    #         Q(name__icontains=query) |
    #         Q(location__icontains=query) |
    #         Q(description__icontains=query)
    #     )

    # # 💰 Price Filter
    # if price_min and price_max:
    #     try:
    #         min_val = int(price_min)
    #         max_val = int(price_max)
    #         properties = properties.filter(price__gte=min_val, price__lte=max_val)
    #     except ValueError:
    #         pass

    # # 🏡 BHK Filter
    # if bhk:
    #     properties = properties.filter(bhk_type=bhk)

    properties = Property.objects.all()

    banner = Property.objects.exclude(brochure='').order_by('-id')[:3]



    
    
   



    context = {
        'properties': properties,
        'banner': banner,

    }
    print("data is coming " , context)
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


from django.shortcuts import render
from .models import Property

def properties(request):
    properties = Property.objects.all()

    q = request.GET.get('q')
    bhk = request.GET.get('bhk')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # --- Filtering ---
    if q:
        properties = properties.filter(
            Q(name__icontains=q) | Q(location__icontains=q)
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

    return render(request, "properties.html", context)


# def submit_form(request):
    
#     # name = request.POST.get('name')
   
#     phone = request.POST.get('phone_number')
#     check_phone_number = Lead.objects.get(phone= phone)

#     token = request.POST.get('token')

#     if token :
#         return render(request,'properties.html')

#     if not check_phone_number:
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         token = request.POST.get('token')
#         lead = Lead.objects.create(name=name,phone=phone,email=email,token=token)
#         lead.save()

#         return render(request,'properties.html',{"token": token})

        

def submit_contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        property_id = request.POST.get("property_id")

        # Save lead
        token = generate_key(len(email))
        Lead.objects.create(name=name, email=email, phone=phone, token=token)

        # Mark that user has filled the form
        request.session['form_filled'] = True
        request.session.modified = True

        messages.success(request, "Thank you! You can now download brochures directly.")
        return redirect('properties')
    return redirect('properties')










def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()

        # Basic validation
        # if not name or not email or not subject or not message_text:
        #     messages.error(request, 'Please fill in all fields.')
        #     return redirect('contact')

        # Save to database (optional)
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message_text
        )

        # # Send email (optional)
        # send_mail(
        #     f"New Contact Message: {subject}",
        #     f"Name: {name}\nEmail: {email}\n\nMessage:\n{message_text}",
        #     settings.DEFAULT_FROM_EMAIL,
        #     [settings.DEFAULT_FROM_EMAIL],
        #     fail_silently=False,
        # )

        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')

    return render(request, 'contact.html')





def getBanner(request):

    banner = Property.objects.order_by('-id')[:3]
