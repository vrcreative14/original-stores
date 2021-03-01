from rest_framework import serializers
from accounts.models import User
from rest_framework.authtoken.models import Token
from accounts.models import Seller
from django.contrib.auth import authenticate
from stores.models import Store,StoreDetails, StoreCategory, StoreSubcategory
from django.contrib.auth import login
from products.models import  *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['pk','name','phone','email','password']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}


    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        #token = Token.objects.create(user=user)
        return user


class SellerUserSerializer(serializers.HyperlinkedModelSerializer):

    user = UserSerializer(required=True)

    class Meta:
        model= Seller
        fields=('pk','user','first_name', 'last_name')  

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = UserSerializer.create(user_serializer, validated_data=user_data)
        seller = Seller.objects.create(user=user,
                            first_name=validated_data.pop('first_name'), last_name=validated_data.pop('last_name'))

        return seller


class SellerSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Seller
        


class StoreCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = StoreCategory


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = ProductCategory


class StoreSubCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = StoreSubcategory


class StoreSerializer(serializers.ModelSerializer):
    store_category = StoreCategorySerializer(read_only = True, many=True)
    product_category = ProductCategorySerializer(read_only=True, many=True)
    #store_subcategory = StoreSubCategorySerializer(read_only = True, many=True)
    #seller = SellerSerializer(read_only = True, many=True)
    print(serializers.ModelSerializer)
    class Meta:
        model = Store
        fields=('seller','name','state','city','pincode','latitude','longitude','store_category','product_category','storeimage')


    def create(self, validated_data, *args, **kwargs):
        #email = validated_data.pop('seller')
        #user = User.objects.get(email = email)  
        #product_categories = validated_data.pop('product_category') 
        #store_categories = validated_data.pop('store_category')
        store = Store.objects.create(**validated_data)            
        return store

        # print('*******')
        # print(validated_data.pop('seller'))
        # store = Store.objects.create(seller = validated_data.get('seller'),
        #                         name=validated_data.pop('name'),
        #                         state=validated_data.pop('state'),
        #                         city=validated_data.pop('city'),
        #                         pincode=validated_data.pop('pincode')                                
        #                         )
        # print(store)                                
        # return store
       


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = User
        fields = ['email','password', 'phone']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}
    # def validate(self, attrs):
    #     email = attrs.get('email', '')
    #     username = attrs.get('username', '')

    #     if not username.isalnum():
    #         raise serializers.ValidationError(
    #             self.default_error_messages)
    #     return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        #Token.objects.create(user=user)
        return user
# class StudentSerializer(serializers.ModelSerializer):
#     """
#     A student serializer to return the student details
#     """
#     user = UserSerializer(required=True)

#     class Meta:
#         model = UnivStudent
#         fields = ('user', 'subject_major',)

#     def create(self, validated_data):
#         """
#         Overriding the default create method of the Model serializer.
#         :param validated_data: data containing all the details of student
#         :return: returns a successfully created student record
#         """
#         user_data = validated_data.pop('user')
#         user = UserSerializer.create(UserSerializer(), validated_data=user_data)
#         student, created = UnivStudent.objects.update_or_create(user=user,
#                             subject_major=validated_data.pop('subject_major'))
#         return student


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()   
    pft = serializers.CharField(
        style={'input_type':'password'}, trim_whitespace = False
    )

    def validate(self, attrs):
        print(attrs)
        email = attrs.get('email')      
        pft = attrs.get('pft')

        if email and pft:
            if User.objects.filter(email = email).exists():
                #print(email, password)
                #user = authenticate (request = self.context.get('request'),email = email, password = password)
                user = User.objects.filter(email = email)
            else:
                msg = {'detail' : 'Email is not registered', 'register' : False }
                raise serializers.ValidationError(msg, code='authorization')
        
        else:
            msg = 'Must include email and password.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs



class MobileNoLoginSerializer(serializers.Serializer):
    
    #email = serializers.CharField()
    phone = serializers.CharField()
    pft = serializers.CharField(
        style={'input_type':'password'}, trim_whitespace = False
    )

    def validate(self, attrs):
        print(attrs)
        
        #email = attrs.get('email')
        phone = attrs.get('phone')
        password = attrs.get('pft')

        if phone and password:
            if User.objects.filter(phone = phone).exists():
                print(phone, password)
                #user = authenticate(request = self.context.get('request'),phone = phone, password = password,backend='accounts.backends.PhoneBackend')
                #login(self.context.get('request'),user, backend='django.contrib.auth.backends.ModelBackend')
                user = User.objects.filter(phone = phone)
            else:
                msg = {'detail' : 'Mobile number is not registered', 'register' : False }
                raise serializers.ValidationError(msg, code='authorization')
        
        else:
            msg = 'Must include "Mobile number" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs



class StorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class StoreDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreDetails
        fields = '__all__'

class Prod_Details_Serializer(serializers.ModelSerializer):
    sizes_available = serializers.ListField()
    class Meta:
        model = Garment
        fields = '__all__'

class Product_Serializer(serializers.ModelSerializer):    
    #details = Prod_Details_Serializer(required=True)
    class Meta:
        model = Garment
        fields = ('name','img_path','brand_name','price','store','category','garment_details')
    # def create(self, validated_data):
    #     details_data = validated_data.pop('details')
    #     details = Prod_Details_Serializer.create(Prod_Details_Serializer(), validated_data=details_data)
    #     product, created = UnivStudent.objects.update_or_create(user=user,
    #                         subject_major=validated_data.pop('subject_major'))
    #     return student
# # Login Serializer
# class LoginSerializer(serializers.Serializer):
#   username = serializers.CharField()
#   password = serializers.CharField()

#   def validate(self, data):
#     user = authenticate(**data)
#     if user and user.is_active:
#       return user
#     raise serializers.ValidationError("Incorrect Credentials")

class Garment_Serializer(serializers.ModelSerializer):    
    store = StoreSerializer(read_only=True ,many = True)
    class Meta:
        model = Garment
        fields = ['name','image','img_path','brand_name','price','category','store']

class GarmentDetailsSerializer(serializers.ModelSerializer):    
    store = StoreSerializer(read_only=True ,many = True)
    class Meta:
        model = GarmentDetails
        fields = ['garment','pockets_qty','description','neck_design','design_pattern','sizes_available']

