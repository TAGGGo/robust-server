import re
from django.shortcuts import render, redirect
from .forms import NewUserForm, CustomerForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .models import Customer, Product, Category, cartProduct, Order, Cart, Warehouse, orderProduct
from django.contrib.auth.forms import AuthenticationForm
from django.db import connection
import sys, socket, time, threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

sys.path.append('/code/amazon_server')
import amazon_webapp_pb2 as amz
from request_handlers import _sendProtoStrWithLock
from server import connectToServer

def sendEmail(receiverAddress, content):
    print("-----------")
    print(receiverAddress)
    senderAddress = '1073424278@qq.com'
    senderPassword = 'ehkbtnuwkqxibbde'
    msg = MIMEMultipart()
    msg.attach(MIMEText(content, 'plain'))
    msg['Subject'] = 'Hey, Your Order Has been checked out'
    msg['From'] = senderAddress

    s = smtplib.SMTP_SSL("smtp.qq.com", 465)
    s.login(senderAddress, senderPassword)
    s.sendmail(senderAddress, receiverAddress, msg.as_string())
    print("email sent")

SERVER_SIMULATOR = ("127.0.0.1", 5555)
serverSocket = None
WRITE_TO_SERVER_LOCK = threading.Lock()
def connectToAMZServer():
    global serverSocket
    while True:
        try:
            print("connect to SERVER with {}:{}".format(SERVER_SIMULATOR[0], SERVER_SIMULATOR[1]))
            serverSocket = connectToServer(SERVER_SIMULATOR)
            break
        except socket.error as msg:
            print("ERROR MSG: {}".format(msg))
            time.sleep(3)
            continue
    
def signupHandler(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(user=user).save()
            login(request, user)
            return redirect('/index')
        print(form.errors)
        return render(request, 'signup.html', {'form': form})


def loginHandler(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/index')
            else:
                return render(request, 'login.html', {'form': 'Invalid username or password'})
        else:
            return render(request, 'login.html', {'form': form})

def accountHandler(request):
    if request.user.is_authenticated:
        customer = Customer.objects.filter(user=request.user).first()
        return render(request, 'account.html', {
            'user': request.user,
            'customer': customer
            })
    else:
        return render(request, 'login.html')

@login_required(login_url='/login')
def updateProfile(request):
    if request.method == "POST":
        customer = Customer.objects.filter(user_id=request.user).first()
        if customer is None:
            form = CustomerForm(request.POST)
        else :
            form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.save()
            return redirect('/account')
        else:
            print(form.errors)
            return render(request, 'account.html', {'form': form})

def logoutHandler(request):
    logout(request)
    return redirect('/login')

def indexPage(request):
    return render(request, 'index.html', {'products': getAllProducts()})

def productsPage(request):
    return render(request, 'products.html', {'products': getAllProducts()})

def productsCategoryPage(request, category):
    print(category)
    return render(request, 'products.html', {'products': getProductsByCategory(category)})

@login_required(login_url='/login')
def storePage(request):
    cartProducts = getCartProductsDetail(request)
    orderProducts = getOrderProducts(request)
    orders = getOrders(request)
    subPrice = 0
    for product in cartProducts:
        subPrice += product['price'] * product['count']
    taxPrice = subPrice * 0.05
    shippingPrice = subPrice * 0.1
    totalPrice =  subPrice + taxPrice + shippingPrice
    return render(request, 'store.html', {
        'products': getAllProducts(),
        'cartProducts': cartProducts,
        'orderProducts': orderProducts,
        'orders': orders,
        'subPrice': subPrice,
        'taxPrice': taxPrice,
        'shippingPrice': shippingPrice,
        'totalPrice': totalPrice
        })

def getAllProducts():
    products = Product.objects.all().values('id', 'name', 'price', 'photo', 'category_id__cat_name')
    return products

def getCartProductsDetail(request):
    with connection.cursor() as cursor:
        customer = Customer.objects.filter(user_id=request.user).first()
        cursor.execute(
            "SELECT amazon_product.name, amazon_product.price, amazon_product.photo, amazon_cartproduct.count \
            FROM amazon_cartproduct INNER JOIN amazon_product ON amazon_cartproduct.product_id = amazon_product.id \
            WHERE amazon_cartproduct.cart_id = (SELECT id FROM amazon_cart WHERE amazon_cart.user_id = %s)", (customer.id, )
            )
        data = dictfetchall(cursor)
        print(data)
        return data

def getOrderProducts(request):
    with connection.cursor() as cursor:
        customer = Customer.objects.filter(user_id=request.user).first()
        cursor.execute(
            "SELECT DISTINCT amazon_product.name, amazon_product.price, amazon_product.photo \
            FROM amazon_orderproduct INNER JOIN amazon_product ON amazon_orderproduct.product_id = amazon_product.id \
            WHERE amazon_orderproduct.order_id = (SELECT  id FROM amazon_order WHERE amazon_order.user_id = %s  order by id desc limit 1)", (customer.id, ))
        data = dictfetchall(cursor)
        print(data)
        return data

def getOrders(request):
    with connection.cursor() as cursor:
        customer = Customer.objects.filter(user_id=request.user).first()
        cursor.execute(
            "SELECT * \
            FROM amazon_order WHERE amazon_order.user_id = %s order by amazon_order.created_at desc", (customer.id, )
            )
        data = dictfetchall(cursor)
        print(data)
        return data

def getProductsByCategory(category_name):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT amazon_product.id, amazon_product.name, amazon_product.price, amazon_product.photo\
            FROM amazon_product, amazon_category \
            WHERE amazon_product.category_id = amazon_category.id AND amazon_category.cat_name = %s", (category_name, )
            )
        data = dictfetchall(cursor)
        print(data)
        return data

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def sendCommandToServer(command):
    global serverSocket
    if serverSocket is None:
        connectToAMZServer()
    try:
        _sendProtoStrWithLock(serverSocket, command, WRITE_TO_SERVER_LOCK)
    except Exception:
        connectToAMZServer()
        _sendProtoStrWithLock(serverSocket, command, WRITE_TO_SERVER_LOCK)
    
    
@login_required(login_url='/login')
def addToChart(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        # check current user has cart
        customer = Customer.objects.filter(user=request.user).first()
        cart = Cart.objects.filter(user_id=customer).first()
        # if not, create new cart
        if cart is None:
            cart = Cart.objects.create(user_id=customer)
        # check if product is already in cart
        product = cartProduct.objects.filter(cart_id=cart, product_id=product_id).first()
        if product is None:
            productInstance = Product.objects.filter(id=product_id).first()
            product = cartProduct.objects.create(cart_id=cart, product_id=productInstance)
        else:
            product.count += 1
            product.save()
        return redirect('/index')

@login_required(login_url='/login')
def purchase(request):
    if request.method == "POST":
        customer = Customer.objects.filter(user=request.user).first()
        cart = Cart.objects.filter(user_id=customer).first()
        if cart is None:
            return HttpResponse('400 Invalid', status=400)
        allProducts = cartProduct.objects.filter(cart_id=cart)
        warehouse = Warehouse.objects.first()
        if warehouse is None:
            warehouse = Warehouse.objects.create()
        order = Order.objects.create(user_id=customer, warehouse_id=warehouse, ups_name=customer.ups_name)
        order.save()
        for product in allProducts:
            orderProduct.objects.create(order_id=order, product_id=product.product_id, count=product.count).save()
        # TODO : send Order to warehouse
        command = amz.AWCommands()
        command.buy.orderid = order.id

        thread = threading.Thread(target=sendCommandToServer, args=(command,))
        thread2 = threading.Thread(target=sendEmail, args=(request.user.email,  'Hello please check the order page for your order'))
        thread.start()
        thread2.start()

        cart.delete()
        return redirect('/store')

@login_required(login_url='/login')
def cancelOrder(request):
    if request.method == "POST":
        customer = Customer.objects.filter(user=request.user).first()
        order = Order.objects.filter(id=request.POST.get('order_id'))\
            .filter(user_id=customer).first()
        
        # TODO cancel
        if order.status != Order.delivered and order.status != Order.delivering and order.status != Order.cancelled:
            order.status = Order.cancelled
            order.save()
        else:
            return HttpResponse('400 Invalid', status=400)
        return HttpResponseRedirect('/store', status=200)

def subscribe(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if email is None:
            return HttpResponse('400 Invalid', status=400)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return HttpResponse('400 Invalid', status=400)
        
        thread = threading.Thread(target=sendEmail, args=(email,  'You have subscribe the newsletter'))
        thread.start()
        return HttpResponse('200 OK', status=200)

def product(request):
    return render(request, 'products.html')

def singleProduct(request):
    return render(request, 'singleproduct.html')

def store(request):
    return render(request, 'store.html')