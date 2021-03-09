from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import Seller
from django.utils import timezone
from django import forms
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
import datetime
from stores.models import States, StoreCategory, Store
from products.models import *
from api.utils import convert_toWords
from django.shortcuts import redirect
from orders.models import Order, ShippingAddress

#from .forms import SellerForm
#from api.models import Product
# Create your views here.


def Home(request):
    try:
        #name = request.session['user_name']
        #phone = request.session['phone']
        #token = request.session['user_token']
        user_name = token["user"]["name"]
        date_string = token["expiry"]
        format = "%Y-%m-d"
        #d=datetime.datetime.strftime(float(date_string), format)
        
        context = {'loggedin' : True}

    except Exception as e:
        context = {'loggedin' : False}
    
    print(request.session)
    return render(request,'frontend/Home.html', context)


def Login(request):
    #put logic here to check whether len(request.GET)==0 OR check that token in cookie has expired..
    return render(request,'frontend/Login.html')


def SignUp(request):   
        
        # return render(request,'frontend/SignUp.html')
   
  
        # #dynamic_content = DynamicPageContent.breif_signup_hindi  
        context = {'states' : "states", 'store_categories' : "store_categories", 'store_subcategories' : "store_subcategories"}
        # print('no')
        return render(request,'frontend/SignUp.html', context)

@login_required(login_url='/login')
def Checkout(request):      
        user_id = request.session['userid']
        saved_addresses = ShippingAddress.objects.filter(user = user_id)
        context = {'addresses': saved_addresses,'states': States.STATE_UT}
        save_address = ''
        # if orders:
        #         saved_address = orders.destination
        return render(request,'frontend/Checkout.html', context)

@login_required(login_url='/login')
def categories(request):
      context = {'states' : "states", 'store_categories' : "store_categories", 'store_subcategories' : "store_subcategories"}
        # print('no')
      return render(request,'frontend/Cart.html', context)


@permission_classes([IsAuthenticated])
@login_required(login_url='/login')
def RegisterSeller(request):
    #token = request.data.get('token', False)    
    # if request.user.is_seller:
    #     return redirect('/SellerDashboard');
    #     # return render(request, 'frontend/SellerDashboard.html')
    # else:
    if request.session['seller'] :
        return render(request, 'frontend/SellerDashboard.html')
    else:
        try:
            token = request.session['user_token']
            user_email = token["user"]["email"]
            user_name = token["user"]["name"]
            categories = ProductCategory.objects.all()
            store_category = StoreCategory.objects.all()
            context = {'loggedin':True,'email' : user_email, 'states': States.STATE_UT, 'categories': categories, 'store_categories': store_category}
        except:            
            categories = ProductCategory.objects.all()   
            store_category = StoreCategory.objects.all() 
            context = {'loggedin':True, 'email' : '', 'states': States.STATE_UT, 'categories': categories, 'store_categories': store_category}

        return render(request,'frontend/SellerRegistration.html',context)
   
        

@login_required(login_url='/login')
def SellerDashboard(request):
    stores = Store.objects.filter(seller = request.user.seller.pk)
    seller = Seller.objects.filter(user = request.user.pk)
    products = ''
    if len(stores) > 0:
        for store in stores:
            products = Article.objects.filter(store = store.pk)
    context = {'stores': stores,'seller_name':seller[0].first_name+ ' ' +seller[0].last_name,'products':products}    
    return render(request,'frontend/SellerDashboard.html', context)

@login_required(login_url='/login')
def AddStore(request):
    categories = ProductCategory.objects.all()
    store_category = StoreCategory.objects.all()
    context = {'states': States.STATE_UT, 'categories': categories, 'store_categories': store_category}
    return render(request, 'AddStore.html', context)


def Products(request,type):
    message="{}".format(selected_category)
    template="frontend/Products.html"
    context={
        'message': message
    }
    return render(request,template,context)


def FetchProducts(request):
    
   # products = Product.objects.all()
    #productsM = Product.objects.filter()
    #context = {'states' : states}
    #serializer=ArticleSerializer(articles, many=True)
    fetched_products = []
    dic = {}
    product_category = request.GET.get('category')
    switcher = {
                'clothing':'Fashion & Clothing',
                'household_essentials':'Household Essentials',
                'kitchen_essentials':'Kitchen Essentials',
                'handicrafts_home_decor':'Handicrafts & Home Decor',                          
        }
    selected_category = switcher.get(product_category, None)

    if(selected_category is not None):
        category = ProductCategory.objects.get(name = selected_category)
        sub_categories = ProductSubCategory.objects.filter(type = category.pk)
        keys =range(len(sub_categories))
        for i in keys :
            try:
                prods = Garment.objects.filter(product_category = sub_categories[i].pk)
                for p in prods :                   
                    fetched_products.append(Garment(name = p.name, brand_name=p.brand_name, image = p.image
                    ,price = p.price))   
                if len(prods) != 0:
                    dic[sub_categories[i].name] = fetched_products    
            #print(sub_category)
            except Exception as e:
                print("An exception occurred: ", e) 
                continue
        
        pass
    print(dic)
    category = request.GET.get('category','')
    categories = ProductCategory.objects.all()
    article = Garment.objects.all()
    context = {'articles' : article,}
    return render(request,'frontend/Products.html', context)


def index(request):
    if request.method == "POST":
        print(request.POST)


@login_required(login_url='/login')
def AddProducts(request):
    categories = ProductCategory.objects.all()    
    seller_id = request.session['seller']
    
    if seller_id :
        store = Store.objects.filter(seller = seller_id)

    
    context = {'productcategories': categories, 'stores':store}
    return render(request,'frontend/AddProducts.html', context)


def SelectedProduct(request):
    category = request.GET.get('category','')
    default_items = []
    context = {}
    sub_categories = []
    articles = []
    # if category == 'clothing':
    default_items = ['T-Shirts','Formal Shirts','Casual Shirts','Formal Trousers','Lowers','Jeans & Casual Tousers']
    default_items_menu_class = 'ui bottom attached inverted ' + convert_toWords(len(default_items)) + ' item menu'
    #selected_product_categories = ProductSubCategory.objects.filter(type = 1012)
    selected_product_category = ProductCategory.objects.filter(name = category)
    if len(selected_product_category) > 0:
        sub_category = get_default_subcategory(category)
        sub_category_obj = ProductSubCategory.objects.filter(type = selected_product_category[0].pk, name = sub_category)

        if sub_category_obj:                   
            articles = Article.objects.filter(product_category = sub_category_obj[0].pk).order_by('-id')[:10]

    
            item_in_words = convert_toWords(len(sub_categories))
            div_class_name = 'ui ' +  item_in_words + ' item secondary pointing menu' 
            context = {'category':category,'selected_product_categories' : sub_categories,'articles':articles ,'div_class_name': div_class_name,'default_items':default_items,'default_items_menu_class':default_items_menu_class}           
    else:
            context = {'category':category,'selected_product_categories' : sub_categories}
    return render(request,'SelectedProductList.html',context)


def ProductDetails(request):
    slug = request.GET.get('details','')
    context = {}
    if slug:
        article = Article.objects.get(slug_field = slug)
        article_details = ArticleDetails.objects.get(article = article.pk)
        context = {'article': article,'details':article_details}
    return render(request,'frontend/ProductDetails.html', context)



def get_default_subcategory(category):

        switcher={
            'Fashion & Clothing':"Men's Wear",
            'Home Appliances':'Refrigerators',
            'Kitchen Essentials':'Kitchen Appliances',
            'Electronic Devices':'Television',
            'Groceries':'Thursday',
            'Personal Care':'Friday',
            'Automobile Accesories':'Saturday'
        }
        return switcher.get(category,"Invalid")