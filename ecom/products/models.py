from django.db import models
from base.models import BaseModel
from django.utils.text import slugify


class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category_image = models.ImageField(upload_to='category')

    def save( self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name
    
class ColorVariant(BaseModel):
    color_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    price = models.IntegerField(default=0)

    def save( self, *args, **kwargs):
        self.slug = slugify(self.color_name)
        super(ColorVariant, self).save(*args, **kwargs)

    def __str__(self):
        return self.color_name

class SizeVariant(BaseModel):
    size_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    price = models.IntegerField(default=0)

    def save( self, *args, **kwargs):
        self.slug = slugify(self.size_name)
        super(SizeVariant, self).save(*args, **kwargs)

    def __str__(self):
        return self.size_name


class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.IntegerField()
    modal_number = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    color_variant = models.ManyToManyField(ColorVariant, blank=True)
    size_variant = models.ManyToManyField(SizeVariant, blank=True)


    def save( self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        new_modal_number = self.modal_number if self.modal_number else ''
        if not self.modal_number:
            product_count = Product.objects.filter(category=self.category).count() + 1
            new_modal_number = f"{self.category.slug}-{str(product_count).zfill(3)}"

            while Product.objects.filter(modal_number=new_modal_number).exists():
                product_count += 1
                new_modal_number = f"{self.category.slug}-{str(product_count).zfill(3)}"

        self.modal_number = new_modal_number
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name
    
    def get_product_price_by_variant(self, size, color):
        return self.price + SizeVariant.objects.get(size_name=size).price + ColorVariant.objects.get(color_name=color).price




class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='product')

class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=100)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)
    
