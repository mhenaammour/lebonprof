from django import forms
from .models import Annonce,Offer,MessageAnn,Commune,Wilaya,Modalité,Theme

class AnnonceForm(forms.ModelForm):
#ce form est utiliser pour saisir les differents champs d une annonce#
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






class OfferForm(forms.ModelForm):
#ceci est un form pour publier un commentaire sur une annocne#
    class Meta:
        model=Offer
        fields=('details',)
        widgets ={
            'details': forms.Textarea(attrs={
                'class':'w-full p-4 border border-gray-200'

            }),
            
        }


class MessageForm(forms.ModelForm):
#ceci est un form pour envoyer un message a l annonceur#
    class Meta:
        model=MessageAnn
        fields=('amount','message',)
        widgets ={
            'amount': forms.NumberInput(attrs={
                'class':'w-full p-4 border border-gray-200'

            }),
            'message': forms.Textarea(attrs={
                'class':'w-full p-4 border border-gray-200'

            }),
            
        }

class SearchFilterForm(forms.Form):
#ceci est un form pour filtrer les annonces selon plusieurs criteres #
    wilaya = forms.ModelChoiceField(queryset=Wilaya.objects.all())
    commune = forms.ModelChoiceField(queryset=Commune.objects.none(), required=False)
    module = forms.ModelChoiceField(queryset=Theme.objects.all(), required=False)
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['commune'].queryset = Commune.objects.none()
        if 'wilaya' in self.data:
            try:
                wilaya_id = int(self.data.get('wilaya'))
                self.fields['commune'].queryset = Commune.objects.filter(wilaya_id=wilaya_id).order_by('title')
            except (ValueError, TypeError):
                pass
        else:
            self.fields['commune'].queryset = Commune.objects.none()





    
