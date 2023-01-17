from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from io import BytesIO
from PIL import Image


class Category(models.Model):
    title=models.CharField(max_length=50)
    slug=models.SlugField(max_length=50)

    class meta:
        verbose_name_plural='Categories'

    def __str__(self):
        return self.title

class Theme(models.Model):
    title=models.CharField(max_length=50)
    slug=models.SlugField(max_length=50)

    class meta:
        verbose_name_plural='Thémes'

    def __str__(self):
        return self.title

class Modalité(models.Model):
    title=models.CharField(max_length=50)
    slug=models.SlugField(max_length=50)

    class meta:
        verbose_name_plural='Modalitées'

    def __str__(self):
        return self.title

class Wilaya(models.Model):
    title=models.CharField(max_length=50)
    slug=models.SlugField(max_length=50)

    class meta:
        verbose_name_plural='wilayas'

    def __str__(self):
        return self.title

class Commune(models.Model):
    wilaya=models.ForeignKey(Wilaya, related_name='Communes',on_delete=models.CASCADE,default=1)
    title=models.CharField(max_length=50)
    slug=models.SlugField(max_length=50)

    class meta:
        verbose_name_plural='Communes'

    def __str__(self):
        return self.title


class Annonce(models.Model):
    title=models.CharField(max_length=50)
    slug=models.SlugField(max_length=50)
    user=models.ForeignKey(User, related_name='annonces', on_delete=models.CASCADE)
    category=models.ForeignKey(Category, related_name='annonces', on_delete=models.CASCADE)
    modalite=models.ForeignKey(Modalité, related_name='annonces', on_delete=models.CASCADE)
    wilaya=models.ForeignKey(Wilaya, related_name='annonces', on_delete=models.CASCADE)
    theme=models.ForeignKey(Theme, related_name='annonces', on_delete=models.CASCADE)
    image=models.ImageField(upload_to='uploads/annoces_images/',blank=True,null=True)
    thumbnail=models.ImageField(upload_to='uploads/annoces_images/thumbnail',blank=True,null=True)
    commune=models.ForeignKey(Commune, related_name='annonces', on_delete=models.CASCADE)
    tarif=models.IntegerField()
    addresse=models.TextField(blank=False,max_length=70,default="")
    description=models.TextField(blank=True)
    date_pub=models.DateTimeField(auto_now_add=True)
    date_modif=models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.title

    def make_thumbnail(self , image , size=(300,300)):
        img=Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        thumb_io=BytesIO()
        img.save(thumb_io, 'PNG',quality=80)
        name=image.name.replace('uploads/annonces_images/','')
        thumbnail=File(thumb_io , name=name)
        return thumbnail


    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail=self.make_thumbnail(self.image)
                self.save() 
                return self.thumbnail.url

            else:
                return 'https://via.placeholder.com/240x240x.jpg'              

    

    
class Offer(models.Model):
    vendor = models.ForeignKey( User , on_delete=models.CASCADE)
    annonc = models.ForeignKey(Annonce ,related_name='offers', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    details= models.TextField(blank=True)
