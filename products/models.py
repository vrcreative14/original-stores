from django.db import models
from multiselectfield import MultiSelectField
from stores.models import Store
from app_global.validator import check_thumbnail,check_detailed_image
from PIL import Image
import io
from django.core.files.base import ContentFile
import qrcode
import random

# Create your models here.


class ProductCategory(models.Model):
       id = models.IntegerField(primary_key=True)
       name = models.CharField(max_length=50, unique=True)

       class Meta:
           verbose_name_plural = 'ProductCategories'

       def __str__(self):
           return self.name

class ProductSubCategory(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    def __str__(self):
            return str(self.name)

class ProductIdentity(models.Model):
    type = models.ForeignKey(ProductSubCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


quantity_unit = [
    ('Pieces','Pieces'),
    ('Dozen','Dozen'),
    ('Kg','Kilogram'),
    ('L','Litre'),
    ('G','Gram'),
    ('M','Metre')
]


class Product(models.Model):
    name = models.CharField(max_length=70)
    image = models.ImageField(validators=[check_thumbnail],upload_to='static/images', height_field=None, blank=True)
    #image_front = models.ImageField(validators=[check_detailed_image],upload_to='static/images', height_field=None, blank=True)
    image_rear = models.ImageField(upload_to='static/images', height_field=None, blank=True, null=True)
    image_side1 = models.ImageField(upload_to='static/images', height_field=None, blank=True, null=True)
    image_thumbnail = models.ImageField(upload_to='static/images', height_field=None, blank=True, null=True)
    #store=models.ManyToManyField(Store)
    #type=models.ForeignKey(ProductType, on_delete=models.CASCADE)        
    img_path = models.CharField(max_length=100, blank=True)    
    brand_name = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    qrcode_text = models.CharField(max_length=250, blank=True, null=True)
    product_id = models.CharField(max_length=50,blank=True, null=True)
    #product_details = models.ForeignKey(ProductDetails, on_delete=models.SET_DEFAULT)
    #product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    store = models.ManyToManyField(Store)   
    product_category = models.ForeignKey(ProductSubCategory, on_delete=models.CASCADE)
    product_class = models.ForeignKey(ProductIdentity, on_delete=models.CASCADE)
    # def __str__(self):
    #     return str(self.name) + str(self.product_id)
    
    def save(self, *args, **kwargs):
       if(self.qrcode_text == None):
            qrcode_img = qrcode.make(self.name)
            self.qrcode_text = qrcode_img
       
       img_field = self.image   
       image = Image.open(img_field)
       w,h = image.size
       if w > 250 or h > 310 :
             output_size = (300,300)
             image.thumbnail(output_size)

       super().save(*args, **kwargs)       
             #image.save(self.image)
             #img = image.resize((250,310), Image.ANTIALIAS)
    #    elif w > 260 :
    #          img = image.resize((int(w/2),int(h)), Image.ANTIALIAS)  
    #    elif h > 320:
    #          img = image.resize((int(w),int(h/2)), Image.ANTIALIAS)  
       
      
    #    image_file = io.BytesIO()
    #    img.save(image_file,'JPEG',quality=90)
    #    self.image.instance.image = img
       #self.image.instance.image.save(str(img),ContentFile(image_file.getvalue()), save = False)
       #super(Product, self).save(*args, **kwargs)
       #self.image = image_file
       #self.image.instance.save()
       #img.save(img.filename, quality = )
       
    class Meta:
        abstract = True


class ProductDetails(models.Model):
    #specific_name = models.CharField(max_length=100)
    weight=models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    height=models.DecimalField(max_digits=20, decimal_places=2,blank=True,null=True)
    width=models.DecimalField(max_digits=20, decimal_places=2,blank=True,null=True)
    depth=models.DecimalField(max_digits=20, decimal_places=2,blank=True,null=True)
    primary_color = models.CharField(max_length=30)
    other_colors = models.CharField(max_length=150, blank=True, null=True)
    material = models.CharField(max_length=100)
    is_discounted = models.BooleanField(default=False, blank=True, null=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
   # product = models.OneToOneField(Product, on_delete=models.CASCADE)
    #is_available = models.BooleanField(default=True)
    quantity = models.IntegerField()   
    quantity_unit = models.CharField(max_length=20,choices=quantity_unit,default='Pieces')
    colors_available = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        abstract = True       


class Article(Product):
    def __str__(self):
        return self.name

class ArticleDetails(ProductDetails):
    article = models.OneToOneField(Article, on_delete=models.CASCADE)
    def __str__(self):
        return self.article.name


class GarmentSubcategory (models.Model):
    name = models.CharField(max_length=50)

    class Meta:
           verbose_name_plural = 'GarmentSubcategories'

    def __str__(self):
        return str(self.name)


StandardGarmentSizes = [
          ('S','Small'),
          ('M','Medium'),
          ('L','Large'),
          ('XL','XL'),
          ('XXL','XXL'),
          ('XXXL','XXXL'),
]

class GarmentClassification(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

class Garment(Product):    
    GARMENT_CATEGORY = (
        ('Men', "Men's Wear"),
        ('Women',"Women's Wear"),
        ('Infant', "Baby wear"),
        ('Boy', "Boys wear"),
        ('Girl',"Girls Wear"),
        # ('Ethnic', "Ethnic Wear"),
        # ('Designer','Designer Wear'),
        # ('Casual', 'Casual'),
        # ('Party', 'Party Wear'),
        # ('Uniform', 'School Uniform')
    )
    #name = models.CharField(max_length=100)
    #product = models.OneToOneField(Product,on_delete=models.CASCADE)
    #fabric = models.CharField(max_length=30)
    #category = MultiSelectField(choices = GARMENT_CATEGORY)
    #_classification = models.ForeignKey(GarmentClassification, on_delete=models.CASCADE)    
    
    def save(self, *args, **kwargs):
            if(self.product_id == None):
                self.product_id = '6109' + str(random.randint(9, 99))
            super().save(*args, **kwargs) 

    
    def __str__(self):
        return str(self.name) + ' id:'+ str(self.product_id)


class GarmentDetails(ProductDetails):
    
    season = (
        ('Rainy', 'Rainy'),
        ('Spring', 'Spring'),
        ('Winter', 'Winter'),
        ('Autumn', 'Autumn'),
        ('Summer', 'Summer'),
        ('Standard','Standard')
    )

    neck_design = (
        ('Round', 'Round'),
        ('V-neck' , 'V-neck'),
        ('PoloCollar','PoloCollar'),
        ('NA','Not Applicable')
    )
    
    design_patterns = (
          ('Checks','Checks'),
          ('Floral','Floral'),
          ('Stripes','Stripes'),
          ('Plain','Plain'),
          ('Prints','Prints'),
          ('Dots','Dots'),
          ('Logos','Logos'),
          ('Slogans','Slogans'),
          ('Others','Others')
      )
    # used_for = (
    #     ('upperbody','upperbody')
    #     ('lowerbody','lowerbody')
    #     ('head','head')
    #     ('feet','feet')
    #     ('hands' , 'hands' 
    # )
    garment = models.OneToOneField(Garment, on_delete=models.CASCADE)
    pockets_qty = models.IntegerField(default=1, blank=True)
    #zip_qty = models.IntegerField(default=0, blank=True)
    description = models.TextField(blank=True)
    #subcategory = models.ManyToManyField(GarmentSubcategory)
    #suitable_season = MultiSelectField(choices = season)
    neck_design = models.CharField(max_length=20, choices=neck_design, default='Round')
    design_pattern = MultiSelectField(choices = design_patterns)
    sizes_available = MultiSelectField(choices=StandardGarmentSizes)
    class Meta(ProductDetails.Meta):
           verbose_name_plural = 'GarmentDetails'

    def __str__(self):
        return str(self.garment.name)


class Inventory(models.Model):
    clothing = models.ManyToManyField(Garment)
    # jewellery = models.ManyToManyField()


# class KitchenItem(Product):
#     def __str__(self):
#         return self.name + ' id:' + str(self.product_id)


class KitchenItemDetails(ProductDetails):
    kitchen_item = models.OneToOneField(Article, models.CASCADE)

    def __str__(self):
        return str(self.kitchen_item.name)

# class StationeryItem(Product):
    # def __str__(self):
    #     return self.name + ' id:' + str(self.product_id)

class StationeryItemDetails(ProductDetails):
    stationery_item = models.OneToOneField(Article, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.stationery_item.name)

# class SportsFitnessEquipment(Product):
#     def __str__(self):
#         return self.name + ' id:' + str(self.product_id)

class SportsFitnessEquipmentDetails(ProductDetails):
    sports_fitness_equipment = models.OneToOneField(Article, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.sports_fitness_equipment.name)

# class HomeDecor(Product):
#     def __str__(self):
#         return self.name + ' id:' + str(self.product_id)

class HomeDecorDetails(ProductDetails):
    HomeDecor = models.OneToOneField(Article, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.HomeDecor.name)

# class HomeAppliance(Product):
#     def __str__(self):
#         return self.name + ' id:' + str(self.product_id)

class HomeApplianceDetails(ProductDetails):
    home_appliance = models.OneToOneField(Article, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.home_appliance.name)



# class ProductType(models.Model):
#     name = models.CharField(max_length=100, unique=True)


# class Cart(models.Model):
#     products = models.ManyToManyField(Inventory)



