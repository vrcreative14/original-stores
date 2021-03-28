from django.db import models
from accounts.models import User
import random
import os

# Create your models here.

def get_upload_path(self, title):
        #seller_id = request.session['seller']
        # if seller_id:
        #         seller_name = Seller.objects.filter(seller = seller_id)
        #         seller_name = seller_name + seller_id
        #         return os.path.join("static/images/products/seller_%d/category_%d" %seller_name ,self.product_class,name)
        # else: 
                file_path = os.path.join("static/images/posts/author_%s" %random.randint(9, 99)+self.author.id+random.randint(9, 99),title)
                path_folders = file_path.split("\\")
                if os.path.exists(file_path):
                    file_path = path_folders[0] + "/" + path_folders[1] + "/" + title
                
                    #file_path = os.path.join("static/images/products/store_%s" %self.store.all().first().store_id,"product_%s" %self.slug_field,name)
                return file_path


class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image1 = models.ImageField(upload_to = get_upload_path, blank=True)
    image2 = models.ImageField(upload_to = get_upload_path, blank=True)
    image3 = models.ImageField(upload_to = get_upload_path, blank=True)

