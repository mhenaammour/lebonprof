from django import forms
from .models import Annonce

class AnnonceForm(forms.ModelForm):
    class Meta:
        model=Annonce
        fields=('title','category','modalite','theme','description','tarif','wilaya','addresse','commune','image',)
        widgets ={
            'title': forms.TextInput(attrs={
                'class':'w-full p-4 border border-gray-200'

            }),
            'category': forms.Select(attrs={
                'class':'w-full p-4 border border-gray-200'

            }),
            'modalite': forms.Select(attrs={
                'class':'w-full p-4 border border-gray-200'

            }),
            'theme': forms.Select(attrs={
                'class':'w-full p-4 border border-gray-200'

            }),
            'description': forms.Textarea(attrs={
                'class':'w-full p-4 border border-gray-200'

            }),
            'tarif': forms.TextInput(attrs={
                'class':'w-full p-4 border border-gray-200'

            }),
            'wilaya': forms.Select(attrs={
                'class':'w-full p-4 border border-gray-200'

            }),
            'addresse': forms.TextInput(attrs={
                'class':'w-full p-4 border border-gray-200'

            }),
            'commune': forms.Select(attrs={
                'class':'w-full p-4 border border-gray-200'

            }),
            'image': forms.FileInput(attrs={
                'class':'w-full p-4 border border-gray-200'

            }),







        }