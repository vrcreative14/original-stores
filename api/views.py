from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from accounts.models import User, UserOTP, PhoneOTP
from .serializers import *
from accounts.models import Seller
from rest_framework.response import Response
from django.http import  JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, status, views, permissions
from .renderers import UserRenderer
#from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from knox.views import LoginView as KnoxLoginView, LogoutView
from knox.auth import TokenAuthentication
from django.contrib.auth import login, logout
from stores.models import Store, StoreCategory, StoreSubcategory,States,StoreDetails
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from django.core.mail import send_mail
from django.conf import settings
from .utils import otp_generator
import sys
import random
import requests
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404
from rest_framework.decorators import parser_classes
from products.models import *

# Create your views here.

#link = f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=d422a24f-24aa-11eb-83d4-0200cd936042&to={phone}&from='


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



def validate_phone_otp(phone, usr_first_name):        
        user = User.objects.filter(phone = phone)
        if user.exists():
            return Response({
                'status':False,
                'detail':'Mobile number already exists'
            })
        else:
            otp = send_otp(phone)
            if otp:
                otp = str(otp)
                count = 0
                old = PhoneOTP.objects.filter(phone__iexact = phone)
                if old.exists():
                    old = old.first().count()
                    old.first().count = count + 1
                    old.first().save()

                else:
                    count = count + 1       
                    PhoneOTP.objects.create(
                        phone = phone,
                        otp = otp,
                        count = count
                    )

                    if count > 5:
                        return Response({
                            'status':'False',
                            'detail':'Error in sending OTP, Limit exceeded. Please contact customer support.'
                        })
                    
                    # old.count = count + 1
                    # old.save()
                    print("count increase", count)
                    return Response({
                        'status' : True,
                        'detail': 'OTP sent successfully'
                    })
                PhoneOTP.objects.create(
                    phone = phone,
                    otp = key
                )
                pass
            else:
                return Response({
                    'status':False,
                    'detail':'Error in sending OTP'
                })



class ValidatePhoneSendOTP(APIView):
    '''
    This class view takes phone number and if it doesn't exists already then it sends otp for
    first coming phone numbers'''

    def post(self, request, *args, **kwargs):
        # user_name = request.data.get('name')
        phone_number = request.data.get('phone')
        # if user_name:
        #     user_name = str(user_name)
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact = phone)
            if user.exists():
                return Response({'status': False, 'detail': 'Phone Number already exists'})
                # logic to send the otp and store the phone number and that otp in table. 
            else:
                otp = send_otp(phone)
                print(phone, otp)
                if otp:
                    otp = str(otp)
                    count = 0
                    old = PhoneOTP.objects.filter(phone__iexact = phone)
                    if old.exists():
                        count = old.first().count
                        old_otp_obj = old.first()
                        old_otp_obj.otp = otp
                        old_otp_obj.count = count + 1
                        old_otp_obj.save(force_update=True)
                    
                    else:
                        count = count + 1
               
                        PhoneOTP.objects.create(
                                phone =  phone, 
                                otp =   otp,
                                count = count        
                                )

                    if count > 5:
                        return Response({
                            'status' : False, 
                             'detail' : 'Maximum otp limits reached. Kindly support our customer care or try with different number'
                        })
                    
                    
                else:
                    return Response({
                                'status': 'False', 'detail' : "OTP sending error. Please try after some time."
                            })

                return Response({
                    'status': True, 'detail': 'An SMS with an OTP(One Time Password) has been sent <br/> to your Mobile number'
                })
        else:
            return Response({
                'status': 'False', 'detail' : "We haven't received any phone number. Please do a POST request."
            })


class ValidatePhoneOTP(APIView):
    '''
    If you have received otp, post a request with phone and that otp and you will be redirected to set the password    
    '''
    def post(self, request, *args, **kwargs):

        try:
            phone = request.data.get('mobile', False)
            otp_sent = request.data.get('otp', False)           

        except:
            return Response({
                            'status' : False, 
                            'detail' : 'Please provide required fields.'
                        })

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp) == str(otp_sent):
                    old.logged = True
                    old.save()
                    # temp_data = {'name': name,'phone': phone,'email':email,'password': password }
                    # if(RegisterUser(temp_data)):                        
                    return Response({
                            'status' : True, 
                            'detail' : 'OTP matched'
                        })
                else:
                    return Response({
                        'status' : False, 
                        'detail' : 'OTP incorrect, please try again'
                    })
            else:
                return Response({
                    'status' : False,
                    'detail' : 'Phone not recognised. Kindly request a new otp with this number'
                })


        else:
            return Response({
                'status' : 'False',
                'detail' : 'Either phone or otp was not received'
            })


@login_required(login_url='http://127.0.0.1:8000/login')
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def RegisterSeller(request):    
    usr = request.data.get('user', False)
    first_name = request.data.get('firstname', False)
    middle_name = request.data.get('middlename', False)
    last_name = request.data.get('lastname', False)
    secondary_email = request.data.get('secondaryemail', False)
    secondary_phone = request.data.get('secondarymobile', False)

    try:
        user_phone = request.COOKIES.get('upl','') 
        user_email = request.COOKIES.get('uel','')
        user = User.objects.get(phone = user_phone) if user_phone != '' else User.objects.get(email = user_email)
        
        Temp_data = {'user': user.pk, 'first_name' : first_name,'middle_name': middle_name,'last_name': last_name, 'secondary_email': secondary_email, 'secondary_phone': secondary_phone}
      
    except:
       return Response({
           'status': False,
           'detail': 'Please provide User Data'
       })
   

    serializer = SellerSerializer(data=Temp_data)
    # user = UserSerializer()
    #try:
    if serializer.is_valid(raise_exception=ValueError):
            seller = serializer.save()
            # usr_otp = random.randint(100000, 999999)
            # print(seller.user)
            # UserOTP.objects.create(user = seller.user, otp = usr_otp)
            #msg = f"Hello {seller.first_name} \n Your OTP is {usr_otp} \n Thanks"

            # send_mail(
            #     "Welcome to the world of Vykyoo - Verify Your Email",
            #     msg,
            #     settings.EMAIL_HOST_USER,
            #     [seller.user.email],
            #     fail_silently=False
            # )

            # print('seller serializer data:',json.dump(serializer.data,4) )
            #serializer.create(validated_data=request.data)
            resp =  Response({
                'status': True,
                'detail':'Seller registered successfully. Continue filling the Store Info.'
            })
            resp.set_cookie('seller', seller)
            return resp
            #return Response(serializer.data,status=status.HTTP_201_CREATED)              
    
    # except:
    #     e = sys.exc_info()[0]
    #     print(e)
    return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


# @login_required(login_url='http://127.0.0.1:8000/login')

class RegisterStore(APIView):
        permission_classes = [permissions.IsAuthenticated]
        #parser_classes = [MultiPartParser]

        def post(self, request, format = None):
                #user_ph = request.data.get('user_ph', '')
                #user = User.objects.get(phone = user_ph)
                input_gstin = ''
                user_phone = request.session["user_phone"] 
                user = ''
                if user_phone is None:
                    user_email = request.session["user_email"]
                    user = User.objects.filter(email = user_email)
                else:
                    user = User.objects.filter(phone = user_phone)

                seller = Seller.objects.get(user = user[0].pk)
                is_gst_registered = request.data.get("is_gst_registered", False)
                if is_gst_registered:
                            input_gstin = request.data.get("gstin",False)
                else:
                            input_gstin = None
                store_existing = Store.objects.filter(seller = seller.pk)                 
                if len(store_existing) > 0:
                            check_existing = StoreDetails.objects.filter(gstin = input_gstin)
                            if len(check_existing) > 0:
                                 if(check_existing[0].store.seller.pk != seller.pk):
                                     return Response({
                                          'status' : False,
                                          'detail':'This GSTIN is already regstered with another Seller'
                                     })                                   
                
                name = request.data.get('shopname', False)
                state = request.data.get('state', False)
                city = request.data.get('city', False)
                pincode = request.data.get('pincode', False)
                latitude = request.data.get('latitude', False)
                longitude = request.data.get('longitude', False)
                product_categories = request.data.get('productcategory','')
                store_categories = request.data.get('storecategory','')
                product_categories_list = []
                store_category_list = []
                #    # storeimage = request.data["storeimage"]
                for category in product_categories:
                    prod_category = ProductCategory.objects.filter(name = category)
                    product_categories_list.append(prod_category[0].pk)
                
                for store_category in store_categories:
                    category = StoreCategory.objects.filter(name = store_category)
                    store_category_list.append(category[0].pk)

                temp_data = {"seller": seller.pk, "name": name, "state": state, "city" : city, "pincode": pincode, "latitude": latitude, "longitude": longitude,"store_category":store_categories,"product_category":product_categories }

                serializer = StoreSerializer(data= temp_data)
                if serializer.is_valid():
                        store = serializer.save()
                        # for product_category in product_categories:
                        #        store.product_category.add(ProductCategory.objects.create(product_category))
                        
                        # for store_category in store_categories:
                        #        StoreCategory.objects.create(**store_category)
                   #store = self.create(self, request)
                #    store_id = str(pincode) + str(random.randint(9, 99))
                #    new_store = Store.objects.create(name = name,seller = seller,state=state,city = city,pincode = pincode,latitude=latitude,longitude=longitude,store_id=store_id)
                #    #new_store.save()
                #    for category in product_categories:
                #        prod_category = ProductCategory.objects.get(name = category)
                #        new_store.product_category.add(prod_category)

                #    for store_category in store_categories:
                #        category = StoreCategory.objects.get(name = store_category)
                #        new_store.store_category.add(category) 
                #if new_store:
                        address_line1 = request.data.get("address")
                        landmark = request.data.get("landmark", "")                                          
                        details_data = {"store":store.pk, "address_line1": address_line1, "nearest_landmark": landmark,"is_gst_registered":is_gst_registered ,"gstin": input_gstin}
                        serializer2 = StoreDetailsSerializer(data = details_data)
                        if serializer2.is_valid():
                            serializer2.save()                           
                            return JsonResponse({
                                'status': True,
                                'detail': 'Store Successfully Created. Continue saving further information',
                                'store' : store.pk
                            })
                        else:
                            error = serializer.errors
                            return Response({
                               'status': False,
                               'detail': error
                            })
        
        def create(self, request, *args, **kwargs):
                user_phone = request.session["user_phone"] 
                user = ''
                if user_phone is None:
                            user_email = request.session["user_email"]
                            user = User.objects.filter(email = user_email)
                else:
                            user = User.objects.filter(phone = user_phone)

                seller = Seller.objects.get(user = user[0].pk)
                name = request.data.get('shopname', False)
                state = request.data.get('state', False)
                city = request.data.get('city', False)
                pincode = request.data.get('pincode', False)
                latitude = request.data.get('latitude', False)
                longitude = request.data.get('longitude', False)
                product_categories = request.data.get('productcategory','')
                store_categories = request.data.get('storecategory','')
                store_id  = str(self.pincode) +str(self.pk)+ str(random.randint(9, 99))
                new_store = Store.objects.create(name = name,seller = seller.pk,state=state,city = city,pincode = pincode,latitude=latitude,longitude=longitude,product_category= product_categories,store_category=store_categories,store_id=store_id)
                new_store.save()
                product_categories_list = []
                store_category_list = []
                        #    # storeimage = request.data["storeimage"]
                for category in product_categories:
                            prod_category = ProductCategory.objects.filter(name = category)
                            #product_categories_list.append(prod_category[0].pk)
                            new_store.product_category.add(prod_category[0])
                        
                for store_category in store_categories:
                            category = StoreCategory.objects.filter(name = store_category)
                            new_store.store_category.add(category[0])


        def patch(self, request):
            pk = request.data["store"]
            model = get_object_or_404(Store, pk=pk)
            storeimage = request.data["storeimage"]
            model.storeimage = storeimage
            model.save()
            return Response({
                'status': True,
                'detail': 'Image uploaded succcesfully'
            }) 
        #     temp_data = {"storeimage" : storeimage}
        #     serializer = StoreSerializer(Store,data= temp_data, partial = True)

        #     if serializer.is_valid():
        #         serializer.save(update_fields=['storeimage'])
        #         return Response(serializer.data)
        # # return a meaningful error response
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddProductDetails(APIView):
        #permission_classes = [permissions.IsAuthenticated]
        #parser_classes = [MultiPartParser]

        def post(self, request, format = None):
                # user_ph = request.data.get('user_ph', '')
                # user = User.objects.get(phone = user_ph)
                # seller = Seller.objects.get(user = user.pk)
                # name = request.data.get('shopname', False)
                # state = request.data.get('state', False)
                # city = request.data.get('city', False)
                # pincode = request.data.get('pincode', False)
                # latitude = request.data.get('latitude', False)
                # longitude = request.data.get('longitude', False)
               
               # storeimage = request.data["storeimage"]

               #temp_data = {"seller": seller.pk, "name": name, "state": state, "city" : city, "pincode": pincode, "latitude": latitude, "longitude": longitude}

                serializer = Prod_Details_Serializer(data= request.data)
                if serializer.is_valid():
                   prod = serializer.save()
                   return Response({
                       'status': True,
                       'details': prod.id
                   })
                #    if prod:
                #         address_line1 = request.data.get("address")
                #         landmark = request.data.get("landmark", "")
                #         is_gst_registered = request.data.get("is_gst_registered", False)
                #         gstin = request.data.get("gstin")

                #         details_data = {"store":store.pk, "address_line1": address_line1, "nearest_landmark": landmark,"is_gst_registered":is_gst_registered ,"gstin": gstin}
                #         serializer2 = StoreDetailsSerializer(data = details_data)
                #         if serializer2.is_valid():
                #             serializer2.save()                           
                #             return JsonResponse({
                #                 'status': True,
                #                 'detail': 'Store Successfully Created. Continue saving further information',
                #                 'store' : store.pk
                #             })
                # else:
                #     error = serializer.errors
                #     return Response({
                #         'status': False,
                #         'detail': error
                #     })
        
        def patch(self, request):
            pk = request.data["store"]
            model = get_object_or_404(Store, pk=pk)
            storeimage = request.data["storeimage"]
            model.storeimage = storeimage
            model.save()
            return Response({
                'status': True,
                'detail': 'Image uploaded succcesfully'
            })


class AddProduct(APIView):
    def post(self, request, format = None):
        serializer = Product_Serializer(data = request.data)
        if(serializer.is_valid()):
            prod = serializer.save()
            return Response({
                       'status': True,
                       'details': prod.id
                   })

def RegisterUser(temp_data):
        try:
            serializer = UserSerializer(data=temp_data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            u=user.save()
            return True
        
        except:
            return False

# @api_view(["GET"])
# def GetProducts(request):
#     category = request.data.get

class Register(APIView):
    
    '''Takes phone and a password and creates a new user only if otp was verified and phone is new'''

    def post(self, request, *args, **kwargs):
        phone = request.data.get('mobile', False)
        password = request.data.get('pw', False)
        email = request.data.get('email', False)
        name = request.data.get('name', False)
        otp = request.data.get('otp', False)
       
        if phone and password:
            phone = str(phone)
            if email:
                user_email = User.objects.filter(email__iexact = email)
                if user_email.exists():
                    return Response({'status': False,
                    'detail': 'Email entered is already registered.Try with different Email OR <br/> <a href="/login">Login into existing account from here</a>'})

            user = User.objects.filter(phone__iexact = phone)
            if user.exists():
                return Response({'status': False,
                 'detail': 'Phone number entered is already registered.Try with different mobile number OR <br/> <a href="/Login">Login into existing account from here</a>'})
            else:
                old = PhoneOTP.objects.filter(phone__iexact = phone)
                if old.exists():
                    old = old.first()
                    if old.logged:
                        Temp_data = {'name':name,'phone': phone,'email':email, 'password': password}

                        serializer = UserSerializer(data=Temp_data)
                        serializer.is_valid(raise_exception=True)
                        user = serializer.save()
                        user.save()                       
                        old.delete()
                        request.session['user_name'] = name
                        request.session['phone'] = phone
                        request.session['email'] = email                        
                        resp = Response({
                            'status' : True, 
                            'detail' : 'User registered successfully'
                        })
                        #resp.set_cookie('user', user.pk)
                        request.session['user'] = user.pk
                        return resp
                        # return Response({
                        #     'status' : True, 
                        #     'detail' : 'User registered successfully'
                        # })

                    else:
                        return Response({
                            'status': False,
                            'detail': 'Your otp was not verified earlier. Please go back and verify otp'
                        })
                else:
                    return Response({
                    'status' : False,
                    'detail' : 'Phone number not recognised. Kindly request a new otp with this number'
                })              


        else:
            return Response({
                'status' : 'False',
                'detail' : 'Either phone or password was not received '
            })



class GetSellers(generics.ListAPIView):
        permission_classes = [permissions.IsAuthenticated,] 
        serializer_class=SellerSerializer
        def get_object(self):            
            seller = Seller.objects.all()   
            serializer=SellerSerializer(seller, many=True)
            return Response(serializer.data)


class GetUser(generics.RetrieveAPIView):
        permission_classes = [permissions.IsAuthenticated,] 
        serializer_class = UserSerializer
    
        def get_object(self):  
             return self.request.user


@login_required()
@api_view(['GET'])
def GetSellerbyId(request,pk):
    seller = Seller.objects.get(id = pk)
    serializer = SellerSerializer(seller, many=False)
    return Response(serializer.data)

@login_required()
@api_view(['GET'])
def GetSellerbyUserId(request,pk):
    user = User.objects.get(id = pk)
    seller = Seller.objects.get(user = user.id)
    serializer = SellerSerializer(seller, many=False)
    return Response(serializer.data)



class RegisterView(generics.GenericAPIView):
    
    serializer_class = SellerSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi '+user.username + \
            ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        #Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        print('result for request data is:')
        print(request.data)        
        user_obj = ''
        try:
            print(request.data["phone"])
            user_phone = request.data["phone"]                  
            serializer = MobileNoLoginSerializer(data = request.data)       
            serializer.is_valid(raise_exception = True)
            print(serializer.is_valid)
            user = serializer.validated_data['user']
            if user[0].is_active == False:
                    return Response({
                    'status': False,
                    'detail':'Please verify your Mobile number through OTP, before logging in.'
                })
            # if user.last_login is None :
            #         #user.first_login = True
            #         user.save()
                
            # elif user.first_login:
            #     #user.first_login = False
            #     user.save()
            login(request, user[0], backend='accounts.backends.PhoneBackend')           
            user_obj = user[0]
            # request.session['user_token'] = b.data

            #return response           
       
        except Exception as e:            
            if(not str(e.args[0]).find("Mobile number is not registered") == -1):
                    return Response({
                           'status' : False,
                           'detail' : 'Entered Mobile number is not registered. <a style="font-size:15px;font-weight:300;" href="/SignUp"> New users Signup from here</a>',                          
                            })

            serializer = LoginSerializer(data = request.data)                            
            serializer.is_valid(raise_exception = True)
            print(serializer.is_valid)
            user = serializer.validated_data['user']
            if user[0].is_active == False:
                return Response({
                    'status': False,
                    'detail':'Please verify your Email through OTP, before logging in.'
                })

            # if user.last_login is None :
            #         #user.first_login = True
            #         user.save()
                
            # elif user.first_login:
            #     #user.first_login = False
            #     user.save()
            login(request, user[0], backend = 'django.contrib.auth.backends.ModelBackend')            
            user_obj = user[0]
            # v = super().post(request, format=None)
            # HttpResponse.set_cookie("atl",v.data["token"],expires=v.data["expiry"],httponly=True)
            # return v
        #request.session['userid'] = user
        request.session['user_name'] = user_obj.name
        request.session['user_phone'] = user_obj.phone 
        request.session['user_email'] = user_obj.email 
        response = super().post(request, format=None)
        auth_token = response.data["token"]
        # expiry = response.data["expiry"]
        response.set_cookie('tkl',auth_token,24*60*60*10,httponly=True) 
        return response       
                #response.set_cookie('upl', user_phone, 24*60*60*10)                
       
                #response.set_cookie('uel', user_email, 24*60*60*10)          
        # return Response({
        #     'status':True,
        #     'Detail':'Logged in Successfully'
        # })


class LogoutAPI(LogoutView):
    permission_classes = (permissions.AllowAny, )
    def post(self, request, format=None):
        print(request)
        v = logout(request)
        response =  Response({'status': True,'detail': 'You have been logged out Successfully.'})
        response.delete_cookie('upe')
        response.delete_cookie('tkl')
        return response
    pass


@api_view(['GET'])
def GetToken(request):    
        #credential = request.data["phone"]    
        credential=request.GET.get('phone', '')
        #user = User.objects.get(phone = credential)
        #if credential == ''
        if credential == '':
            user = User.objects.get(email = credential)
            if user == '':
                user = User.objects.get
                res = Response({'status': False,
                'detail': 'It seems you have been registered. Please Signup and continue.'})
            else:
               res = GetTokenforUser(request,user)

        else:
           res = GetTokenforUser(request,user)
        # def post(self, request, *args, **kwargs):
        #     token = request.COOKIES['atl']
        #     pass
        return res

@api_view(['GET'])
def GetTokenforUser(request):
    tkl = request.COOKIES["tkl"]   
    return Response({'status':True, 'tkl':tkl})



@api_view(['POST'])
def AddStoreDetails(request): 
    permission_classes = (permissions.IsAuthenticated,)
    serializer = StoreDetailsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


def send_otp(phone):
    """
    This is an helper function to send otp to session stored phones or 
    passed phone number as argument.
    """

    if phone:        
        key = otp_generator()
        phone = str(phone)
        otp_key = str(key)
        # seller_name = str(usr_first_name)
        #link = f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=fc9e5177-b3e7-11e8-a895-0200cd936042&to={phone}&from=wisfrg&templatename=wisfrags&var1={otp_key}'
        #link =  f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=d422a24f-24aa-11eb-83d4-0200cd936042&to={phone}&from=ORIGST&templatename=MobileVerificationOTP&var1={seller_name}&var2={otp_key}'
        #link = f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=d422a24f-24aa-11eb-83d4-0200cd936042&to={phone}&from=VCNITY&templatename=Mobile+Number+Verification+OTP&var1={seller_name}&var2={otp_key}'
        #result = requests.get(link, verify=False)

        return otp_key
    else:
        return False


def LoginHelper(request,password,phone=None, email=None):
     try:            
            login_data = {'phone': phone, 'pft': password}        
            serializer = MobileNoLoginSerializer(data = login_data)       
            serializer.is_valid(raise_exception = True)
            print(serializer.is_valid)
            user = serializer.validated_data['user']
            if user[0].is_active == False:
                    return Response({
                    'status': False,
                    'detail':'Please verify your Mobile number through OTP, before logging in.'
                })
            # if user.last_login is None :
            #         #user.first_login = True
            #         user.save()
                
            # elif user.first_login:
            #     #user.first_login = False
            #     user.save()
            login(request, user[0], backend='accounts.backends.PhoneBackend')
            b = super().post(request, format=None)  
            request.session['user_token'] = b.data
            return b
            # return Response({
            #     'status' : True,
            #     'detail' : 'Logged in Successfully',
            #     'info' : b,
            # })  

       
     except Exception as e:
            
            if(not str(e.args[0]).find("Mobile number is not registered") == -1):
                    return Response({
                           'status' : False,
                           'detail' : 'Entered Mobile number is not registered. <a style="font-size:15px;font-weight:300;" href="/SignUp"> New users Signup from here</a>',                          
                            })

            serializer = LoginSerializer(data = request.data)                           
            serializer.is_valid(raise_exception = True)
            print(serializer.is_valid)
            user = serializer.validated_data['user']
            if user[0].is_active == False:
                return Response({
                    'status': False,
                    'detail':'Please verify your Email through OTP, before logging in.'
                })

            # if user.last_login is None :
            #         #user.first_login = True
            #         user.save()
                
            # elif user.first_login:
            #     #user.first_login = False
            #     user.save()
            login(request, user[0], backend = 'django.contrib.auth.backends.ModelBackend')
            return super().post(request, format=None)

@api_view(['POST'])
@parser_classes((MultiPartParser,))
def handle_uploaded_image(request):
    #process image
    if not 'uploaded_media' in request.FILES:
        return Response({'msg':'Photo missing.'},status.HTTP_400_BAD_REQUEST)
    try:
        img = Image.open(StringIO(request.FILES['uploaded_media'].read()))
    except IOError:
        return Response({'msg':'Bad image.'}, status.HTTP_400_BAD_REQUEST)

    serializer = Product_Serializer(data = request.DATA)
    if not serializer.is_valid():
        return Response({'msg':serializer.errors}, status.HTTP_400_BAD_REQUEST)

    clothing = Garment.create()


@api_view(['GET'])
def GetProducts(request):
    products = Garment.objects.all()
    Temp_data = []
    for product in products:
        print(product)     
        dictionary = {'name':product.name, 'price' : product.price, 'category' : 'Men', 'store' : product.store}
        Temp_data.append(dictionary)
        #Temp_data.append(dictionary)
        # Temp_data.update({'name' : product.name})
        # Temp_data.update({'price' : product.price})
        # Temp_data.update({'category' : 'Men'})
        # Temp_data.update({'store' : product.store})          

    
    serializer = Garment_Serializer(data = Temp_data)
    if serializer.is_valid():
        return Response(serializer.data)
    else:
        return Response({'status': False, 'error': serializer.errors}) 


class GarmentViewSet(viewsets.ModelViewSet):
    queryset = Garment.objects.all()
    serializer_class = Garment_Serializer

class GarmentDetailsViewSet(viewsets.ModelViewSet):
    queryset = GarmentDetails.objects.all()
    serializer_class = GarmentDetailsSerializer

