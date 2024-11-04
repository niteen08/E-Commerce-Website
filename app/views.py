from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced
from .forms import customerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponse
from django.db.models import Q
from django.http import JsonResponse
from .models import Cart, Product
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Sum
from django.db import transaction
from django.shortcuts import redirect
from django.http import Http404


 
class ProductView(View):
 def get(self,request):
  laptop = Product.objects.filter(category='L')
  mouse = Product.objects.filter(category='Mou')
  cpu = Product.objects.filter(category='C')
  return render(request,'app/home.html',{'laptop':laptop,'mouse':mouse,'cpu':cpu})

 

'''class productdetailView(View):
 def get(self,request,pk):
  product = Product.objects.get(pk=pk)
  return render(request,'app/productdetail.html',{'product':product})'''

@method_decorator(login_required,name='dispatch')
class ProductDetailView(View):
    template_name = 'app/productdetail.html'

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        
         
        # Check if the product is already in the cart
       # is_product_in_cart = Cart.objects.filter(product=product).exists()
        is_product_in_cart = Cart.objects.filter(user=request.user, product=product).exists()

        context = {
            'product': product,
            'is_product_in_cart': is_product_in_cart,
        }

        return render(request, self.template_name, context)


'''def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)

    # Check if the product is already in the cart
    cart_item, created = Cart.objects.get_or_create(user=user, product=product)

    # If the item is already in the cart, increase the quantity
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('/cart/')'''

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
     

    # Check if the product is already in the cart
    if not Cart.objects.filter(user=user, product=product).exists():
        
        # If not, add it to the cart
        Cart(user=user, product=product).save()
    else:   
     Cart.objects.filter(user=user, product=product).delete()
        

    return redirect('/cart/')


'''
@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')

    if product_id:
        # If prod_id is provided, it means the "Remove item" button was clicked
        # and you want to remove the product from the cart
        product = get_object_or_404(Product, id=product_id)
        Cart.objects.filter(user=user, product=product).delete()
    else:
        # If prod_id is not provided, it means the "Add to Cart" button was clicked
        # and you want to add the product to the cart
        product_id = request.GET.get('prod_id')
        product = get_object_or_404(Product, id=product_id)

        # Check if the product is already in the cart
        if not Cart.objects.filter(user=user, product=product).exists():
            # If not, add it to the cart
            Cart(user=user, product=product).save()

    return redirect('/cart/')'''




@login_required
def show_cart(request):
  if request.user.is_authenticated:
    user = request.user
    cart = Cart.objects.filter(user=user)
    #print(cart)
    amount = 0.0
    shipping_amount = 80.0
    total_amount = 0.0
    cart_product =[ p for p in Cart.objects.all() if p.user == user]
    #print(cart_product)
    if cart_product :
      for p in cart_product:
        tempamount =(p.quantity * p.product.discounted_price)
        amount += tempamount
        totalamount = amount + shipping_amount
      return render(request, 'app/addtocart.html',{'carts':cart, 'totalamount':totalamount,'amount':amount})
    else:
      return render(request,'app/emptycart.html')
    

def plus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity+=1
    c.save()
    amount = 0.0
    shipping_amount = 80.0
    cart_product = [ p for p in Cart.objects.all() if p.user == request.user]
    for p in cart_product:
        tempamount =(p.quantity * p.product.discounted_price)
        amount += tempamount 

    data ={
       'quantity': c.quantity,
       'amount': amount,
       'totalamount': amount + shipping_amount
        }
    return JsonResponse(data)






def buy_now(request):
 return render(request, 'app/buynow.html')

def contactus(request):
  return render(request,'app/contactus.html')

def aboutus(request):
  return render(request,'app/aboutus.html')

@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'add':add, 'active': 'btn-dark'})


@login_required
def orders(request):
 op =OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html',{'order_placed':op})




'''def laptop(request, data=None):
 if data == None:
  laptop = Product.objects.filter(category='L')
 elif data =='lenovo' or data =='dell':
  laptop = Product.objects.filter(category='L').filter(brand=data)
 return render(request, 'app/laptop.html',{'laptop':laptop})'''

def laptop(request, data=None):
    
    laptops = Product.objects.filter(category='L')

    if data == 'lenovo' or data == 'dell':
        laptops = laptops.filter(brand=data)
    return render(request, 'app/laptop.html', {'laptops': laptops})


class customerRegistrationView(View):
 def get(self, request):
  form = customerRegistrationForm
  return render(request, 'app/customerregistration.html',{'form':form})
 def post(self,request):  
  form = customerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request,' You Succesfully Ragistered Go to Login...')
   form.save()
  return render(request, 'app/customerregistration.html',{'form':form})
 
def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to the home page after logout
 
@login_required
def checkout(request):
     user = request.user
     add = Customer.objects.filter(user=user)
     cart_item = Cart.objects.filter(user=user)
     amount = 0.0
     shipping_amount = 80.0
     totalamount = 0.0
     cart_product =[ p for p in Cart.objects.all() if p.user == user]
    #print(cart_product)
     if cart_product :
      for p in cart_product:
        tempamount =(p.quantity * p.product.discounted_price)
        amount += tempamount
      totalamount = amount + shipping_amount


     return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_item':cart_item})


@login_required
def payment_done(request):
  user = request.user
  custid = request.GET.get('custid')
  customer = Customer.objects.get(id=custid)
  cart = Cart.objects.filter(user=user)
  for c in cart:
    OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
    c.delete()
  return redirect("orders")

#def my_view(request):
 #   return render(request, 'orders.html')

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
  def get(self,request):
    form = CustomerProfileForm()
    return render(request, 'app/profile.html',{'form':form,'active':'btn-danger'})
  
  def post(self,request):
    form = CustomerProfileForm(request.POST)
    if form.is_valid():
      usr = request.user
      name = form.cleaned_data['name']
      locality = form.cleaned_data['locality']
      city = form.cleaned_data['city']
      state = form.cleaned_data['state']
      zipcode = form.cleaned_data['zipcode']
      reg = Customer(user=usr,name=name, locality=locality, city=city, state=state, zipcode=zipcode)
      reg.save()
      messages.success(request,'Profile Update Successfully..!!')
      return render(request, 'app/profile.html',{'form':form, 'active': 'btn-red'})
 
