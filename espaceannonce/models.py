# Import the required models and image manipulation library#
from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from io import BytesIO
from PIL import Image

# Define the Category model#
class Category(models.Model):
    # CharField for the title of the category#
    title = models.CharField(max_length=50)
    # SlugField for the URL of the category#
    slug = models.SlugField(max_length=50)

    class Meta:
        # Verbose name for the model in plural form#
        verbose_name_plural = 'Categories'

    def __str__(self):
        # Return the title of the category#
        return self.title

# Define the Theme model#
class Theme(models.Model):
    # CharField for the title of the theme#
    title = models.CharField(max_length=50)
    # SlugField for the URL of the theme#
    slug = models.SlugField(max_length=50)

    class Meta:
        # Verbose name for the model in plural form#
        verbose_name_plural = 'Themes'

    def __str__(self):
        # Return the title of the theme#
        return self.title

# Define the Modalité model#
class Modalité(models.Model):
    # CharField for the title of the modalité#
    title = models.CharField(max_length=50)
    # SlugField for the URL of the modalité#
    slug = models.SlugField(max_length=50)

    class Meta:
        # Verbose name for the model in plural form#
        verbose_name_plural = 'Modalités'

    def __str__(self):
        # Return the title of the modalité#
        return self.title

# Define the Wilaya model#
class Wilaya(models.Model):
    # CharField for the title of the wilaya#
    title = models.CharField(max_length=50)
    # SlugField for the URL of the wilaya#
    slug = models.SlugField(max_length=50)

    class Meta:
        # Verbose name for the model in plural form#
        verbose_name_plural = 'Wilayas'

    def __str__(self):
        # Return the title of the wilaya#
        return self.title

# Define the Commune model#
class Commune(models.Model):
    # ForeignKey to the Wilaya model#
    wilaya = models.ForeignKey(Wilaya, related_name='Communes', on_delete=models.CASCADE, default=1)
    # CharField for the title of the commune#
    title = models.CharField(max_length=50)
    # SlugField for the URL of the commune#
    slug = models.SlugField(max_length=50)

    class Meta:
        # Verbose name for the model in plural form#
        verbose_name_plural = 'Communes'

    def __str__(self):
        # Return the title of the commune#
        return self.title


 
# Define the Annonce model Classe Annonce qui représente un modèle d'annonce #
class Annonce(models.Model):
    # Titre de l annonce, de type CharField avec une longueur maximale de 50 caractères#
    title = models.CharField(max_length=50)
    # Slug de l'annonce, de type SlugField avec une longueur maximale de 50 caractères#
    slug = models.SlugField(max_length=50)
    # Utilisateur qui a publié l'annonce, ForeignKey lié à la classe User#
    user = models.ForeignKey(User, related_name='annonces', on_delete=models.CASCADE)
    # Catégorie de l'annonce, ForeignKey lié à la classe Category#
    category = models.ForeignKey(Category, related_name='annonces', on_delete=models.CASCADE)
    # Modalité de l'annonce, ForeignKey lié à la classe Modalité#
    modalite = models.ForeignKey(Modalité, related_name='annonces', on_delete=models.CASCADE)
    # Wilaya de l'annonce, ForeignKey lié à la classe Wilaya#
    wilaya = models.ForeignKey(Wilaya, related_name='annonces', on_delete=models.CASCADE)
    # Thème de l'annonce, ForeignKey lié à la classe Theme#
    theme = models.ForeignKey(Theme, related_name='annonces', on_delete=models.CASCADE)
    # Image principale de l'annonce, de type ImageField avec une répertoire d'upload 'uploads/annoces_images/'#
    image = models.ImageField(upload_to='uploads/annoces_images/', blank=True, null=True)
    # Image en miniature de l'annonce, de type ImageField avec une répertoire d'upload 'uploads/annoces_images/thumbnail'#
    thumbnail = models.ImageField(upload_to='uploads/annoces_images/thumbnail', blank=True, null=True)
    # Commune de l'annonce, ForeignKey lié à la classe Commune#
    commune = models.ForeignKey(Commune, related_name='annonces', on_delete=models.CASCADE)
    # Tarif de l'annonce, de type IntegerField#
    tarif = models.IntegerField()
    # Adresse de l'annonce, de type TextField avec une longueur maximale de 70 caractères et un champ obligatoire#
    addresse = models.TextField(blank=False, max_length=70, default="")
    # Description de l'annonce, de type TextField avec un champ facultatif#
    description = models.TextField(blank=True)
    # Date de publication de l'annonce, de type DateTimeField avec une valeur automatique définie lors de l'ajout#
    date_pub = models.DateTimeField(auto_now_add=True)
    # Date de modification de l'annonce, de type DateTimeField avec une valeur automatique définie#
    date_modif=models.DateTimeField(auto_now=True)




    def __str__(self):
        return self.title
    #This function generates a thumbnail image from a given image file. It opens the image file using the Python Imaging Library (PIL) and converts it to RGB format.#
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
        #This function retrieves the URL of a thumbnail image for an object.#
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail=self.make_thumbnail(self.image)
                self.save() 
                return self.thumbnail.url

            else:
                return 'https://via.placeholder.com/240x240x.jpg'              

    

#La classe Offer représente un commentaire pour une annonce donnée. Elle est associée à un utilisateur (internaute) et une annonce via des clés étrangères 
#
class Offer(models.Model):

    vendor = models.ForeignKey( User , on_delete=models.CASCADE)
    annonc = models.ForeignKey(Annonce ,related_name='offers', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    details= models.TextField(blank=True)



#La classe MessageAnn représente un message échangé entre un acheteur et un vendeur pour une annonce donnée. Les deux utilisateurs sont associés à la classe MessageAnn via des clés étrangères
#
class MessageAnn(models.Model):
    buyer = models.ForeignKey(User,related_name='buyers', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name='sellers' , on_delete=models.CASCADE)
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE)
    #Le montant de l'offre et le contenu du message sont stockés dans les champs "amount" et "message" respectivement. Les dates de création et de mise à jour du message sont enregistrées automatiquement
    #
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
