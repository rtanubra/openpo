from django.shortcuts import render, redirect
from .models import *
from .filters import *
from .forms import *
from datetime import date 
from django.forms import inlineformset_factory
from django.conf import settings

from django.contrib.auth.decorators import login_required
# Create your views here.
def dashboard(request):
    #landing page. 
    user = request.user 
    try:
        seller = user.seller
        return redirect('seller_products')
    except:
        context = {}
        
    return render(request,'store/dashboard.html',context)



########################## AUTH VIEWS ##########################
def register_seller(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context={
        'form':form
    }
    return render(request,'store/users/register.html',context)
########################## LIST VIEWS ##########################
@login_required
def seller_customers(request):
    user = request.user
    #if User does not have a seller (vendor account yet)
    try:
        seller_user = user.seller
    except:
        return redirect('create_seller')
    customers = seller_user.customer_set.all()
    total_customers = customers.count()
    myFilter = CustomerFilter(request.GET, queryset=customers)
    customers= myFilter.qs
    context = {
        "total_customers":total_customers,
        'customers':customers,
        'myFilter':myFilter
    }


    return render(request,'store/customer/seller_customers.html',context)

@login_required
def seller_locations(request):
    user = request.user
    try:
        seller_user = user.seller
    except:
        return redirect('create_seller')
    pickup_locations = seller_user.location_set.all()
    total_locations = pickup_locations.count()

    myFilter = LocationFilter(request.GET,queryset=pickup_locations)
    pickup_locations = myFilter.qs

    context = {
        'locations' :pickup_locations,
        'total_locations':total_locations,
        'myFilter':myFilter
    }
    return render(request,'store/location/seller_locations.html',context)
@login_required
def seller_products(request):
    user = request.user
    #if User does not have a seller (vendor account yet)
    try:
        seller_user = user.seller
    except:
        return redirect('create_seller')
    products = seller_user.product_set.all()
    total_products = products.count()
    total_active_products = products.filter(active=True).count()
    total_inactive_products = total_products - total_active_products

    myFilter = ProductFilter(request.GET, queryset= products)
    products= myFilter.qs
    context = {
        'seller':seller_user,
        'products':products,
        'total_products':total_products,
        'total_active_products':total_active_products,
        'total_inactive_products':total_inactive_products,
        'myFilter':myFilter
    }
    return render(request,'store/product/seller_products.html',context)

@login_required
def seller_baskets(request):
    user = request.user
    #if User does not have a seller (vendor account yet)
    try:
        seller_user = user.seller
    except:
        return redirect('create_seller')
    baskets = seller_user.basket_set.all()
    
    total_baskets = baskets.count()
    total_delivered_baskets = baskets.filter(status='Delivered').count()
    total_active_baskets = total_baskets - total_delivered_baskets

    myFilter = BasketFilter(request.GET,queryset=baskets,request=request)
    
    baskets = myFilter.qs
    #Required to see the total cost of the basket 
        #Must be done after filtering since costs are not a part of any specific table. They are calculated based on current costs.
    for basket in baskets:
        orders = basket.order_set.all()
        cost = 0

        for order in orders:
            print(order.product)
            print(order.product.price)
            cost += order.product.price
        basket.cost=cost


    context = {
        'baskets':baskets,
        'total_baskets':total_baskets,
        'total_active_baskets':total_active_baskets,
        'total_delivered_baskets':total_delivered_baskets,
        'myFilter':myFilter
    }
    return render(request,'store/basket/seller_baskets.html',context)



########################## Edit VIEWS ##########################
@login_required
def edit_basket(request,basket_id):
    user = request.user
    #if User does not have a seller (vendor account yet)
    try:
        seller_user = user.seller
    except:
        return redirect('create_seller')
    
    if request.method == 'POST':
        #old basket
        basket = seller_user.basket_set.get(id=basket_id)

        #pull information from form
        customer_id = request.POST.get('customer') 
        pickup_id = request.POST.get('pickup')
        status = request.POST.get('status')
        customer = Customer.objects.get(id=customer_id)
        pickup_location = Location.objects.get(id=pickup_id)
        note = request.POST.get('note')
        
        #edit my basket
        basket.pickup_location = pickup_location
        basket.customer= customer
        basket.status = status
        basket.note = note
        
        #delete orders
        basket.order_set.all().delete()
        #keep the same date of creation for orders
        today = basket.date_created

        #Create orders for the basket 
        products = seller_user.product_set.filter(active=True)
        orders = []
        for product in products:
            current_product = int(request.POST.get('order_product_'+str(product.id)))
            if current_product>0:
                orders.append(Order(product=product,basket=basket,date_created=today,quantity=current_product))
        Order.objects.bulk_create(orders)

        #save changes
        basket.save()
        #completed
        return redirect('seller_baskets')
    
    #Creating context for the form
    products = seller_user.product_set.all()
    for p in products:
        p.number = 0
    customers = seller_user.customer_set.all()
    pickup_locations= seller_user.location_set.all()
    statuses = ['Pending','Out for delivery','Delivered']
    context = {
        'seller_user':seller_user,
        'customers':customers,
        'pickup_locations':pickup_locations,
        'statuses':statuses
    }    
    try :

        basket = seller_user.basket_set.get(id=basket_id)
        orders = basket.order_set.all()
        current_customer = basket.customer
        current_pickup_location = basket.pickup_location
        current_status = basket.status
        #Assign the current ordered quantity for the product.
        for o in orders:
            for p in products:
                if o.product.id == p.id:
                    p.number = o.quantity
        context['basket'] = basket
        context['products'] = products
        context['current_customer'] = current_customer
        context['current_pickup_location']= current_pickup_location
        context['current_status']= current_status
    except :
        #Could not locate the basket
        print('something went wrong')
        return redirect('seller_baskets')
        
    
    return render(request,'store/basket/edit_basket.html',context)

@login_required
def edit_product(request,product_id):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    user = request.user
    #if User does not have a seller (vendor account yet)
    try:
        seller_user = user.seller
    except:
        return redirect('create_seller')
    context= {}
    try:
        #identify if the url is correct
        product = seller_user.product_set.get(id=product_id)
        
        if request.method == 'POST':
            form = ProductForm(request.POST,instance=product)
            if form.is_valid():
                form.save()
                return redirect('seller_products')
        else:
            form = ProductForm(instance= product)
            context['form']=form
    except:
        #Could not locate the product
        return redirect('seller_products')
    
    return render(request,'store/product/product_form.html',context)
@login_required
def edit_customer(request,pk):
    user = request.user
    #if User does not have a seller (vendor account yet)
    try:
        seller= user.seller
    except:
        return redirect('create_seller')
    try:
        customer = seller.customer_set.get(id=pk)
        if request.method == 'POST':
            form =  CustomerForm(request.POST,instance=customer)
            if form.is_valid():
                form.save()
            return redirect('seller_customers')

        form = CustomerForm(instance=customer)
    except:
        return redirect('seller_customers')
    
    context = {
        'form':form,
        'customer':customer
    }
    return render(request,'store/customer/edit_customer.html',context)

@login_required
def edit_location(request,pk):
    user = request.user
    #if User does not have a seller (vendor account yet)
    try:
        seller= user.seller
    except:
        return redirect('create_seller')
    try:
        print(seller.location_set.all())
        print(seller.location_set.get(id=pk))
        location = seller.location_set.get(id=pk)
        if request.method == 'POST':
            form = LocationForm(request.POST,instance=location)
            if form.is_valid():
                form.save()
            return redirect('seller_locations')
        
        form = LocationForm(instance=location)
    except:
        return redirect('seller_locations')
    
    context = {
        'form':form,
        'location':location
    }
    return render(request,'store/location/edit_location.html',context)
########################## Create VIEWS ##########################
@login_required  
def create_product(request):
    user = request.user
    #if User does not have a seller (vendor account yet)
    try:
        seller_user = user.seller
    except:
        return redirect('create_seller')
    if request.method == 'POST':
        form = ProductForm(request.POST)
        form.seller= seller_user.id

        if form.is_valid():
            new_product = form.save()
            new_product.seller = seller_user
            new_product.save()
            return redirect('seller_products')
        else: 
            print('something is wrong')
    form = ProductForm()
    context = {
        'form':form,
        'seller_user':seller_user
    }
    return render(request,'store/product/product_form.html',context)

@login_required
def create_locations(request):
    user = request.user
    try:
        seller = user.seller
    except:
        return redirect('create_seller')
    LocationFormSet= inlineformset_factory(Seller,Location,fields=('name',),extra=5)
    formset = LocationFormSet(queryset=Location.objects.none(),instance=seller)
    if request.method == 'POST':
        formset= LocationFormSet(request.POST, instance = seller)
        if formset.is_valid():
            formset.save()
            return redirect('seller_locations')
    context = {
        'formset':formset
    }
    return render(request,'store/location/create_locations.html',context)
@login_required
def create_customers(request):
    user = request.user
    #if User does not have a seller (vendor account yet)
    try:
        seller= user.seller
    except:
        return redirect('create_seller')
    CustomerFormSet = inlineformset_factory(Seller,Customer,fields=('name','phone','email'),extra=5)
    formset = CustomerFormSet(queryset=Customer.objects.none(),instance=seller)
    if request.method == 'POST':
        formset = CustomerFormSet(request.POST, instance= seller)
        if formset.is_valid():
            formset.save()
            return redirect('seller_customers')
    context = {
        'formset':formset
    }
    return render(request,'store/customer/create_customers.html',context)

@login_required
def create_basket(request):
    user = request.user
    #if User does not have a seller (vendor account yet)
    try:
        seller_user = user.seller
    except:
        return redirect('create_seller')
    
    if request.method == "POST":
        #Create Basket
        customer_id = request.POST.get('customer') 
        pickup_id = request.POST.get('pickup')
        customer = Customer.objects.get(id=customer_id)
        pickup_location = Location.objects.get(id=pickup_id)
        note = request.POST.get('note')
        today = date.today()
        basket = Basket(
            seller=seller_user,customer=customer,
            status='Pending',pickup_location=pickup_location,
            date_created= today,note=note
        )
        basket.save()

        #Create orders for the basket 
        products = seller_user.product_set.filter(active=True)
        orders = []
        for product in products:
            current_product = int(request.POST.get('order_product_'+str(product.id)))
            if current_product>0:
                orders.append(Order(product=product,basket=basket,date_created=today,quantity=current_product))
        Order.objects.bulk_create(orders)

        #completed
        return redirect('seller_baskets')
  
    products = seller_user.product_set.filter(active=True)
    customers = seller_user.customer_set.all()
    pickup_locations= seller_user.location_set.all()
    context = {
        'products':products,
        'seller_user':seller_user,
        'customers':customers,
        'pickup_locations':pickup_locations
    }

    return render(request,'store/basket/create_basket.html',context)
@login_required
def create_seller(request):
    user = request.user
    if request.method == 'POST':
        form = SellerForm(request.POST)
        if form.is_valid():
            seller = form.save()
            seller.user=user
            seller.save()
            print(seller)
            return redirect('seller_products')
    #double negative logic if the user already has seller we can send them back to products page.
    try:
        seller_user = user.seller 
        return redirect('seller_products')
        context = {}
    #if they do not then we register this stuff
    except:
        #does not have a seller account
        form  = SellerForm()
        context= {
            'form':form
        }
    return render(request,'store/seller/create_seller.html',context)
########################## Delete VIEWS ##########################
@login_required
def delete_basket(request,basket_id):
    user = request.user
    #if User does not have a seller (vendor account yet)
    try:
        seller_user = user.seller
    except:
        return redirect('create_seller')
    
    context = {}
    if request.method == 'POST':
        try :
            basket = seller_user.basket_set.get(id=basket_id)
            basket.delete()
        except:
            #Could not locate the basket 
            return redirect('seller_baskets')
    try :
        basket = seller_user.basket_set.get(id=basket_id)
        context['item']= basket
    except:
        #Could not locate the basket 
        return redirect('seller_baskets')
    return render(request,'store/delete/delete_template.html',context)














@login_required
def delete_product(request,product_id):
    user = request.user
    #if User does not have a seller (vendor account yet)
    try:
        seller_user = user.seller
    except:
        return redirect('create_seller')
    try:
        product = seller_user.product_set.get(id=product_id)
        if request.method == 'POST':
            product.delete()
            return redirect('seller_products')
        
    except:
        #if cannot locate that product for the seller
        return redirect('seller_products')
    
    context = {
        'item':product
    }
    return render(request,'store/delete/delete_template.html',context)







@login_required
def delete_customer(request,pk):
    user = request.user
    try:
        seller = user.seller
    except:
        return redirect('create_seller')
    try:
        customer = seller.customer_set.get(id=pk)
        if request.method == 'POST':
            customer.delete()
            return redirect('seller_customers')
    except:
        # main error cannot locate the customer for this seller
        return redirect('seller_customers')
    context= {
        'item':customer
    }
    return render(request,'store/delete/delete_template.html',context)

####################### End of Views #######################




    