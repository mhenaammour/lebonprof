from django.test import TestCase
from .models import Annonce,Category,Commune,Wilaya,Modalité,Theme
from .views import search
from django.contrib.auth.models import User
from userprofile.models import Userprofile

# test to create an annonce#
class SearchViewTestCase(TestCase):


    def test_create_annonce(self):
    # Create a new Category instance#
        user = User.objects.create(username='testuser')

        category = Category.objects.create(title='Test Category')
        modalite = Modalité.objects.create(title='modalite Category')
        theme = Theme.objects.create(title='theme Category')

        # Create a new Commune instance#
        wilaya = Wilaya.objects.create(title='Test Wilaya')
        commune = Commune.objects.create(title='Test Commune', wilaya=wilaya)


        # Create a new Annonce instance with the Category and Commune instances#
        annonce = Annonce(title='Test Annonce', tarif=50, addresse='Paris', category=category, commune=commune, wilaya=wilaya,modalite=modalite, theme=theme,user=user)

        # Save the Annonce instance to the database#
        annonce.save()

        # Check that the Annonce instance was saved to the database#
        self.assertEqual(Annonce.objects.count(), 1)
        self.assertEqual(Annonce.objects.first().title, 'Test Annonce')
        self.assertEqual(Annonce.objects.first().tarif, 50)
        self.assertEqual(Annonce.objects.first().addresse, 'Paris')



from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from userprofile.models import Userprofile
#unit test for login view#
class LoginViewTestCase(TestCase):

    def setUp(self):
        # Create a user#
        self.username = 'testuser24'
        self.email = 'testuser24@example.com'
        self.password = 'testpassword'
        self.user = User.objects.create_user(self.username, self.email, self.password)

        # Create a client to make requests#
        self.client = Client()

    def test_login_view_post_success(self):
        # create a test user
        test_user = User.objects.create_user(username="testuser244", password="password123")

        # log the user in#
        success = self.client.login(username="testuser244", password="password123")
        self.assertTrue(success)

        # Manually store the session#
        session = self.client.session
        session['_auth_user_id'] = test_user.id
        session.save()

        # submit the form#
        response = self.client.post(reverse("login"), {"username": "testuser244", "password": "password123"})

        # check if the response is correct#
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("moncompte"))

        # check if the user profile exists#
        try:
            profile = Userprofile.objects.get(user__username="testuser244")
        except Userprofile.DoesNotExist:
            profile = None
        self.assertIsNotNone(profile)




from django.test import RequestFactory, TestCase
from django.urls import reverse
from .models import Annonce
#test of the searching view
#"
class SearchViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    

        user = User.objects.create(username='testuser2')

        # Create some categories to associate with the annonces#
        category1 =Category.objects.create(title='Test Category 1')
        category2 =Category.objects.create(title='Test Category 2')
        category3 =Category.objects.create(title='Test Category 3')


      

        modalite1 = Modalité.objects.create(title='Vente')
        modalite2 = Modalité.objects.create(title='Location')
        modalite3 = Modalité.objects.create(title='Echange')

        wilaya1 = Wilaya.objects.create(title='Alger')
        wilaya2 = Wilaya.objects.create(title='Oran')
        wilaya3 = Wilaya.objects.create(title='Constantine')

        theme1 = Theme.objects.create(title='Maison')
        theme2 = Theme.objects.create(title='Voiture')
        theme3 = Theme.objects.create(title='Ordinateur')

        commune1 = Commune.objects.create(title='Bab-Ezzouar')
        commune2 = Commune.objects.create(title='El-Harrach')
        commune3 = Commune.objects.create(title='Birkhadem')

        # Create the annonces#
        self.annonce1 = Annonce.objects.create(title='Annonce 1', slug='maison-a-vendre', user=user, category=category1, modalite=modalite1, wilaya=wilaya1, theme=theme1, tarif=1000000, addresse='Bab Ezzouar, Alger', description='Une maison a vendre dans un quartier calme', commune=commune1)
        self.annonce2 = Annonce.objects.create(title='Annonce 2', slug='voiture-a-vendre', user=user, category=category2, modalite=modalite1, wilaya=wilaya2, theme=theme2, tarif=200000, addresse='El Harrach, Oran', description='Une voiture a vendre en excellent etat', commune=commune2)
        self.annonce3 = Annonce.objects.create(title='Annonce 3', slug='ordinateur-portable-a-vendre', user=user, category=category3, modalite=modalite1, wilaya=wilaya3, theme=theme3, tarif=10000, addresse='Birkhadem, Constantine', description='Un ordinateur portable a vendre presque neuf', commune=commune3)

    
    def test_search_view_with_query(self):
        request = self.factory.get(reverse('search'), {'q': 'Annonce 1'})
        response = search(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['annonces']), 1)
        self.assertEqual(response.context['annonces'][0], self.annonce1)
        
    def test_search_view_without_query(self):
        request = self.factory.get(reverse('search'))
        response = search(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['annonces']), 3)
        self.assertEqual(response.context['annonces'][0], self.annonce1)
        self.assertEqual(response.context['annonces'][1], self.annonce2)
        self.assertEqual(response.context['annonces'][2], self.annonce3)

from django.test import RequestFactory, TestCase
from django.urls import reverse
from .views import add_to_fav

class AddToFavTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.annonce_id = 1

    def test_add_to_fav(self):
        request = self.factory.get(reverse('add_to_fav', args=[self.annonce_id]))
        request.session = {}
        response = add_to_fav(request, self.annonce_id)

        # Assert that the response is a redirect#
        self.assertEqual(response.status_code, 302)

        # Assert that the item is added to the cart#
        self.assertIn(str(self.annonce_id), request.session['cart'])

    def test_add_to_fav_with_existing_item(self):
        request = self.factory.get(reverse('add_to_fav', args=[self.annonce_id]))
        request.session = {'cart': {str(self.annonce_id): 1}}
        response = add_to_fav(request, self.annonce_id)

        # Assert that the response is a redirect#
        self.assertEqual(response.status_code, 302)

        # Assert that the item's quantity is incremented#
        self.assertEqual(request.session['cart'][str(self.annonce_id)], 2)

#

from django.test import TestCase, Client
from django.urls import reverse
from .models import Annonce
#
#unit test to display the annonce detail#
class AnnonceDetailViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        user = User.objects.create(username='testuser')

        category = Category.objects.create(title='Test Category')
        modalite = Modalité.objects.create(title='modalite Category')
        theme = Theme.objects.create(title='theme Category 2')

        # Create a new Commune instance#
        wilaya = Wilaya.objects.create(title='Test Wilaya')
        commune = Commune.objects.create(title='Test Commune', wilaya=wilaya)

        self.annonce = Annonce.objects.create(
            title='Test Annonce',
            description='This is a test annonce',
            tarif=100.00,
            slug='test-annonce',
            commune=commune,
            wilaya=wilaya,
            user=user,
            theme=theme,
            modalite=modalite,
            category=category,
        )
        self.url = reverse('annonce_detail', kwargs={'slug': self.annonce.slug})

    def test_view_success_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'espaceannonce/annonce_detail.html')

    def test_view_passes_correct_data_to_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['annonce'], self.annonce)



