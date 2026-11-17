from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from django.db.models import Q
from django.contrib.auth import authenticate

# Create your views here.

def weather(request):
    from .getWeather import main

    data = main()
    if request.POST:
        location = request.POST['location']
        data = main(location)
    context = {
        'location_name': data['location']['name'],
        'region': data['location']['region'],
        'country': data['location']['country'],
        'local_time': data['location']['localtime'],
        'temperature_c': data['current']['temp_c'],
        'temperature_f': data['current']['temp_f'],
        'condition_text': data['current']['condition']['text'],
        'icon_url': 'https://' + data['current']['condition']['icon'],  # Add 'https://' to the icon URL
        'wind_kph': data['current']['wind_kph'],
        'wind_direction': data['current']['wind_dir'],
        'humidity': data['current']['humidity'],
        'pressure_mb': data['current']['pressure_mb'],
        'visibility_km': data['current']['vis_km'],
        'uv_index': data['current']['uv']
    }
    return render(request,"weather.html",context)



def index(request):
    return render(request,"index.html")


def userregistration(request):
    msg = ''
    if request.method == 'POST':
        name = request.POST['fullname']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        if CustomUser.objects.filter(username=email).exists():
            messages.info(request,'Username/email already registred..')
            return redirect("/userregistration")
        elif User.objects.filter(Q(phone=phone)).exists() or Supplier.objects.filter(Q(phone=phone)).exists():
            messages.info(request,'Phone number already registred..')
            return redirect("/userregistration")
        else:
            usr = CustomUser.objects.create_user(
                username=email, password=password, is_active=0, usertype='User')
            usr.save()
            par = User.objects.create(
                name=name, email=email, phone=phone, address=address, user=usr)
            par.save()
            messages.info(request,"Regisgtered Successfull...")
            return redirect('/userregistration')
    else:
        return render(request,"userregistration.html",{"msg":msg})
    

def supplierreg(request):
    msg = ''
    if request.method == 'POST':
        companyname = request.POST['fullname']
        ownername = request.POST['ownername']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        license = request.FILES['license']
        if CustomUser.objects.filter(username=email).exists():
            messages.info(request,'Username/email already registred..')
            return redirect("/supplierreg")
        elif User.objects.filter(Q(phone=phone)).exists() or Supplier.objects.filter(Q(phone=phone)).exists():
            messages.info(request,'Phone number already registred..')
            return redirect("/supplierreg")
        else:
            usr = CustomUser.objects.create_user(
                username=email, password=password, is_active=0, usertype='Supplier')
            usr.save()
            par = Supplier.objects.create(
                compnay_name=companyname,owner_name=ownername, email=email, phone=phone, address=address,proof=license, user=usr)
            par.save()
            messages.info(request,"Regisgtered Successfull...")
            return redirect('/supplierreg')
    else:
        return render(request,"supplierreg.html")
    
def login(request):
    msg = ""
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        auth = authenticate(username=email, password=password)

        if auth is not None:

            if auth.is_superuser:
                return redirect("/adminHome")
            elif auth.usertype == 'User':
                st = User.objects.get(email=email)
                request.session['id'] = st.id
                return redirect("/userHome")
            elif auth.usertype == 'Supplier':
                st = Supplier.objects.get(email=email)
                request.session['id'] = st.id
                return redirect("/supplierHome")
        else:
            msg = "Invalid username/password!"
            return render(request, "login.html", {"msg": msg})
    else:
        return render(request,"login.html",{"msg":msg})
    

def adminHome(request):
    return render(request,"adminHome.html")


def adminUser(request):
    data=User.objects.filter().order_by("-id")
    return render(request,"adminUser.html",{"data":data})


def adm_app_user(request):
    id = request.GET['id']
    status = request.GET['status']
    data = CustomUser.objects.get(id=id)
    if status=='active':
        data.is_active = 1
    else:
        data.is_active = 0
    data.save()
    return redirect("/adminUser")



def adminSupplier(request):
    data=Supplier.objects.filter().order_by("-id")
    return render(request,"adminSupplier.html",{"data":data})



def adm_app_supplier(request):
    id = request.GET['id']
    status = request.GET['status']
    data = CustomUser.objects.get(id=id)
    if status=='active':
        data.is_active = 1
    else:
        data.is_active = 0
    data.save()
    return redirect("/adminSupplier")

def adminProducts(request):
    data=Product.objects.filter().order_by("-id")
    return render(request,"adminProducts.html",{"data":data})

def adminApproveProduct(request):
    product_id = request.GET['product_id']
    status = request.GET['status']
    product = Product.objects.get(id=product_id)
    product.status = status
    product.save()
    return redirect('/adminProducts')

def adminBookings(request):
    data=Booking.objects.filter().exclude(status="CART").order_by("-id")
    return render(request,"adminBookings.html",{"data":data})

def adminFeedbacks(request):
    data=Feedback.objects.filter().order_by("-id")
    return render(request,"adminFeedbacks.html",{"data":data})


def supplierHome(request):
    return render(request,"supplierHome.html")

def supplierAdd(request):
    id=request.session['id']
    supplier=Supplier.objects.get(id=id)

    products=Product.objects.filter(supplier=supplier).order_by("-id")
    msg = ''
    if request.method == 'POST':
        productname = request.POST['productname']
        category = request.POST['category']
        description = request.POST['description']
        quantity = request.POST['quantity']
        price = request.POST['price']
        image = request.FILES.get('image')
        weather = request.POST['weather']
       
        product = Product.objects.create(
            supplier=Supplier.objects.get(id=supplier.id),
            name=productname,
            category=category,  
            weather=weather,
            description=description,
            quantity=quantity,
            price=price,
            image=image
            
        )
        product.save()
        messages.info(request,"Product Added Successfully...")
        return redirect('/supplierAdd')
    else:
        return render(request,"supplierAdd.html",{"msg":msg,"products":products})
    
def addqty(request):
    if request.method == 'POST':
        product_id = request.POST['product_id']
        added_quantity = int(request.POST['quantity'])

        try:
            product = Product.objects.get(id=product_id)
            product.quantity += added_quantity
            product.save()
            messages.info(request, "Quantity updated successfully.")
        except Product.DoesNotExist:
            messages.error(request, "Product not found.")

    return redirect('/supplierAdd')

def supplierBooking(request):
    id=request.session['id']
    supplier=Supplier.objects.get(id=id)
    products=Product.objects.filter(supplier=supplier)
    bookings=Booking.objects.filter(product__in=products).exclude(status="CART").order_by("-id")
    booking_total = sum(item.total_price for item in bookings)

    if request.method == 'GET' and 'booking_id' in request.GET and 'status' in request.GET:
        booking_id = request.GET['booking_id']
        status = request.GET['status']
        try:
            booking = Booking.objects.get(id=booking_id, product__in=products)
            booking.status = status.upper()
            booking.save()
            messages.info(request, "Booking status updated successfully.")
        except Booking.DoesNotExist:
            messages.error(request, "Booking not found.")
        return redirect('/supplierBooking')
    return render(request,"supplierBooking.html",{"bookings":bookings,"booking_total":booking_total})

def supplierFeedback(request):
    id=request.session['id']
    supplier=Supplier.objects.get(id=id)
    products=Product.objects.filter(supplier=supplier)
    bookings=Booking.objects.filter(product__in=products).exclude(status="CART").order_by("-id")
    feedbacks=Feedback.objects.filter(booking__in=bookings).order_by("-id")
    return render(request,"supplierFeedback.html",{"feedbacks":feedbacks})

def userHome(request):
    return render(request,"userHome.html")

def userProduct(request):
    products=Product.objects.filter(status="Approved").order_by("-id")

    if request.method == 'POST':
        product_i=request.POST['product_id']
        quantity=request.POST['quantity']
        product=Product.objects.get(id=product_i)
        book = Booking.objects.filter(user=User.objects.get(id=request.session['id']),product=product,status="CART")
        if book.exists():
            book=book.first()
            book.quantity += int(quantity)
            book.total_price = float(book.total_price) + (float(product.price)*int(quantity))
            book.save()
            messages.info(request,"Product quantity updated in cart...")
            return redirect('/userProduct')
        booking=Booking.objects.create(
            user=User.objects.get(id=request.session['id']),
            product=product,
            quantity=quantity,
            status="CART",
            total_price=float(product.price)*int(quantity),

        )
        booking.save()
        messages.info(request,"Product added to cart...")
        return redirect('/userProduct')

    
    return render(request,"userProduct.html",{"products":products})

def userSearch(request):
    products=Product.objects.filter().order_by("-id")

    if request.method == 'POST':
        search_query = request.POST.get('search', '')
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(weather__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    return render(request,"userProduct.html",{"products":products})

def userCart(request):
    id=request.session['id']
    user=User.objects.get(id=id)
    bookings=Booking.objects.filter(user=user,status="CART").order_by("-id")
    cart_total = sum(item.total_price for item in bookings)

    if request.method == 'POST':
        booking_id = request.POST['item_id']
        new_quantity = int(request.POST['quantity'])
        try:
            booking = Booking.objects.get(id=booking_id, user=user, status="CART")
            booking.quantity = new_quantity
            booking.total_price = float(booking.product.price) * new_quantity
            booking.save()
            messages.info(request, "Cart updated successfully.")
        except Booking.DoesNotExist:
            messages.error(request, "Booking item not found.")
        return redirect('/userCart')
    return render(request,"userCart.html",{"bookings":bookings,"cart_total":cart_total})

def remove_fromCart(request):
    if request.method == 'POST':
        booking_id = request.POST['item_id']
        id=request.session['id']
        user=User.objects.get(id=id)
        try:
            booking = Booking.objects.get(id=booking_id, user=user, status="CART")
            booking.delete()
            messages.info(request, "Item removed from cart.")
        except Booking.DoesNotExist:
            messages.error(request, "Booking item not found.")
    return redirect('/userCart') 

from django.utils import timezone
def payment(request):
    id=request.session['id']
    user=User.objects.get(id=id)
    bookings=Booking.objects.filter(user=user,status="CART").order_by("-id")
    cart_total = sum(item.total_price for item in bookings)

    if request.method == 'POST':
        for booking in bookings:
            booking.status = "BOOKED"
            booking.payment_date = timezone.now()
            booking.product.quantity -= booking.quantity
            booking.product.save()
            booking.save()
        messages.info(request, "Payment successful. Thank you for your purchase!")
        return redirect('/userBookings')

    return render(request,"payment.html",{"bookings":bookings,"cart_total":cart_total})

def userBookings(request):
    id=request.session['id']
    user=User.objects.get(id=id)
    bookings=Booking.objects.filter(user=user).exclude(status="CART").order_by("-id")
    booking_total = sum(item.total_price for item in bookings)

    if request.method == 'GET' and 'booking_id' in request.GET and 'status' in request.GET:
        booking_id = request.GET['booking_id']
        status = request.GET['status']
        try:
            booking = Booking.objects.get(id=booking_id, user=user)
            booking.status = status.upper()
            booking.save()
            messages.info(request, "Booking status updated successfully.")
        except Booking.DoesNotExist:
            messages.error(request, "Booking not found.")
        return redirect('/userBookings')

    return render(request,"userBookings.html",{"bookings":bookings,"booking_total":booking_total})

def userAddFeedback(request):
   booking_id = request.GET['booking_id']
   if request.method == 'POST':
        comments = request.POST['comment']
        rating = request.POST['rating']
        booking = Booking.objects.get(id=booking_id)
        feedback = Feedback.objects.create(
            booking=booking,
            rating=rating,
            comments=comments
        )
        booking.status = "FEEDBACK SUBMITTED"
        booking.save()
        feedback.save()
        messages.info(request, "Feedback submitted successfully.")
        return redirect('/userBookings')
   else:

    return render(request,"userAddFeedback.html")
   

def userProfile(request):
    id=request.session['id']
    user=User.objects.get(id=id)
    if request.method == 'POST':
        name= request.POST['fullname']
        email= request.POST['email']
        phone= request.POST['phone']
        address= request.POST['address']
        password= request.POST['password']


        if CustomUser.objects.filter(username=email).exclude(id=user.user.id).exists():
            messages.info(request,'Username/email already registred..')
            return redirect("/userProfile")

        user.name = name
        if email != user.email:
            user.user.username = email
            user.user.save()
        user.email = email
        user.phone = phone
        user.address = address
        if password:
            user.user.set_password(password)
            user.user.save()
        user.save()
        messages.info(request, "Profile updated successfully.")
        return redirect('/userProfile')
    return render(request,"userProfile.html",{"user":user})