from django.test import TestCase
from .models import Annonce,Category,Commune,Wilaya,Modalité,Theme
from .views import search
from django.contrib.auth.models import User

# Create your tests here.
class SearchViewTestCase(TestCase):

    def test_create_annonce(self):
    # Create a new Category instance
        user = User.objects.create(username='testuser')

        category = Category.objects.create(title='Test Category')
        modalite = Modalité.objects.create(title='modalite Category')
        theme = Theme.objects.create(title='theme Category')

        # Create a new Commune instance
        wilaya = Wilaya.objects.create(title='Test Wilaya')
        commune = Commune.objects.create(title='Test Commune', wilaya=wilaya)


        # Create a new Annonce instance with the Category and Commune instances
        annonce = Annonce(title='Test Annonce', tarif=50, addresse='Paris', category=category, commune=commune, wilaya=wilaya,modalite=modalite, theme=theme,user=user)

        # Save the Annonce instance to the database
        annonce.save()

        # Check that the Annonce instance was saved to the database
        self.assertEqual(Annonce.objects.count(), 1)
        self.assertEqual(Annonce.objects.first().title, 'Test Annonce')
        self.assertEqual(Annonce.objects.first().tarif, 50)
        self.assertEqual(Annonce.objects.first().addresse, 'Paris')


